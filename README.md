# Truck Fleet Evaluation System - Quick Start Guide

## Overview

This is an **automated truck fleet evaluation system** that analyzes 6 data sources to help you decide whether to **KEEP**, **SELL**, or **INSPECT** each truck in your fleet.

**Current Status:** 320 active trucks analyzed
- **317 KEEP** - Performing well, maintain
- **2 SELL** - High cost/low usage, recommend liquidation
- **1 INSPECT** - Borderline metrics, needs review

---

## Files in This System

### 📊 Dashboard & Results
- **`truck_evaluation_dashboard.xlsx`** - Main dashboard with all truck evaluations
  - Sheet 1: Truck Evaluation (all trucks with metrics & recommendations)
  - Sheet 2: Summary (statistics by category)

### 📋 Documentation
- **`TRUCK_EVALUATION_GUIDE.md`** - Comprehensive user manual (read this first!)
  - Explains all metrics used
  - Decision criteria explained
  - How to interpret results
  - FAQ and troubleshooting

- **`README.md`** - This file

### 🔧 Automation Script
- **`truck_evaluation_auto_update.py`** - Runs daily to update dashboard
  - Reads all 6 source files
  - Recalculates scores
  - Exports updated dashboard
  - Logs all activity

### 📁 Source Data Files
- `truck-finance.xlsx` - Financial info (payments, ownership, odometer)
- `maintenancepo-truck.xlsx` - Repair costs & history
- `vehicle-distance-traveled.xlsx` - Daily mileage tracking
- `truck-odometer-data-week-.xlsx` - Weekly odometer snapshots
- `stub-data.xlsx` - Payroll & usage records
- `truck-paper.xlsx` - Market resale value data

---

## Quick Start (5 Minutes)

### Step 1: Open the Dashboard
```
Open: truck_evaluation_dashboard.xlsx
```

### Step 2: Check Summary Sheet
- See breakdown of recommendations
- View average scores by category
- Check total miles and repair costs

### Step 3: Review Individual Trucks
- Go to "Truck Evaluation" sheet
- Filter by **Recommendation** column
- Sort by **Score (0-100)** for priority

### Step 4: Check SELL & INSPECT Trucks
- For SELL trucks: Consider liquidation
- For INSPECT trucks: Investigate further

---

## Decision Guide

### What Does Each Recommendation Mean?

| Status | Meaning | Action |
|--------|---------|--------|
| **KEEP** | Truck is performing well | Continue normal operations |
| **SELL** | High cost, low usage | Begin liquidation process |
| **INSPECT** | Mixed signals, borderline | Review metrics manually, make judgment call |

### Key Metrics to Review

**For SELL Trucks:**
- Check **CPM** (cost per mile) - very high = unreliable
- Check **Miles (10w)** - very low = underutilized
- Check **Total Repairs** - high costs over short time

**For INSPECT Trucks:**
- Compare **Score** with actual **Usage Count**
- Check if recently acquired (may need time to show usage)
- Consider special circumstances (seasonal equipment?)

---

## Daily Usage Workflow

### Morning Check-In (2 minutes)
```
1. Open truck_evaluation_dashboard.xlsx
2. Check Summary sheet
3. Filter for SELL & INSPECT trucks
4. Scan CPM column for problem trucks (>0.25)
```

### Weekly Deep Dive (15 minutes)
```
1. Sort entire Truck Evaluation sheet by Recommendation
2. Review top 10 KEEP trucks (ensure still performing)
3. Review all SELL trucks (confirm liquidation targets)
4. Review all INSPECT trucks (make decisions)
```

### Monthly Strategy Review (1 hour)
```
1. Compare this month's scores vs last month
2. Identify trucks with deteriorating scores
3. Look for seasonal patterns in usage
4. Plan resale/replacement strategy
```

---

## Updating the Dashboard

### Manual Update (When Needed)

If you want to update dashboard immediately after new data:

```bash
python truck_evaluation_auto_update.py
```

This will:
- Read all 6 source files
- Recalculate all metrics & scores
- Generate new recommendations
- Update dashboard
- Log the activity in `evaluation_log.txt`

### Automatic Daily Update (Recommended)

Schedule the script to run automatically each morning:

#### Windows Task Scheduler:
1. Open Task Scheduler
2. Create New Task:
   - **Name:** Truck Evaluation Update
   - **Trigger:** Daily at 8:00 AM
   - **Action:** Run program
     - Program/script: `C:\Users\USER\AppData\Local\Programs\Python\Python310\python.exe`
     - Arguments: `c:\Users\USER\Downloads\spotter\truck_evaluation_auto_update.py`
   - **Conditions:** Run whether user is logged in or not

---

## Understanding the Metrics

### Basic Metrics
- **Truck ID** - Unique identifier
- **Make/Model/Year** - Vehicle specs
- **Current Odometer** - Total miles on truck
- **Ownership Type** - Financed, Lease, Owner Op, etc.

### Usage Metrics (10-week window = March 3 - May 12, 2025)
- **Miles (10w)** - Total miles driven
- **Active Days (10w)** - Days truck was used
- **Avg Daily Miles** - Miles per working day
- **Usage Count** - Times assigned in payroll

### Cost Metrics
- **Total Repairs** - Sum of all maintenance costs
- **Repair Count** - Number of service events
- **CPM** - Cost per mile (repairs ÷ miles)
- **Monthly/Annual Payment** - Ownership cost

### Financial Metrics
- **Charges Collected** - Revenue from truck
- **Resale Value** - Market estimate
- **Net Position** - Resale value minus annual cost

### Decision Metrics
- **Score (0-100)** - Composite decision score
- **Recommendation** - KEEP / SELL / INSPECT

---

## Key Performance Indicators

### Fleet Health Checklist
- [ ] Average CPM < 0.15 (good reliability)
- [ ] >80% of trucks with usage > 20,000 miles/10w
- [ ] <5% SELL recommendations
- [ ] Average decision score > 70

### Red Flags to Watch
- CPM > 0.30 (unreliable truck)
- Miles (10w) < 5,000 (underutilized)
- Repair Count > 20 in 10 weeks (frequent failures)
- Usage Count < 20 (rarely assigned)

---

## Common Scenarios

### Scenario 1: New Truck Shows KEEP
- **Normal:** New trucks often score high (low repairs, good value)
- **Action:** Monitor after 6-8 weeks to confirm pattern

### Scenario 2: Older Truck Shows SELL
- **Normal:** High mileage + accumulated repairs = sell candidates
- **Action:** Check resale value vs remaining loan balance

### Scenario 3: High-Value Truck Shows INSPECT
- **Investigate:** Why is such a valuable truck underperforming?
- **Possible Causes:** 
  - Recently acquired (needs time)
  - Operational issue (assignment pattern?)
  - Mechanical problem (get inspection?)
- **Action:** Manual review with operations manager

### Scenario 4: All Trucks Show KEEP
- **Good News:** Fleet is healthy!
- **Caution:** Verify data is current and complete
- **Action:** Continue monitoring trends

---

## Troubleshooting

### Dashboard won't open
- Ensure all 6 source files are in same directory
- Try: `python truck_evaluation_auto_update.py` to regenerate
- Check that source files aren't corrupted

### Dashboard shows 0 trucks
- Verify truck-finance.xlsx has ACTIVE trucks
- Check for spelling issues in truck ID cleanup logic
- Ensure source files have data

### Scores look wrong
- Verify Miles (10w) is calculating correctly
- Check if repair data is recent
- Confirm resale value matches similar trucks

### Missing data in columns
- Some trucks may not have all metrics (NaN values)
- This is normal for new trucks or Owner Operator owned
- Use "INSPECT" for these cases to make manual judgment

### Update script fails
- Run from command line to see error message
- Check that Python files aren't locked by Excel
- Verify all 6 source files are present and readable

---

## Data Dictionary

| Column | Type | Range | Source |
|--------|------|-------|--------|
| Truck ID | Text | - | truck-finance |
| Make/Model | Text | - | truck-finance |
| Year | Number | 2006-2025 | truck-finance |
| Current Odometer | Number | 0-900,000 | truck-finance |
| Ownership Type | Text | - | truck-finance |
| Miles (10w) | Number | 0-60,000 | vehicle-distance-traveled |
| Active Days (10w) | Number | 0-121 | vehicle-distance-traveled |
| Total Repairs | Number | $0-$46,000 | maintenancepo-truck |
| Repair Count | Number | 0-39 | maintenancepo-truck |
| CPM | Number | 0.00-3.29 | calculated |
| Charges Collected | Currency | $0-$50,000 | stub-data |
| Usage Count | Number | 0-500+ | stub-data |
| Resale Value | Currency | $18K-$170K | truck-paper |
| Score | Number | 0-100 | calculated |
| Recommendation | Text | KEEP/SELL/INSPECT | calculated |

---

## Scoring Formula (Simplified)

```
Base Score: 100

+ Usage Miles (High miles = +25, Low miles = -25)
+ Repair Costs (Low cost = +20, High cost = -20)  
+ Assignment Frequency (+15 if used >100 times)
+ Financial Position (+10 if resale > annual cost)
- Ownership Type (-5 if owner operator)

Result: Clamped between 0-100

Decision:
  Score >= 70 → KEEP
  Score <= 40 & low miles & high repairs → SELL
  Otherwise → INSPECT
```

---

## Support & Questions

### For Questions About:
- **How the system works** → See TRUCK_EVALUATION_GUIDE.md
- **How to interpret metrics** → See data dictionary above
- **How to schedule automation** → See "Automatic Daily Update" section
- **Technical issues** → Check evaluation_log.txt for error messages

### Documentation Files:
1. **README.md** (this file) - Quick overview & troubleshooting
2. **TRUCK_EVALUATION_GUIDE.md** - Detailed user manual (start here!)
3. **truck_evaluation_auto_update.py** - Automation script with comments

---

## Next Steps

1. **Read the Full Guide:** Open `TRUCK_EVALUATION_GUIDE.md` for complete details
2. **Review Dashboard:** Open `truck_evaluation_dashboard.xlsx` and explore
3. **Set Up Automation:** Schedule `truck_evaluation_auto_update.py` to run daily
4. **Make Decisions:** Use recommendations to plan fleet strategy
5. **Monitor Trends:** Review dashboard weekly for changes

---

**Last Updated:** May 5, 2026  
**System Version:** 1.0  
**Status:** ACTIVE & READY FOR DAILY USE

---

*For detailed metrics explanations and decision frameworks, see TRUCK_EVALUATION_GUIDE.md*
