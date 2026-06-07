# Log Anomaly Detector

ML-powered server log monitoring using Isolation Forest. Automatically detects anomalous patterns in server logs in real time — no labeled data required.

**Live demo:** https://jasil-log-anomaly.streamlit.app

---

## What it does

Servers generate thousands of log lines every second. This tool:
1. Parses raw server logs into structured time windows
2. Trains an Isolation Forest model to learn what "normal" looks like
3. Flags windows with unusual error spikes as anomalies
4. Visualizes everything on an interactive dashboard

On the included sample dataset it achieves **100% detection rate** with **0% false positives**.

---

## Demo

![Dashboard](https://i.imgur.com/placeholder.png)

> The green line shows normal error rate over time. Red ✕ marks are anomalies automatically flagged by the ML model.

---

## Tech stack

| Layer | Technology |
|---|---|
| Language | Python 3.11 |
| ML model | Isolation Forest (scikit-learn) |
| Data processing | pandas |
| Dashboard | Streamlit + Plotly |
| Deployment | Streamlit Cloud |

---

## Run it locally

**1. Clone the repo**
```bash
git clone https://github.com/mohammedjasil2005/log-anomaly-detector.git
cd log-anomaly-detector
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Generate sample logs**
```bash
python generate_logs.py
```

**4. Run the ML model**
```bash
python parser.py
python model.py
```

**5. Launch the dashboard**
```bash
streamlit run dashboard.py
```

Open http://localhost:8501 in your browser.

---

## How it works

### 1. Log parsing (`parser.py`)
Reads raw log files and extracts structured features using regex. Rolls up individual log lines into 1-minute time windows with:
- Total log count
- Error count and error rate
- Warning count
- Average message length

### 2. Anomaly detection (`model.py`)
Trains an **Isolation Forest** — an unsupervised ML algorithm that isolates outliers by randomly partitioning the feature space. Windows that require fewer partitions to isolate are more anomalous.

No labeled data needed. The model learns what "normal" looks like entirely from the data.

### 3. Dashboard (`dashboard.py`)
Interactive Streamlit dashboard showing:
- Summary metrics (total windows, anomaly count, detection rate)
- Error rate over time with anomalies highlighted
- Log volume per minute
- Detailed anomaly table with scores

---

## Project structure

```
log-anomaly-detector/
├── data/
│   ├── server.log          # Raw generated logs
│   ├── features.csv        # Parsed feature windows
│   └── results.csv         # Model output with anomaly flags
├── generate_logs.py        # Synthetic log generator with injected anomalies
├── parser.py               # Log parser and feature engineer
├── model.py                # Isolation Forest anomaly detector
├── dashboard.py            # Streamlit dashboard
└── requirements.txt
```

---

## Results

| Metric | Value |
|---|---|
| Total time windows | 50 |
| Anomalies injected | 5 |
| Anomalies detected | 5 |
| Detection rate | 100% |
| False positive rate | 0% |

---

## Author

**Mohammed Jasil**
- GitHub: [@mohammedjasil2005](https://github.com/mohammedjasil2005)

---

## What's next

This project is part of a larger portfolio being built toward FAANG-level roles. Coming next:
- **Project 2:** Semantic Search Engine using vector embeddings and RAG
- **Project 3:** Network Intrusion Detection System
- **Project 4:** AI-powered Code Review & Security Audit Bot
