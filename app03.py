import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (버튼 증발 방지 및 강제 정렬)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }
    
    /* 검색창 스타일 */
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
        height: 45px !important;
    }

    /* 🔥 버튼 컨테이너: 양옆에 여백을 주어 버튼을 가운데로 모음 */
    div[data-testid="stHorizontalBlock"] {
        padding: 0 15% !important; /* 좌우 15%씩 비워서 가운데로 몰기 */
        gap: 10px !important;
    }

    /* 모바일에서 버튼이 세로로 쌓이는 것 방지 */
    div[data-testid="stHorizontalBlock"] > div {
        flex: 1 1 auto !important;
        min-width: 0 !important;
    }

    /* 버튼 공통 스타일 */
    .stButton > button {
        width: 100% !important;
        height: 42px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        white-space: nowrap !important;
    }

    /* 검색 버튼 (파랑) */
    div[data-testid="column"]:nth-child(1) button {
        background-color: #007bff !important;
        color: white !important;
    }

    /* 초기화 버튼 (회색) */
    div[data-testid="column"]:nth-child(2) button {
        background-color: #f0f2f6 !important;
        color: #333 !important;
    }

    /* 리스트 카드 */
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

# 4. 초기화 함수
def reset_all():
    st.session_state["my_input_widget"] = ""

# 5. 검색 레이아웃
query = st.text_input(
    "search",
    placeholder="🔍 검색 후 엔터 또는 버튼 클릭",
    label_visibility="collapsed",
    key="my_input_widget"
)

# 1:1 비율로 컬럼 생성
col1, col2 = st.columns(2)
with col1:
    if st.button("검색"):
        st.rerun()

with col2:
    st.button("초기화", on_click=reset_all)

# 6. 리스트 출력
if not df.empty:
    term = query.lower()
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
