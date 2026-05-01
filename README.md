# 🏦 CLV & RFM Customer Segmentation Dashboard

> An end-to-end Customer Lifetime Value (CLV) and RFM segmentation pipeline built on synthetic fintech data — with BG-NBD & Gamma-Gamma probabilistic models, AI-powered customer explanations, and interactive visualizations.

---

## 📌 Project Overview

This project simulates a real-world fintech analytics workflow to predict **Customer Lifetime Value**, segment customers using **RFM scoring**, and generate **AI-driven insights** per customer profile. It mirrors the kind of work done at scale in financial services for retention, targeting, and revenue forecasting.

**Built with:** Python · Pandas · Lifetimes · Scikit-learn · Plotly · LangChain · Groq LLM · Google Colab

---

## 🎯 Key Features

| Feature | Description |
|---|---|
| 📊 Synthetic Dataset | 7,000 customers with 22 features including spend, transactions, loyalty, satisfaction |
| 🔁 RFM Segmentation | Customers scored and labeled: Champions, Loyal, At Risk, Hibernating, Lost, etc. |
| 📈 BG-NBD Model | Predicts expected repeat purchases in the next 90 days |
| 💰 Gamma-Gamma Model | Predicts expected average transaction value per customer |
| 🔮 CLV Forecasting | 90-day, 180-day, and 365-day CLV computed per customer |
| 🤖 AI Explanations | LLM (Groq/LLaMA 3) generates plain-English insights for each customer |
| 📉 Interactive Charts | Plotly dashboards for spend distribution, segment breakdown, CLV by channel |
| 🐙 GitHub Ready | Clean export pipeline with versioning setup |

---

## 🗂️ Project Structure

```
clv-merchant-segmentation/
│
├── CLV_Fintech_Dashboard.ipynb   # Main notebook (all sections)
├── README.md
└── outputs/                      # Generated charts and exports (optional)
```

---

## 🔬 Methodology

### 1. Data Generation
A synthetic dataset of 7,000 fintech customers is generated with realistic distributions across:
- Demographics: Age, Location, Income Level
- Behavioural: Total Transactions, Active Days, App Usage Frequency
- Financial: Total Spent, Avg/Max/Min Transaction Value, Cashback, LTV
- Categorical: Acquisition Channel, Product Type, Preferred Payment Method

### 2. Data Cleaning & Preprocessing
- Outlier capping at 1st–99th percentile
- Null removal on critical columns
- Duplicate customer ID removal
- Feature engineering: `recency_days`, `tenure_days`, `avg_spend_per_txn`

### 3. RFM Scoring
Each customer is scored 1–5 on Recency, Frequency, and Monetary dimensions using quintile bucketing. Segments assigned:

| Segment | Criteria |
|---|---|
| Champions | R≥4, F≥4, M≥4 |
| Loyal | R≥3, F≥3 |
| Potential Loyal | R≥3, F≤2 |
| New | R=5, F=1 |
| At Risk | R≤2, F≥3 |
| Hibernating | R≤2, F≤2, M≥3 |
| Lost | Everything else |

### 4. Probabilistic CLV Modelling
- **BG-NBD (Beta-Geometric/NBD):** Models the buy-till-you-die purchase process to predict future transaction frequency
- **Gamma-Gamma:** Models monetary value variation to predict expected spend per transaction
- Combined to produce discounted CLV at 90 / 180 / 365-day horizons (10% annual discount rate)

### 5. AI-Powered Customer Explanations
Using LangChain + Groq (LLaMA 3.3-70B), each customer row is passed to an LLM that generates a plain-English retention recommendation tailored to their segment, CLV, and behavioural profile.

---

## 📊 Dashboard Sections

1. **EDA** — Spend distribution, transaction histograms, correlation heatmap
2. **RFM Analysis** — Segment distribution, RFM score scatter, treemap
3. **CLV Predictions** — CLV by segment, acquisition channel, product type
4. **BG-NBD Validation** — Frequency-recency matrix, probability alive chart
5. **AI Insights** — Per-customer LLM explanations for Champions and At Risk segments

---

## ⚙️ Setup & Usage

### Run on Google Colab (Recommended)
[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/drive/1DEKdE2Ttw2puxMjtlCnlt6YsOMnIznvM)

### Requirements
```bash
pip install lifetimes==0.11.3 plotly==5.20.0 langchain==0.2.5 \
            langchain-groq==0.1.6 scikit-learn==1.4.2 \
            ipywidgets nbformat kaleido
```

### API Keys Needed
| Service | Purpose | Get it |
|---|---|---|
| Groq API | LLM customer explanations | [console.groq.com](https://console.groq.com) |

---

## 📈 Sample Results

- **7,000 customers** processed end-to-end
- RFM segments distributed across 7 categories
- BG-NBD model predicts 90-day purchase probability per customer
- CLV range: ₹0 (churned) to ₹1.2M+ (high-value Champions)
- AI explanations generated for Champion and At Risk cohorts

---

## 💼 Business Context

This project maps directly to real fintech analytics use cases:

- **Customer Retention:** Identify At Risk and Hibernating segments before churn
- **Revenue Forecasting:** 90/180/365-day CLV for financial planning
- **Campaign Targeting:** Personalise offers by segment × acquisition channel
- **Portfolio Analysis:** Product-level CLV breakdown for cross-sell strategy

---

## 🛠️ Tech Stack

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Pandas](https://img.shields.io/badge/Pandas-2.x-150458)
![Plotly](https://img.shields.io/badge/Plotly-5.20-3F4F75)
![Lifetimes](https://img.shields.io/badge/Lifetimes-0.11.3-green)
![LangChain](https://img.shields.io/badge/LangChain-0.2.5-black)
![Groq](https://img.shields.io/badge/Groq-LLaMA3-orange)

---

## 👤 Author

**Gaurav Yadav**
- GitHub: [@Gauravscriptx](https://github.com/Gauravscriptx)

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
