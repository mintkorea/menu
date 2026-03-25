import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일: 검색창과 버튼을 '진짜 하나'처럼 결합
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }

    /* 검색창 컨테이너 (버튼의 기준점) */
    .search-outer {
        position: relative;
        display: flex;
        align-items: center;
        width: 100%;
    }

    /* 입력창 디자인: 둥글고 우측에 버튼 공간 확보 */
    div[data-testid="stTextInput"] { width: 100% !important; }
    div[data-testid="stTextInput"] input {
        border-radius: 25px !important;
        padding-right: 45px !important;
        height: 45px !important;
        border: 1px solid #ddd !important;
        background-color: #f8f9fa !important;
    }

    /* X 버튼 위치: 입력창 안쪽 우측 끝으로 강제 고정 */
    div.clear-button-inner {
        position: absolute;
        right: 12px;
        top: 50%;
        transform: translateY(-50%);
        z-index: 1000;
    }

    /* Streamlit 버튼을 아이콘처럼 투명하게 디자인 */
    div.clear-button-inner button {
        background: transparent !important;
        border: none !important;
        color: #888 !important;
        font-size: 20px !important;
        padding: 0 !important;
        margin: 0 !important;
        width: 30px !important;
        height: 30px !important;
        box-shadow: none !important;
    }
    div.clear-button-inner button:hover { color: #333 !important; }

    /* 연락처 카드 및 아이콘 스타일 */
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
    .name-text { font-weight: 700; font-size: 1.05rem; }
    .pos-dept { font-size: 0.85rem; color: #666; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 3px; }
    .icon-link { text-decoration: none !important; font-size: 1.25rem; font-weight: 800; color: #007bff !important; margin-left: 15px; }
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

# 4. 세션 상태 관리 (깜빡임 방지의 핵심)
if "search_input" not in st.session_state:
    st.session_state.search_input = ""

def handle_clear():
    st.session_state.search_input = ""
    st.session_state["search_widget"] = "" # 위젯 값 직접 초기화

# 5. 검색창 레이아웃
# 검색창과 버튼을 감싸는 div
st.markdown('<div class="search-outer">', unsafe_allow_html=True)

st.text_input(
    "search",
    value=st.session_state.search_input,
    placeholder="🔍 성함, 부서, 업무 검색",
    label_visibility="collapsed",
    key="search_widget"
)
st.session_state.search_input = st.session_state["search_widget"]

# X 버튼 (위젯을 쓰되 CSS로 위치를 검색창 안으로 삽입)
with st.container():
    st.markdown('<div class="clear-button-inner">', unsafe_allow_html=True)
    st.button("✕", on_click=handle_clear, key="clear_trigger")
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

        t_clean = ext.replace("-", "").strip()
        m_clean = mobile.replace("-", "").strip()
        t_html = f'<a href="tel:{t_clean}" class="icon-link">T</a>' if t_clean else ""
        m_html = f'<a href="tel:{m_clean}" class="icon-link">M</a>' if m_clean else ""
        sep = " · " if pos and dept else ""
        
        st.markdown(f"""
            <div class="contact-card">
                <div>
                    <div style="display: flex; align-items: baseline; gap: 6px;">
                        <span class="name-text">{name}</span>
                        <span class="pos-dept">{pos}{sep}{dept}</span>
                    </div>
                    <div class="work-text">{"- "+work if work.strip() else ""}</div>
                </div>
                <div style="display:flex;">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
