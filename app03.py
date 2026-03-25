import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (버튼 크기 강제 고정 및 한 줄 레이아웃)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem !important; }
    
    /* 검색 영역 한 줄 강제 고정 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 5px !important;
    }
    
    /* 검색창 컬럼 */
    [data-testid="column"]:nth-child(1) {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }
    
    /* 버튼 컬럼: 너비를 아이콘 하나 크기 정도로 제한 */
    [data-testid="column"]:nth-child(2) {
        flex: 0 0 45px !important; 
        min-width: 45px !important;
        max-width: 45px !important;
    }

    /* X 버튼 스타일: 길게 늘어지지 않도록 고정 */
    .stButton > button {
        width: 40px !important; /* 너비 고정 */
        height: 40px !important; /* 높이 고정 (정사각형 느낌) */
        padding: 0px !important;
        margin: 0px !important;
        border: 1px solid #ddd !important;
        border-radius: 4px !important;
        background-color: #f8f9fa !important;
        font-size: 1rem !important;
        line-height: 40px !important;
    }

    .main-title { font-size: 1.5rem; font-weight: 800; text-align: center; margin-bottom: 10px; }
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 10px 0px; border-bottom: 1px solid #eeeeee; }
    .name-text { font-weight: 700; font-size: 1.05rem; color: #000; }
    .pos-dept { font-size: 0.85rem; color: #555; }
    .work-text { font-size: 0.8rem; color: #777; margin-top: 2px; line-height: 1.3; }
    .icon-section { min-width: 60px; display: flex; justify-content: flex-end; gap: 10px; flex-shrink: 0; }
    .icon-link { text-decoration: none !important; font-size: 1.2rem; font-weight: 800; color: #007bff !important; width: 25px; text-align: center; }
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
c1, c2 = st.columns([0.88, 0.12]) # 비율을 더 극단적으로 조정

with c1:
    query = st.text_input(
        "search", 
        value=st.session_state["search_input"],
        placeholder="성함, 부서, 업무 검색...",
        label_visibility="collapsed",
        key="search_widget"
    )
    st.session_state["search_input"] = query

with c2:
    # "초기화" 대신 "X"로 표시하여 공간 절약
    if st.button("X"):
        st.session_state["search_input"] = ""
        st.rerun()

# 5. 리스트 출력
SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"

try:
    df = load_data(SHEET_URL)
    search_term = st.session_state["search_input"].lower()

    for _, row in df.iterrows():
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

        if search_term and search_term not in f"{name}{dept}{work}{pos}".lower():
            continue

        # 전화번호 정제 (T, M 링크)
        t_num = ext.replace("-", "").replace(" ", "").strip()
        m_num = mobile.replace("-", "").replace(" ", "").strip()

        # 내선번호가 숫자만 있는 경우 02-3147 등을 붙여야 한다면 여기서 처리 가능
        # 현재는 시트의 번호 그대로 tel: 링크 생성
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
    st.info("데이터 로딩 중...")
