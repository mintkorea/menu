import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (버튼 가로 정렬 및 모바일 최적화)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }

    /* 타이틀 */
    .main-title { font-size: 1.6rem; font-weight: 800; text-align: center; margin-bottom: 15px; }

    /* 검색창 둥글게 */
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
        height: 45px !important;
        border: 1px solid #ddd !important;
    }

    /* 버튼 영역 가로 배치 고정 */
    [data-testid="stHorizontalBlock"] {
        gap: 10px !important;
    }

    /* 버튼 공통 스타일 */
    .stButton > button {
        width: 100% !important;
        height: 42px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }

    /* 검색 버튼 (파란색 강조) */
    div[data-testid="column"]:nth-child(1) button {
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
    }

    /* 취소 버튼 (회색) */
    div[data-testid="column"]:nth-child(2) button {
        background-color: #f0f2f6 !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
    }

    /* 카드 디자인 */
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
    .name-text { font-weight: 700; font-size: 1.1rem; }
    .pos-dept { font-size: 0.85rem; color: #666; margin-left: 5px; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 4px; }
    .icon-link { text-decoration: none !important; font-size: 1.3rem; font-weight: 800; color: #007bff !important; margin-left: 15px; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

# 4. 세션 상태 관리
if "search_word" not in st.session_state:
    st.session_state.search_word = ""

# 5. 검색창 및 하단 버튼 레이아웃
# 검색어 입력 (Enter를 쳐도 검색됨)
query = st.text_input(
    "search",
    value=st.session_state.search_word,
    placeholder="🔍 이름, 부서, 업무를 입력하세요",
    label_visibility="collapsed"
)

# 버튼 두 개를 가로로 배치
col1, col2 = st.columns(2)

with col1:
    if st.button("검색"):
        st.session_state.search_word = query
        # 별도의 로직 없이 rerun으로 필터링 적용

with col2:
    if st.button("초기화"):
        st.session_state.search_word = ""
        st.rerun()

# 6. 리스트 출력
if not df.empty:
    # 버튼을 누르거나 엔터를 쳤을 때의 값을 기준으로 필터링
    term = st.session_state.search_word.lower()
    
    for _, row in df.iterrows():
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

        if term and term not in f"{name}{dept}{work}{pos}".lower():
            continue

        t_num = ext.replace("-", "").strip()
        m_num = mobile.replace("-", "").strip()
        t_html = f'<a href="tel:{t_num}" class="icon-link">T</a>' if t_num else ""
        m_html = f'<a href="tel:{m_num}" class="icon-link">M</a>' if m_num else ""
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
