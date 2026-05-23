import streamlit as st
import pandas as pd


PDF_ICON='https://cdn-icons-png.flaticon.com/512/11180/11180582.png'
EXCEL_ICON='https://res.cdn.office.net/files/fabric-cdn-prod_20251117.001/assets/brand-icons/product/svg/excel_16x1.svg'
LOGO='https://stats.gov.sa/o/resources/images/logo/logo.svg'


st.set_page_config(page_title='Saudi Statistics', page_icon=LOGO, layout='wide', initial_sidebar_state='collapsed')


@st.cache_data
def load_data():
    df = pd.read_csv('data/saudi_documents.csv')
    for c in ['title','year','pdf_url','excel_url']:
        if c not in df.columns:
            df[c]=None
    df['title']=df['title'].fillna('')
    df['year']=df['year'].fillna('Unknown').astype(str)
    return df

df=load_data()
if 'sa_page' not in st.session_state:
    st.session_state.sa_page=1

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

/* Inputs */
.stTextInput input,
.stSelectbox div[data-baseweb="select"] > div {
    background: rgba(15,23,42,0.72) !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    border-radius: 16px !important;
    color: white !important;
    height: 50px !important;
}

/* hide ugly hr */
hr {
    display: none !important;
}

/* hero */
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

/* filters */
.filter-wrap {
    background: rgba(15,23,42,0.52);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 20px;
    padding: 1rem;
    margin-bottom: 0.8rem;
    backdrop-filter: blur(16px);
}

/* dataset card */
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

/* titles */
.title-ar {
    font-family: 'Cairo', sans-serif;
    font-size: 1.18rem;
    font-weight: 700;
    color: white;
    direction: rtl;
    text-align: right;
    width: 100%;
    padding-right: 6px;
    line-height: 1.7;
}

.title-en {
    font-size: 1.08rem;
    font-weight: 700;
    color: white;
}

/* buttons */
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
    width: 16px;
    height: 16px;
    object-fit: contain;
}

.pdf-btn {
    background: rgba(255,80,80,0.10);
    color: #ffb3b3 !important;
}

.pdf-btn:hover {
    background: rgba(255,80,80,0.18);
}

.excel-btn {
    background: rgba(30,200,120,0.10);
    color: #b9ffd6 !important;
}

.excel-btn:hover {
    background: rgba(30,200,120,0.18);
}

/* year */
.year-badge {
    display: flex;
    align-items: center;
    justify-content: center;
    height: 48px;
    border-radius: 999px;
    background: rgba(59,130,246,0.14);
    border: 1px solid rgba(59,130,246,0.28);
    color: #93c5fd;
    font-weight: 700;
    font-size: 14px;
}

/* pagination cleanup */
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

if st.button('← Back to Sources'):
    st.switch_page('app.py')

st.markdown(f"""<div class='hero'><img src='{LOGO}'><h1>Saudi Statistics</h1><p>Official Saudi statistical publications, downloadable reports, and Excel datasets.</p></div>""", unsafe_allow_html=True)

st.markdown("<div class='filter-wrap'>", unsafe_allow_html=True)
c1,c2,c3=st.columns([5,1.5,1.5])
with c1: search=st.text_input('Search', placeholder='Search Saudi statistical reports...')
with c2: selected_year=st.selectbox('Year',['All']+sorted(df['year'].unique(), reverse=True))
with c3: file_type=st.selectbox('Type',['All','PDF','Excel'])
st.markdown('</div>', unsafe_allow_html=True)

filtered=df.copy()
if search: filtered=filtered[filtered['title'].str.contains(search, case=False, na=False)]
if selected_year!='All': filtered=filtered[filtered['year']==selected_year]
if file_type=='PDF': filtered=filtered[filtered['pdf_url'].notna()]
elif file_type=='Excel': filtered=filtered[filtered['excel_url'].notna()]

page_size=12
total_pages=max(1,(len(filtered)-1)//page_size+1)
if st.session_state.sa_page>total_pages: st.session_state.sa_page=1

if filtered.empty:
    st.markdown("<div class='empty-box' style='padding:3rem;text-align:center;color:#cbd5e1'><h2>🔍 No datasets found</h2><p>Try adjusting filters.</p></div>", unsafe_allow_html=True)
    st.stop()

p1,p2,p3=st.columns([1,2,1])
with p1:
    if st.button('← Previous', disabled=st.session_state.sa_page==1): st.session_state.sa_page-=1; st.rerun()
with p2: st.markdown(f"<div style='text-align:center;color:#cbd5e1;padding-top:10px;font-weight:700'>Page {st.session_state.sa_page} of {total_pages}</div>", unsafe_allow_html=True)
with p3:
    if st.button('Next →', disabled=st.session_state.sa_page==total_pages): st.session_state.sa_page+=1; st.rerun()

start=(st.session_state.sa_page-1)*page_size
page_df=filtered.iloc[start:start+page_size]

for _, row in page_df.iterrows():

    title = row["title"]
    arabic = any('\u0600' <= c <= '\u06FF' for c in title)

    st.markdown('<div class="dataset-card">', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([8, 1.8, 1.8, 1])

    with c1:
        if arabic:
            st.markdown(
                f'<div class="title-ar">📄 {title}</div>',
                unsafe_allow_html=True
            )
        else:
            st.markdown(
                f'<div class="title-en">📄 {title}</div>',
                unsafe_allow_html=True
            )

    with c2:
        if pd.notna(row["pdf_url"]):
            st.markdown(
                f"""
                <a href="{row['pdf_url']}" target="_blank" class="file-btn pdf-btn">
                    <img src="{PDF_ICON}">
                    PDF
                </a>
                """,
                unsafe_allow_html=True
            )

    with c3:
        if pd.notna(row["excel_url"]):
            st.markdown(
                f"""
                <a href="{row['excel_url']}" target="_blank" class="file-btn excel-btn">
                    <img src="{EXCEL_ICON}">
                    Excel
                </a>
                """,
                unsafe_allow_html=True
            )

    with c4:
        st.markdown(
            f'<div class="year-badge">{row["year"]}</div>',
            unsafe_allow_html=True
        )

    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("<div class='footer'>Research Data Library • Powered by official Saudi public datasets</div>", unsafe_allow_html=True)