import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (검색창 내부 X 버튼처럼 보이게 속임수 레이아웃)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }
    
    /* 검색창 컨테이너 */
    .search-container {
        display: flex;
        align-items: center;
        position: relative;
        width: 100%;
        margin-bottom: 20px;
    }
    
    /* 입력창 디자인: 둥근 형태 */
    div[data-testid="stTextInput"] { width: 100% !important; }
    div[data-testid="stTextInput"] input {
        border-radius: 30px !important;
        padding-right: 45px !important; /* X 버튼 자리 */
        height: 45px !important;
        border: 1px solid #ddd !important;
    }

    /* X 버튼을 입력창 안으로 겹치기 (절대 안 잘리게 배치) */
    .clear-btn-pos {
        position: absolute;
        right: 15px;
        top: 22px; /* 입력창 높이의 중간 지점 */
        transform: translateY(-50%);
        z-index: 999;
    }
    
    .clear-btn-pos button {
        background: none !important;
        border: none !important;
        color: #bbb !important;
        font-size: 20px !important;
        font-weight: bold !important;
        cursor: pointer;
    }

    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
    .name-text { font-weight: 700; font-size: 1.05rem; }
    .pos-dept { font-size: 0.85rem; color: #666; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 3px; line-height: 1.3; }
    .icon-section { display: flex; gap: 15px; flex-shrink: 0; }
    .icon-link { text-decoration: none !important; font-size: 1.3rem; font-weight: 800; color: #007bff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="font-size:1.5rem; font-weight:800; text-align:center; margin-bottom:15px;">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

# 4. 세션 상태 관리 (오류 방지 핵심)
if "search_val" not in st.session_state:
    st.session_state.search_val = ""

# 초기화 함수
def clear_search():
    st.session_state.search_val = ""
    st.session_state.my_input = "" # 입력 위젯 초기화

# 5. 검색창 레이아웃 (HTML 겹치기 대신 Streamlit 위젯 조합)
# 컨테이너를 써서 입력을 감쌉니다.
search_area = st.container()
with search_area:
    # 텍스트 입력창
    st.text_input(
        "search", 
        value=st.session_state.search_val, 
        placeholder="🔍 성함, 부서, 업무 검색", 
        label_visibility="collapsed",
        key="my_input"
    )
    st.session_state.search_val = st.session_state.my_input

    # X 버튼을 CSS로 입력창 내부 우측에 강제 배치
    st.markdown('<div class="clear-btn-pos">', unsafe_allow_html=True)
    if st.button("✕", on_click=clear_search):
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

# 6. 리스트 출력 (오류 발생 지점 수정)
if not df.empty:
    # search_val이 None이 아님을 보장
    term = str(st.session_state.search_val).lower()
    
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
