"""
   Risk–Return Analysis of Investments — Streamlit Dashboard                    
   Run: streamlit run app.py  
"""

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
import os
import warnings

warnings.filterwarnings('ignore')

# ── Page Config ──────────────────────────────────────────────────
st.set_page_config(
    page_title="Risk–Return Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── CSS Styling ───────────────────────────────────────────────────
st.markdown("""
<style>
    .main { background-color: #0f1117; }
    .metric-card {
        background: linear-gradient(135deg, #1e2130, #252a3d);
        border-radius: 12px;
        padding: 18px 22px;
        border-left: 4px solid;
        margin-bottom: 8px;
    }
    .metric-val { font-size: 28px; font-weight: 700; }
    .metric-lbl { font-size: 12px; color: #aaa; margin-top: 2px; }
    .section-title {
        font-size: 20px; font-weight: 700;
        color: #e0e0e0; margin: 18px 0 8px 0;
        border-bottom: 2px solid #2a2f45;
        padding-bottom: 6px;
    }
    .winner-badge {
        background: linear-gradient(135deg, #1a3a2a, #1e4a30);
        border: 1px solid #4CAF7D;
        border-radius: 8px;
        padding: 10px 16px;
        color: #4CAF7D;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── Constants ─────────────────────────────────────────────────────
COLORS = {'TCS': '#378ADD', 'SUNPHARMA': '#E8874A', 'M&M': '#4CAF7D'}
RISK_FREE_DAILY = 0.065 / 252
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')

# ── Load & Cache Data ─────────────────────────────────────────────
@st.cache_data
def load_data():
    def clean(df, name):
        df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.drop_duplicates().dropna().sort_values('date').reset_index(drop=True)
        df['daily_return'] = df['adj_close'].pct_change()
        return df

    tcs = clean(pd.read_csv(os.path.join(DATA_DIR, 'TCS_10y.csv')),       'TCS')
    sun = clean(pd.read_csv(os.path.join(DATA_DIR, 'SUNPHARMA_10y.csv')), 'SUNPHARMA')
    mm  = clean(pd.read_csv(os.path.join(DATA_DIR, 'MM_10years_data.csv')),'M&M')
    return tcs, sun, mm

@st.cache_data
def compute_metrics(tcs, sun, mm):
    rows = []
    for df, name in [(tcs, 'TCS'), (sun, 'SUNPHARMA'), (mm, 'M&M')]:
        r = df['daily_return'].dropna()
        roll_max = df['adj_close'].cummax()
        dd = (df['adj_close'] - roll_max) / roll_max
        rows.append({
            'Stock'                  : name,
            'Annual Return (%)'      : round(r.mean() * 252 * 100, 2),
            'Annual Volatility (%)'  : round(r.std() * np.sqrt(252) * 100, 2),
            'Sharpe Ratio'           : round((r.mean() - RISK_FREE_DAILY) / r.std() * np.sqrt(252), 3),
            'Max Drawdown (%)'       : round(dd.min() * 100, 2),
            'Total Return (%)'       : round(((df['adj_close'].iloc[-1] / df['adj_close'].iloc[0]) - 1) * 100, 2),
            'Positive Days'          : int((r > 0).sum()),
            'Negative Days'          : int((r < 0).sum()),
        })
    res = pd.DataFrame(rows).set_index('Stock')
    return res

# ── Load ──────────────────────────────────────────────────────────
tcs, sun, mm = load_data()
results = compute_metrics(tcs, sun, mm)
stocks  = [(tcs, 'TCS', COLORS['TCS']),
           (sun, 'SUNPHARMA', COLORS['SUNPHARMA']),
           (mm,  'M&M',       COLORS['M&M'])]

# ════════════════════════════════════════════════════════════════
#  SIDEBAR
# ════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("## ⚙️ Controls")
    selected = st.multiselect(
        "Select Stocks",
        ['TCS', 'SUNPHARMA', 'M&M'],
        default=['TCS', 'SUNPHARMA', 'M&M']
    )

    st.markdown("---")
    date_range = st.date_input(
        "Date Range",
        value=(tcs['date'].iloc[0].date(), tcs['date'].iloc[-1].date()),
        min_value=tcs['date'].iloc[0].date(),
        max_value=tcs['date'].iloc[-1].date(),
    )

    st.markdown("---")
    rf_rate = st.slider("Risk-Free Rate (%)", 4.0, 10.0, 6.5, 0.5)
    rolling_window = st.slider("Rolling Volatility Window (days)", 10, 90, 30, 5)

    st.markdown("---")
    st.markdown("### 📌 Project Info")
    st.info("**Exchange:** NSE India\n\n**Period:** 2016–2026\n\n**Data Points:** 2,470 days/stock")

# Filter by date and selection
start_date = pd.Timestamp(date_range[0])
end_date   = pd.Timestamp(date_range[1]) if len(date_range) > 1 else pd.Timestamp(date_range[0])
rf_daily   = rf_rate / 100 / 252

def filter_df(df):
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)].copy()

filtered = {name: filter_df(df) for df, name, _ in stocks if name in selected}
active_stocks = [(filtered[name], name, col) for _, name, col in stocks if name in selected]

# ════════════════════════════════════════════════════════════════
#  HEADER
# ════════════════════════════════════════════════════════════════
st.markdown("# 📊 Risk–Return Analysis of Indian Stocks")
st.markdown("**TCS · Sun Pharma · Mahindra & Mahindra &nbsp;|&nbsp; NSE India &nbsp;|&nbsp; 2016–2026**")
st.markdown("---")

# ════════════════════════════════════════════════════════════════
#  TABS
# ════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🏠 Overview",
    "📈 Price & Returns",
    "⚖️ Risk Analysis",
    "🔗 Correlation",
    "📋 Raw Data",
])

# ──────────────────────────────────────────────
# TAB 1 — OVERVIEW
# ──────────────────────────────────────────────
with tab1:
    st.markdown('<div class="section-title">📊 Key Metrics</div>', unsafe_allow_html=True)

    for name in selected:
        r = results.loc[name]
        col_color = COLORS[name]
        c1, c2, c3, c4, c5 = st.columns(5)
        st.markdown(f"#### {name}")
        cols = st.columns(5)
        metrics = [
            ("Annual Return", f"{r['Annual Return (%)']:.2f}%"),
            ("Volatility",    f"{r['Annual Volatility (%)']:.2f}%"),
            ("Sharpe Ratio",  f"{r['Sharpe Ratio']:.3f}"),
            ("Max Drawdown",  f"{r['Max Drawdown (%)']:.2f}%"),
            ("Total Return",  f"{r['Total Return (%)']:.1f}%"),
        ]
        for col, (lbl, val) in zip(cols, metrics):
            col.metric(lbl, val)
        st.markdown("---")

    # Summary table
    st.markdown('<div class="section-title">📋 Comparison Table</div>', unsafe_allow_html=True)
    st.dataframe(results.loc[selected].style.highlight_max(
        subset=['Annual Return (%)', 'Sharpe Ratio', 'Total Return (%)'],
        color='#27ae60'
    ).highlight_min(
        subset=['Annual Volatility (%)', 'Max Drawdown (%)'],
        color='#27ae60'
    ), use_container_width=True)

    # Winner
    if selected:
        best = results.loc[selected, 'Sharpe Ratio'].idxmax()
        st.markdown(f"""
        <div class="winner-badge">
        🏆 Best Risk-Adjusted Pick (Sharpe Ratio): <strong>{best}</strong>
        &nbsp;|&nbsp; Sharpe = {results.loc[best, 'Sharpe Ratio']}
        </div>
        """, unsafe_allow_html=True)

# ──────────────────────────────────────────────
# TAB 2 — PRICE & RETURNS
# ──────────────────────────────────────────────
with tab2:
    if not active_stocks:
        st.warning("Please select at least one stock from the sidebar.")
    else:
        # Price Trend
        st.markdown('<div class="section-title">📈 Adjusted Closing Price</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(13, 4), facecolor='#0f1117')
        ax.set_facecolor('#1a1d27')
        for df, name, col in active_stocks:
            ax.plot(df['date'], df['adj_close'], label=name, color=col, linewidth=1.4)
        ax.set_xlabel('Date', color='#aaa'); ax.set_ylabel('Price (₹)', color='#aaa')
        ax.tick_params(colors='#aaa'); ax.spines[:].set_color('#333')
        ax.legend(facecolor='#1a1d27', labelcolor='white')
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Normalised
        st.markdown('<div class="section-title">📊 Normalised Performance (Base = ₹100)</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(13, 4), facecolor='#0f1117')
        ax.set_facecolor('#1a1d27')
        for df, name, col in active_stocks:
            norm = df['adj_close'] / df['adj_close'].iloc[0] * 100
            ax.plot(df['date'], norm, label=name, color=col, linewidth=1.4)
        ax.axhline(100, color='#555', linestyle='--', linewidth=0.8)
        ax.set_ylabel('Indexed Value', color='#aaa'); ax.tick_params(colors='#aaa')
        ax.spines[:].set_color('#333')
        ax.legend(facecolor='#1a1d27', labelcolor='white')
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Cumulative Return
        st.markdown('<div class="section-title">💰 Cumulative Return (₹1 invested)</div>', unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(13, 4), facecolor='#0f1117')
        ax.set_facecolor('#1a1d27')
        for df, name, col in active_stocks:
            cum = (1 + df['daily_return'].fillna(0)).cumprod()
            ax.plot(df['date'], cum, label=name, color=col, linewidth=1.4)
        ax.set_ylabel('Growth of ₹1', color='#aaa'); ax.tick_params(colors='#aaa')
        ax.spines[:].set_color('#333')
        ax.legend(facecolor='#1a1d27', labelcolor='white')
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Daily Return Distribution
        st.markdown('<div class="section-title">📉 Daily Return Distributions</div>', unsafe_allow_html=True)
        fig, axes = plt.subplots(1, len(active_stocks),
                                  figsize=(5 * len(active_stocks), 4), facecolor='#0f1117')
        if len(active_stocks) == 1:
            axes = [axes]
        for ax, (df, name, col) in zip(axes, active_stocks):
            ax.set_facecolor('#1a1d27')
            r = df['daily_return'].dropna()
            ax.hist(r, bins=70, color=col, alpha=0.85, edgecolor='none')
            ax.axvline(r.mean(), color='red', linestyle='--', linewidth=1.2,
                       label=f'Mean: {r.mean():.4f}')
            ax.set_title(name, color='white', fontsize=12)
            ax.tick_params(colors='#aaa'); ax.spines[:].set_color('#333')
            ax.legend(facecolor='#1a1d27', labelcolor='white', fontsize=9)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

# ──────────────────────────────────────────────
# TAB 3 — RISK ANALYSIS
# ──────────────────────────────────────────────
with tab3:
    if not active_stocks:
        st.warning("Please select at least one stock.")
    else:
        c1, c2 = st.columns(2)

        # Risk vs Return Scatter
        with c1:
            st.markdown('<div class="section-title">⚖️ Risk vs Return</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(6, 5), facecolor='#0f1117')
            ax.set_facecolor('#1a1d27')
            for _, name, col in active_stocks:
                r = results.loc[name]
                ax.scatter(r['Annual Volatility (%)'], r['Annual Return (%)'],
                           color=col, s=200, zorder=5)
                ax.annotate(name, (r['Annual Volatility (%)'], r['Annual Return (%)']),
                            xytext=(8, 4), textcoords='offset points',
                            color='white', fontsize=10)
            ax.set_xlabel('Risk / Volatility (%)', color='#aaa')
            ax.set_ylabel('Annual Return (%)', color='#aaa')
            ax.tick_params(colors='#aaa'); ax.spines[:].set_color('#333')
            fig.tight_layout()
            st.pyplot(fig)
            plt.close()

        # Sharpe Ratio
        with c2:
            st.markdown('<div class="section-title">⭐ Sharpe Ratio</div>', unsafe_allow_html=True)
            fig, ax = plt.subplots(figsize=(6, 5), facecolor='#0f1117')
            ax.set_facecolor('#1a1d27')
            names   = [name for _, name, _ in active_stocks]
            sharpes = [results.loc[name, 'Sharpe Ratio'] for name in names]
            colors  = [COLORS[name] for name in names]
            bars = ax.bar(names, sharpes, color=colors, width=0.5)
            for bar, val in zip(bars, sharpes):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01,
                        f'{val:.3f}', ha='center', color='white', fontsize=12, fontweight='bold')
            ax.axhline(0, color='#555', linewidth=0.8)
            ax.set_ylabel('Sharpe Ratio', color='#aaa')
            ax.tick_params(colors='#aaa'); ax.spines[:].set_color('#333')
            fig.tight_layout()
            st.pyplot(fig)
            plt.close()

        # Rolling Volatility
        st.markdown(f'<div class="section-title">📉 Rolling {rolling_window}-Day Volatility</div>',
                    unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(13, 4), facecolor='#0f1117')
        ax.set_facecolor('#1a1d27')
        for df, name, col in active_stocks:
            rv = df['daily_return'].rolling(rolling_window).std() * np.sqrt(252) * 100
            ax.plot(df['date'], rv, label=name, color=col, linewidth=1.2)
        ax.set_ylabel('Annualised Volatility (%)', color='#aaa')
        ax.tick_params(colors='#aaa'); ax.spines[:].set_color('#333')
        ax.legend(facecolor='#1a1d27', labelcolor='white')
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Drawdown
        st.markdown('<div class="section-title">📉 Drawdown from Peak</div>', unsafe_allow_html=True)
        fig, axes = plt.subplots(1, len(active_stocks),
                                  figsize=(5 * len(active_stocks), 4), facecolor='#0f1117')
        if len(active_stocks) == 1:
            axes = [axes]
        for ax, (df, name, col) in zip(axes, active_stocks):
            ax.set_facecolor('#1a1d27')
            roll_max = df['adj_close'].cummax()
            dd = (df['adj_close'] - roll_max) / roll_max * 100
            ax.fill_between(df['date'], dd, 0, color=col, alpha=0.6)
            ax.set_title(name, color='white')
            ax.set_ylabel('Drawdown (%)', color='#aaa')
            ax.tick_params(colors='#aaa'); ax.spines[:].set_color('#333')
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

        # Positive vs Negative Days
        st.markdown('<div class="section-title">📅 Positive vs Negative Days</div>',
                    unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(8, 4), facecolor='#0f1117')
        ax.set_facecolor('#1a1d27')
        names = [name for _, name, _ in active_stocks]
        x = np.arange(len(names)); w = 0.35
        pos = [results.loc[n, 'Positive Days'] for n in names]
        neg = [results.loc[n, 'Negative Days'] for n in names]
        ax.bar(x - w/2, pos, w, label='Positive Days', color='#4CAF7D')
        ax.bar(x + w/2, neg, w, label='Negative Days', color='#E57373')
        ax.set_xticks(x); ax.set_xticklabels(names, color='white')
        ax.tick_params(colors='#aaa'); ax.spines[:].set_color('#333')
        ax.legend(facecolor='#1a1d27', labelcolor='white')
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

# ──────────────────────────────────────────────
# TAB 4 — CORRELATION
# ──────────────────────────────────────────────
with tab4:
    if len(active_stocks) < 2:
        st.warning("Select at least 2 stocks to view correlation.")
    else:
        combined = pd.DataFrame({
            name: df['daily_return']
            for df, name, _ in active_stocks
        }).dropna()
        corr = combined.corr()

        st.markdown('<div class="section-title">🔗 Correlation Matrix — Daily Returns</div>',
                    unsafe_allow_html=True)
        fig, ax = plt.subplots(figsize=(7, 5), facecolor='#0f1117')
        ax.set_facecolor('#1a1d27')
        sns.heatmap(corr, annot=True, fmt='.3f', cmap='RdYlGn',
                    center=0, vmin=-1, vmax=1, linewidths=0.5,
                    annot_kws={'color': 'white', 'size': 13}, ax=ax)
        ax.tick_params(colors='white')
        fig.tight_layout()
        st.pyplot(fig)
        plt.close()

        st.markdown("**Interpretation:**")
        for i, s1 in enumerate(corr.columns):
            for s2 in corr.columns[i+1:]:
                v = corr.loc[s1, s2]
                level = "Strong" if abs(v) > 0.7 else "Moderate" if abs(v) > 0.4 else "Weak"
                st.markdown(f"- **{s1} ↔ {s2}:** `{v:.3f}` — {level} positive correlation")

# ──────────────────────────────────────────────
# TAB 5 — RAW DATA
#────────────────────────────────────────────
with tab5:
    stock_choice = st.selectbox("View data for:", selected)
    df_map = {name: df for df, name, _ in active_stocks}
    if stock_choice in df_map:
        df_show = df_map[stock_choice][['date', 'open', 'high', 'low', 'close', 'adj_close', 'volume', 'daily_return']].copy()
        df_show['daily_return'] = df_show['daily_return'].round(5)
        st.dataframe(df_show, use_container_width=True, height=400)
        csv = df_show.to_csv(index=False).encode('utf-8')
        st.download_button(f"⬇️ Download {stock_choice} CSV", csv,
                           file_name=f"{stock_choice}_cleaned.csv", mime='text/csv')

# ── Footer ────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<center style='color:#555;font-size:13px;'>"
    "📊 Risk–Return Analysis | Final Year Project | NSE India 2016–2026"
    "</center>",
    unsafe_allow_html=True
)
