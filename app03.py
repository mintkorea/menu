import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (검색창과 버튼을 강제로 한 줄에 묶음)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding-top: 1rem !important; }

    /* 검색바 컨테이너: 절대 줄바꿈 금지 */
    .search-container {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 20px;
        width: 100%;
    }
    
    /* Streamlit 입력창 내부 여백 제거 */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stTextInput"]) {
        flex: 1; /* 검색창이 남은 공간 다 차지 */
    }

    .main-title { font-size: 1.5rem; font-weight: 800; text-align: center; margin-bottom: 15px; }
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0px; border-bottom: 1px solid #eeeeee; }
    .name-text { font-weight: 700; font-size: 1.05rem; }
    .pos-dept { font-size: 0.85rem; color: #555; }
    .work-text { font-size: 0.8rem; color: #777; margin-top: 3px; line-height: 1.3; }
    .icon-section { min-width: 55px; display: flex; justify-content: flex-end; gap: 10px; }
    .icon-link { text-decoration: none !important; font-size: 1.2rem; font-weight: 800; color: #007bff !important; }
    
    /* 초기화 버튼 전용 스타일 */
    .clear-btn {
        height: 42px;
        padding: 0 15px;
        background-color: #eee;
        border: none;
        border-radius: 4px;
        font-weight: bold;
        cursor: pointer;
        white-space: nowrap;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드 및 세션 상태 관리
if "search_input" not in st.session_state:
    st.session_state["search_input"] = ""

def clear_text():
    st.session_state["search_input"] = ""

@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

# 4. 검색 영역 (강제 한 줄 레이아웃)
# st.columns 대신 직접 레이아웃을 구성하기 위해 container 사용
search_col, btn_col = st.columns([0.85, 0.15])

with search_col:
    query = st.text_input(
        "검색",
        value=st.session_state["search_input"],
        placeholder="성함, 부서, 업무 검색...",
        label_visibility="collapsed",
        key="search_input_widget"
    )
    # 텍스트 입력 시 세션 상태 업데이트
    st.session_state["search_input"] = query

with btn_col:
    # 좁은 화면에서 버튼이 아래로 떨어지는 것을 방지하기 위해 
    # CSS에서 [data-testid="column"]을 강제 가로 정렬함
    st.markdown("""
        <style>
        [data-testid="column"]:nth-child(1) { flex: 85% !important; min-width: 0px !important; }
        [data-testid="column"]:nth-child(2) { flex: 15% !important; min-width: 60px !important; }
        [data-testid="stHorizontalBlock"] { display: flex !important; flex-wrap: nowrap !important; align-items: center !important; }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("X"):
        st.session_state["search_input"] = ""
        # 텍스트 입력 위젯도 초기화하기 위해 rerun
        st.rerun()

# 5. 리스트 출력
SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"

try:
    df = load_data(SHEET_URL)
    search_term = st.session_state["search_input"].lower()

    for _, row in df.iterrows():
        name, dept, pos, ext, mobile, work = row['성명'], row['부서'], row['직함'], str(row['내선']), str(row['휴대폰']), row['담당업무']

        if search_term and search_term not in f"{name}{dept}{work}{pos}".lower():
            continue

        clean_ext = ext.replace("-", "").replace(" ", "")
        clean_mobile = mobile.replace("-", "").replace(" ", "")

        t_html = f'<a href="tel:{clean_ext}" class="icon-link">T</a>' if clean_ext else ""
        m_html = f'<a href="tel:{clean_mobile}" class="icon-link">M</a>' if clean_mobile else ""
        sep = " · " if pos and dept else ""
        
        st.markdown(f"""
            <div class="contact-card">
                <div class="info-section">
                    <div class="name-row"><span class="name-text">{name}</span><span class="pos-dept">{pos}{sep}{dept}</span></div>
                    <div class="work-text">{"- "+work if work else ""}</div>
                </div>
                <div class="icon-section">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
except Exception as e:
    st.error("데이터 로딩 중...")
