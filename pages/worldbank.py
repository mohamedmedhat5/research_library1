import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title='World Bank Datasets',
    page_icon="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAABoVBMVEVHcEwAUnsAN14AN1wAOF8AUn8AZ5gAZ5kAdKgAerAAhbwAlNAAntwDqegKs/ALsu4PtfAaufFCyPQ+xfK66vwete4APWMAM1oASnUARnAAWIcAZJQAb6IAea8Ae7EAkcwdu/Iyw/NAx/RQzPRXzfW46u8AMFYASXQASXMAWYcAZJQAjMYAks4YufErwfNJyvRi0PZx1PaI2fYAL1QAL1QAO2IAhLsJsO01xfRWzfV41feG2fet4vqr4voAMVcALlQAP2gATXkAWokAouBUzfWa3fmu4/qy5PoAL1QAMFYAea8AicAAouAIsO5TzPUAMlgALlMAL1UAXo4AWogAbp8AWYUgqt8BoN4Ao+ICqOggvPI4xvQ+xvS/6PwAL1UALlQAVoQAisMAlNAAntwAl9QZs+vV8f8AMVcALlQAgrkNs+8XuPEOs+2X3Pmu4/rC6PwALlMAj8oAltECot8ALlMAL1QAM1gANlsAYpMAaJsLsO5x0/YAMVUAaZuK2vcAcKQCrewkvvIALlMAMFUAZ5oIlcwASHIAn90ASHMAOF8ASXTQ1jq/AAAAi3RSTlMAAgYRJUBrn8Da5Ofs8dnLrYJZOQwJCzJge56Mk6Gxysqyo4VnA2W2xuK0kLjr4Ny5dxw+e5q2+sjLz6tjNnTG0aV4yZvApVGXsWBhqqSOX6mI0IMyIRRqeVWUfE0qbqTFQH+eXysjRr2Bab1ehnpC1VEjHN6eVCoU2zniGU/TeYxs7pFbDVGMcryNSI47cgAAA0tJREFUeAFVkwV7qlAYgI85u7tdMNeF6+F64gJZdwe6wsLu9lffw+p57kvDC5zzBWDhcHl8gbBLJJZIZXK5QqlSa7Q6PfiDYzCazBarze5wfgkKl7u7p1fb1/f7nMdH+j0Dg1bb0DArjIyMjo6NjU9M6n7fn0K9nn5Ll80+PeyUzcxAYXZ8bn5hcennOR/zLS+vrFptjunh4TU5NEbd6+PzG5tbgIVrRFA/Dr9gFQa2h4Z3dpUjcAh7E4uLP1/gEUES8/Z79g8Oj45Phk/Pzl2qi729y77Jq0mdDg6Uf43f+L0rt7erh4d39w+PT2qX+vJivXdpa3Fr6VmnAy+kj8K95hUoBEJD93f68OvbsWZ9b+J982Px8/kKYEEaJwmB6eDAaneEIlF9WPUW02p6xhc2P7bgQEDQF08wSZASWNNicSgai4V3w5mnp71sduP982NzE1A+Ck3mgOFIOCgS2e/vT3eVu2r1Rffc+MLi1cfGBoj7/C8AYsizkXI615QK5atr1r2+vn6pmygUQDyIGGG4OCnhYDEf2X48Kal21WWNRrM3rjmemJ8Hlaox9xXPg9saG9jjs1I4EwOgfjHbO3kxNwcqiRc+jCe/sWrJfwvNk0wUAF3ZXdb2zM2CCk4YORzDi7llOgSQeqT5+PWFy/Oy5nwWCj4/kTMYGG9LcPQtDD0+sYJWXS6fu1yApn3kFD+HtQkD9084BkCfCZfVKihQQX+VRJhqm+BwfoTt6LdQUkFAFb1OUDdVnCI4XFapB+yBWB0eM6e7ClWpBBC0iiFogqLJqSTPwAqOQF0P6tHHhzXZw9kbmEJxBtaEj765Zox8Hu+oKBKmUqno3b1TKr2PRmE9BK+nENJ/Q15jmNncWh1MdwmLxWJoWuIcfqwfAwPjRzHINYKQeNvjuR0Y2IdpEznEkunQHVuTSQZNJPwk8mKcYhiTCZaOtVYLFO0icegu+t0WCEVRfpgyFp6xtdLgGlJ5a1dXHnB++gp+POgn+Dy2xomWuZFstA6sq/lDKHzDYxI4Rb4YebwcQ6IIYer0rxwI/h7DbyQZBIVgGAwIniAxmDnB0Vdk/8hNXcPqpOlKpUJTVSLJA//Dzb1gQYqm6XglDgUEVukP/wBwkt2jqNTNwAAAAABJRU5ErkJggg==",
    layout='wide',
    initial_sidebar_state='collapsed'
)

WORLD_BANK_LOGO = "https://www.worldbank.org/content/dam/sites/edge/wbglogo-topnav-eng.svg"
BACK_ICON = "https://cdn-icons-png.flaticon.com/128/10238/10238019.png"
SEARCH_ICON = "https://cdn-icons-png.flaticon.com/128/151/151773.png"
DOWNLOAD_ICON = "https://cdn-icons-png.flaticon.com/128/7268/7268609.png"
DATASET_ICON = "https://cdn-icons-png.flaticon.com/128/18289/18289400.png"

@st.cache_data
def load_worldbank():
    url = "https://api.worldbank.org/v2/sources?format=json&per_page=200"
    r = requests.get(url, timeout=20)

    if r.status_code != 200:
        return pd.DataFrame(columns=["id", "name"])

    data = r.json()
    if len(data) < 2:
        return pd.DataFrame(columns=["id", "name"])

    df = pd.DataFrame(data[1])[["id", "name"]]
    df["name"] = df["name"].fillna("")
    return df


df = load_worldbank()

if 'wb_page' not in st.session_state:
    st.session_state.wb_page = 1

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=Cairo:wght@400;700;800&display=swap');

html, body, .stApp {
    font-family: 'Inter', 'Cairo', sans-serif;
    background:
        radial-gradient(circle at top right, rgba(37,99,235,0.14), transparent 35%),
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
    max-width: 1380px;
    padding-top: 0.6rem;
    padding-bottom: 2rem;
}

hr {
    display: none !important;
}

.stTextInput input {
    background: rgba(15,23,42,0.72) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    color: white !important;
    height: 50px !important;
    padding-left: 52px !important;
}

.search-wrap {
    position: relative;
}

.search-wrap img {
    position: absolute;
    top: 14px;
    left: 16px;
    width: 20px;
    height: 20px;
    z-index: 10;
}

.hero {
    text-align: center;
    padding: 0.2rem 0 1.2rem;
}

.hero img {
    height: 74px;
    margin-bottom: 0.7rem;
}

.hero h1 {
    font-size: 4rem;
    font-weight: 800;
    margin-bottom: 0.4rem;
    background: linear-gradient(90deg,#ffffff,#93c5fd);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero p {
    color: #94a3b8;
    font-size: 1.05rem;
}

.filter-wrap {
    background: rgba(15,23,42,0.52);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    backdrop-filter: blur(16px);
}

.dataset-card {
    background: linear-gradient(
        180deg,
        rgba(8,18,40,0.96),
        rgba(2,8,23,0.98)
    );
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 20px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.65rem;
    box-shadow: 0 10px 24px rgba(0,0,0,0.24);
    transition: all 0.2s ease;
}

.dataset-card:hover {
    transform: translateY(-2px);
    border-color: rgba(96,165,250,0.25);
}

.title-en {
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 1.08rem;
    font-weight: 700;
    color: white;
}

.title-en img {
    width: 22px;
    height: 22px;
}

.file-btn {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    width: 100%;
    height: 48px;
    border-radius: 14px;
    text-decoration: none !important;
    font-weight: 700;
    font-size: 0.95rem;
    border: 1px solid rgba(255,255,255,0.08);
    transition: 0.2s;
}

.file-btn img {
    width: 18px;
    height: 18px;
}

.download-btn {
    background: rgba(59,130,246,0.10);
    color: #dbeafe !important;
}

.download-btn:hover {
    background: rgba(59,130,246,0.18);
}

.source-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 48px;
    border-radius: 999px;
    background: rgba(59,130,246,0.14);
    border: 1px solid rgba(59,130,246,0.28);
}

.source-badge img {
    height: 22px;
}

.nav-btn img {
    width: 16px;
    height: 16px;
}

.nav-next {
    transform: rotate(180deg);
}

.stButton > button {
    height: 44px;
    border-radius: 14px;
    font-weight: 700;
    border: none;
    background: linear-gradient(135deg,#1d4ed8,#2563eb);
    color: white;
}

.footer {
    text-align: center;
    color: #64748b;
    margin-top: 1.5rem;
}
</style>
""", unsafe_allow_html=True)

if st.button('Back to Sources'):
    st.switch_page('app.py')

st.markdown(f"""
<div class='hero'>
    <img src='{WORLD_BANK_LOGO}'>
    <h1>World Bank Datasets</h1>
    <p>
        Trusted global datasets, economic indicators,
        development metrics, and downloadable World Bank resources.
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("<div class='filter-wrap'>", unsafe_allow_html=True)

st.markdown(f"""
<div class='search-wrap'>
    <img src="{SEARCH_ICON}">
</div>
""", unsafe_allow_html=True)

search = st.text_input(
    "Search",
    placeholder="Search World Bank datasets..."
)

st.markdown("</div>", unsafe_allow_html=True)

filtered = df.copy()

if search:
    filtered = filtered[
        filtered["name"].str.contains(search, case=False, na=False)
    ]

page_size = 12
total_pages = max(1, (len(filtered)-1)//page_size + 1)

if st.session_state.wb_page > total_pages:
    st.session_state.wb_page = 1

if filtered.empty:
    st.markdown("""
    <div style='padding:3rem;text-align:center;color:#cbd5e1'>
        <h2>No datasets found</h2>
    </div>
    """, unsafe_allow_html=True)
    st.stop()

p1, p2, p3 = st.columns([1,2,1])

with p1:
    if st.button('Previous'):
        if st.session_state.wb_page > 1:
            st.session_state.wb_page -= 1
            st.rerun()

with p2:
    st.markdown(f"""
    <div style='text-align:center;color:#cbd5e1;padding-top:10px;font-weight:700'>
        Page {st.session_state.wb_page} of {total_pages}
    </div>
    """, unsafe_allow_html=True)

with p3:
    if st.button('Next'):
        if st.session_state.wb_page < total_pages:
            st.session_state.wb_page += 1
            st.rerun()

start = (st.session_state.wb_page - 1) * page_size
page_df = filtered.iloc[start:start+page_size]

for _, row in page_df.iterrows():
    st.markdown('<div class="dataset-card">', unsafe_allow_html=True)

    c1, c2, c3 = st.columns([8, 2, 2])

    with c1:
        st.markdown(
            f'''
            <div class="title-en">
                <img src="{DATASET_ICON}">
                {row["name"]}
            </div>
            ''',
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f'''
            <div class="source-badge">
                <img src="{WORLD_BANK_LOGO}">
            </div>
            ''',
            unsafe_allow_html=True
        )

    with c3:
        download_url = f"https://api.worldbank.org/v2/en/sources/{row['id']}/download"

        st.markdown(
            f"""
            <a href="{download_url}" target="_blank" class="file-btn download-btn">
                <img src="{DOWNLOAD_ICON}">
                Download
            </a>
            """,
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    "<div class='footer'>Research Data Library • Powered by World Bank official datasets</div>",
    unsafe_allow_html=True
)