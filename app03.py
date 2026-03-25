import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일: 검색창 내부 X 버튼 구현
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }

    /* 타이틀 디자인 */
    .main-title { font-size: 1.5rem; font-weight: 800; text-align: center; margin-bottom: 20px; }

    /* 검색창 컨테이너 */
    .search-box-container {
        position: relative;
        width: 100%;
        margin-bottom: 20px;
    }

    /* Streamlit 입력창 커스텀 (라운드형 + 오른쪽 여백) */
    div[data-testid="stTextInput"] input {
        border-radius: 25px !important;
        padding-right: 45px !important; /* X 버튼이 들어갈 자리 확보 */
        height: 45px !important;
        border: 1px solid #ddd !important;
    }

    /* 지우기 버튼을 입력창 안으로 강제 배치 */
    .clear-btn-wrapper {
        position: absolute;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        z-index: 100;
    }

    .stButton > button {
        background: none !important;
        border: none !important;
        color: #999 !important;
        font-size: 18px !important;
        font-weight: bold !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 30px !important;
        height: 30px !important;
        box-shadow: none !important;
    }
    
    .stButton > button:hover { color: #333 !important; }

    /* 카드 디자인 */
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
    .name-text { font-weight: 700; font-size: 1.05rem; }
    .pos-dept { font-size: 0.85rem; color: #666; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 3px; }
    .icon-section { display: flex; gap: 15px; flex-shrink: 0; }
    .icon-link { text-decoration: none !important; font-size: 1.3rem; font-weight: 800; color: #007bff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 및 세션 관리
if "search_term" not in st.session_state:
    st.session_state.search_term = ""

@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

# 4. 검색창 내부 X 버튼 레이아웃 (Overlay 방식)
st.markdown('<div class="search-box-container">', unsafe_allow_html=True)

# 검색창
query = st.text_input(
    "search", 
    value=st.session_state.search_term,
    placeholder="🔍 성함, 부서, 업무 검색", 
    label_visibility="collapsed",
    key="search_input"
)
st.session_state.search_term = query

# 검색창 안에 겹쳐질 X 버튼 (값이 있을 때만 노출하는 것이 좋지만, 구조상 상시 배치)
with st.container():
    st.markdown('<div class="clear-btn-wrapper">', unsafe_allow_html=True)
    if st.button("✕", key="clear_btn"):
        st.session_state.search_term = ""
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 5. 데이터 리스트 출력
SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

if not df.empty:
    search = st.session_state.search_term.lower()
    for _, row in df.iterrows():
        name, dept, pos, ext, mobile, work = row['성명'], row['부서'], row['직함'], str(row['내선']), str(row['휴대폰']), row['담당업무']
        
        if search and search not in f"{name}{dept}{work}{pos}".lower():
            continue

        t_num = ext.replace("-", "").strip()
        m_num = mobile.replace("-", "").strip()
        t_html = f'<a href="tel:{t_num}" class="icon-link">T</a>' if t_num else ""
        m_html = f'<a href="tel:{m_num}" class="icon-link">M</a>' if m_num else ""
        sep = " · " if pos and dept else ""

        st.markdown(f"""
            <div class="contact-card">
                <div class="info-section">
                    <div class="name-row"><span class="name-text">{name}</span><span class="pos-dept">{pos}{sep}{dept}</span></div>
                    <div class="work-text">{"- "+work if work.strip() else ""}</div>
                </div>
                <div class="icon-section">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
