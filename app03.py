import streamlit as st
import pandas as pd

# 1. 페이지 설정 (모든 여백 제거)
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 강력한 CSS 스타일 (Streamlit 기본 패딩 강제 제거 및 한 줄 고정)
st.markdown("""
<style>
    /* 1. 상단 헤더 및 기본 여백 제거 */
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { 
        padding: 0.5rem 0.8rem !important; 
        max-width: 100% !important;
    }

    /* 2. 검색창 영역 커스텀 디자인 (한 줄 박제) */
    .search-row {
        display: flex;
        align-items: center;
        gap: 8px;
        width: 100%;
        margin-bottom: 15px;
    }

    /* 3. Streamlit 입력창 강제 너비 조절 */
    div[data-testid="stTextInput"] {
        width: 100% !important;
        flex: 1 !important;
    }
    
    /* 4. 초기화 버튼 강제 고정 (절대 안 잘림) */
    .stButton > button {
        width: 45px !important;
        height: 42px !important;
        min-width: 45px !important;
        padding: 0px !important;
        border: 1px solid #ddd !important;
        background-color: #f8f9fa !important;
        font-weight: bold !important;
        font-size: 16px !important;
    }

    /* 5. 연락처 카드 레이아웃 */
    .contact-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0px;
        border-bottom: 1px solid #eee;
        width: 100%;
    }
    .info-section { flex: 1; min-width: 0; padding-right: 5px; }
    .name-row { display: flex; align-items: baseline; gap: 6px; overflow: hidden; }
    .name-text { font-weight: 700; font-size: 1.1rem; white-space: nowrap; }
    .pos-dept { font-size: 0.85rem; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 4px; line-height: 1.3; }
    
    /* 6. 아이콘 섹션 (T, M 버튼) */
    .icon-section { 
        display: flex; 
        gap: 12px; 
        flex-shrink: 0; 
        justify-content: flex-end;
        margin-left: 10px;
    }
    .icon-link { 
        text-decoration: none !important; 
        font-size: 1.3rem; 
        font-weight: 800; 
        color: #007bff !important;
        width: 25px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 3. 세션 상태 및 데이터 로드
if "search_input" not in st.session_state:
    st.session_state["search_input"] = ""

@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    try:
        df = pd.read_csv(csv_url)
        return df.fillna('')
    except:
        return pd.DataFrame()

# 4. 타이틀 및 검색바 (커스텀 컨테이너 활용)
st.markdown('<div style="font-size: 1.6rem; font-weight: 800; text-align: center; margin-bottom: 15px;">비상연락망</div>', unsafe_allow_html=True)

# 검색창과 버튼을 나란히 배치하기 위해 수동으로 처리
# Streamlit의 columns가 모바일에서 쪼개지는 것을 방지하기 위해 CSS에서 flex-direction 강제함
col_search, col_btn = st.columns([0.86, 0.14])

with col_search:
    st.text_input(
        "search", 
        value=st.session_state["search_input"],
        placeholder="이름, 부서, 업무 검색...",
        label_visibility="collapsed",
        key="search_widget"
    )
    # 위젯 값을 세션 상태에 저장
    st.session_state["search_input"] = st.session_state["search_widget"]

with col_btn:
    # 이 컬럼이 아래로 떨어지지 않도록 CSS에서 제어됨
    st.markdown("""
        <style>
        [data-testid="stHorizontalBlock"] {
            display: flex !important;
            flex-direction: row !important;
            flex-wrap: nowrap !important;
            align-items: center !important;
        }
        [data-testid="column"]:nth-child(2) {
            margin-left: auto !important;
        }
        </style>
    """, unsafe_allow_html=True)
    
    if st.button("X"):
        st.session_state["search_input"] = ""
        st.rerun()

# 5. 데이터 렌더링
SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

if not df.empty:
    search_term = st.session_state["search_input"].lower()

    for _, row in df.iterrows():
        name, dept, pos = str(row.get('성명','')), str(row.get('부서','')), str(row.get('직함',''))
        ext, mobile, work = str(row.get('내선','')), str(row.get('휴대폰','')), str(row.get('담당업무',''))

        if search_term and search_term not in f"{name}{dept}{work}{pos}".lower():
            continue

        # 전화 링크 생성
        t_num = ext.replace("-", "").replace(" ", "").strip()
        m_num = mobile.replace("-", "").replace(" ", "").strip()
        
        t_html = f'<a href="tel:{t_num}" class="icon-link">T</a>' if t_num else ""
        m_html = f'<a href="tel:{m_num}" class="icon-link">M</a>' if m_num else ""
        sep = " · " if pos and dept else ""
        
        card_html = f"""
            <div class="contact-card">
                <div class="info-section">
                    <div class="name-row">
                        <span class="name-text">{name}</span>
                        <span class="pos-dept">{pos}{sep}{dept}</span>
                    </div>
                    {"<div class='work-text'>- "+work+"</div>" if work.strip() else ""}
                </div>
                <div class="icon-section">{t_html}{m_html}</div>
            </div>
        """
        st.markdown(card_html, unsafe_allow_html=True)
else:
    st.info("시트 데이터를 불러오고 있습니다...")
