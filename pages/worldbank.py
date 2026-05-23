import math
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

WORLD_BANK_LOGO = "https://www.worldbank.org/content/dam/sites/edge/wbglogo-topnav-eng.svg"
BACK_ICON = "https://cdn-icons-png.flaticon.com/128/10238/10238019.png"
SEARCH_ICON = "https://cdn-icons-png.flaticon.com/128/151/151773.png"
DOWNLOAD_ICON = "https://cdn-icons-png.flaticon.com/128/7268/7268609.png"
DATASET_ICON = "https://cdn-icons-png.flaticon.com/128/18289/18289400.png"
EXCEL_ICON = "https://res.cdn.office.net/files/fabric-cdn-prod_20251117.001/assets/brand-icons/product/svg/excel_16x1.svg"

st.set_page_config(
    page_title="World Bank Data",
    page_icon="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAMAAABEpIrGAAABoVBMVEVHcEwAUnsAN14AN1wAOF8AUn8AZ5gAZ5kAdKgAerAAhbwAlNAAntwDqegKs/ALsu4PtfAaufFCyPQ+xfK66vwete4APWMAM1oASnUARnAAWIcAZJQAb6IAea8Ae7EAkcwdu/Iyw/NAx/RQzPRXzfW46u8AMFYASXQASXMAWYcAZJQAjMYAks4YufErwfNJyvRi0PZx1PaI2fYAL1QAL1QAO2IAhLsJsO01xfRWzfV41feG2fet4vqr4voAMVcALlQAP2gATXkAWokAouBUzfWa3fmu4/qy5PoAL1QAMFYAea8AicAAouAIsO5TzPUAMlgALlMAL1UAXo4AWogAbp8AWYUgqt8BoN4Ao+ICqOggvPI4xvQ+xvS/6PwAL1UALlQAVoQAisMAlNAAntwAl9QZs+vV8f8AMVcALlQAgrkNs+8XuPEOs+2X3Pmu4/rC6PwALlMAj8oAltECot8ALlMAL1QAM1gANlsAYpMAaJsLsO5x0/YAMVUAaZuK2vcAcKQCrewkvvIALlMAMFUAZ5oIlcwASHIAn90ASHMAOF8ASXTQ1jq/AAAAi3RSTlMAAgYRJUBrn8Da5Ofs8dnLrYJZOQwJCzJge56Mk6Gxysqyo4VnA2W2xuK0kLjr4Ny5dxw+e5q2+sjLz6tjNnTG0aV4yZvApVGXsWBhqqSOX6mI0IMyIRRqeVWUfE0qbqTFQH+eXysjRr2Bab1ehnpC1VEjHN6eVCoU2zniGU/TeYxs7pFbDVGMcryNSI47cgAAA0tJREFUeAFVkwV7qlAYgI85u7tdMNeF6+F64gJZdwe6wsLu9lffw+p57kvDC5zzBWDhcHl8gbBLJJZIZXK5QqlSa7Q6PfiDYzCazBarze5wfgkKl7u7p1fb1/f7nMdH+j0Dg1bb0DArjIyMjo6NjU9M6n7fn0K9nn5Ll80+PeyUzcxAYXZ8bn5hcennOR/zLS+vrFptjunh4TU5NEbd6+PzG5tbgIVrRFA/Dr9gFQa2h4Z3dpUjcAh7E4uLP1/gEUES8/Z79g8Oj45Phk/Pzl2qi729y77Jq0mdDg6Uf43f+L0rt7erh4d39w+PT2qX+vJivXdpa3Fr6VmnAy+kj8K95hUoBEJD93f68OvbsWZ9b+J982Px8/kKYEEaJwmB6eDAaneEIlF9WPUW02p6xhc2P7bgQEDQF08wSZASWNNicSgai4V3w5mnp71sduP982NzE1A+Ck3mgOFIOCgS2e/vT3eVu2r1Rffc+MLi1cfGBoj7/C8AYsizkXI615QK5atr1r2+vn6pmygUQDyIGGG4OCnhYDEf2X48Kal21WWNRrM3rjmemJ8Hlaox9xXPg9saG9jjs1I4EwOgfjHbO3kxNwcqiRc+jCe/sWrJfwvNk0wUAF3ZXdb2zM2CCk4YORzDi7llOgSQeqT5+PWFy/Oy5nwWCj4/kTMYGG9LcPQtDD0+sYJWXS6fu1yApn3kFD+HtQkD9084BkCfCZfVKihQQX+VRJhqm+BwfoTt6LdQUkFAFb1OUDdVnCI4XFapB+yBWB0eM6e7ClWpBBC0iiFogqLJqSTPwAqOQF0P6tHHhzXZw9kbmEJxBtaEj765Zox8Hu+oKBKmUqno3b1TKr2PRmE9BK+nENJ/Q15jmNncWh1MdwmLxWJoWuIcfqwfAwPjRzHINYKQeNvjuR0Y2IdpEznEkunQHVuTSQZNJPwk8mKcYhiTCZaOtVYLFO0icegu+t0WCEVRfpgyFp6xtdLgGlJ5a1dXHnB++gp+POgn+Dy2xomWuZFstA6sq/lDKHzDYxI4Rb4YebwcQ6IIYer0rxwI/h7DbyQZBIVgGAwIniAxmDnB0Vdk/8hNXcPqpOlKpUJTVSLJA//Dzb1gQYqm6XglDgUEVukP/wBwkt2jqNTNwAAAAABJRU5ErkJggg==",
    layout="wide"
)

ROWS_PER_PAGE = 20


@st.cache_data
def load_data():
    df = pd.read_csv("data/worldbank_documents.csv")
    df.fillna("", inplace=True)

    df["title"] = (
        df["title"]
        .str.replace(r"https?://\S+", "", regex=True)
        .str.strip()
    )
    return df


df = load_data()

search = st.query_params.get("q", "")
page = int(st.query_params.get("page", 1))
file_type = st.query_params.get("type", "All")


st.markdown("""
<style>
html, body, .stApp {
    background:
        radial-gradient(circle at top right, rgba(37,99,235,0.18), transparent 35%),
        radial-gradient(circle at top left, rgba(16,185,129,0.08), transparent 35%),
        #020617;
    color: white;
}

#MainMenu, footer, header {
    visibility: hidden;
}

[data-testid="stSidebar"],
[data-testid="collapsedControl"] {
    display: none;
}

.block-container {
    max-width: 1450px;
    padding-top: 2rem;
}

.hero {
    text-align: center;
    margin-bottom: 2rem;
}

.hero img {
    height: 70px;
    margin-bottom: 1rem;
}

.hero h1 {
    font-size: 4rem;
    font-weight: 800;
    color: #e2e8f0;
}

.hero p {
    color: #94a3b8;
    font-size: 1.15rem;
}

.toolbar {
    background: rgba(15,23,42,0.6);
    padding: 1rem;
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.06);
    margin-bottom: 1.5rem;
}

.card {
    background: rgba(15,23,42,0.65);
    border: 1px solid rgba(255,255,255,0.06);
    border-radius: 22px;
    padding: 1.2rem 1.5rem;
    margin-bottom: 1rem;
    backdrop-filter: blur(14px);
}

.dataset-row {
    display: flex;
    align-items: center;
    gap: 16px;
}

.dataset-icon {
    width: 38px;
    height: 38px;
}

.dataset-title {
    color: white;
    font-size: 1.08rem;
    font-weight: 700;
}

.stButton button {
    background: linear-gradient(135deg, #1d4ed8, #2563eb) !important;
    color: white !important;
    border: none !important;
    border-radius: 16px !important;
    height: 52px !important;
    font-weight: 700 !important;
}

.pagination {
    text-align: center;
    color: white;
    font-weight: 700;
    margin: 1rem 0;
}
</style>
""", unsafe_allow_html=True)


if st.button("⬅ Back to Sources"):
    st.switch_page("app.py")


st.markdown(f"""
<div class="hero">
    <img src="{WORLD_BANK_LOGO}">
    <h1>World Bank Data</h1>
    <p>Official World Bank datasets related to Saudi Arabia.</p>
</div>
""", unsafe_allow_html=True)


st.markdown('<div class="toolbar">', unsafe_allow_html=True)

c1, c2 = st.columns([3, 1])

with c1:
    new_search = st.text_input(
        "Search",
        value=search,
        placeholder="Search World Bank datasets..."
    )

with c2:
    new_type = st.selectbox(
        "Type",
        ["All", "CSV", "Excel"],
        index=["All", "CSV", "Excel"].index(file_type)
    )

st.markdown('</div>', unsafe_allow_html=True)


filtered = df.copy()

if new_search:
    filtered = filtered[
        filtered["title"].str.contains(new_search, case=False, na=False)
    ]

if new_type == "CSV":
    filtered = filtered[filtered["csv_url"] != ""]

elif new_type == "Excel":
    filtered = filtered[filtered["excel_url"] != ""]


total_rows = len(filtered)
total_pages = max(1, math.ceil(total_rows / ROWS_PER_PAGE))

start = (page - 1) * ROWS_PER_PAGE
end = start + ROWS_PER_PAGE
page_df = filtered.iloc[start:end]


p1, p2, p3 = st.columns([1, 2, 1])

with p1:
    if page > 1:
        if st.button("⬅ Previous"):
            st.query_params["page"] = page - 1
            st.rerun()

with p2:
    st.markdown(
        f'<div class="pagination">Page {page} of {total_pages} — {total_rows} datasets</div>',
        unsafe_allow_html=True
    )

with p3:
    if page < total_pages:
        if st.button("Next ➜"):
            st.query_params["page"] = page + 1
            st.rerun()


for _, row in page_df.iterrows():
    st.markdown(f"""
    <div class="card">
        <div class="dataset-row">
            <img src="{DATASET_ICON}" class="dataset-icon">
            <div class="dataset-title">{row['title']}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    buttons_html = f"""
    <div style="display:flex; justify-content:flex-end; gap:14px; margin-bottom:25px;">
        <a href="{row['csv_url']}" target="_blank"
           style="
             display:flex;
             align-items:center;
             gap:10px;
             background:linear-gradient(135deg,#ca8a04,#eab308);
             color:white;
             padding:14px 24px;
             border-radius:16px;
             text-decoration:none;
             font-weight:700;">
            <img src="{DOWNLOAD_ICON}" width="18">
            CSV
        </a>

        <a href="{row['excel_url']}" target="_blank"
           style="
             display:flex;
             align-items:center;
             gap:10px;
             background:linear-gradient(135deg,#047857,#10b981);
             color:white;
             padding:14px 24px;
             border-radius:16px;
             text-decoration:none;
             font-weight:700;">
            <img src="{EXCEL_ICON}" width="18">
            Excel
        </a>
    </div>
    """

    components.html(buttons_html, height=80)