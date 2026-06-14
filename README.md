# Data Drift Reporter

> **AI Prototype Challenge — Infinite Solutions Round 3**

A full-stack AI-powered prototype that automatically monitors data quality
and detects drift in business datasets. Upload CSV snapshots of your tables,
and the system computes statistics, stores historical snapshots, compares
trends week-over-week, and generates AI-narrated business reports explaining
what changed and why it matters.

---

## Team Information

| Member | Role Number | Responsibility |
|---|---|---|
| [Student 1 Name] | [Roll No] | UI — Bootstrap dashboard, Chart.js, frontend pages |
| [Student 2 Name] | [Roll No] | Backend — Flask routes, SQLAlchemy models, drift_engine.py |
| [Student 3 Name] | [Roll No] | AI layer — narrator.py, LLM prompts, structured output |
| [Student 4 Name] | [Roll No] | README, test cases, GitHub cleanup, demo video |

**College**: [Your College Name]
**Team Name**: [Your Team Name]

---

## Demo Video

▶️ **[Watch 5-7 min Demo Video Here](https://your-demo-video-link-here)**

---

## Problem Statement

In real-world data pipelines, datasets silently degrade over time — columns
accumulate null values, row counts drop unexpectedly, and value distributions
shift. Without automated monitoring, these changes go undetected until they
cause broken dashboards or bad business decisions.

**Data Drift Reporter** solves this by making drift visible, measurable, and
explainable — in plain English using AI.

---

## Features Implemented

- ✅ CSV dataset upload with schema validation
- ✅ Automatic snapshot generation (row count, null %, mean/median/std/unique per column)
- ✅ Week-over-week drift detection with drift score (0–100) and level (Low/Medium/High)
- ✅ AI-generated business narrative (Claude API with offline rule-based fallback)
- ✅ Interactive dashboard with trend charts (Chart.js)
- ✅ "Update with New Data" — upload a new weekly CSV directly from the UI
- ✅ Downloadable PDF Drift Report and CSV Snapshot History
- ✅ 8 automated pytest tests (all passing)

---

## Architecture Overview

```
User (Browser)
     │
     ▼
Flask App (app.py)
     │
     ├─► drift_engine.py  ──► compute_snapshot_stats()  [pandas/numpy]
     │                    ──► compare_snapshots()        [drift score]
     │                    ──► classify_drift()           [Low/Med/High]
     │
     ├─► narrator.py      ──► LLM (Claude API) or rule-based fallback
     │                    ──► Business narrative + recommendation
     │
     ├─► models.py        ──► SQLAlchemy ORM
     │                    ──► datasets / snapshots / drift_reports tables
     │
     ├─► report_generator.py ──► PDF (fpdf2) + CSV export
     │
     └─► templates/ + static/ ──► Bootstrap 5 + Chart.js dashboard
```

---

## Tools and Technologies Used

| Component | Technology |
|---|---|
| Backend | Python Flask |
| Database | SQLite + SQLAlchemy ORM |
| Data Processing | Pandas + NumPy |
| Frontend | HTML + Bootstrap 5 + Chart.js |
| AI Layer | Claude API (Anthropic) + offline rule-based fallback |
| Reports | fpdf2 (PDF) + Python csv module |
| Testing | pytest |
| Version Control | GitHub |

---

## Project Structure

```
Data-Drift-reporter/
├── app.py                   # Flask app, routes, orchestration
├── models.py                # SQLAlchemy ORM models
├── drift_engine.py          # Stats computation + drift detection
├── narrator.py              # AI narration module
├── report_generator.py      # PDF + CSV report generation
├── requirements.txt         # Python dependencies
├── prompts.md               # All LLM prompts used
├── ai_usage_note.md         # What AI helped with / got wrong
├── .gitignore
│
├── data/                    # Sample input files
│   ├── sample_input.csv         (orders week 1)
│   ├── sample_input_week2.csv   (orders week 2 - with drift)
│   ├── customers_week1.csv
│   └── customers_week2.csv
│
├── outputs/                 # Sample output files
│   ├── final_report.md          (sample drift narrative report)
│   └── sample_output.csv        (sample snapshot CSV export)
│
├── tests/
│   └── test_basic.py        # 8 pytest happy-path tests
│
├── templates/               # Jinja2 HTML templates
│   ├── base.html
│   ├── dashboard.html
│   ├── upload.html
│   ├── datasets.html
│   └── dataset_detail.html
│
└── static/
    ├── css/style.css
    └── js/
        ├── common.js
        ├── dashboard.js
        ├── dataset_detail.js
        ├── datasets.js
        └── upload.js
```

---

## Setup Instructions

### Requirements
- Python 3.9+
- pip

### Install and Run

```bash
# 1. Clone the repository
git clone https://github.com/akki3102/Data-Drift-reporter.git
cd Data-Drift-reporter

# 2. Create virtual environment
python -m venv venv

# 3. Activate (Windows)
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the app
python app.py
```

Open browser: **http://127.0.0.1:5000**

On first run the app auto-creates the database and seeds two sample
datasets (Orders + Customers) with week 1 and week 2 snapshots, so
drift reports and charts are visible immediately.

---

## Sample Input

`data/sample_input.csv` (Week 1 — baseline):
```
order_id,customer_email,order_amount,quantity,region
1001,alice@example.com,120.50,2,East
1002,bob@example.com,85.00,1,West
...
```

`data/sample_input_week2.csv` (Week 2 — with drift):
```
order_id,customer_email,order_amount,quantity,region
1021,,95.00,2,East
1022,bob@example.com,70.00,1,West
...
```

---

## Sample Output

```
Data Quality Report for 'Orders Dataset': overall drift level is High
(drift score: 21.5%). Row count decreased by 15.0%. customer_email
null rate increased from 0% to 29.4%. Average order_amount dropped
18.3% (from $154.62 to $126.18).
Recommendation: Investigate the upstream data pipeline immediately.
```

Full sample: [outputs/final_report.md](outputs/final_report.md)

---

## AI Capability Demonstrated

- **LLM Structured Output**: Drift metrics passed as structured JSON to
  Claude API → returns business narrative with Result / Reasoning /
  Recommended Action.
- **Agent Loop**: read CSV → compute stats → compare snapshots → call
  LLM → validate → save to DB → display on dashboard.
- **Offline Fallback**: Rule-based template narrator works with no API key.

See [prompts.md](prompts.md) for all prompts.
See [ai_usage_note.md](ai_usage_note.md) for AI usage details.

---

## Running Tests

```bash
python -m pytest tests/test_basic.py -v
```

8/8 tests pass covering stats computation, null rate detection,
drift score calculation, level classification, and false-alarm
prevention.

---

## Assumptions and Limitations

- Each CSV = one point-in-time snapshot of a single business table
- Drift compared to immediately previous snapshot only
- SQLite used for simplicity (not for production multi-user use)
- LLM narration needs Anthropic API key (offline fallback provided)
- Sample data uses 8-20 rows (prototype scale per guidelines)

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/upload` | Upload CSV, generate first snapshot |
| GET | `/api/datasets` | List all datasets |
| GET | `/api/snapshots?dataset_id=<id>` | List snapshots |
| GET | `/api/drift-report/<dataset_id>` | List drift reports |
| GET | `/api/dashboard` | Dashboard stats |
| POST | `/api/generate-snapshot/<dataset_id>` | Generate new snapshot |
| POST | `/api/dataset/<dataset_id>/update-data` | Upload new weekly CSV |
| GET | `/reports/pdf/<dataset_id>` | Download PDF report |
| GET | `/reports/csv/<dataset_id>` | Download CSV history |
