# Risk–Return Analysis of Investments 
## Final Year Project Report

**Student:** Data Analyst  
**Period Analysed:** April 2016 – April 2026  
**Stocks:** TCS · Sun Pharma · Mahindra & Mahindra  
**Exchange:** NSE (National Stock Exchange of India)

---

## 1. Introduction

This project analyses 10 years of historical stock data for three major Indian companies listed on the NSE. The objective is to evaluate each stock's risk and return profile and determine which offers the best risk-adjusted performance for different types of investors.

The three companies represent three different sectors:
- **TCS** — Information Technology
- **Sun Pharma (SUNPHARMA)** — Pharmaceuticals
- **Mahindra & Mahindra (M&M)** — Automobile & Manufacturing

---

## 2. Objectives

1. Load and clean 10-year historical stock price data
2. Calculate daily returns, annualised return and risk (volatility)
3. Compute Sharpe Ratio for risk-adjusted performance comparison
4. Analyse correlation between the three stocks
5. Visualise price trends, drawdowns and rolling volatility
6. Derive investment recommendations based on data

---

## 3. Methodology

### 3.1 Data Collection
Historical adjusted closing price data was downloaded from NSE for the period April 2016 to April 2026, resulting in 2,470 trading days per stock.

### 3.2 Data Cleaning
- Standardised column names (lowercase, underscores)
- Parsed date columns to datetime format
- Checked and confirmed zero null values
- Removed duplicate rows
- Sorted by date ascending

### 3.3 Key Formulas

**Daily Return:**
$$R_t = \frac{P_t - P_{t-1}}{P_{t-1}}$$

**Annualised Return:**
$$R_{annual} = \bar{R}_{daily} \times 252$$

**Annualised Volatility (Risk):**
$$\sigma_{annual} = \sigma_{daily} \times \sqrt{252}$$

**Sharpe Ratio:**
$$Sharpe = \frac{R_{annual} - R_f}{\sigma_{annual}}$$

Where $R_f$ = 6.5% (RBI Repo Rate) — risk-free rate benchmark

**Maximum Drawdown:**
$$MDD = \min\left(\frac{P_t - \max(P_0 \ldots P_t)}{\max(P_0 \ldots P_t)}\right)$$

---

## 4. Results

### 4.1 Key Metrics Summary

| Metric | TCS | SUNPHARMA | M&M |
|--------|-----|-----------|-----|
| Annual Return (%) | 12.17 | 12.09 | **21.60** |
| Annual Volatility (%) | **23.63** | 27.43 | 30.35 |
| Sharpe Ratio | 0.240 | 0.204 | **0.497** |
| Max Drawdown (%) | **-45.36** | -60.80 | -72.28 |
| Total 10-Year Return (%) | 150.73 | 126.15 | **429.54** |
| Positive Trading Days | 1,250 | 1,254 | 1,279 |
| Negative Trading Days | 1,214 | 1,209 | 1,185 |

### 4.2 Risk vs Return Analysis

The scatter plot (Chart 03) shows that **M&M** occupies the upper-right quadrant — higher return but also higher risk. **TCS** sits in the lower-left — lower risk with moderate return. **SUNPHARMA** is in an intermediate position but with relatively low return for its level of risk.

### 4.3 Sharpe Ratio Analysis

The Sharpe Ratio measures return earned per unit of risk taken:
- **M&M: 0.497** — Best risk-adjusted performance
- **TCS: 0.240** — Acceptable risk-adjusted performance
- **SUNPHARMA: 0.204** — Lowest risk-adjusted performance

### 4.4 Correlation Analysis

| Pair | Correlation |
|------|------------|
| TCS ↔ SUNPHARMA | ~0.35 |
| TCS ↔ M&M | ~0.45 |
| SUNPHARMA ↔ M&M | ~0.40 |

All stocks show moderate positive correlation, suggesting limited diversification benefit when combining them in a portfolio.

### 4.5 Cumulative Return

₹1 invested in 2016:
- **TCS** → ₹2.51 by 2026
- **SUNPHARMA** → ₹2.26 by 2026
- **M&M** → ₹5.30 by 2026

---

## 5. Visualisations Generated

| Chart | Description |
|-------|-------------|
| 01_price_trend | Absolute closing prices over 10 years |
| 02_normalised_performance | All stocks on same ₹100 base |
| 03_risk_vs_return | Scatter: volatility vs annual return |
| 04_sharpe_ratio | Bar chart of Sharpe Ratios |
| 05_return_distributions | Histogram of daily returns |
| 06_rolling_volatility | 30-day rolling annualised volatility |
| 07_drawdown | Drawdown from peak for each stock |
| 08_correlation_heatmap | Pearson correlation matrix |
| 09_pos_neg_days | Positive vs negative trading days |
| 10_cumulative_return | Growth of ₹1 from 2016 to 2026 |
| 11_summary_dashboard | Combined summary dashboard |

---

## 6. Conclusions

1. **M&M is the best overall performer** with a 429% total return and the highest Sharpe Ratio (0.497), making it ideal for growth-oriented investors despite higher volatility.

2. **TCS is the safest bet** with the lowest volatility (23.6%) and a maximum drawdown of only -45%, suitable for conservative investors seeking stable returns.

3. **SUNPHARMA underperformed** on a risk-adjusted basis — it carries the highest drawdown risk (-60.8%) for a similar annual return to TCS.

4. **Moderate correlations** between all three stocks mean a portfolio combining them would still carry significant market risk.

5. **All three stocks beat inflation** (avg ~5.5% in India) and bank FD rates (~6-7%), confirming equity as a superior long-term wealth creator.

---

## 7. Recommendations

| Investor Profile | Recommended Stock | Reason |
|-----------------|------------------|--------|
| Conservative | TCS | Lowest risk, stable returns |
| Balanced | TCS + M&M (50/50) | Blend of safety and growth |
| Aggressive | M&M | Highest return potential |
| Avoid | SUNPHARMA alone | High risk, low Sharpe Ratio |

---

## 8. Tools & Technologies

- **Python 3** — Core programming language
- **Pandas** — Data manipulation and analysis
- **NumPy** — Numerical computing (returns, std, Sharpe)
- **Matplotlib** — Chart generation
- **Seaborn** — Heatmaps and styled plots

---

*Report generated by: Risk-Return Analysis Pipeline*  
*Data source: NSE Historical Data | Period: 2016–2026*
