import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding-top: 1rem !important; }
    .main-title { font-size: 1.6rem; font-weight: 800; text-align: center; margin-bottom: 15px; }
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 10px 0px; border-bottom: 1px solid #eeeeee; width: 100%; }
    .info-section { flex: 1; min-width: 0; padding-right: 10px; }
    .name-row { display: flex; align-items: baseline; gap: 6px; }
    .name-text { font-weight: 700; font-size: 1.05rem; color: #000; white-space: nowrap; }
    .pos-dept { font-size: 0.85rem; color: #555; white-space: nowrap; }
    .work-text { font-size: 0.8rem; color: #777; margin-top: 3px; line-height: 1.3; word-break: keep-all; }
    .icon-section { min-width: 55px; display: flex; justify-content: flex-end; gap: 8px; flex-shrink: 0; }
    .icon-link { text-decoration: none !important; font-size: 1.15rem; font-weight: 800; color: #007bff !important; width: 24px; text-align: center; }
    
    /* 버튼 스타일 조정 */
    .stButton > button { width: 100%; height: 42px; background-color: #f0f2f6; border: none; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 구글 시트 데이터 로드 함수
@st.cache_data(ttl=60) # 테스트를 위해 1분으로 설정 (상용 시 600 권장)
def load_data(sheets_url):
    csv_url = sheets_url.replace('/edit?usp=sharing', '/export?format=csv')
    try:
        df = pd.read_csv(csv_url)
        return df.fillna('')
    except:
        return pd.DataFrame()

# 4. 세션 상태 초기화 (검색어 저장용)
if 'search_query' not in st.session_state:
    st.session_state.search_query = ""

def clear_search():
    st.session_state.search_query = ""

# 5. 검색창 레이아웃 (검색창 + 초기화 버튼)
col1, col2 = st.columns([6, 1])
with col1:
    query = st.text_input(
        "search", 
        value=st.session_state.search_query,
        placeholder="성함, 부서 또는 업무 검색...", 
        label_visibility="collapsed",
        key="search_input"
    )
    # 입력값이 바뀔 때마다 세션 상태 업데이트
    st.session_state.search_query = query

with col2:
    if st.button("취소", on_click=clear_search):
        # 버튼 클릭 시 clear_search 함수 실행 후 리런
        st.rerun()

# 6. 데이터 출력
SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

if not df.empty:
    for _, row in df.iterrows():
        # 시트 컬럼명에 맞춰 수정 (실제 시트 헤더 확인 필요)
        name = str(row.get('성명', ''))
        dept = str(row.get('부서', ''))
        pos = str(row.get('직함', ''))
        ext = str(row.get('내선', ''))
        mobile = str(row.get('휴대폰', ''))
        work = str(row.get('담당업무', ''))

        # 검색 필터링
        if st.session_state.search_query:
            q = st.session_state.search_query.lower()
            if q not in f"{name}{dept}{work}{pos}".lower():
                continue

        # 아이콘 생성
        t_html = f'<a href="tel:{ext.replace("-","")}" class="icon-link">T</a>' if ext.strip() else ""
        m_html = f'<a href="tel:{mobile.replace("-","")}" class="icon-link">M</a>' if mobile.strip() else ""
        
        sep = " · " if pos and dept else ""
        work_display = f'<div class="work-text">- {work}</div>' if work else ""

        card_html = (
            f'<div class="contact-card">'
            f'<div class="info-section">'
            f'<div class="name-row"><span class="name-text">{name}</span><span class="pos-dept">{pos}{sep}{dept}</span></div>'
            f'{work_display}'
            f'</div>'
            f'<div class="icon-section">{t_html}{m_html}</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)
else:
    st.warning("데이터를 불러올 수 없습니다. 시트 설정을 확인하세요.")
