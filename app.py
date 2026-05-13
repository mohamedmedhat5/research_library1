import re
from urllib.parse import unquote

from fastapi import background
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="Saudi Research Library",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------- HELPERS ----------------
def clean_title(title):
    if pd.isna(title):
        return "Untitled"

    title = unquote(str(title))
    title = re.sub(r"\.(pdf|xlsx|xls|csv)$", "", title, flags=re.I)
    title = re.sub(r"%\d+", "", title)
    title = title.replace("+", " ")
    title = re.sub(r"\(\d+\)", "", title)
    title = re.sub(r"_", " ", title)
    title = re.sub(r"\s+", " ", title).strip()

    return title


@st.cache_data
def load_data():
    df = pd.read_csv("documents.csv")

    df["title"] = df["title"].apply(clean_title)
    df["source"] = df["source"].fillna("Unknown")
    df["type"] = df["type"].fillna("Unknown")
    df["year"] = df["year"].fillna("Unknown").astype(str)

    return df


df = load_data()

# ---------------- SESSION ----------------
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = False

if "page" not in st.session_state:
    st.session_state.page = 1

# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    st.session_state.dark_mode = st.toggle("🌙 Dark Mode")

dark_mode = st.session_state.dark_mode

# ---------------- COLORS ----------------
if dark_mode:
    BG = "#0f172a"
    CARD = "#1e293b"
    SIDEBAR = "#111827"
    TEXT = "#f8fafc"
    MUTED = "#94a3b8"
    BORDER = "#334155"
    BTN = "#2563eb"
    BTN_HOVER = "#1d4ed8"
else:
    BG = "#f8fafc"
    CARD = "#ffffff"
    SIDEBAR = "#f1f5f9"
    TEXT = "#0f172a"
    MUTED = "#64748b"
    BORDER = "#e2e8f0"
    BTN = "#0f172a"
    BTN_HOVER = "#1e293b"

# ---------------- CSS ----------------
st.markdown(f"""
<style>

/* APP */
.stApp {{
    background-color: {BG};
    color: {TEXT};
}}

.block-container {{
    padding-top: 2rem;
    max-width: 1400px;
}}

/* SIDEBAR */
section[data-testid="stSidebar"] {{
    background: {SIDEBAR} !important;
    border-right: 1px solid {BORDER};
}}

section[data-testid="stSidebar"] * {{
    color: {TEXT} !important;
}}

/* INPUTS */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] > div {{
    background: {CARD} !important;
    color: {TEXT} !important;
    border: 1px solid {BORDER} !important;
    border-radius: 12px !important;
}}

/* HERO */
.hero {{
    background: {CARD};
    border: 1px solid {BORDER};
    padding: 30px;
    border-radius: 24px;
    margin-bottom: 28px;
    box-shadow: 0 4px 18px rgba(0,0,0,0.05);
}}

.hero h1 {{
    margin: 0;
    color: {TEXT};
    font-size: 46px;
}}

.hero p {{
    color: {MUTED};
    margin-top: 8px;
}}

/* METRICS */
.metric-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 20px;
    padding: 28px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
}}

.metric-value {{
    font-size: 42px;
    font-weight: 700;
    color: {TEXT};
}}

.metric-label {{
    color: {MUTED};
    font-size: 15px;
    margin-top: 8px;
}}

/* DOCUMENT CARD */
.doc-card {{
    background: {CARD};
    border: 1px solid {BORDER};
    border-radius: 22px;
    padding: 24px;
    margin-bottom: 18px;
    box-shadow: 0 4px 14px rgba(0,0,0,0.04);
}}

.doc-title {{
    font-size: 20px;
    font-weight: 700;
    color: {TEXT};
    margin-bottom: 10px;
}}

.doc-meta {{
    color: {MUTED};
    font-size: 14px;
    margin-bottom: 18px;
}}

/* BADGES */
.badge {{
    padding: 10px 18px;
    border-radius: 999px;
    font-weight: 600;
    display: inline-block;
    text-align: center;
    min-width: 120px;
}}

.pdf {{
    background: #FEE2E2;
    color: #B91C1C;
}}

.excel {{
    background: #DCFCE7;
    color: #166534;
}}

.year {{
    background: #DBEAFE;
    color: #1D4ED8;
}}

/* BUTTON FIX */
a[data-testid="stLinkButton"] {{
    background: {BTN} !important;
    color: white !important;
    border-radius: 14px !important;
    padding: 12px 22px !important;
    font-weight: 600 !important;
    border: none !important;
    text-decoration: none !important;
}}

a[data-testid="stLinkButton"]:hover {{
    background: {BTN_HOVER} !important;
    color: white !important;
}}

a[data-testid="stLinkButton"] * {{
    color: white !important;
}}

/* REMOVE STREAMLIT WEIRD STYLES */
[data-testid="stMetricValue"] {{
    color: {TEXT} !important;
}}

[data-testid="stMetricLabel"] {{
    color: {MUTED} !important;
}}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("""
<div class="navbar">
    <h1>📚 Saudi Research Library</h1>
    <p>Internal Research Document Portal</p>
</div>
""", unsafe_allow_html=True)

# ---------------- FILTERS ----------------
with st.sidebar:
    st.markdown("## 🔎 Search & Filters")

    search = st.text_input("Search by title")

    sources = ["All"] + sorted(df["source"].unique().tolist())
    selected_source = st.selectbox("Source", sources)

    years = ["All"] + sorted(df["year"].unique().tolist(), reverse=True)
    selected_year = st.selectbox("Year", years)

    types = ["All"] + sorted(df["type"].unique().tolist())
    selected_type = st.selectbox("File Type", types)

# ---------------- FILTERING ----------------
filtered = df.copy()

if search:
    filtered = filtered[
        filtered["title"].str.contains(search, case=False, na=False)
    ]

if selected_source != "All":
    filtered = filtered[filtered["source"] == selected_source]

if selected_year != "All":
    filtered = filtered[filtered["year"] == selected_year]

if selected_type != "All":
    filtered = filtered[filtered["type"] == selected_type]

# reset page
total_pages = max(1, (len(filtered) - 1) // 25 + 1)
if st.session_state.page > total_pages:
    st.session_state.page = 1

# ---------------- METRICS ----------------
pdf_count = len(filtered[filtered["type"] == "PDF"])
excel_count = len(filtered[filtered["type"] == "Excel"])

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f'<div class="metric"><h2>{len(filtered)}</h2><p>Total Files</p></div>',
        unsafe_allow_html=True
    )

with c2:
    st.markdown(
        f'<div class="metric"><h2>{filtered["source"].nunique()}</h2><p>Sources</p></div>',
        unsafe_allow_html=True
    )

with c3:
    st.markdown(
        f'<div class="metric"><h2>{pdf_count}</h2><p>PDF Files</p></div>',
        unsafe_allow_html=True
    )

with c4:
    st.markdown(
        f'<div class="metric"><h2>{excel_count}</h2><p>Excel Files</p></div>',
        unsafe_allow_html=True
    )

st.markdown("## Documents")

# ---------------- PAGINATION ----------------
per_page = 25
start = (st.session_state.page - 1) * per_page
end = start + per_page
page_df = filtered.iloc[start:end]

# ---------------- DOCUMENTS ----------------
if page_df.empty:
    st.warning("No matching documents found.")

for _, row in page_df.iterrows():
    with st.container():
        st.markdown('<div class="doc-card">', unsafe_allow_html=True)

        st.markdown(f"### {row['title']}")
        st.caption(f"Source: {row['source']}")

        col1, col2, col3 = st.columns([1, 1, 1.2])

        with col1:
            badge = "pdf" if row["type"] == "PDF" else "excel"
            st.markdown(
                f'<div class="badge {badge}">{row["type"]}</div>',
                unsafe_allow_html=True
            )

        with col2:
            st.markdown(
                f'<div class="badge year">{row["year"]}</div>',
                unsafe_allow_html=True
            )

        with col3:
            st.link_button(
                "📂 Open Document",
                row["url"],
                use_container_width=True
            )

        st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PAGINATION BUTTONS ----------------
prev_col, mid_col, next_col = st.columns([1, 2, 1])

with prev_col:
    if st.button("⬅ Previous", disabled=st.session_state.page == 1):
        st.session_state.page -= 1
        st.rerun()

with mid_col:
    st.markdown(
        f"<div class='pagination'>Page {st.session_state.page} of {total_pages}</div>",
        unsafe_allow_html=True
    )

with next_col:
    if st.button("Next ➡", disabled=st.session_state.page == total_pages):
        st.session_state.page += 1
        st.rerun()