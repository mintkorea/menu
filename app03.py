import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (강력한 가로 배치 고정)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }
    
    /* 검색창 디자인 */
    div[data-testid="stTextInput"] input {
        border-radius: 10px !important;
        height: 45px !important;
    }

    /* 🔥 핵심: columns 레이아웃을 무시하고 가로 정렬 강제 */
    div[data-testid="stHorizontalBlock"] {
        display: grid !important;
        grid-template-columns: 1fr 1fr !important; /* 정확히 50%씩 2열 고정 */
        gap: 10px !important;
        align-items: center !important;
    }

    /* 컬럼 자체의 마진이나 너비 초기화 */
    div[data-testid="column"] {
        width: 100% !important;
        flex: none !important;
    }

    /* 버튼 스타일 통일 */
    .stButton > button {
        width: 100% !important;
        height: 48px !important;
        border-radius: 8px !important;
        font-weight: bold !important;
        font-size: 16px !important;
        white-space: nowrap !important;
        display: block !important;
    }

    /* 검색 버튼 (파란색) */
    div[data-testid="column"]:nth-child(1) button {
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
    }

    /* 초기화 버튼 (흰색 배경) */
    div[data-testid="column"]:nth-child(2) button {
        background-color: #ffffff !important;
        color: #333 !important;
        border: 1px solid #ddd !important;
    }

    /* 리스트 카드 디자인 */
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
    .name-text { font-weight: 700; font-size: 1.1rem; }
    .pos-dept { font-size: 0.85rem; color: #666; margin-left: 5px; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 4px; line-height: 1.4; }
    .icon-link { text-decoration: none !important; font-size: 1.4rem; font-weight: 800; color: #007bff !important; margin-left: 15px; }
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
    st.session_state["search_widget"] = ""

# 5. 검색 레이아웃
query = st.text_input(
    "search",
    placeholder="🔍 검색어 입력 후 엔터",
    label_visibility="collapsed",
    key="search_widget"
)

# 🔥 이 블록이 CSS Grid의 영향을 받아 무조건 1:1 가로 배치가 됩니다.
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
