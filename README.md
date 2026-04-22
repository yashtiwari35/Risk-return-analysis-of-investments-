# 📊 Risk–Return Analysis of Indian Stocks
## Final Year Project — Data Analytics

---

###  Project Overview
| Field | Detail |
|-------|--------|
| **Stocks** | TCS · Sun Pharma · Mahindra & Mahindra (M&M) |
| **Period** | April 2016 – April 2026 (10 Years) |
| **Exchange** | NSE — National Stock Exchange of India |
| **Risk-Free Rate** | 6.5% p.a. (RBI Repo Rate) |
| **Data Points** | 2,470 trading days per stock |

---

###  Folder Structure
```
Risk_Return_Project/
│
├── data/                          ← Raw CSV files
│   ├── TCS_10y.csv
│   ├── SUNPHARMA_10y.csv
│   └── MM_10years_data.csv
│
├── charts/                        ← All 11 generated charts
│   ├── 01_price_trend.png
│   ├── 02_normalised_performance.png
│   ├── 03_risk_vs_return.png
│   ├── 04_sharpe_ratio.png
│   ├── 05_return_distributions.png
│   ├── 06_rolling_volatility.png
│   ├── 07_drawdown.png
│   ├── 08_correlation_heatmap.png
│   ├── 09_pos_neg_days.png
│   ├── 10_cumulative_return.png
│   └── 11_summary_dashboard.png
│
├── report/
│   ├── results_summary.csv        ← Key metrics table
│   └── Final_Report.md            ← Written project report
│
├── analysis.py                    ← Main Python script (run this)
└── README.md                      ← This file
```

---

###  How to Run
```bash
# Install dependencies (if needed)
pip install pandas numpy matplotlib seaborn

# Run full analysis
python analysis.py
```

---

###  Key Results

| Stock | Annual Return | Volatility | Sharpe Ratio | Total Return (10Y) |
|-------|-------------|------------|-------------|-------------------|
| TCS | 12.17% | 23.63% | 0.240 | 150.73% |
| SUNPHARMA | 12.09% | 27.43% | 0.204 | 126.15% |
| **M&M** | **21.60%** | **30.35%** | **0.497** | **429.54%** |

---

###  Conclusions
1. **M&M** delivered the highest return (429% in 10 years) with the best Sharpe Ratio (0.497)
2. **TCS** is the safest pick — lowest volatility (23.6%) and moderate returns
3. **SUNPHARMA** had the deepest drawdown (-60.8%), indicating high risk periods
4. All three stocks are positively correlated — diversification benefit is limited
5. **Aggressive investors** → M&M | **Conservative investors** → TCS

---

###  Tools Used
- **Python 3** — Core programming
- **Pandas** — Data loading and cleaning
- **NumPy** — Numerical calculations
- **Matplotlib / Seaborn** — Data visualisation
