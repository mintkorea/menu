import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (강력한 한 줄 고정 레이아웃)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem !important; }
    
    /* 검색창 영역 강제 한 줄 고정 */
    .search-wrapper {
        display: flex;
        align-items: center;
        gap: 5px;
        width: 100%;
        margin-bottom: 15px;
    }
    
    /* 검색창 본체 */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stTextInput"]) {
        flex: 1 !important;
        min-width: 0 !important; /* 잘림 방지 */
    }
    
    /* 버튼이 있는 컬럼 강제 고정 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important; /* 절대 줄바꿈 금지 */
        align-items: center !important;
    }
    
    [data-testid="column"] {
        width: auto !important;
        flex: none !important;
    }
    
    /* 검색창 컬럼 (85%) */
    [data-testid="column"]:nth-child(1) {
        flex: 1 1 85% !important;
    }
    
    /* 버튼 컬럼 (15%) */
    [data-testid="column"]:nth-child(2) {
        flex: 0 0 50px !important; /* 버튼 너비 고정 */
        min-width: 50px !important;
    }

    /* 버튼 스타일 */
    .stButton > button {
        width: 100% !important;
        height: 42px !important;
        padding: 0px !important;
        border: 1px solid #ddd !important;
        border-radius: 4px !important;
        background-color: #f8f9fa !important;
    }

    .main-title { font-size: 1.5rem; font-weight: 800; text-align: center; margin-bottom: 10px; }
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 10px 0px; border-bottom: 1px solid #eeeeee; }
    .name-text { font-weight: 700; font-size: 1.05rem; }
    .pos-dept { font-size: 0.85rem; color: #555; }
    .work-text { font-size: 0.8rem; color: #777; margin-top: 2px; line-height: 1.3; }
    .icon-section { min-width: 55px; display: flex; justify-content: flex-end; gap: 10px; }
    .icon-link { text-decoration: none !important; font-size: 1.2rem; font-weight: 800; color: #007bff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드 및 세션 관리
if "search_input" not in st.session_state:
    st.session_state["search_input"] = ""

@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

# 4. 검색창 레이아웃
c1, c2 = st.columns([0.85, 0.15])

with c1:
    # 텍스트 입력을 세션 상태와 연동
    query = st.text_input(
        "search", 
        value=st.session_state["search_input"],
        placeholder="성함, 부서, 업무 검색...",
        label_visibility="collapsed",
        key="search_widget"
    )
    # 위젯의 값이 바뀔 때 세션 상태 동기화
    st.session_state["search_input"] = query

with c2:
    if st.button("X"):
        st.session_state["search_input"] = ""
        st.rerun()

# 5. 리스트 출력
SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"

try:
    df = load_data(SHEET_URL)
    search_term = st.session_state["search_input"].lower()

    for _, row in df.iterrows():
        # 컬럼 이름이 시트와 정확히 일치해야 합니다 (성명, 부서, 직함, 내선, 휴대폰, 담당업무)
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

        if search_term and search_term not in f"{name}{dept}{work}{pos}".lower():
            continue

        # 전화 연결 번호 정제
        t_num = ext.replace("-", "").replace(" ", "")
        m_num = mobile.replace("-", "").replace(" ", "")

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
except Exception as e:
    st.info("시트 데이터를 불러오고 있습니다...")
