import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (모바일 최적화)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }

    /* 검색창 디자인 */
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
        height: 45px !important;
        border: 1px solid #ddd !important;
    }

    /* 버튼 영역 가로 배치 고정 */
    [data-testid="column"] { width: 100% !important; }
    
    /* 버튼 스타일 */
    .stButton > button {
        width: 100% !important;
        height: 45px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
    }

    /* 검색 버튼 (파랑) */
    div[data-testid="column"]:nth-child(1) button {
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
    }

    /* 초기화 버튼 (연회색) */
    div[data-testid="column"]:nth-child(2) button {
        background-color: #f0f2f6 !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
    }

    /* 리스트 카드 스타일 */
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
    .name-text { font-weight: 700; font-size: 1.1rem; }
    .pos-dept { font-size: 0.85rem; color: #666; margin-left: 5px; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 4px; }
    .icon-link { text-decoration: none !important; font-size: 1.35rem; font-weight: 800; color: #007bff !important; margin-left: 15px; }
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

# 4. 초기화 함수 (핵심!)
def reset_all():
    # 1. 필터링용 세션 상태 비우기
    st.session_state["search_word"] = ""
    # 2. 위젯(st.text_input)의 내부 값 강제 비우기
    st.session_state["my_input_widget"] = ""

# 5. 세션 상태 초기화
if "search_word" not in st.session_state:
    st.session_state["search_word"] = ""

# 6. 검색창 및 버튼 레이아웃
# 검색어 입력 (key를 지정해야 강제 초기화가 가능합니다)
query = st.text_input(
    "search",
    placeholder="🔍 이름, 부서, 업무 검색",
    label_visibility="collapsed",
    key="my_input_widget"
)

# 버튼 가로 배치 (모바일에서 한 줄로 나옴)
col1, col2 = st.columns(2)

with col1:
    if st.button("검색"):
        st.session_state["search_word"] = query

with col2:
    # on_click을 사용하여 페이지가 그려지기 전에 세션을 먼저 비웁니다.
    st.button("초기화", on_click=reset_all)

# 7. 리스트 출력
if not df.empty:
    term = st.session_state["search_word"].lower()
    
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
        
