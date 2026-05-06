# TRUCK FLEET EVALUATION SYSTEM - 5 MINUTE LOOM PRESENTATION

## Presentation Structure (5 minutes total)

### SLIDE 1: TITLE & INTRODUCTION (0:00 - 0:30)
**What to show:**
- Show the desktop with the project folder open
- Show: `truck_evaluation_dashboard.xlsx`

**What to say:**
"Hi everyone, today I'm showing you a complete **Truck Fleet Evaluation System** that I built to automatically analyze 320 trucks and make data-driven decisions about which trucks to keep, sell, or inspect.

This system pulls from 6 different data sources and gives us instant recommendations. Let me show you what we built."

---

### SLIDE 2: THE PROBLEM (0:30 - 1:00)
**What to show:**
- Show the 6 Excel source files in the folder

**What to say:**
"Before this system, evaluating trucks meant manually combining data from 6 separate Excel files:
- Truck Finance (payments, ownership)
- Maintenance records (repair costs)
- Vehicle Distance Traveled (daily mileage)
- Truck Odometer data (weekly snapshots)
- Payroll/Stub data (usage & revenue)
- Truck Paper market data (resale values)

That's a lot of manual work. We needed a better way."

---

### SLIDE 3: THE SOLUTION - DASHBOARD (1:00 - 2:00)
**What to show:**
- Open `truck_evaluation_dashboard.xlsx`
- Show the "Summary" sheet first

**What to say:**
"So I built an automated system that combines all 6 data sources into one dashboard. Let me show you the Summary first.

[Point to Summary sheet]

We have:
- **317 trucks to KEEP** (performing well)
- **2 trucks to SELL** (high cost, low usage)
- **1 truck to INSPECT** (borderline metrics)

That's 99.1% of the fleet performing great! 

The system analyzed:
- 7.2 million miles driven
- $1.3 million in repairs
- $10.3 million in revenue collected"

---

### SLIDE 4: THE DECISION LOGIC (2:00 - 3:00)
**What to show:**
- Switch to "Truck Evaluation" sheet
- Show the scoring columns
- Filter to show SELL trucks

**What to say:**
"Here's how the system makes decisions. Each truck gets a score from 0-100 based on:

1. **Usage** - Is the truck being driven? (40% weight)
2. **Repair costs** - Is it reliable? (30% weight)
3. **Frequency** - How often is it assigned? (20% weight)
4. **Financial position** - Is the resale value good? (10% weight)

Look at this SELL candidate - SPOT-Truck 0055:
[Point to truck data]
- Only 3,986 miles in 10 weeks (very low usage)
- $13,114 in repairs (very high cost)
- CPM of $3.29 per mile (extremely expensive to operate)
- Score: 60/100
- Recommendation: **SELL**

Compare that to a top performer like Truck 0002:
- 30,267 miles in 10 weeks (good usage)
- $0 repairs (excellent)
- CPM $0.00 (free to operate)
- Score: 100/100
- Recommendation: **KEEP**

The system is objective - purely data-driven."

---

### SLIDE 5: HOW IT WORKS (3:00 - 4:00)
**What to show:**
- Show the Python script file: `truck_evaluation_auto_update.py`
- Show a few key metrics columns in dashboard

**What to say:**
"The system uses Python to:

1. **Read all 6 data sources** - pulls from Excel files
2. **Clean & normalize** the data - standardizes truck IDs, handles missing values
3. **Calculate metrics**:
   - CPM (cost per mile)
   - 10-week usage patterns
   - Assignment frequency
   - Resale values
4. **Score each truck** - applies decision logic
5. **Generate recommendations** - KEEP, SELL, or INSPECT
6. **Export to dashboard** - updates the Excel file

You can run it manually anytime, or schedule it to run automatically every day at 8 AM.

The best part? It takes 10 seconds to run, gives you instant insights on 320 trucks."

---

### SLIDE 6: KEY RESULTS & BUSINESS IMPACT (4:00 - 4:45)
**What to show:**
- Switch back to Summary sheet
- Show the key numbers

**What to say:**
"Here are the key business results:

**Fleet Health:**
- Average truck score: 96.6/100 - excellent
- Average reliability (CPM): $0.18 per mile - very good
- Only 2 trucks need to be sold

**Financial Impact:**
- Fleet resale value: $26 million
- Annual payment obligation: $11.3 million
- Net fleet equity: **$14.6 million POSITIVE**

**Revenue Generation:**
- Charges collected: $10.3 million
- Repair costs: $1.3 million
- Revenue to repair ratio: **7.74 to 1** - for every $1 spent on repairs, we collect $7.74

This fleet is generating strong revenue and equity is very healthy."

---

### SLIDE 7: DELIVERABLES & HOW TO USE (4:45 - 5:00)
**What to show:**
- Show the 4 main files in folder:
  1. `truck_evaluation_dashboard.xlsx`
  2. `EXECUTIVE_SUMMARY.md`
  3. `TRUCK_EVALUATION_GUIDE.md`
  4. `truck_evaluation_auto_update.py`

**What to say:**
"Here's what you're getting:

1. **Dashboard** - Excel file with all 320 trucks and recommendations
2. **Executive Summary** - One-page overview of key findings
3. **User Guide** - Detailed documentation on how everything works
4. **Auto-update script** - Runs daily to keep data fresh

To use it:
- Open the dashboard Excel file
- Filter by Recommendation column
- Review SELL and INSPECT trucks
- Use the guide for detailed explanations

That's it! The system does all the heavy lifting."

---

## PRESENTATION TIMING SUMMARY

```
0:00-0:30 = Introduction (30 sec)
0:30-1:00 = Problem statement (30 sec)
1:00-2:00 = Dashboard overview (60 sec)
2:00-3:00 = Decision logic & examples (60 sec)
3:00-4:00 = How it works - technical (60 sec)
4:00-4:45 = Results & business impact (45 sec)
4:45-5:00 = Deliverables & next steps (15 sec)
```

---

## LOOM RECORDING TIPS

### What to Show on Screen:
1. **Start:** Desktop with project folder
2. **Throughout:** Keep dashboard visible
3. **Zoom in:** Make sure text is readable (use browser zoom if needed)
4. **Point:** Use mouse cursor to highlight what you're talking about
5. **Move smoothly:** Don't jump around too much

### Best Practices:
- **Speak clearly** - slow down, don't rush
- **Use your pointer** - highlight important numbers
- **Make eye contact** - look at camera occasionally
- **Show, don't tell** - let viewers see the data
- **Practice once** - do a dry run before recording final version
- **Good lighting** - make sure face is visible in camera
- **No distractions** - close Slack, email, etc.

### Technical Setup:
- Use Loom's Chrome extension or web recorder
- Select "Share entire tab" if recording just the files
- Select "Share microphone" for audio
- Record in full screen (no taskbar visible)
- Test audio levels before recording

---

## SCRIPT WORDS (USE AS TALKING POINTS)

**Intro (30 sec):**
"Today I'm demonstrating an automated truck fleet evaluation system that analyzes 320 active trucks across 6 data sources to generate data-driven recommendations. Instead of manual analysis taking hours, this system delivers insights in seconds."

**Problem (30 sec):**
"Fleet managers typically work with scattered data - finance records, maintenance logs, GPS tracking, payroll, and market data all in separate files. Combining this information manually is time-consuming and error-prone. We needed a centralized, automated solution."

**Solution (60 sec):**
"The dashboard consolidates everything. It shows all 320 trucks with comprehensive metrics - usage patterns, repair costs, revenue generation, and financial position. The system recommends: Keep 317 trucks, Sell 2 trucks, and Inspect 1 truck. Each recommendation is based on a 0-100 score calculated from usage, reliability, frequency, and financial metrics."

**Logic (60 sec):**
"The scoring works like this: High usage and low maintenance costs increase the score. Low usage with high repairs decrease it. A truck like Truck 0002 with 30,000 miles, zero repairs, and perfect reliability scores 100 - keep it. But SPOT-Truck 0055 with only 4,000 miles, $13,000 in repairs, and a cost of $3.29 per mile scores 60 - sell it. It's purely objective mathematics."

**How It Works (60 sec):**
"Under the hood, Python automates the entire process: Read data from 6 Excel files, clean and standardize it, calculate key metrics like cost-per-mile and 10-week usage, apply the decision algorithm, and export a fresh dashboard. You can run it manually or schedule it daily. The whole analysis completes in 10 seconds for 320 trucks."

**Results (45 sec):**
"The results are strong: 96.6 average score, $0.18 cost-per-mile, $14.6 million in fleet equity, and $10.3 million in revenue. For every dollar spent on maintenance, we collect $7.74 in charges. The fleet is healthy and profitable."

**Closing (15 sec):**
"You get four deliverables: the dashboard Excel file, an executive summary, a detailed user guide, and an automation script. Everything is ready to use immediately for daily fleet management."

---

## VIDEO EDITING NOTES (Optional)

If you want to make it fancier in post-production:
- Add title card at start (5 sec)
- Add captions to key numbers
- Slow down when showing data tables
- Zoom in on important metrics
- Add transitions between sections
- Speed up less interesting parts slightly
- Add music (optional, subtle)
- Add end card with next steps

---

## ALTERNATIVE: SHORTER 3-MINUTE VERSION

If you only have 3 minutes, focus on:
1. **What problem it solves** (30 sec)
2. **Show the dashboard** (90 sec)
3. **Key results** (45 sec)
4. **Call to action** (15 sec)

Remove the detailed technical explanation and keep it high-level.

---

**Ready to record!** Practice once, then hit record in Loom. You've got this!
