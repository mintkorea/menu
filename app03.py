import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (검색창 디자인의 끝판왕)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 2rem 1.2rem !important; }
    
    /* 🏆 타이틀 중앙 & 세련된 폰트 */
    .centered-title {
        font-size: 1.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 25px;
        color: #1c1c1e;
        letter-spacing: -1px;
    }

    /* 🔍 검색창 컨테이너 */
    div[data-testid="stTextInput"] {
        max-width: 450px;
        margin: 0 auto !important;
    }
    
    /* 검색창 입력칸 상세 디자인 */
    div[data-testid="stTextInput"] input {
        border-radius: 25px !important; /* 완전한 라운드 */
        height: 52px !important;
        border: 1px solid #efefef !important;
        background-color: #ffffff !important;
        font-size: 16px !important;
        text-align: center;
        /* 은은한 그림자 효과 */
        box-shadow: 0 4px 12px rgba(0,0,0,0.05) !important;
        transition: all 0.3s ease;
    }

    /* 클릭 시 검색창이 살짝 떠오르는 느낌 */
    div[data-testid="stTextInput"] input:focus {
        border-color: #007bff !important;
        box-shadow: 0 6px 15px rgba(0,123,255,0.15) !important;
        transform: translateY(-1px);
    }

    /* 리스트 디자인 가독성 업그레이드 */
    .contact-card { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 16px 8px; 
        border-bottom: 1px solid #f2f2f7; 
        max-width: 550px;
        margin: 0 auto;
    }
    
    .name-info { display: flex; flex-direction: column; }
    .name-text { font-weight: 700; font-size: 1.15rem; color: #1c1c1e; }
    .pos-dept { font-size: 0.88rem; color: #8e8e93; margin-top: 2px; }
    .work-text { font-size: 0.82rem; color: #a1a1a6; margin-top: 5px; font-weight: 400; }

    /* 통화 버튼 디자인 */
    .icon-box { display: flex; gap: 10px; }
    .icon-link { 
        text-decoration: none !important; 
        font-size: 1.2rem; 
        font-weight: 800; 
        color: #007bff !important;
        width: 44px;
        height: 44px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f0f7ff;
        border-radius: 14px; /* 사각형 라운드 */
        transition: background 0.2s;
    }
    .icon-link:active { background: #e0efff; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="centered-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

# 4. 고품격 검색창
term = st.text_input(
    "search", 
    placeholder="🔍 누구를 찾으시나요?", 
    label_visibility="collapsed"
).lower()

st.markdown('<div style="margin-bottom:15px;"></div>', unsafe_allow_html=True)

# 5. 리스트 출력
if not df.empty:
    for _, row in df.iterrows():
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

        if term and term not in f"{name}{dept}{work}{pos}".lower():
            continue

        t_clean = ext.replace("-", "").strip()
        m_clean = mobile.replace("-", "").strip()
        t_html = f'<a href="tel:{t_clean}" class="icon-link">내선</a>' if t_clean else ""
        m_html = f'<a href="tel:{m_clean}" class="icon-link">폰</a>' if m_clean else ""
        sep = " | " if pos and dept else ""
        
        st.markdown(f"""
            <div class="contact-card">
                <div class="name-info">
                    <div>
                        <span class="name-text">{name}</span>
                        <span class="pos-dept">{pos}{sep}{dept}</span>
                    </div>
                    <div class="work-text">{work}</div>
                </div>
                <div class="icon-box">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
