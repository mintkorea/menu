import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (강력한 위치 고정)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }
    
    /* 검색 영역을 감싸는 전체 박스 */
    .search-wrapper {
        position: relative;
        width: 100%;
        margin-bottom: 20px;
    }

    /* Streamlit 입력창 커스텀: 둥근 모양 + 오른쪽 공간 확보 */
    div[data-testid="stTextInput"] input {
        border-radius: 30px !important;
        padding-right: 45px !important; /* X 버튼이 들어갈 자리 */
        height: 45px !important;
        border: 1px solid #ddd !important;
    }

    /* X 버튼을 입력창 우측 안쪽으로 강제 삽입 */
    div.clear-btn-container {
        position: absolute;
        top: 22px; /* 입력창 높이 절반 */
        right: 15px;
        transform: translateY(-50%);
        z-index: 9999;
    }

    /* 버튼 기본 스타일 제거 (글자만 남김) */
    div.clear-btn-container button {
        background: transparent !important;
        border: none !important;
        color: #999 !important;
        font-size: 20px !important;
        font-weight: bold !important;
        padding: 0 !important;
        cursor: pointer;
        box-shadow: none !important;
    }
    
    div.clear-btn-container button:hover { color: #333 !important; }

    /* 연락처 카드 스타일 */
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0px; border-bottom: 1px solid #eee; width: 100%; }
    .name-text { font-weight: 700; font-size: 1.05rem; }
    .pos-dept { font-size: 0.85rem; color: #666; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 3px; line-height: 1.3; }
    .icon-section { display: flex; gap: 15px; flex-shrink: 0; margin-left: 10px; }
    .icon-link { text-decoration: none !important; font-size: 1.3rem; font-weight: 800; color: #007bff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="font-size:1.6rem; font-weight:800; text-align:center; margin-bottom:15px;">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

# 4. 세션 상태 관리 (검색어 초기화용)
if "search_input" not in st.session_state:
    st.session_state.search_input = ""

def reset_search():
    st.session_state.search_input = ""
    # text_input의 key를 이용해 강제로 초기화
    st.session_state["search_widget"] = ""

# 5. 검색바 구현 (X 버튼 레이어 겹치기)
# CSS 클래스 search-wrapper로 감싸서 위치를 제어합니다.
st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)

st.text_input(
    "search",
    placeholder="🔍 성함, 부서, 업무 검색",
    label_visibility="collapsed",
    key="search_widget"
)
# 위젯 값을 세션에 동기화
st.session_state.search_input = st.session_state["search_widget"]

# X 버튼을 별도의 컨테이너에 담아 CSS로 입력창 위로 올립니다.
with st.container():
    st.markdown('<div class="clear-btn-container">', unsafe_allow_html=True)
    # 검색어가 있을 때만 X 버튼 작동 (눈에는 항상 보이거나 빈 공간 차지)
    if st.button("✕", on_click=reset_search):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

# 6. 리스트 출력
if not df.empty:
    term = st.session_state.search_input.lower()
    
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
                <div class="info-section">
                    <div class="name-row"><span class="name-text">{name}</span><span class="pos-dept">{pos}{sep}{dept}</span></div>
                    {"<div class='work-text'>- "+work+"</div>" if work.strip() else ""}
                </div>
                <div class="icon-section">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
