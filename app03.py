import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (한 줄 고정 및 디자인)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding-top: 1rem !important; }
    
    /* 컬럼 내부 요소들을 한 줄로 강제 정렬 */
    [data-testid="column"] {
        display: flex !important;
        flex-direction: row !important;
        align-items: center !important;
        gap: 5px !important;
    }
    
    /* 검색창 너비 최대화 */
    .stTextInput { width: 100% !important; }
    
    /* 버튼 스타일: 테두리 강조 및 높이 맞춤 */
    .stButton > button {
        height: 42px !important;
        width: 60px !important;
        padding: 0px !important;
        border-radius: 5px !important;
        border: 1px solid #ccc !important;
        background-color: #f8f9fa !important;
        color: #333 !important;
        font-weight: 600 !important;
    }

    .main-title { font-size: 1.5rem; font-weight: 800; text-align: center; margin-bottom: 15px; }
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0px; border-bottom: 1px solid #eeeeee; }
    .name-text { font-weight: 700; font-size: 1.05rem; color: #000; }
    .pos-dept { font-size: 0.85rem; color: #555; }
    .work-text { font-size: 0.8rem; color: #777; margin-top: 3px; line-height: 1.3; }
    .icon-section { min-width: 55px; display: flex; justify-content: flex-end; gap: 10px; }
    .icon-link { text-decoration: none !important; font-size: 1.2rem; font-weight: 800; color: #007bff !important; width: 25px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드 함수
@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

# 4. 검색창 제어 로직
# 검색창의 key를 "search_input"으로 설정하여 session_state에서 직접 제어합니다.
if "search_input" not in st.session_state:
    st.session_state["search_input"] = ""

def handle_clear():
    # 버튼 클릭 시 세션 상태의 값을 직접 빈 문자열로 교체
    st.session_state["search_input"] = ""

# 5. 검색 레이아웃 (비율 조정)
c1, c2 = st.columns([85, 15]) # 버튼 영역을 조금 더 좁게 설정

with c1:
    # key를 지정하면 st.session_state["search_input"]과 동기화됩니다.
    query = st.text_input(
        "검색",
        placeholder="성함, 부서, 업무 검색...",
        label_visibility="collapsed",
        key="search_input"
    )

with c2:
    # on_click에서 세션 상태를 직접 변경합니다.
    st.button("취소", on_click=handle_clear)

# 6. 리스트 출력
SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"

try:
    df = load_data(SHEET_URL)
    
    # 검색어 정규화
    search_term = st.session_state["search_input"].lower()

    for _, row in df.iterrows():
        name = str(row.get('성명', ''))
        dept = str(row.get('부서', ''))
        pos = str(row.get('직함', ''))
        ext = str(row.get('내선', ''))
        mobile = str(row.get('휴대폰', ''))
        work = str(row.get('담당업무', ''))

        # 필터링 로직
        if search_term and search_term not in f"{name}{dept}{work}{pos}".lower():
            continue

        # 전화번호 기호 제거
        clean_ext = ext.replace("-", "").replace(" ", "")
        clean_mobile = mobile.replace("-", "").replace(" ", "")

        t_html = f'<a href="tel:{clean_ext}" class="icon-link">T</a>' if clean_ext else ""
        m_html = f'<a href="tel:{clean_mobile}" class="icon-link">M</a>' if clean_mobile else ""
        sep = " · " if pos and dept else ""
        
        card_html = (
            f'<div class="contact-card">'
            f'<div class="info-section">'
            f'<div class="name-row"><span class="name-text">{name}</span><span class="pos-dept">{pos}{sep}{dept}</span></div>'
            f'{"<div class='work-text'>- "+work+"</div>" if work else ""}'
            f'</div>'
            f'<div class="icon-section">{t_html}{m_html}</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

except Exception as e:
    st.error("데이터 로드 중 오류가 발생했습니다.")
