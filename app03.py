import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (모든 여백 제거 및 강제 가로 정렬)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { 
        padding: 0.5rem 0.5rem !important; 
        max-width: 100vw !important;
        overflow-x: hidden !important;
    }

    /* 검색창과 버튼이 들어있는 블록 강제 제어 */
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important; /* 가로 정렬 강제 */
        flex-wrap: nowrap !important;   /* 줄바꿈 절대 금지 */
        align-items: center !important;
        width: 100% !important;
        gap: 5px !important;
    }

    /* 검색창 컬럼: 남는 공간 다 쓰기 */
    div[data-testid="column"]:nth-child(1) {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    /* 버튼 컬럼: 딱 45px만 차지 */
    div[data-testid="column"]:nth-child(2) {
        flex: 0 0 45px !important;
        min-width: 45px !important;
        max-width: 45px !important;
    }

    /* X 버튼 디자인 */
    .stButton > button {
        width: 42px !important;
        height: 42px !important;
        padding: 0 !important;
        margin: 0 !important;
        font-size: 16px !important;
        font-weight: bold !important;
        border: 1px solid #ddd !important;
        background-color: #f8f9fa !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* 연락처 카드 디자인 */
    .contact-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0px;
        border-bottom: 1px solid #eee;
        width: 100%;
    }
    .info-section { flex: 1; min-width: 0; padding-right: 5px; }
    .name-row { display: flex; align-items: baseline; gap: 5px; }
    .name-text { font-weight: 700; font-size: 1.05rem; white-space: nowrap; }
    .pos-dept { font-size: 0.85rem; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 3px; line-height: 1.3; }
    
    .icon-section { display: flex; gap: 10px; flex-shrink: 0; margin-left: 5px; }
    .icon-link { text-decoration: none !important; font-size: 1.25rem; font-weight: 800; color: #007bff !important; width: 25px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="font-size: 1.5rem; font-weight: 800; text-align: center; margin-bottom: 15px;">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드 및 세션 관리
if "search_input" not in st.session_state:
    st.session_state["search_input"] = ""

@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

# 4. 검색창 레이아웃 (columns를 쓰되 CSS로 성질을 완전히 바꿈)
c1, c2 = st.columns([0.85, 0.15])

with c1:
    # key를 주어 세션 상태와 연동
    st.text_input(
        "search", 
        value=st.session_state["search_input"],
        placeholder="성함, 부서, 업무 검색...",
        label_visibility="collapsed",
        key="search_widget"
    )
    # 입력 시 세션 업데이트
    st.session_state["search_input"] = st.session_state["search_widget"]

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
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

        if search_term and search_term not in f"{name}{dept}{work}{pos}".lower():
            continue

        t_clean = ext.replace("-", "").replace(" ", "").strip()
        m_clean = mobile.replace("-", "").replace(" ", "").strip()

        t_html = f'<a href="tel:{t_clean}" class="icon-link">T</a>' if t_clean else ""
        m_html = f'<a href="tel:{m_clean}" class="icon-link">M</a>' if m_clean else ""
        sep = " · " if pos and dept else ""
        
        st.markdown(f"""
            <div class="contact-card">
                <div class="info-section">
                    <div class="name-row">
                        <span class="name-text">{name}</span>
                        <span class="pos-dept">{pos}{sep}{dept}</span>
                    </div>
                    {"<div class='work-text'>- "+work+"</div>" if work.strip() else ""}
                </div>
                <div class="icon-section">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
except Exception as e:
    st.info("데이터 로딩 중...")
