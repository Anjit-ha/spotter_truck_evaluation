#!/usr/bin/env python3
r"""
TRUCK FLEET EVALUATION SYSTEM - AUTO-UPDATE SCRIPT
===================================================

This script automatically:
1. Reads all 6 data sources
2. Combines metrics
3. Calculates decision scores
4. Generates recommendations
5. Exports to Excel dashboard

Usage:
    python truck_evaluation_auto_update.py
    
Or schedule with Windows Task Scheduler:
    Task Trigger: Daily at 8:00 AM
    Action: Run C:\Users\USER\AppData\Local\Programs\Python\Python310\python.exe truck_evaluation_auto_update.py
    
Version: 1.0
Last Updated: May 5, 2026
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
import warnings

warnings.filterwarnings('ignore')

# Configuration
WORKSPACE_PATH = r"c:\Users\USER\Downloads\spotter"
OUTPUT_FILE = os.path.join(WORKSPACE_PATH, "truck_evaluation_dashboard.xlsx")
LOG_FILE = os.path.join(WORKSPACE_PATH, "evaluation_log.txt")

def log_message(msg):
    """Log messages to both console and file"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] {msg}"
    print(log_entry)
    with open(LOG_FILE, 'a') as f:
        f.write(log_entry + "\n")

def validate_files():
    """Check if all required files exist"""
    required_files = [
        "truck-finance.xlsx",
        "maintenancepo-truck.xlsx",
        "vehicle-distance-traveled.xlsx",
        "truck-odometer-data-week-.xlsx",
        "stub-data.xlsx",
        "truck-paper.xlsx"
    ]
    
    missing = []
    for file in required_files:
        if not os.path.exists(os.path.join(WORKSPACE_PATH, file)):
            missing.append(file)
    
    if missing:
        raise FileNotFoundError(f"Missing files: {', '.join(missing)}")
    
    log_message(f"All {len(required_files)} source files validated")

def read_data():
    """Read all data sources"""
    log_message("Reading data sources...")
    
    finance_df = pd.read_excel(f"{WORKSPACE_PATH}/truck-finance.xlsx", sheet_name="truck_finance")
    maintenance_df = pd.read_excel(f"{WORKSPACE_PATH}/maintenancepo-truck.xlsx", sheet_name="repairs")
    distance_df = pd.read_excel(f"{WORKSPACE_PATH}/vehicle-distance-traveled.xlsx", sheet_name="distanceTraveled")
    odometer_df = pd.read_excel(f"{WORKSPACE_PATH}/truck-odometer-data-week-.xlsx", sheet_name="truckData")
    stub_df = pd.read_excel(f"{WORKSPACE_PATH}/stub-data.xlsx", sheet_name="StubData")
    paper_df = pd.read_excel(f"{WORKSPACE_PATH}/truck-paper.xlsx", sheet_name="tp_listings")
    
    log_message(f"Data loaded: Finance({len(finance_df)}), Maintenance({len(maintenance_df)}), Distance({len(distance_df)}), Odometer({len(odometer_df)}), Stub({len(stub_df)}), Paper({len(paper_df)})")
    
    return finance_df, maintenance_df, distance_df, odometer_df, stub_df, paper_df

def extract_active_trucks(finance_df):
    """Extract active trucks from finance data"""
    finance_df['unit_id_clean'] = finance_df['unit_id'].str.strip()
    active_trucks = finance_df[finance_df['status'] == 'ACTIVE'][['unit_id_clean', 'ownership_type', 'monthly_payment', 'odometer', 'fair_market_value', 'make', 'model', 'year']].copy()
    active_trucks = active_trucks.rename(columns={'unit_id_clean': 'unit_id'})
    active_trucks = active_trucks.drop_duplicates(subset=['unit_id'])
    
    log_message(f"Identified {len(active_trucks)} active trucks")
    return active_trucks

def calculate_maintenance_metrics(maintenance_df):
    """Calculate maintenance costs and repair frequency"""
    maintenance_df['unit_id_clean'] = maintenance_df['unit_id'].str.strip()
    maint_summary = maintenance_df.groupby('unit_id_clean').agg({
        'amount': ['sum', 'count', 'mean'],
        'company_covered': 'sum'
    }).reset_index()
    maint_summary.columns = ['unit_id', 'total_repair_cost', 'repair_count', 'avg_repair_cost', 'company_paid_total']
    
    log_message(f"Maintenance data: {len(maint_summary)} trucks with repair records")
    return maint_summary

def calculate_usage_metrics(distance_df):
    """Calculate usage metrics for 10-week window"""
    distance_df['date'] = pd.to_datetime(distance_df['date'])
    distance_df['unit_id_clean'] = distance_df['unit_id'].str.strip()
    
    latest_date = distance_df['date'].max()
    ten_weeks_ago = latest_date - timedelta(weeks=10)
    
    usage_10w = distance_df[distance_df['date'] >= ten_weeks_ago].groupby('unit_id_clean').agg({
        'distance': 'sum',
        'date': 'count'
    }).reset_index()
    usage_10w.columns = ['unit_id', 'miles_10w', 'active_days_10w']
    
    log_message(f"Usage data: {len(usage_10w)} trucks with distance records ({ten_weeks_ago.date()} to {latest_date.date()})")
    return usage_10w

def calculate_stub_metrics(stub_df):
    """Calculate usage frequency from payroll records"""
    stub_df['TRUCK_clean'] = stub_df['TRUCK'].str.strip()
    stub_summary = stub_df.groupby('TRUCK_clean').agg({
        'TRUCK CHARGE': 'sum',
        'DATE': 'count'
    }).reset_index()
    stub_summary.columns = ['unit_id', 'total_charges_collected', 'usage_count']
    
    log_message(f"Payroll data: {len(stub_summary)} trucks with usage records")
    return stub_summary

def estimate_resale_values(active_trucks, paper_df):
    """Estimate resale values from truck paper listings"""
    def find_resale_value(make, model, year, odometer):
        filtered = paper_df[
            (paper_df['truck_brand'].str.upper() == make.upper()) &
            (paper_df['truck_model'].str.upper() == model.upper()) &
            (paper_df['truck_year'] == year)
        ].copy()
        
        if len(filtered) == 0:
            filtered = paper_df[(paper_df['truck_brand'].str.upper() == make.upper()) & (paper_df['truck_year'] == year)].copy()
        
        if len(filtered) > 0:
            if not pd.isna(odometer) and odometer > 0:
                filtered['mileage_diff'] = abs(filtered['truck_mileage'] - odometer)
                closest = filtered.loc[filtered['mileage_diff'].idxmin()]
                return closest['truck_price']
            else:
                return filtered['truck_price'].mean()
        
        return np.nan
    
    active_trucks['estimated_resale'] = active_trucks.apply(
        lambda row: find_resale_value(row['make'], row['model'], row['year'], row['odometer']),
        axis=1
    )
    
    matched = active_trucks['estimated_resale'].notna().sum()
    log_message(f"Resale values: {matched}/{len(active_trucks)} trucks matched with market data")
    return active_trucks

def combine_all_metrics(active_trucks, maint_summary, usage_10w, stub_summary):
    """Combine all metrics into single evaluation dataframe"""
    evaluation = active_trucks.copy()
    
    evaluation = evaluation.merge(maint_summary, on='unit_id', how='left')
    evaluation['total_repair_cost'] = evaluation['total_repair_cost'].fillna(0)
    evaluation['repair_count'] = evaluation['repair_count'].fillna(0)
    evaluation['avg_repair_cost'] = evaluation['avg_repair_cost'].fillna(0)
    
    evaluation = evaluation.merge(usage_10w, on='unit_id', how='left')
    evaluation['miles_10w'] = evaluation['miles_10w'].fillna(0)
    evaluation['active_days_10w'] = evaluation['active_days_10w'].fillna(0)
    evaluation['avg_daily_miles_10w'] = np.where(
        evaluation['active_days_10w'] > 0,
        evaluation['miles_10w'] / evaluation['active_days_10w'],
        0
    )
    
    evaluation = evaluation.merge(stub_summary, on='unit_id', how='left')
    evaluation['total_charges_collected'] = evaluation['total_charges_collected'].fillna(0)
    evaluation['usage_count'] = evaluation['usage_count'].fillna(0)
    
    evaluation['cpm'] = np.where(
        evaluation['miles_10w'] > 0,
        evaluation['total_repair_cost'] / evaluation['miles_10w'],
        0
    )
    
    evaluation['financial_burden'] = (evaluation['monthly_payment'] * 12)
    evaluation['net_resale_position'] = evaluation['estimated_resale'] - evaluation['monthly_payment'] * 12
    
    log_message(f"Metrics combined for {len(evaluation)} trucks")
    return evaluation

def calculate_decision_score(row):
    """Calculate decision score for a truck"""
    score = 100
    
    if row['miles_10w'] > 30000:
        score += 25
    elif row['miles_10w'] > 15000:
        score += 10
    elif row['miles_10w'] > 5000:
        score -= 10
    else:
        score -= 25
    
    if row['cpm'] < 0.05:
        score += 20
    elif row['cpm'] < 0.15:
        score += 10
    elif row['cpm'] < 0.30:
        score -= 5
    else:
        score -= 20
    
    if row['usage_count'] > 100:
        score += 15
    elif row['usage_count'] > 50:
        score += 5
    elif row['usage_count'] > 20:
        score -= 5
    else:
        score -= 15
    
    if not pd.isna(row['estimated_resale']) and row['estimated_resale'] > 0:
        if row['net_resale_position'] > 0:
            score += 10
        else:
            score -= 10
    
    if row['ownership_type'] in ['Owner Operator Owned', 'Owner operator owned']:
        score -= 5
    
    return max(0, min(100, score))

def assign_recommendation(row):
    """Assign recommendation based on score and metrics"""
    score = row['decision_score']
    cpm = row['cpm']
    miles = row['miles_10w']
    
    if score >= 70:
        return 'KEEP'
    elif score <= 40:
        if row['miles_10w'] < 10000 and row['total_repair_cost'] > 5000:
            return 'SELL'
        else:
            return 'INSPECT'
    else:
        if cpm > 0.25 and miles < 15000:
            return 'SELL'
        else:
            return 'INSPECT'

def score_and_recommend(evaluation):
    """Generate scores and recommendations"""
    evaluation['decision_score'] = evaluation.apply(calculate_decision_score, axis=1)
    evaluation['recommendation'] = evaluation.apply(assign_recommendation, axis=1)
    
    keep_count = (evaluation['recommendation'] == 'KEEP').sum()
    sell_count = (evaluation['recommendation'] == 'SELL').sum()
    inspect_count = (evaluation['recommendation'] == 'INSPECT').sum()
    
    log_message(f"Scoring complete: KEEP({keep_count}), SELL({sell_count}), INSPECT({inspect_count})")
    return evaluation

def create_output_table(evaluation):
    """Create formatted output table"""
    output_table = evaluation[[
        'unit_id', 'make', 'model', 'year', 'odometer', 'ownership_type',
        'miles_10w', 'active_days_10w', 'avg_daily_miles_10w',
        'total_repair_cost', 'repair_count', 'cpm',
        'total_charges_collected', 'usage_count',
        'monthly_payment', 'financial_burden', 'estimated_resale', 'net_resale_position',
        'decision_score', 'recommendation'
    ]].copy()
    
    output_table.columns = [
        'Truck ID', 'Make', 'Model', 'Year', 'Current Odometer', 'Ownership Type',
        'Miles (10w)', 'Active Days (10w)', 'Avg Daily Miles', 
        'Total Repairs', 'Repair Count', 'CPM',
        'Charges Collected', 'Usage Count',
        'Monthly Payment', 'Annual Cost', 'Resale Value', 'Net Position',
        'Score (0-100)', 'Recommendation'
    ]
    
    output_table = output_table.sort_values(['Recommendation', 'Score (0-100)'], ascending=[True, False])
    
    output_table['Score (0-100)'] = output_table['Score (0-100)'].round(1)
    output_table['CPM'] = output_table['CPM'].round(4)
    output_table['Avg Daily Miles'] = output_table['Avg Daily Miles'].round(2)
    
    return output_table

def create_summary_sheet(output_table):
    """Create summary statistics"""
    summary_data = {
        'Category': ['KEEP', 'SELL', 'INSPECT', 'TOTAL'],
        'Count': [
            (output_table['Recommendation'] == 'KEEP').sum(),
            (output_table['Recommendation'] == 'SELL').sum(),
            (output_table['Recommendation'] == 'INSPECT').sum(),
            len(output_table)
        ],
        'Avg Score': [
            output_table[output_table['Recommendation'] == 'KEEP']['Score (0-100)'].mean(),
            output_table[output_table['Recommendation'] == 'SELL']['Score (0-100)'].mean(),
            output_table[output_table['Recommendation'] == 'INSPECT']['Score (0-100)'].mean(),
            output_table['Score (0-100)'].mean()
        ],
        'Total Miles (10w)': [
            output_table[output_table['Recommendation'] == 'KEEP']['Miles (10w)'].sum(),
            output_table[output_table['Recommendation'] == 'SELL']['Miles (10w)'].sum(),
            output_table[output_table['Recommendation'] == 'INSPECT']['Miles (10w)'].sum(),
            output_table['Miles (10w)'].sum()
        ],
        'Total Repair Cost': [
            output_table[output_table['Recommendation'] == 'KEEP']['Total Repairs'].sum(),
            output_table[output_table['Recommendation'] == 'SELL']['Total Repairs'].sum(),
            output_table[output_table['Recommendation'] == 'INSPECT']['Total Repairs'].sum(),
            output_table['Total Repairs'].sum()
        ]
    }
    
    return pd.DataFrame(summary_data)

def export_to_excel(output_table, summary_df):
    """Export to Excel with formatting"""
    with pd.ExcelWriter(OUTPUT_FILE, engine='openpyxl') as writer:
        output_table.to_excel(writer, sheet_name='Truck Evaluation', index=False)
        summary_df.to_excel(writer, sheet_name='Summary', index=False)
    
    log_message(f"Dashboard exported to: {OUTPUT_FILE}")

def main():
    """Main execution function"""
    try:
        log_message("=" * 80)
        log_message("TRUCK EVALUATION AUTO-UPDATE STARTED")
        log_message("=" * 80)
        
        # Validate files
        validate_files()
        
        # Read data
        finance_df, maintenance_df, distance_df, odometer_df, stub_df, paper_df = read_data()
        
        # Extract and calculate metrics
        active_trucks = extract_active_trucks(finance_df)
        active_trucks = estimate_resale_values(active_trucks, paper_df)
        
        maint_summary = calculate_maintenance_metrics(maintenance_df)
        usage_10w = calculate_usage_metrics(distance_df)
        stub_summary = calculate_stub_metrics(stub_df)
        
        # Combine all metrics
        evaluation = combine_all_metrics(active_trucks, maint_summary, usage_10w, stub_summary)
        
        # Score and recommend
        evaluation = score_and_recommend(evaluation)
        
        # Create output
        output_table = create_output_table(evaluation)
        summary_df = create_summary_sheet(output_table)
        
        # Export
        export_to_excel(output_table, summary_df)
        
        log_message("=" * 80)
        log_message("TRUCK EVALUATION AUTO-UPDATE COMPLETED SUCCESSFULLY")
        log_message("=" * 80)
        
        return 0
    
    except Exception as e:
        log_message(f"ERROR: {str(e)}")
        log_message("TRUCK EVALUATION AUTO-UPDATE FAILED")
        return 1

if __name__ == "__main__":
    sys.exit(main())
