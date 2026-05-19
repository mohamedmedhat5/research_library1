import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Research Data Library",
    page_icon="https://cdn-icons-png.flaticon.com/128/4300/4300059.png",
    layout="wide",
    initial_sidebar_state="collapsed"
)

SAUDI_LOGO = "https://stats.gov.sa/o/resources/images/logo/logo.svg"
WORLD_BANK_LOGO = "https://www.worldbank.org/content/dam/sites/edge/wbglogo-topnav-eng.svg"
SEARCH_ICON = "https://cdn-icons-png.flaticon.com/128/151/151773.png"
LIBRARY_ICON = "https://cdn-icons-png.flaticon.com/128/4300/4300059.png"

@st.cache_data
def get_counts():
    saudi = pd.read_csv("data/saudi_documents.csv")
    world = pd.read_csv("data/worldbank_documents.csv")
    return len(saudi), len(world)

saudi_count, world_count = get_counts()
total = saudi_count + world_count

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, .stApp {
    font-family: 'Inter', sans-serif;
    background:
        radial-gradient(circle at top right, rgba(37,99,235,0.16), transparent 35%),
        radial-gradient(circle at top left, rgba(16,185,129,0.08), transparent 35%),
        #020617;
}

#MainMenu, footer, header,
[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none !important;
    visibility: hidden !important;
}

.block-container {
    max-width: 1280px;
    padding-top: 2rem;
    padding-bottom: 4rem;
}

.metric-box {
    background: rgba(15,23,42,0.72);
    backdrop-filter: blur(18px);
    border-radius: 22px;
    padding: 1.6rem;
    text-align: center;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 12px 35px rgba(0,0,0,0.35);
}

.metric-icon {
    width: 28px;
    height: 28px;
    margin-bottom: 10px;
}

.metric-number {
    font-size: 2.4rem;
    font-weight: 800;
    color: #60a5fa;
}

.source-card {
    min-height: 540px;
    background: linear-gradient(180deg, rgba(8,18,40,0.95), rgba(2,8,23,0.98));
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 2rem;
    box-shadow: 0 18px 45px rgba(0,0,0,0.35);
    transition: 0.2s ease;
}

.source-card:hover {
    transform: translateY(-4px);
    border-color: rgba(96,165,250,0.25);
}

.logo-wrap {
    height: 90px;
    display: flex;
    align-items: center;
    margin-bottom: 1rem;
}

.logo-wrap img {
    max-height: 70px;
    width: auto;
    object-fit: contain;
}

.source-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: white;
    margin: 0.6rem 0;
}

.source-count {
    font-size: 3rem;
    font-weight: 800;
    color: #60a5fa;
}

.source-desc {
    color: #cbd5e1;
    font-size: 1.05rem;
    line-height: 1.6;
    margin-top: 1rem;
}

.badge {
    display: inline-flex;
    align-items: center;
    gap: 10px;
    margin-top: 1.2rem;
    padding: 10px 18px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 14px;
}

.badge img {
    width: 18px;
    height: 18px;
}

.badge-green {
    background: rgba(16,185,129,0.14);
    border: 1px solid rgba(16,185,129,0.3);
    color: #86efac;
}

.badge-blue {
    background: rgba(59,130,246,0.14);
    border: 1px solid rgba(59,130,246,0.3);
    color: #93c5fd;
}

.stButton > button {
    height: 56px;
    border-radius: 16px;
    font-size: 18px;
    font-weight: 700;
    border: none;
    color: white;
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    box-shadow: 0 10px 25px rgba(37,99,235,0.3);
}

.why-box {
    background: rgba(15,23,42,0.68);
    backdrop-filter: blur(18px);
    border-radius: 24px;
    padding: 2.2rem;
    border: 1px solid rgba(255,255,255,0.08);
}

.why-item {
    display: flex;
    align-items: center;
    gap: 14px;
    font-size: 1.05rem;
    color: #cbd5e1;
    margin: 1rem 0;
}

.why-item img {
    width: 20px;
    height: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown(f"""
<div style="text-align:center; padding: 2rem 0 3rem 0;">
    <img src="{LIBRARY_ICON}" style="width:70px;height:70px;margin-bottom:18px;">
    <h1 style="
        font-size:4.6rem;
        font-weight:800;
        background: linear-gradient(90deg,#ffffff,#93c5fd);
        -webkit-background-clip:text;
        -webkit-text-fill-color:transparent;
        margin-bottom:0.8rem;
    ">
        Research Data Library
    </h1>

    <p style="
        font-size:1.2rem;
        color:#94a3b8;
        max-width:760px;
        margin:auto;
        line-height:1.7;
    ">
        Trusted official datasets. Fast access. Research-ready downloads.
    </p>
</div>
""", unsafe_allow_html=True)

m1, m2, m3 = st.columns(3)

with m1:
    st.markdown(f"""
    <div class="metric-box">
        <img src="{LIBRARY_ICON}" class="metric-icon">
        <div class="metric-number">{total}+</div>
        <div>Available Resources</div>
    </div>
    """, unsafe_allow_html=True)

with m2:
    st.markdown(f"""
    <div class="metric-box">
        <img src="{SEARCH_ICON}" class="metric-icon">
        <div class="metric-number">2</div>
        <div>Official Sources</div>
    </div>
    """, unsafe_allow_html=True)

with m3:
    st.markdown(f"""
    <div class="metric-box">
        <img src="{SEARCH_ICON}" class="metric-icon">
        <div class="metric-number">Monthly</div>
        <div>Auto Updates</div>
    </div>
    """, unsafe_allow_html=True)

c1, c2 = st.columns(2, gap="large")

with c1:
    st.markdown(f"""
    <div class="source-card">
        <div class="logo-wrap">
            <img src="{SAUDI_LOGO}">
        </div>

        <div class="source-title">Saudi Statistics</div>
        <div class="source-count">{saudi_count}</div>

        <div class="source-desc">
            Official Saudi reports, PDF publications, and Excel datasets.
        </div>

        <div class="badge badge-green">
            <img src="{SAUDI_LOGO}">
            Official Government Source
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Explore Saudi Statistics", use_container_width=True):
        st.switch_page("pages/saudi.py")

with c2:
    st.markdown(f"""
    <div class="source-card">
        <div class="logo-wrap">
            <img src="{WORLD_BANK_LOGO}">
        </div>

        <div class="source-title">World Bank</div>
        <div class="source-count">{world_count}</div>

        <div class="source-desc">
            Global economic indicators and downloadable datasets.
        </div>

        <div class="badge badge-blue">
            <img src="{WORLD_BANK_LOGO}">
            Trusted International Source
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Explore World Bank", use_container_width=True):
        st.switch_page("pages/worldbank.py")

st.markdown(f"""
<div class="why-box">
    <h2 style="color:white;">Why this platform?</h2>

    <div class="why-item">
        <img src="{SEARCH_ICON}">
        Unified access to multiple trusted official sources
    </div>

    <div class="why-item">
        <img src="{SEARCH_ICON}">
        Fast search and filtering experience
    </div>

    <div class="why-item">
        <img src="{SEARCH_ICON}">
        Automatically updated downloadable datasets
    </div>

    <div class="why-item">
        <img src="{LIBRARY_ICON}">
        Research-ready resources for analysts and businesses
    </div>
</div>
""", unsafe_allow_html=True)