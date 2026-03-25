import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (버튼을 검색창 안으로 강제 견인)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }
    
    /* 검색창 둥글게 디자인 */
    div[data-testid="stTextInput"] input {
        border-radius: 25px !important;
        height: 45px !important;
        padding-right: 45px !important; /* X 버튼이 텍스트 안 가리게 여백 */
        border: 1px solid #ddd !important;
    }

    /* 버튼을 검색창 오른쪽 끝으로 강제 이동 (핵심 레이아웃) */
    div[data-testid="column"]:nth-child(2) {
        display: flex;
        justify-content: center;
        align-items: center;
        margin-left: -55px !important; /* 검색창 안으로 밀어넣기 */
        margin-top: 2px !important;    /* 위아래 중앙 맞춤 */
        z-index: 999 !important;       /* 검색창보다 위에 보이게 */
        min-width: 45px !important;
    }

    /* X 버튼 모양 (글자만 보이게) */
    div[data-testid="column"]:nth-child(2) button {
        background: transparent !important;
        border: none !important;
        color: #aaa !important;
        font-size: 20px !important;
        font-weight: bold !important;
        box-shadow: none !important;
        height: 45px !important;
        width: 45px !important;
    }

    /* 카드 디자인 */
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
    .name-text { font-weight: 700; font-size: 1.1rem; }
    .pos-dept { font-size: 0.85rem; color: #666; margin-left: 5px; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 4px; }
    .icon-link { text-decoration: none !important; font-size: 1.35rem; font-weight: 800; color: #007bff !important; margin-left: 15px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="font-size:1.6rem; font-weight:800; text-align:center; margin-bottom:20px;">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

# 4. 세션 관리
if "search_query" not in st.session_state:
    st.session_state.search_query = ""

# 5. 검색 레이아웃 (columns를 쓰되 CSS로 억지로 겹침)
col1, col2 = st.columns([0.99, 0.01])

with col1:
    search_input = st.text_input(
        "search",
        value=st.session_state.search_query,
        placeholder="🔍 성함, 부서, 업무 검색",
        label_visibility="collapsed",
        key="main_search"
    )
    st.session_state.search_query = search_input

with col2:
    # X 버튼 클릭 시 초기화
    if st.button("✕"):
        st.session_state.search_query = ""
        st.rerun()

# 6. 결과 출력
if not df.empty:
    term = st.session_state.search_query.lower()
    for _, row in df.iterrows():
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

        if term and term not in f"{name}{dept}{work}{pos}".lower():
            continue

        t_clean = ext.replace("-", "").strip()
        m_clean = mobile.replace("-", "").strip()
        t_html = f'<a href="tel:{t_clean}" class="icon-link">T</a>' if t_clean else ""
        m_html = f'<a href="tel:{m_clean}" class="icon-link">M</a>' if m_clean else ""
        sep = " · " if pos and dept else ""
        
        st.markdown(f"""
            <div class="contact-card">
                <div>
                    <div style="display: flex; align-items: baseline;">
                        <span class="name-text">{name}</span>
                        <span class="pos-dept">{pos}{sep}{dept}</span>
                    </div>
                    <div class="work-text">{"- "+work if work.strip() else ""}</div>
                </div>
                <div style="display:flex;">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
