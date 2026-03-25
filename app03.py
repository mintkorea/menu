import streamlit as st
import pandas as pd

# 1. 페이지 설정 (좌우 여백 최소화)
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (잘림 방지 및 모바일 풀 너비 최적화)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    
    /* 전체 컨테이너 여백 최적화 */
    [data-testid="stMainBlockContainer"] {
        padding: 1rem 0.5rem !important; /* 좌우 여백을 0.5rem으로 대폭 축소 */
    }

    /* 검색창과 버튼을 포함한 가로 블록 강제 설정 */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        align-items: center !important;
        gap: 5px !important;
        width: 100% !important;
    }

    /* 첫 번째 컬럼 (검색창): 남은 공간 모두 차지 */
    [data-testid="column"]:nth-child(1) {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    /* 두 번째 컬럼 (X 버튼): 딱 필요한 만큼만 차지 */
    [data-testid="column"]:nth-child(2) {
        flex: 0 0 42px !important;
        min-width: 42px !important;
        max-width: 42px !important;
    }

    /* 입력창 내부 여백 제거 */
    .stTextInput { width: 100% !important; }
    
    /* X 버튼 스타일 최적화 */
    .stButton > button {
        width: 40px !important;
        height: 40px !important;
        padding: 0px !important;
        margin: 0px !important;
        border: 1px solid #ccc !important;
        background-color: #fcfcfc !important;
        display: flex;
        justify-content: center;
        align-items: center;
    }

    /* 연락처 카드 스타일 */
    .contact-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 5px; /* 내부 패딩 살짝 부여 */
        border-bottom: 1px solid #eee;
        width: 100%;
    }
    .info-section { flex: 1; min-width: 0; overflow: hidden; }
    .name-row { display: flex; align-items: baseline; gap: 6px; }
    .name-text { font-weight: 700; font-size: 1.05rem; white-space: nowrap; }
    .pos-dept { font-size: 0.85rem; color: #555; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .work-text { font-size: 0.8rem; color: #777; margin-top: 3px; line-height: 1.3; }
    .icon-section { min-width: 60px; display: flex; justify-content: flex-end; gap: 12px; flex-shrink: 0; }
    .icon-link { text-decoration: none !important; font-size: 1.25rem; font-weight: 800; color: #007bff !important; }
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

# 4. 검색창 레이아웃
c1, c2 = st.columns([0.85, 0.15])

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

        # 번호에서 기호 제거 (전화 걸기용)
        t_clean = ext.replace("-", "").replace(" ", "").strip()
        m_clean = mobile.replace("-", "").replace(" ", "").strip()

        t_html = f'<a href="tel:{t_clean}" class="icon-link">T</a>' if t_clean else ""
        m_html = f'<a href="tel:{m_clean}" class="icon-link">M</a>' if m_clean else ""
        sep = " · " if pos and dept else ""
        
        # HTML 카드 출력
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
    st.info("데이터를 동기화 중입니다...")
