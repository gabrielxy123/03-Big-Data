"""
╔════════════════════════════════════════════════════════════════════╗
║   Amazon Sales Pipeline — Premium Professional Dashboard            ║
║   Version: 4.0 — Elegant & Professional with Brand Typography      ║
║   Jalankan: streamlit run app.py                                   ║
╚════════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
from pathlib import Path
from datetime import datetime
import time

# ═══════════════════════════════════════════════════════════════════
# PAGE CONFIG
# ═══════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Amazon Sales Pipeline Dashboard",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ═══════════════════════════════════════════════════════════════════
# PREMIUM COLOR PALETTE
# ═══════════════════════════════════════════════════════════════════
COLORS = {
    # Primary & Background
    "bg_main": "#fafbfd",
    "bg_secondary": "#ffffff",
    "bg_accent": "#eef2f9",
    "bg_warm": "#fef9f5",
    
    # Amazon Brand Colors
    "amazon_orange": "#ff9900",
    "amazon_blue": "#146eb4",
    "amazon_dark": "#37475a",
    
    # Premium Accent Colors
    "accent_emerald": "#059669",
    "accent_cyan": "#0891b2",
    "accent_purple": "#7c3aed",
    "accent_rose": "#e11d48",
    "accent_amber": "#d97706",
    "accent_teal": "#0d9488",
    
    # Text Colors
    "text_primary": "#1f2937",
    "text_secondary": "#4b5563",
    "text_light": "#8b92a0",
    "text_muted": "#b0b8c5",
    
    # Borders & Dividers
    "border_default": "#d5dce3",
    "border_light": "#e5ecf3",
}

# ═══════════════════════════════════════════════════════════════════
# PREMIUM CSS STYLING
# ═══════════════════════════════════════════════════════════════════

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&family=Sora:wght@400;500;600;700&family=Lexend:wght@300;400;500;600;700&display=swap');

* {{
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}}

/* ═══ HIDE STREAMLIT DEFAULT HEADER / TOOLBAR ═══ */
[data-testid="stHeader"] {{
    display: none !important;
}}
[data-testid="stToolbar"] {{
    display: none !important;
}}
#MainMenu {{
    display: none !important;
}}
footer {{
    visibility: hidden;
}}
.stDeployButton {{
    display: none !important;
}}

/* ═══ MAIN APP ═══ */
.stApp {{
    background: linear-gradient(135deg, {COLORS['bg_main']} 0%, {COLORS['bg_accent']} 50%, {COLORS['bg_main']} 100%);
    color: {COLORS['text_primary']};
    margin-top: 0 !important;
    padding-top: 0 !important;
}}

/* ═══ INFO BOX — override Streamlit default agar terbaca ═══ */
[data-testid="stNotificationContentInfo"] {{
    background: rgba(20, 110, 180, 0.10) !important;
    border: 1px solid rgba(20, 110, 180, 0.35) !important;
    border-radius: 10px;
    color: {COLORS['amazon_blue']} !important;
    font-weight: 600;
}}
[data-testid="stNotificationContentInfo"] p {{
    color: {COLORS['amazon_blue']} !important;
    font-weight: 600;
}}

/* ═══ SIDEBAR ═══ */
[data-testid="stSidebar"] {{
    background: linear-gradient(180deg, #ffffff 0%, {COLORS['bg_accent']} 100%) !important;
    border-right: 1px solid {COLORS['border_light']};
}}

/* ═══ KPI CARDS - PREMIUM DESIGN ═══ */
.kpi-card {{
    background: linear-gradient(135deg, {COLORS['bg_secondary']} 0%, {COLORS['bg_accent']} 100%);
    backdrop-filter: blur(10px);
    border: 1px solid {COLORS['border_light']};
    border-radius: 20px;
    padding: 28px;
    transition: all 0.4s cubic-bezier(0.34, 1.56, 0.64, 1);
    box-shadow: 0 2px 12px rgba(31, 41, 55, 0.06), inset 0 1px 2px rgba(255, 255, 255, 0.8);
    position: relative;
    overflow: hidden;
}}

.kpi-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, {COLORS['amazon_orange']}, {COLORS['amazon_blue']}, {COLORS['accent_emerald']}, {COLORS['accent_purple']});
    border-radius: 20px 20px 0 0;
}}

.kpi-card:hover {{
    transform: translateY(-6px);
    border-color: {COLORS['amazon_blue']};
    box-shadow: 0 8px 24px rgba(20, 110, 180, 0.12), inset 0 1px 2px rgba(255, 255, 255, 0.8);
}}

/* ═══ KPI LABEL ═══ */
.kpi-label {{
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 1px;
    text-transform: uppercase;
    color: {COLORS['text_light']};
    margin-bottom: 12px;
    font-family: 'Sora', sans-serif;
}}

/* ═══ KPI VALUE - FIXED HEIGHT & ALIGNMENT ═══ */
.kpi-value {{
    font-size: 40px;
    font-weight: 800;
    background: linear-gradient(135deg, {COLORS['amazon_blue']}, {COLORS['accent_purple']});
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    line-height: 1.2;
    font-family: 'Lexend', sans-serif;
    letter-spacing: -0.5px;
    min-height: 58px;
    display: flex;
    align-items: center;
}}

/* ═══ KPI SUBTEXT ═══ */
.kpi-sub {{
    color: {COLORS['text_secondary']};
    font-size: 14px;
    margin-top: 8px;
    font-weight: 500;
}}

/* ═══ BADGES ═══ */
.kpi-badge {{
    display: inline-block;
    margin-top: 14px;
    padding: 8px 16px;
    border-radius: 50px;
    font-size: 12px;
    font-weight: 700;
    font-family: 'Sora', sans-serif;
    letter-spacing: 0.3px;
}}

.badge-blue {{
    background: linear-gradient(135deg, rgba(20, 110, 180, 0.12), rgba(8, 145, 178, 0.08));
    color: {COLORS['amazon_blue']};
    border: 1px solid rgba(20, 110, 180, 0.2);
}}

.badge-green {{
    background: linear-gradient(135deg, rgba(5, 150, 105, 0.12), rgba(13, 148, 136, 0.08));
    color: {COLORS['accent_emerald']};
    border: 1px solid rgba(5, 150, 105, 0.2);
}}

.badge-orange {{
    background: linear-gradient(135deg, rgba(255, 153, 0, 0.12), rgba(217, 119, 6, 0.08));
    color: {COLORS['amazon_orange']};
    border: 1px solid rgba(255, 153, 0, 0.2);
}}

.badge-purple {{
    background: linear-gradient(135deg, rgba(124, 58, 237, 0.12), rgba(168, 85, 245, 0.08));
    color: {COLORS['accent_purple']};
    border: 1px solid rgba(124, 58, 237, 0.2);
}}

/* ═══ SECTION HEADER ═══ */
.section-header {{
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    color: {COLORS['text_primary']};
    margin-top: 40px;
    margin-bottom: 20px;
    padding-bottom: 12px;
    border-bottom: 2px solid {COLORS['border_light']};
    position: relative;
    font-family: 'Sora', sans-serif;
}}

.section-header::before {{
    content: '';
    position: absolute;
    bottom: -2px;
    left: 0;
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, {COLORS['amazon_orange']}, {COLORS['amazon_blue']});
    border-radius: 2px;
}}

/* ═══ TABS ═══ */
.stTabs [data-baseweb="tab-list"] {{
    background: transparent;
    border-radius: 16px;
    padding: 0;
    gap: 10px;
    border-bottom: 2px solid {COLORS['border_light']};
}}

.stTabs [data-baseweb="tab"] {{
    border-radius: 12px;
    color: {COLORS['text_secondary']};
    padding: 14px 22px;
    font-weight: 600;
    font-size: 15px;
    background: transparent;
    border: 2px solid transparent;
    transition: all 0.3s ease;
}}

.stTabs [aria-selected="true"] {{
    background: linear-gradient(135deg, {COLORS['amazon_blue']}, {COLORS['accent_cyan']}) !important;
    color: white !important;
    border: 2px solid {COLORS['amazon_blue']} !important;
    box-shadow: 0 4px 12px rgba(20, 110, 180, 0.2);
}}

/* ═══ SELECTBOX ═══ */
.stSelectbox div[data-baseweb="select"] {{
    background: {COLORS['bg_secondary']};
    border-radius: 12px;
    border: 1px solid {COLORS['border_light']};
    font-size: 14px;
}}

.stSelectbox div[data-baseweb="select"]:hover {{
    border-color: {COLORS['amazon_blue']};
}}

/* ═══ BUTTON ═══ */
.stButton button {{
    background: linear-gradient(135deg, {COLORS['amazon_blue']}, {COLORS['accent_cyan']});
    color: white;
    border: none;
    border-radius: 12px;
    padding: 14px 24px;
    font-weight: 700;
    font-size: 14px;
    transition: all 0.35s cubic-bezier(0.34, 1.56, 0.64, 1);
    font-family: 'Plus Jakarta Sans', sans-serif;
    letter-spacing: 0.3px;
}}

.stButton button:hover {{
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(20, 110, 180, 0.3);
}}

/* ═══ TABLE ═══ */
[data-testid="stDataFrame"] {{
    border-radius: 16px;
    overflow: hidden;
    border: 1px solid {COLORS['border_light']};
    background: {COLORS['bg_secondary']};
    font-size: 14px;
}}

/* ═══ METRICS ═══ */
div[data-testid="metric-container"] {{
    background: linear-gradient(135deg, {COLORS['bg_secondary']}, {COLORS['bg_accent']});
    border: 1px solid {COLORS['border_light']};
    padding: 18px;
    border-radius: 16px;
}}

/* ═══ SCROLLBAR ═══ */
::-webkit-scrollbar {{
    width: 10px;
}}

::-webkit-scrollbar-thumb {{
    background: linear-gradient(180deg, {COLORS['amazon_blue']}, {COLORS['accent_purple']});
    border-radius: 20px;
}}

::-webkit-scrollbar-track {{
    background: {COLORS['bg_accent']};
}}

/* ═══ DIVIDER ═══ */
hr {{
    border: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, {COLORS['border_light']}, transparent);
    margin: 28px 0;
}}

</style>
""", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# PLOTLY PREMIUM THEME
# ═══════════════════════════════════════════════════════════════════
PLOTLY_THEME = dict(
    paper_bgcolor="rgba(255,255,255,0)",
    plot_bgcolor="rgba(250, 251, 253, 0.6)",

    font=dict(
        family="Plus Jakarta Sans, Segoe UI",
        color=COLORS['text_primary'],
        size=13
    ),

    colorway=[
        COLORS['amazon_blue'],
        COLORS['amazon_orange'],
        COLORS['accent_emerald'],
        COLORS['accent_purple'],
        COLORS['accent_amber'],
        COLORS['accent_cyan'],
        COLORS['accent_rose'],
        COLORS['accent_teal'],
    ],

    xaxis=dict(
        gridcolor="rgba(213, 220, 227, 0.3)",
        zeroline=False,
        linecolor=COLORS['border_light'],
        tickfont=dict(size=12, color=COLORS['text_secondary']),
    ),

    yaxis=dict(
        gridcolor="rgba(213, 220, 227, 0.3)",
        zeroline=False,
        linecolor=COLORS['border_light'],
        tickfont=dict(size=12, color=COLORS['text_secondary']),
    ),

    margin=dict(l=20, r=20, t=60, b=20),
)

def apply_theme(fig, title="", title_size=16):
    fig.update_layout(
        **PLOTLY_THEME,
        title=dict(
            text=title,
            font=dict(size=title_size, color=COLORS['text_primary'], family="Sora"),
            x=0.5,
            xanchor="center",
        ),
        showlegend=True,
        legend=dict(
            orientation="v",
            yanchor="top",
            y=0.99,
            xanchor="left",
            x=0.01,
            bgcolor="rgba(255, 255, 255, 0.85)",
            bordercolor=COLORS['border_light'],
            borderwidth=1,
            font=dict(size=12),
        ),
        hovermode="x unified",
    )
    return fig

# ═══════════════════════════════════════════════════════════════════
# DATA LOADING
# ═══════════════════════════════════════════════════════════════════
DATA_DIR = Path("streamlit_data")

def load_json(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return None
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    # Pipeline bisa menghasilkan format list-of-dicts ATAU dict-of-lists
    if isinstance(raw, list):
        return pd.DataFrame(raw)
    elif isinstance(raw, dict):
        # Spark .write.json() kadang: {"columns":[...], "data":[[...]]}
        if "columns" in raw and "data" in raw:
            return pd.DataFrame(raw["data"], columns=raw["columns"])
        # Format dict-of-lists biasa
        return pd.DataFrame(raw)
    return None

def make_dummy_data():
    import numpy as np
    np.random.seed(42)

    categories = ["Set", "kurta", "Western Dress", "Top", "Ethnic Dress", "Blouse", "Bottom", "Saree"]
    months = ["January", "February", "March", "April", "May", "June"]
    states = ["MAHARASHTRA", "KARNATAKA", "DELHI", "TAMIL NADU", "TELANGANA",
              "UTTAR PRADESH", "GUJARAT", "RAJASTHAN", "WEST BENGAL", "ANDHRA PRADESH"]

    cat_stats = pd.DataFrame({
        "category": categories,
        "total_orders": np.random.randint(3000, 30000, len(categories)),
        "total_qty_sold": np.random.randint(5000, 50000, len(categories)),
        "total_revenue": np.random.uniform(500000, 8000000, len(categories)).round(2),
        "avg_price": np.random.uniform(300, 900, len(categories)).round(2),
        "max_price": np.random.uniform(1500, 3000, len(categories)).round(2),
        "min_price": np.random.uniform(50, 200, len(categories)).round(2),
    })

    monthly = pd.DataFrame({
        "year": [2022] * 6,
        "month": range(1, 7),
        "month_name": months,
        "total_orders": np.random.randint(8000, 25000, 6),
        "total_revenue": np.random.uniform(2000000, 8000000, 6).round(2),
        "total_qty": np.random.randint(10000, 40000, 6),
        "unique_categories": [len(categories)] * 6,
    })

    status = pd.DataFrame({
        "status_group": ["Shipped", "Cancelled", "Pending", "Other"],
        "total_orders": [78000, 15000, 5000, 2000],
        "total_revenue": [45000000, 0, 0, 0],
        "pct_orders": [78.0, 15.0, 5.0, 2.0],
    })

    top_states = pd.DataFrame({
        "ship_state": states,
        "total_orders": np.random.randint(2000, 18000, len(states)),
        "total_revenue": np.random.uniform(500000, 6000000, len(states)).round(2),
    })

    b2b_b2c = pd.DataFrame({
        "customer_type": ["B2C", "B2B"],
        "total_orders": [92000, 8000],
        "total_revenue": [52000000, 6000000],
        "avg_order_value": [565.0, 720.0],
    })

    summary = {
        "total_orders": 100000,
        "total_revenue": 58000000.0,
        "shipped_orders": 78000,
        "shipped_rate": 78.0,
        "top_category": "Set",
    }

    heatmap_data = []
    for cat in categories:
        for i, m in enumerate(months):
            heatmap_data.append({
                "category": cat, "month_name": m, "month": i+1,
                "total_revenue": np.random.uniform(50000, 2000000),
            })
    heatmap_df = pd.DataFrame(heatmap_data)

    mom_growth = pd.DataFrame({
        "year": [2022]*6, "month": range(1,7), "month_name": months,
        "total_revenue": [3200000, 4100000, 5800000, 5100000, 6200000, 5700000],
        "total_orders": [10200, 13500, 18900, 16700, 20100, 18400],
        "prev_month_revenue": [None, 3200000, 4100000, 5800000, 5100000, 6200000],
        "mom_growth_pct": [None, 28.1, 41.5, -12.1, 21.6, -8.1],
    })

    price_segs = []
    for cat in categories:
        for seg in ["Budget (<300 INR)", "Mid-Range (300-700 INR)", "Premium (>700 INR)"]:
            price_segs.append({
                "category": cat, "price_segment": seg,
                "total_orders": np.random.randint(500, 8000),
                "total_revenue": np.random.uniform(100000, 2000000).round(2),
                "avg_price": np.random.uniform(150, 1200).round(2),
                "total_qty": np.random.randint(500, 10000),
            })
    price_seg_df = pd.DataFrame(price_segs)

    return {
        "category_stats": cat_stats,
        "monthly_summary": monthly,
        "order_status": status,
        "top_states": top_states,
        "b2b_b2c": b2b_b2c,
        "summary": summary,
        "heatmap_data": heatmap_df,
        "mom_growth": mom_growth,
        "price_segments": price_seg_df,
    }

@st.cache_data(ttl=30)
def load_all_data():
    if DATA_DIR.exists():
        # Bug fix 1: load semua key termasuk summary sekaligus, agar pengecekan None konsisten
        data = {
            "category_stats":  load_json("category_stats.json"),
            "monthly_summary": load_json("monthly_summary.json"),
            "order_status":    load_json("order_status.json"),
            "top_states":      load_json("top_states.json"),
            "b2b_b2c":         load_json("b2b_b2c.json"),
            "heatmap_data":    load_json("heatmap_data.json"),
            "mom_growth":      load_json("mom_growth.json"),
            "price_segments":  load_json("price_segments.json"),
        }
        # Bug fix 2: summary.json berformat dict biasa (bukan list), load terpisah
        summary_path = DATA_DIR / "summary.json"
        if summary_path.exists():
            with open(summary_path, encoding="utf-8") as f:
                data["summary"] = json.load(f)
        else:
            data["summary"] = None  # eksplisit None agar pengecekan di bawah akurat

        # Bug fix 3: cek SEMUA key tidak None sebelum return — termasuk summary
        if all(v is not None for v in data.values()):
            return data, False
        # Jika sebagian file ada tapi tidak lengkap → fallback ke dummy
        # (mencegah KeyError saat akses data["summary"] dll di bagian chart)

    return make_dummy_data(), True

# ═══════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown(f"""
    <div style='text-align:center; padding: 28px 0; background: linear-gradient(135deg, {COLORS["bg_accent"]}, {COLORS["bg_secondary"]}); border-radius: 18px; margin-bottom: 20px;'>
        <div style='font-family: "Lexend"; font-size: 26px; font-weight: 800; background: linear-gradient(90deg, {COLORS["amazon_orange"]} 0%, {COLORS["amazon_blue"]} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>🛒 AMAZON</div>
        <div style='font-family: "Sora"; font-size: 11px; color: {COLORS["text_light"]}; letter-spacing: 2px; margin-top: 6px; font-weight: 700;'>SALES PIPELINE</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    st.markdown(f"""
    <h4 style='color:{COLORS["amazon_blue"]}; font-family: "Sora"; font-size: 13px; font-weight: 700; letter-spacing: 1px;'>🔧 TEKNOLOGI STACK</h4>
    """, unsafe_allow_html=True)
    
    st.markdown(f"""
    <div style='font-size:13px; color:{COLORS["text_secondary"]}; line-height:2.3; background: {COLORS["bg_accent"]}; padding: 18px; border-radius: 14px; border: 1px solid {COLORS["border_light"]};'>
    <span style='font-size: 15px;'>🟠</span> <b style='color:{COLORS["amazon_orange"]}; font-weight: 700;'>PySpark</b> — Data Processing<br>
    <span style='font-size: 15px;'>🔵</span> <b style='color:{COLORS["amazon_blue"]}; font-weight: 700;'>MySQL</b> — Structured Storage<br>
    <span style='font-size: 15px;'>🟢</span> <b style='color:{COLORS["accent_emerald"]}; font-weight: 700;'>MongoDB</b> — Document Storage<br>
    <span style='font-size: 15px;'>🟣</span> <b style='color:{COLORS["accent_purple"]}; font-weight: 700;'>Streamlit</b> — Dashboard
    </div>
    """, unsafe_allow_html=True)
    
    st.divider()

    auto_refresh = st.toggle("⚡ Auto Refresh (30s)", value=False)
    if auto_refresh:
        st.markdown(f"""
        <div style='background: linear-gradient(135deg, {COLORS["accent_emerald"]}, {COLORS["white"]}); 
                    color: white; padding: 12px; border-radius: 10px; text-align: center; 
                    font-weight: 700; font-size: 12px; letter-spacing: 1px;'>
            ● LIVE MODE ENABLED
        </div>
        """, unsafe_allow_html=True)

    refresh_btn = st.button("🔄 Refresh Data", use_container_width=True)
    if refresh_btn:
        st.cache_data.clear()
        st.rerun()

    st.divider()
    st.markdown(f"<div style='font-size:13px; color:{COLORS["text_light"]}; font-weight: 500;'>⏰ Updated: {datetime.now().strftime('%H:%M:%S')}</div>", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:13px; color:{COLORS["text_light"]}; font-weight: 500;'>📅 {datetime.now().strftime('%d %B %Y')}</div>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# LOAD DATA
# ═══════════════════════════════════════════════════════════════════
data, is_demo = load_all_data()
summary      = data["summary"]
df_cat       = data["category_stats"]
df_monthly   = data["monthly_summary"]
df_status    = data["order_status"]
df_states    = data["top_states"]
df_b2b       = data["b2b_b2c"]
df_heatmap   = data["heatmap_data"]
df_mom       = data["mom_growth"]
df_price_seg = data["price_segments"]

for df, cols in [
    (df_cat,    ["total_revenue", "avg_price", "total_orders", "total_qty_sold"]),
    (df_monthly,["total_revenue", "total_orders", "total_qty"]),
    (df_states, ["total_revenue", "total_orders"]),
]:
    for col in cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

# ═══════════════════════════════════════════════════════════════════
# HEADER
# ═══════════════════════════════════════════════════════════════════
col_title, col_badge = st.columns([4, 1])

with col_title:
    st.markdown(f"""
    <div style='padding: 8px 0;'>
        <div style='font-family: "Lexend"; font-size: 48px; font-weight: 800; margin: 0; line-height: 1.1;'>
            <span style='background: linear-gradient(90deg, {COLORS["amazon_orange"]} 0%, {COLORS["amazon_blue"]} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;'>
                Amazon Sales Analytics
            </span>
        </div>
        <p style='color: {COLORS["text_secondary"]}; font-size: 15px; margin: 8px 0 0 0; font-weight: 500; letter-spacing: 0.3px;'>
            🚀 Big Data Pipeline — PySpark · MySQL · MongoDB
        </p>
    </div>
    """, unsafe_allow_html=True)

with col_badge:
    if is_demo:
        st.info("📦 Demo Data", icon="ℹ️")
    else:
        st.success("✅ Pipeline Data", icon="🔗")

st.divider()

# ═══════════════════════════════════════════════════════════════════
# KPI CARDS
# ═══════════════════════════════════════════════════════════════════
st.markdown("<div class='section-header'>📊 Key Performance Indicators</div>", unsafe_allow_html=True)

# Hitung revenue 
rev_cr = summary['total_revenue'] / 1e7

c1, c2, c3, c4, c5 = st.columns(5, gap="medium")

with c1:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Total Orders</div>
        <div class='kpi-value'>{int(summary['total_orders']):,}</div>
        <div class='kpi-sub'>Revenue ₹{rev_cr:.2f} Cr</div>
        <span class='kpi-badge badge-blue'>All Status</span>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Total Revenue</div>
        <div class='kpi-value'>₹{rev_cr:.2f} Cr</div>
        <div class='kpi-sub'>{summary['total_revenue']:,.0f} INR</div>
        <span class='kpi-badge badge-green'>All Orders</span>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Shipped Orders</div>
        <div class='kpi-value'>{int(summary['shipped_orders']):,}</div>
        <div class='kpi-sub'>Success Rate</div>
        <span class='kpi-badge badge-green'>{summary['shipped_rate']:.1f}% ✓</span>
    </div>
    """, unsafe_allow_html=True)

with c4:
    avg_rev = summary['total_revenue'] / max(summary['total_orders'], 1)
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Avg Order Value</div>
        <div class='kpi-value'>₹{avg_rev:,.0f}</div>
        <div class='kpi-sub'>per transaction</div>
        <span class='kpi-badge badge-orange'>INR</span>
    </div>
    """, unsafe_allow_html=True)

with c5:
    st.markdown(f"""
    <div class='kpi-card'>
        <div class='kpi-label'>Top Category</div>
        <div class='kpi-value' style='font-size:36px;'>{summary['top_category']}</div>
        <div class='kpi-sub'>Highest Revenue</div>
        <span class='kpi-badge badge-purple'>#1</span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ═══════════════════════════════════════════════════════════════════
# TABS
# ═══════════════════════════════════════════════════════════════════
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📈 Tren Penjualan",
    "📦 Kategori",
    "🗺️ Geografis",
    "🔍 Segmentasi",
    "📊 Pipeline Stats",
])

# ══════════════════════════════════════════════════════════════════
# TAB 1: TREN PENJUALAN
# ══════════════════════════════════════════════════════════════════
with tab1:
    st.markdown("<div class='section-header'>📈 Tren Penjualan Bulanan</div>", unsafe_allow_html=True)

    col_f1, col_f2 = st.columns([2, 1])
    with col_f1:
        # Filter tahun dihilangkan — dataset hanya berisi tahun 2022
        df_monthly_f = df_monthly.copy() if hasattr(df_monthly, 'copy') else df_monthly
        st.markdown(f"""
        <div style='background: rgba(20,110,180,0.10); border: 1px solid rgba(20,110,180,0.35);
                    border-radius: 10px; padding: 12px 18px; margin-bottom: 4px;
                    color: {COLORS["amazon_blue"]}; font-weight: 600; font-size: 14px;'>
            📅 Dataset Amazon Sale Report hanya mencakup tahun <b>2022</b>
        </div>
        """, unsafe_allow_html=True)
    with col_f2:
        metric_choice = st.selectbox("Metrik", ["Revenue (INR)", "Jumlah Order", "Qty Terjual"])

    df_monthly_f = df_monthly_f.sort_values(["year", "month"] if "month" in df_monthly_f.columns else ["month"])
    if "month_name" in df_monthly_f.columns and "year" in df_monthly_f.columns:
        df_monthly_f["period"] = df_monthly_f["month_name"].astype(str) + " " + df_monthly_f["year"].astype(str)
    elif "month_name" in df_monthly_f.columns:
        df_monthly_f["period"] = df_monthly_f["month_name"]

    metric_map = {
        "Revenue (INR)":  ("total_revenue", "Revenue (INR)"),
        "Jumlah Order":   ("total_orders",  "Total Orders"),
        "Qty Terjual":    ("total_qty",      "Total Qty"),
    }
    y_col, y_label = metric_map[metric_choice]

    if y_col in df_monthly_f.columns and "period" in df_monthly_f.columns:
        fig_trend = go.Figure()
        fig_trend.add_trace(go.Scatter(
            x=df_monthly_f["period"],
            y=df_monthly_f[y_col],
            mode="lines+markers",
            name=y_label,
            line=dict(color=COLORS['amazon_blue'], width=3.5),
            marker=dict(size=11, color=COLORS['amazon_blue'], line=dict(width=2.5, color="white")),
            fill="tozeroy",
            fillcolor=f"rgba(20, 110, 180, 0.1)",
            hovertemplate=f"<b>%{{x}}</b><br>{y_label}: %{{y:,.0f}}<extra></extra>",
        ))
        apply_theme(fig_trend, f"📈 {y_label} per Bulan", title_size=18)
        fig_trend.update_xaxes(tickangle=-30)
        st.plotly_chart(fig_trend, use_container_width=True, height=500)

    st.markdown("<div class='section-header'>📊 Month-over-Month Growth</div>", unsafe_allow_html=True)
    if "mom_growth_pct" in df_mom.columns and "period" not in df_mom.columns:
        df_mom["period"] = df_mom["month_name"].astype(str) + " " + df_mom["year"].astype(str)

    # Pastikan kolom numerik — JSON dengan None bisa menghasilkan dtype object
    df_mom["mom_growth_pct"] = pd.to_numeric(df_mom["mom_growth_pct"], errors="coerce")

    df_mom_clean = df_mom.dropna(subset=["mom_growth_pct"])
    if len(df_mom_clean) > 0:
        df_mom_clean = df_mom_clean.copy().reset_index(drop=True)

        x_col    = "period" if "period" in df_mom_clean.columns else "month_name"
        vals_raw = df_mom_clean["mom_growth_pct"].tolist()
        x_vals   = df_mom_clean[x_col].tolist()

        # ── Hitung CLIP CEILING ────────────────────────────────────────────
        # Semua bar tetap ditampilkan (tidak ada yang dihapus).
        # Bar yang nilainya sangat besar akan "dipotong" secara visual di batas atas
        # axis, sehingga bar negatif kecil tetap terlihat.
        # Nilai asli selalu muncul di label teks (▲) dan tooltip hover.
        pos_vals  = [v for v in vals_raw if v > 0]
        neg_vals  = [v for v in vals_raw if v < 0]

        # ── Tentukan CLIP CEILING ──────────────────────────────────────────
        # Logika: jika nilai positif terbesar jauh melebihi nilai negatif terbesar
        # (rasio > 10×), maka bar positif di-clip agar bar negatif tetap terlihat.
        # Nilai asli tetap muncul di label (▲) dan tooltip hover.
        max_neg_abs = max(abs(v) for v in neg_vals) if neg_vals else 1
        DOMINANT_RATIO = 10   # jika positif > 10× negatif → anggap outlier

        if pos_vals and neg_vals:
            max_pos = max(pos_vals)
            if max_pos > max_neg_abs * DOMINANT_RATIO:
                # Ada bar positif yang sangat dominan → clip
                if len(pos_vals) >= 2:
                    # Gunakan 2.5× nilai positif terbesar ke-2
                    clip_ceil = sorted(pos_vals)[-2] * 2.5
                else:
                    # Hanya 1 positif → set ceiling = DOMINANT_RATIO × max_neg_abs
                    clip_ceil = max_neg_abs * DOMINANT_RATIO
            else:
                clip_ceil = max_pos       # semua proporsional, tampilkan penuh
        elif pos_vals:
            clip_ceil = max(pos_vals)     # tidak ada negatif, tampilkan penuh
        else:
            clip_ceil = 20                # tidak ada positif sama sekali

        y_neg_floor = min(neg_vals) if neg_vals else 0

        span    = max(clip_ceil - y_neg_floor, 1)
        pad_top = span * 0.30
        pad_bot = abs(y_neg_floor) * 0.35 if y_neg_floor < 0 else clip_ceil * 0.08

        y_range_min = y_neg_floor - pad_bot
        y_range_max = clip_ceil   + pad_top

        # ── Nilai visual (terpotong) dan label ────────────────────────────
        clip_limit   = clip_ceil * 0.94
        display_vals = [min(v, clip_limit) if v > 0 else v for v in vals_raw]
        is_clipped   = [raw_v > clip_limit for raw_v in vals_raw]

        labels_text = [
            f"▲ {v:+,.1f}%" if clipped else f"{v:+.1f}%"
            for v, clipped in zip(vals_raw, is_clipped)
        ]
        colors = [
            COLORS["accent_emerald"] if v >= 0 else COLORS["accent_rose"]
            for v in vals_raw
        ]
        bar_line_colors = [
            COLORS["amazon_dark"] if c else "rgba(0,0,0,0.15)" for c in is_clipped
        ]
        bar_line_widths = [3 if c else 1 for c in is_clipped]

        fig_mom = go.Figure(go.Bar(
            x=x_vals,
            y=display_vals,          # visual: terpotong di clip_limit
            customdata=vals_raw,     # nilai asli untuk hover
            marker=dict(
                color=colors,
                line=dict(color=bar_line_colors, width=bar_line_widths),
            ),
            text=labels_text,
            textposition="outside",  # label di luar bar
            cliponaxis=False,        # label tidak dipotong oleh batas axis
            textfont=dict(size=12, family="Sora, sans-serif"),
            width=0.55,
            hovertemplate=(
                "<b>%{x}</b><br>"
                "MoM Growth: <b>%{customdata:+.1f}%</b>"
                "<extra></extra>"
            ),
        ))

        apply_theme(fig_mom, "📊 Month-over-Month Revenue Growth (%)", title_size=18)
        fig_mom.update_layout(
            showlegend=False,
            hovermode="x unified",
            margin=dict(l=20, r=20, t=80, b=60),
        )
        fig_mom.update_yaxes(
            zeroline=True,
            zerolinecolor=COLORS["amazon_dark"],
            zerolinewidth=2,
            ticksuffix="%",
            range=[y_range_min, y_range_max],
            autorange=False,
        )
        fig_mom.add_hline(
            y=0, line_dash="dash",
            line_color=COLORS["amazon_dark"],
            line_width=1.5, opacity=0.45,
        )

        # Info kecil jika ada bar yang di-clip
        if any(is_clipped):
            clipped_months = ", ".join(x for x, c in zip(x_vals, is_clipped) if c)
            st.markdown(f"""
            <div style='background:rgba(5,150,105,0.08); border:1px solid rgba(5,150,105,0.30);
                        border-radius:10px; padding:9px 16px; margin-bottom:6px;
                        color:{COLORS["accent_emerald"]}; font-size:13px; font-weight:600;'>
                ℹ️ Bar <b>{clipped_months}</b> dipotong secara visual agar skala axis tidak mendominasi.
                Nilai asli tetap tampil di label (▲) dan tooltip hover.
            </div>
            """, unsafe_allow_html=True)

        fig_mom.add_annotation(
            x=0.5, y=-0.18, xref="paper", yref="paper",
            text=(f"<span style='color:{COLORS['accent_emerald']}'>■ Positif (naik)</span>"
                  f"&nbsp;&nbsp;&nbsp;"
                  f"<span style='color:{COLORS['accent_rose']}'>■ Negatif (turun)</span>"),
            showarrow=False,
            font=dict(size=13, family="Sora"),
            align="center",
        )
        st.plotly_chart(fig_mom, use_container_width=True, height=460)

# ══════════════════════════════════════════════════════════════════
# TAB 2: KATEGORI
# ══════════════════════════════════════════════════════════════════
with tab2:
    st.markdown("<div class='section-header'>📊 Analisis Kategori Produk</div>", unsafe_allow_html=True)

    col_left, col_right = st.columns(2, gap="large")

    with col_left:
        df_cat_sorted = df_cat.sort_values("total_revenue", ascending=True)
        fig_rev_cat = go.Figure(go.Bar(
            x=df_cat_sorted["total_revenue"],
            y=df_cat_sorted["category"],
            orientation="h",
            marker=dict(
                color=df_cat_sorted["total_revenue"],
                colorscale=[[0, COLORS['bg_accent']], [0.5, COLORS['accent_cyan']], [1, COLORS['amazon_blue']]],
                showscale=False,
            ),
            text=df_cat_sorted["total_revenue"].apply(lambda x: f"₹{x/1e6:.1f}M"),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
        ))
        apply_theme(fig_rev_cat, "💰 Revenue per Kategori", title_size=16)
        st.plotly_chart(fig_rev_cat, use_container_width=True, height=480)

    with col_right:
        fig_pie = go.Figure(go.Pie(
            labels=df_cat["category"],
            values=df_cat["total_orders"],
            hole=0.45,
            textinfo="percent",
            textposition="inside",
            insidetextorientation="radial",
            marker=dict(
                colors=[COLORS['amazon_blue'], COLORS['amazon_orange'], COLORS['accent_emerald'],
                        COLORS['accent_purple'], COLORS['accent_amber'], COLORS['accent_cyan'],
                        COLORS['accent_rose'], COLORS['accent_teal']],
                line=dict(color="white", width=3)
            ),
            hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>",
        ))
        fig_pie.update_traces(
            textfont=dict(size=12, color="white"),
            # automargin: label slice kecil otomatis dipindahkan agar tidak terpotong
            automargin=True,
        )
        apply_theme(fig_pie, "🍩 Distribusi Order per Kategori", title_size=16)
        fig_pie.update_layout(
            # Sembunyikan label yang terlalu kecil daripada membiarkannya overflow
            uniformtext=dict(minsize=10, mode="hide"),
            legend=dict(
                orientation="v",
                yanchor="middle",
                y=0.5,
                xanchor="left",
                x=1.05,
                font=dict(size=13, color=COLORS["text_primary"]),
                bgcolor="rgba(255,255,255,0.85)",
                borderwidth=0,
            ),
            margin=dict(l=20, r=140, t=60, b=20),
        )
        st.plotly_chart(fig_pie, use_container_width=True, height=480)

    st.markdown("<div class='section-header'>🔥 Heatmap Revenue — Kategori × Bulan</div>", unsafe_allow_html=True)
    if "category" in df_heatmap.columns and "month_name" in df_heatmap.columns:
        month_order = ["January","February","March","April","May","June",
                       "July","August","September","October","November","December"]
        pivot = df_heatmap.pivot_table(
            index="category", columns="month_name",
            values="total_revenue", aggfunc="sum", fill_value=0
        )
        cols_present = [m for m in month_order if m in pivot.columns]
        pivot = pivot[cols_present]

        fig_heat = go.Figure(go.Heatmap(
            z=pivot.values / 1e6,
            x=pivot.columns.tolist(),
            y=pivot.index.tolist(),
            colorscale=[[0, COLORS['bg_accent']], [0.3, COLORS['accent_cyan']], 
                        [0.6, COLORS['amazon_blue']], [1, COLORS['accent_purple']]],
            text=[[f"₹{v:.1f}M" for v in row] for row in (pivot.values / 1e6)],
            texttemplate="%{text}",
            textfont=dict(size=12, color=COLORS['text_primary']),
            hovertemplate="<b>%{y}</b> | %{x}<br>Revenue: ₹%{z:.2f}M<extra></extra>",
            colorbar=dict(
                title="Revenue<br>(M INR)",
                tickfont=dict(color=COLORS['text_secondary']),
                titlefont=dict(color=COLORS['text_secondary']),
            ),
        ))
        apply_theme(fig_heat, "🔥 Revenue Heatmap (Juta INR)", title_size=16)
        fig_heat.update_layout(height=420)
        st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown("<div class='section-header'>📋 Detail Statistik Kategori</div>", unsafe_allow_html=True)
    df_display = df_cat.copy()
    df_display["total_revenue"] = df_display["total_revenue"].apply(lambda x: f"₹{x:,.0f}")
    df_display["avg_price"] = df_display["avg_price"].apply(lambda x: f"₹{x:,.0f}")
    df_display.columns = [c.replace("_", " ").title() for c in df_display.columns]
    st.dataframe(df_display, use_container_width=True, height=320)

# ══════════════════════════════════════════════════════════════════
# TAB 3: GEOGRAFIS
# ══════════════════════════════════════════════════════════════════
with tab3:
    st.markdown("<div class='section-header'>🗺️ Distribusi Geografis (INDIA)</div>", unsafe_allow_html=True)

    col_g1, col_g2 = st.columns(2, gap="large")

    with col_g1:
        df_states_sorted = df_states.sort_values("total_orders", ascending=True)
        fig_state_orders = go.Figure(go.Bar(
            x=df_states_sorted["total_orders"],
            y=df_states_sorted["ship_state"],
            orientation="h",
            marker=dict(
                color=df_states_sorted["total_orders"],
                colorscale=[[0, COLORS['bg_accent']], [1, COLORS['amazon_orange']]],
                showscale=False,
            ),
            text=df_states_sorted["total_orders"].apply(lambda x: f"{x:,}"),
            textposition="outside",
            cliponaxis=False,
            textfont=dict(size=11, color=COLORS['text_primary']),
            hovertemplate="<b>%{y}</b><br>Orders: %{x:,}<extra></extra>",
        ))
        apply_theme(fig_state_orders, "📦 Top State — Jumlah Order", title_size=16)
        fig_state_orders.update_layout(
            showlegend=False,
            margin=dict(l=10, r=80, t=60, b=20),
        )
        fig_state_orders.update_xaxes(showgrid=True, gridcolor="rgba(213,220,227,0.4)")
        st.plotly_chart(fig_state_orders, use_container_width=True, height=480)

    with col_g2:
        df_states_r = df_states.sort_values("total_revenue", ascending=True)
        fig_state_rev = go.Figure(go.Bar(
            x=df_states_r["total_revenue"],
            y=df_states_r["ship_state"],
            orientation="h",
            marker=dict(
                color=df_states_r["total_revenue"],
                colorscale=[[0, COLORS['bg_accent']], [1, COLORS['accent_emerald']]],
                showscale=False,
            ),
            text=df_states_r["total_revenue"].apply(lambda x: f"₹{x/1e6:.1f}M"),
            textposition="outside",
            cliponaxis=False,
            textfont=dict(size=11, color=COLORS['text_primary']),
            hovertemplate="<b>%{y}</b><br>Revenue: ₹%{x:,.0f}<extra></extra>",
        ))
        apply_theme(fig_state_rev, "💰 Top State — Revenue", title_size=16)
        fig_state_rev.update_layout(
            showlegend=False,
            margin=dict(l=10, r=80, t=60, b=20),
        )
        fig_state_rev.update_xaxes(showgrid=True, gridcolor="rgba(213,220,227,0.4)")
        st.plotly_chart(fig_state_rev, use_container_width=True, height=480)

    st.markdown("<div class='section-header'>🫧 Bubble Chart — Orders vs Revenue</div>", unsafe_allow_html=True)
    fig_bubble = px.scatter(
        df_states,
        x="total_orders", y="total_revenue",
        size="total_orders", color="total_revenue",
        text="ship_state",
        color_continuous_scale=[COLORS['bg_accent'], COLORS['accent_cyan'], COLORS['amazon_blue']],
        labels={"total_orders": "Total Orders", "total_revenue": "Total Revenue (INR)"},
    )
    fig_bubble.update_traces(
        textposition="top center",
        textfont=dict(
            color=COLORS['text_primary'],
            size=11,
            family="Sora, sans-serif",
        ),
        marker=dict(
            opacity=0.75,
            line=dict(color="white", width=1.5),
        ),
    )
    apply_theme(fig_bubble, "🫧 Orders vs Revenue per State", title_size=16)
    fig_bubble.update_layout(
        showlegend=False,
        coloraxis_showscale=False,
    )
    fig_bubble.update_xaxes(title_text="Total Orders", title_font=dict(size=12, color=COLORS['text_secondary']))
    fig_bubble.update_yaxes(title_text="Total Revenue (INR)", title_font=dict(size=12, color=COLORS['text_secondary']))
    st.plotly_chart(fig_bubble, use_container_width=True, height=480)

# ══════════════════════════════════════════════════════════════════
# TAB 4: SEGMENTASI
# ══════════════════════════════════════════════════════════════════
with tab4:
    st.markdown("<div class='section-header'>🎯 Segmentasi Order</div>", unsafe_allow_html=True)

    col_s1, col_s2 = st.columns(2, gap="large")

    with col_s1:
        if "status_group" in df_status.columns:
            colors_status = {"Shipped": COLORS['accent_emerald'], "Cancelled": COLORS['accent_rose'],
                             "Pending": COLORS['amazon_orange'], "Other": COLORS['text_light']}
            fig_status = go.Figure(go.Pie(
                labels=df_status["status_group"],
                values=df_status["total_orders"],
                hole=0.5,
                textinfo="label+percent",
                textposition="outside",
                marker=dict(
                    colors=[colors_status.get(s, COLORS['amazon_blue']) for s in df_status["status_group"]],
                    line=dict(color="white", width=3)
                ),
                hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>",
            ))
            fig_status.update_traces(
                textfont=dict(size=12, color=COLORS['text_primary']),
                automargin=True,
            )
            apply_theme(fig_status, "🎯 Distribusi Status Order", title_size=16)
            fig_status.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.20,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12, color=COLORS['text_primary']),
                    bgcolor="rgba(255,255,255,0.85)",
                    borderwidth=0,
                ),
                margin=dict(l=20, r=20, t=60, b=60),
            )
            st.plotly_chart(fig_status, use_container_width=True, height=500)

    with col_s2:
        if "customer_type" in df_b2b.columns:
            fig_b2b = go.Figure(go.Pie(
                labels=df_b2b["customer_type"],
                values=df_b2b["total_orders"],
                hole=0.5,
                textinfo="label+percent",
                textposition="outside",
                marker=dict(
                    colors=[COLORS['amazon_blue'], COLORS['accent_purple']],
                    line=dict(color="white", width=3)
                ),
                hovertemplate="<b>%{label}</b><br>Orders: %{value:,}<br>Share: %{percent}<extra></extra>",
            ))
            fig_b2b.update_traces(
                textfont=dict(size=13, color=COLORS['text_primary']),
                automargin=True,
            )
            apply_theme(fig_b2b, "🏢 B2B vs B2C", title_size=16)
            fig_b2b.update_layout(
                showlegend=True,
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.20,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=13, color=COLORS['text_primary']),
                    bgcolor="rgba(255,255,255,0.85)",
                    borderwidth=0,
                ),
                margin=dict(l=20, r=20, t=60, b=60),
            )
            st.plotly_chart(fig_b2b, use_container_width=True, height=500)

    st.markdown("<div class='section-header'>💰 Segmentasi Harga per Kategori</div>", unsafe_allow_html=True)

    if "category" in df_price_seg.columns and "price_segment" in df_price_seg.columns:
        seg_filter = st.multiselect(
            "Filter Kategori",
            options=df_price_seg["category"].unique().tolist(),
            default=df_price_seg["category"].unique().tolist()[:5]
        )
        df_ps_f = df_price_seg[df_price_seg["category"].isin(seg_filter)]

        col_ps1, col_ps2 = st.columns(2, gap="large")
        with col_ps1:
            fig_seg_orders = px.bar(
                df_ps_f, x="category", y="total_orders",
                color="price_segment",
                color_discrete_map={
                    "Budget (<300 INR)":        COLORS['accent_emerald'],
                    "Mid-Range (300-700 INR)":  COLORS['amazon_blue'],
                    "Premium (>700 INR)":       COLORS['accent_purple'],
                },
                barmode="group",
                labels={"total_orders": "Total Orders", "category": "Kategori"},
            )
            apply_theme(fig_seg_orders, "📦 Orders per Segmen Harga", title_size=16)
            fig_seg_orders.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.32,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12, color=COLORS['text_primary']),
                    bgcolor="rgba(255,255,255,0.85)",
                    bordercolor=COLORS['border_light'],
                    borderwidth=1,
                ),
                margin=dict(l=20, r=20, t=60, b=90),
            )
            fig_seg_orders.update_traces(textfont=dict(size=11, color=COLORS['text_primary']))
            st.plotly_chart(fig_seg_orders, use_container_width=True, height=480)

        with col_ps2:
            fig_seg_rev = px.bar(
                df_ps_f, x="category", y="total_revenue",
                color="price_segment",
                color_discrete_map={
                    "Budget (<300 INR)":        COLORS['accent_emerald'],
                    "Mid-Range (300-700 INR)":  COLORS['amazon_blue'],
                    "Premium (>700 INR)":       COLORS['accent_purple'],
                },
                barmode="stack",
                labels={"total_revenue": "Total Revenue", "category": "Kategori"},
            )
            apply_theme(fig_seg_rev, "💰 Revenue per Segmen (Stacked)", title_size=16)
            fig_seg_rev.update_layout(
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=-0.32,
                    xanchor="center",
                    x=0.5,
                    font=dict(size=12, color=COLORS['text_primary']),
                    bgcolor="rgba(255,255,255,0.85)",
                    bordercolor=COLORS['border_light'],
                    borderwidth=1,
                ),
                margin=dict(l=20, r=20, t=60, b=90),
            )
            st.plotly_chart(fig_seg_rev, use_container_width=True, height=480)

        df_avg = df_ps_f.groupby("price_segment")["avg_price"].mean().reset_index()
        fig_avg = px.bar(
            df_avg, x="price_segment", y="avg_price",
            color="price_segment",
            color_discrete_map={
                "Budget (<300 INR)": COLORS['accent_emerald'],
                "Mid-Range (300-700 INR)": COLORS['amazon_blue'],
                "Premium (>700 INR)": COLORS['accent_purple'],
            },
            text=df_avg["avg_price"].apply(lambda x: f"₹{x:,.0f}"),
        )
        fig_avg.update_traces(textposition="outside", textfont=dict(size=12))
        apply_theme(fig_avg, "📊 Rata-Rata Harga per Segmen", title_size=16)
        fig_avg.update_layout(showlegend=False)
        st.plotly_chart(fig_avg, use_container_width=True, height=450)

# ══════════════════════════════════════════════════════════════════
# TAB 5: PIPELINE STATS
# ══════════════════════════════════════════════════════════════════
with tab5:
    st.markdown("<div class='section-header'>🏗️ Arsitektur Pipeline</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div style='background:{COLORS["bg_secondary"]}; border:1px solid {COLORS["border_light"]}; border-radius:18px; padding:32px; font-family: "Sora"; font-size:13px; color:{COLORS["text_secondary"]}; line-height:2.4;'>

    <span style='color:{COLORS["amazon_orange"]}; font-weight:700; font-size: 14px;'>PIPELINE FLOW:</span><br><br>

    <span style='color:{COLORS["amazon_orange"]}; font-weight: 700;'>📄 CSV</span>
    <span style='color:{COLORS["border_default"]};'> ──────── </span>
    <span style='color:{COLORS["amazon_blue"]}; font-weight: 700;'>🔥 PySpark</span>
    <span style='color:{COLORS["border_default"]};'> ─── Ingest + Schema ──→ </span>
    <span style='color:{COLORS["accent_cyan"]}; font-weight: 700;'>🧹 Cleaning</span>
    <span style='color:{COLORS["border_default"]};'> ─── 10 Steps ──→ </span>
    <span style='color:{COLORS["accent_emerald"]}; font-weight: 700;'>df_clean</span><br><br>

    <span style='color:{COLORS["accent_emerald"]}; font-weight: 700;'>df_clean</span>
    <span style='color:{COLORS["border_default"]};'> ─── Aggregation ──→ </span>
    <span style='color:{COLORS["accent_purple"]}; font-weight: 700;'>df_by_category</span>
    <span style='color:{COLORS["border_default"]};'> | </span>
    <span style='color:{COLORS["accent_purple"]}; font-weight: 700;'>df_monthly</span>
    <span style='color:{COLORS["border_default"]};'> | </span>
    <span style='color:{COLORS["accent_purple"]}; font-weight: 700;'>df_status</span><br><br>

    <span style='color:{COLORS["accent_emerald"]}; font-weight: 700;'>df_clean</span>
    <span style='color:{COLORS["border_default"]};'> ─── Spark SQL (9 Queries) ──→ </span>
    <span style='color:{COLORS["accent_rose"]}; font-weight: 700;'>Analytics Results</span><br><br>

    <span style='color:{COLORS["accent_emerald"]}; font-weight: 700;'>df_clean</span>
    <span style='color:{COLORS["border_default"]};'> ──→ </span>
    <span style='color:{COLORS["amazon_blue"]}; font-weight: 700;'>MySQL</span>
    <span style='color:{COLORS["border_default"]};'> (orders + monthly_summary + category_stats)</span><br>

    <span style='color:{COLORS["accent_emerald"]}; font-weight: 700;'>df_clean</span>
    <span style='color:{COLORS["border_default"]};'> ──→ </span>
    <span style='color:{COLORS["accent_emerald"]}; font-weight: 700;'>MongoDB</span>
    <span style='color:{COLORS["border_default"]};'> (orders_detail + category_insights)</span>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown("<div class='section-header'>💾 Database Schema Overview</div>", unsafe_allow_html=True)

    col_db1, col_db2 = st.columns(2, gap="large")

    with col_db1:
        st.markdown(f"**🔵 MySQL — amazon_sales_db**")
        tables = {
            "orders (26 cols)": [
                "order_id UNIQUE", "date, year, month, month_name",
                "status, status_group", "fulfilment, sales_channel",
                "category, size, sku, asin", "qty, amount, revenue, currency",
                "ship_city, ship_state, ship_postal_code", "ship_country",
                "b2b, has_promotion", "courier_status, fulfilled_by"
            ],
            "monthly_summary (8 cols)": [
                "year, month, month_name", "total_orders, total_revenue",
                "total_qty, unique_categories"
            ],
            "category_stats (8 cols)": [
                "category UNIQUE", "total_orders, total_qty_sold",
                "total_revenue, avg_price", "max_price, min_price"
            ],
        }
        for tbl, cols in tables.items():
            with st.expander(f"📋 {tbl}"):
                for c in cols:
                    st.markdown(f"<span style='color:{COLORS["text_secondary"]}; font-family:Sora; font-size:13px;'>• {c}</span>", unsafe_allow_html=True)

    with col_db2:
        st.markdown(f"**🟢 MongoDB — amazon_sales**")
        collections = {
            "orders_detail": [
                "order_id, date (string)", "status, status_group",
                "category, size, sku, asin", "qty, amount, revenue",
                "ship_city, ship_state, ship_country", "b2b, has_promotion",
                "promotion_ids: [ARRAY]  ← berbeda dari MySQL",
                "_source: 'amazon_sale_report'"
            ],
            "category_insights": [
                "category", "total_orders, total_qty_sold",
                "total_revenue, avg_price",
                "price_range: {min, max}  ← nested object",
                "sizes_breakdown: [{size, count}]  ← array of objects"
            ],
        }
        for col_name, fields in collections.items():
            with st.expander(f"📄 {col_name}"):
                for f in fields:
                    color = COLORS['accent_rose'] if "←" in f else COLORS['text_secondary']
                    st.markdown(f"<span style='color:{color}; font-family:Sora; font-size:13px;'>• {f}</span>", unsafe_allow_html=True)
    
    # SQL QUERIES SUMMARY
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<div class='section-header'>9 SPARK SQL QUERIES PIPELINE</div>", unsafe_allow_html=True)
    
    queries = [
        ("Q1", "Top Kombinasi Kategori & Ukuran", "GROUP BY category, size | ORDER BY revenue DESC"),
        ("Q2", "Funnel Konversi Order per Status", "COUNT, SUM, AVG, WINDOW OVER() | pct_orders"),
        ("Q3", "Top 10 Hari Revenue Tertinggi", "GROUP BY date | ORDER BY daily_revenue DESC"),
        ("Q4", "Dampak Promosi terhadap Penjualan", "CASE WHEN has_promotion | AVG qty & revenue"),
        ("Q5", "Performa Sales Channel & Fulfillment", "GROUP BY sales_channel, fulfilment | pct_of_total"),
        ("Q6", "Month-over-Month Revenue Growth", "WITH CTE | LAG() WINDOW FUNCTION | mom_growth_pct"),
        ("Q7", "State Performance — Revenue Share", "RANK() OVER | pct_orders, pct_revenue"),
        ("Q8", "Segmentasi Harga Budget/Mid/Premium", "CASE WHEN amount < 300/700 | GROUP BY segment"),
        ("Q9", "Courier Status Impact Analysis", "GROUP BY courier_status, status_group | states_covered"),
    ]
    
    # Warna premium sesuai dengan palette dashboard
    bg_card = COLORS['bg_secondary']
    border_card = COLORS['border_light']
    text_title = COLORS['text_primary']
    text_desc = COLORS['text_secondary']
    badge_bg = COLORS['bg_accent']
    badge_text = COLORS['amazon_blue']
    
    for q_id, q_title, q_desc in queries:
        st.markdown(f"""
        <div style='background:{bg_card}; border:1px solid {border_card}; border-radius:12px;
                    padding:14px 18px; margin:8px 0; display:flex; align-items:center; gap:14px;
                    box-shadow: 0 1px 3px rgba(0,0,0,0.05); transition: all 0.2s ease;'>
            <span style='font-family:"Sora", monospace; font-size:12px; font-weight:700;
                         color:{badge_text}; background:{badge_bg}; padding:4px 10px; border-radius:6px;
                         border:1px solid rgba(20,110,180,0.2); letter-spacing:0.5px;'>{q_id}</span>
            <div>
                <div style='color:{text_title}; font-size:14px; font-weight:700; font-family:"Plus Jakarta Sans", sans-serif;'>{q_title}</div>
                <div style='color:{text_desc}; font-size:12px; font-family:"Plus Jakarta Sans", monospace; margin-top:4px;'>{q_desc}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
 
# ═══════════════════════════════════════════════════════════════════
# FOOTER
# ═══════════════════════════════════════════════════════════════════
st.divider()
st.markdown(f"""
<div style='text-align:center; color:{COLORS["text_light"]}; font-size:13px; padding:14px 0; font-weight: 500;'>
    <span style='font-family: "Sora";'>
        🚀 Amazon Sales Big Data Pipeline &nbsp;|&nbsp;
        <span style='color:{COLORS["amazon_orange"]};'>PySpark</span> · 
        <span style='color:{COLORS["amazon_blue"]};'>MySQL</span> · 
        <span style='color:{COLORS["accent_emerald"]};'>MongoDB</span> · 
        <span style='color:{COLORS["accent_purple"]};'>Streamlit</span> &nbsp;|&nbsp;
        Dataset: ~128K rows
    </span>
</div>
""", unsafe_allow_html=True)

if auto_refresh:
    time.sleep(30)
    st.cache_data.clear()
    st.rerun()