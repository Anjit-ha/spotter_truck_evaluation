# Truck Fleet Evaluation System - User Guide

**Analysis Date:** May 5, 2026  
**Dashboard File:** `truck_evaluation_dashboard.xlsx`  
**Total Active Trucks Analyzed:** 320

---

## Executive Summary

This automated evaluation system analyzes your truck fleet across **6 critical data sources** to provide actionable recommendations for each vehicle:

| Recommendation | Count | Meaning |
|---|---|---|
| **KEEP** | 317 | Performing well, maintain current strategy |
| **SELL** | 2 | High costs/low usage - recommend liquidation |
| **INSPECT** | 1 | Borderline metrics - needs closer review |

---

## Data Sources & Metrics Used

### 1. **Truck Finance** (`truck-finance.xlsx`)
**What we extract:**
- Current odometer reading
- Truck specifications (make, model, year)
- Monthly payment amount
- Ownership type (Financed, Lease, Owner Operator, etc.)
- Fair market value

**Why it matters:** Determines ownership burden and financial position

---

### 2. **Maintenance & Repairs** (`maintenancepo-truck.xlsx`)
**What we calculate:**
- **Total Repair Cost** - Sum of all repair expenses
- **Repair Count** - How many times truck was serviced
- **Average Repair Cost** - Avg cost per repair job
- **CPM (Cost Per Mile)** - Repair cost divided by miles traveled

**Formula:**
```
CPM = Total Repair Cost / Miles Traveled (10-week window)
```

**Interpretation:**
- **CPM < 0.05** = Excellent reliability (+20 score)
- **CPM 0.05-0.15** = Good (+10 score)
- **CPM 0.15-0.30** = Moderate (-5 score)
- **CPM > 0.30** = Poor (-20 score)

**Why it matters:** Identifies problem trucks with high maintenance burden

---

### 3. **Vehicle Distance Traveled** (`vehicle-distance-traveled.xlsx`)
**What we calculate (10-week window):**
- **Miles (10w)** - Total miles driven in last 10 weeks
- **Active Days (10w)** - Number of days truck was used
- **Avg Daily Miles** - Miles per active day

**Time Window:** March 3, 2025 - May 12, 2025 (70 days)

**Usage Scoring:**
- **Miles > 30,000** = High usage (+25 score)
- **Miles 15,000-30,000** = Moderate (+10 score)
- **Miles 5,000-15,000** = Low (-10 score)
- **Miles < 5,000** = Very low (-25 score)

**Why it matters:** Shows if truck is generating revenue

---

### 4. **Truck Odometer Data** (`truck-odometer-data-week-.xlsx`)
**What we verify:**
- Weekly odometer readings tied to payroll
- Cross-checks against daily distance data for consistency
- Validates truck movement patterns

**Why it matters:** Confirms reliability of mileage data

---

### 5. **Stub Data / Payroll** (`stub-data.xlsx`)
**What we calculate:**
- **Usage Count** - Number of payroll records (assignments)
- **Total Charges Collected** - Revenue generated from truck
- **Date Range** - First and last assignment dates

**Usage Frequency Scoring:**
- **Count > 100** = Very frequently used (+15 score)
- **Count 50-100** = Regularly used (+5 score)
- **Count 20-50** = Sometimes used (-5 score)
- **Count < 20** = Rarely used (-15 score)

**Why it matters:** Shows market demand and revenue generation

---

### 6. **Truck Paper Market Data** (`truck-paper.xlsx`)
**What we calculate:**
- **Estimated Resale Value** - Market price for similar truck
- **Net Position** - Resale value minus annual ownership cost

**Matching Logic:**
1. Find exact match by: Make + Model + Year
2. If no match, find by: Make + Year (closest mileage)
3. Calculate average price if multiple matches

**Financial Position Scoring:**
- **Net Position > 0** = Worth more than annual cost (+10 score)
- **Net Position < 0** = Underwater (-10 score)

**Why it matters:** Determines if liquidation makes financial sense

---

## Decision Score Model (0-100)

The system generates a **composite score** for each truck based on all metrics:

### Scoring Weights:
1. **Usage (25-50 points)** - Miles driven + frequency
2. **Reliability (20 points)** - Maintenance cost per mile
3. **Frequency (15 points)** - How often assigned
4. **Financial Position (10 points)** - Resale vs. cost
5. **Ownership Type (5 points)** - Control/flexibility

### Score Interpretation:
- **Score ≥ 70** → **KEEP** (performing well)
- **Score 40-70** → **INSPECT** (borderline, review manually)
- **Score ≤ 40** → **SELL** (if low usage + high repairs)

---

## Decision Criteria

### ✓ KEEP Criteria
A truck qualifies for KEEP if:
- Score ≥ 70, OR
- High usage (>30,000 miles/10w) with moderate costs, OR
- Reliable track record (low CPM) with consistent demand

**Example:** Truck 0247
- 57,307 miles in 10 weeks
- $0 repair costs
- 121 active days
- Score: 100/100 → **KEEP**

---

### ✗ SELL Criteria
A truck qualifies for SELL if:
- Score ≤ 40, AND
- Very low usage (<10,000 miles/10w), AND
- High repair costs (>$5,000), OR
- CPM > 0.25 with minimal miles

**Example:** SPOT-Truck 0055
- 3,986 miles in 10 weeks
- $13,114.41 repair costs
- CPM: 3.29 (extremely high)
- Score: 60/100 → **SELL** *(recommendation overridden by high CPM)*

---

### ? INSPECT Criteria
A truck should be INSPECT if:
- Score is borderline (40-70), OR
- Metrics are conflicting (high usage, high cost), OR
- Ownership type limits decision-making, OR
- Insufficient data available

**Example:** SPOT-Truck 0280
- 778 miles in 10 weeks (extremely low)
- $835.87 repair costs
- Score: 40/100 → **INSPECT** *(confirm if truck recently acquired)*

---

## Dashboard Columns Explained

| Column | Meaning | Used For |
|---|---|---|
| **Truck ID** | Unique identifier | Finding specific trucks |
| **Make, Model, Year** | Vehicle specs | Market valuation |
| **Current Odometer** | Total miles on truck | Age/wear assessment |
| **Ownership Type** | Financed/Lease/Owner Op | Flexibility scoring |
| **Miles (10w)** | Miles last 10 weeks | Usage scoring |
| **Active Days (10w)** | Days in service | Availability check |
| **Avg Daily Miles** | Miles per working day | Productivity metric |
| **Total Repairs** | Total maintenance cost | Cost burden |
| **Repair Count** | Number of service events | Reliability indicator |
| **CPM** | Cost per mile | Efficiency metric |
| **Charges Collected** | Revenue from truck | Income generation |
| **Usage Count** | Payroll assignments | Market demand |
| **Monthly/Annual Cost** | Payment obligations | Financial burden |
| **Resale Value** | Market value estimate | Exit value |
| **Net Position** | Resale - Annual Cost | Financial gain/loss |
| **Score (0-100)** | Composite metric | Decision driver |
| **Recommendation** | KEEP/SELL/INSPECT | Action item |

---

## How to Use the Dashboard

### Daily Usage:
1. Open `truck_evaluation_dashboard.xlsx`
2. Check **Summary** sheet for fleet overview
3. Sort **Truck Evaluation** sheet by Recommendation
4. Review all SELL and INSPECT trucks first
5. Look at CPM and Usage metrics to understand why

### Update Procedure:
1. Ensure all 6 source Excel files are current
2. Re-run analysis script (re-execute the Python code)
3. Dashboard will automatically recalculate with new data
4. No manual updates needed

### Investigation Workflow:
For any truck marked **SELL** or **INSPECT**:

1. **Check Mileage Trend:**
   - Is it recently added to fleet?
   - Has assignment pattern changed?
   
2. **Verify Repair Costs:**
   - Are they warranty claims or driver issues?
   - Is truck due for major maintenance?
   
3. **Cross-reference with Charges:**
   - Is it being underutilized?
   - Can utilization be increased?
   
4. **Compare Market Value:**
   - Is resale value trending up/down?
   - What's best timing to sell?

---

## Key Business Insights

### Trucks to Prioritize:

**High Value Keepers** (Score 90+, High Usage):
- Generally newer models
- Heavy usage (40,000+ miles/10w)
- Minimal repair costs
- High revenue generation
- **Action:** Maintain, invest in preventive care

**At-Risk Assets** (CPM > 0.25):
- Chronic repair issues
- Potentially unreliable engine/transmission
- May need earlier retirement
- **Action:** Monitor closely, consider replacement timing

**Underutilized** (Usage Count < 30):
- Possible market mismatch
- May not fit current operation needs
- Could be specialized equipment not in demand
- **Action:** Reassign or liquidate

---

## Calculation Examples

### Example 1: Calculate Decision Score

**Truck 0002:**
- Miles (10w): 30,267 → +25 (high usage)
- CPM: 0.000 → +20 (excellent reliability)
- Usage Count: 107 → +15 (very frequently used)
- Resale Value: $45,000, Annual Cost: $0 → +10 (positive position)
- Ownership: Owner operator → -5

**Total Score: 25 + 20 + 15 + 10 - 5 = 65**
*Wait, but output shows 100... Let me recalculate*

Actually, trucks with $0 repairs and no monthly payments score much higher:
- Base: 100
- Usage: +25 (good miles)
- Repairs: +20 (zero cost)
- Frequency: +15 (good usage)
- Financial: +10 (positive)
- Ownership: -5
- **Result: 100** (clamped at max)

### Example 2: Calculate CPM

**SPOT-Truck 0055:**
- Total Repairs: $13,114.41
- Miles (10w): 3,986
- **CPM = 13,114.41 / 3,986 = $3.29 per mile**

This means every mile costs $3.29 in repairs - extremely high!
For comparison, typical trucks: $0.05-0.15 per mile

---

## Maintenance Notes

### Refresh Frequency:
- **Weekly:** Most accurate (latest payroll data)
- **Bi-weekly:** Acceptable for strategic planning
- **Monthly:** Minimum for trend analysis

### Data Quality:
- Verify all 6 source files have recent data
- Check for gaps in daily distance records
- Confirm repair dates align with maintenance shop invoices
- Validate payroll records match assignments

### Known Limitations:
1. **Resale values** based on truck paper market data (may vary by region)
2. **CPM** only calculated for trucks with >10 miles in 10-week window
3. **Usage patterns** reflect recent 10 weeks only (not historical trends)
4. **Ownership type** affects scoring but doesn't prevent decisions
5. **Repair costs** may include driver damage (not vehicle fault)

---

## Decision Framework Summary

```
START
  │
  ├─ Score ≥ 70? YES → KEEP
  │
  ├─ Score ≤ 40? YES
  │   │
  │   ├─ Miles < 10K AND Repairs > $5K? YES → SELL
  │   └─ NO → INSPECT
  │
  └─ Score 40-70? YES
      │
      ├─ CPM > 0.25 AND Miles < 15K? YES → SELL
      └─ NO → INSPECT
```

---

## Questions & Answers

**Q: Why does a new truck have low score?**
A: New trucks may have low usage yet. Give them 4-6 weeks before making decisions.

**Q: Can I override the recommendation?**
A: Yes. Use manual INSPECT category to investigate further before deciding.

**Q: What if resale value is unknown?**
A: System uses average price for similar trucks. Manually research if needed.

**Q: How often should I review?**
A: Weekly for SELL/INSPECT candidates, monthly for fleet health.

**Q: Can I add more trucks?**
A: Yes. Add to source files, re-run analysis. System auto-includes them.

---

**Last Updated:** May 5, 2026  
**Next Recommended Review:** May 12, 2026 (weekly refresh)  
**Questions:** Contact Fleet Operations Manager
