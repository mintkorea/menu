import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (타이틀 중앙 및 검색창 최적화)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 2rem 1rem !important; }
    
    /* 🏆 타이틀 중앙 정렬 */
    .centered-title {
        font-size: 1.8rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 25px;
        color: #1c1c1e;
        letter-spacing: -1px;
    }

    /* 🔍 검색창 디자인 (중앙 집중형) */
    div[data-testid="stTextInput"] {
        max-width: 500px;
        margin: 0 auto !important; /* 검색창 자체를 중앙으로 */
    }
    
    div[data-testid="stTextInput"] input {
        border-radius: 15px !important;
        height: 50px !important;
        border: 1px solid #ddd !important;
        background-color: #f2f2f7 !important;
        font-size: 16px !important;
        text-align: center; /* 입력 텍스트도 중앙 정렬 (선택 사항) */
    }

    /* 연락처 카드 */
    .contact-card { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 15px 0; 
        border-bottom: 1px solid #f0f0f0; 
        max-width: 600px;
        margin: 0 auto; /* 리스트도 중앙 정렬 느낌으로 */
    }
    
    .name-text { font-weight: 700; font-size: 1.15rem; color: #1c1c1e; }
    .pos-dept { font-size: 0.9rem; color: #8e8e93; margin-left: 6px; }
    .work-text { font-size: 0.85rem; color: #636366; margin-top: 6px; }

    /* 아이콘 버튼 */
    .icon-box { display: flex; gap: 10px; }
    .icon-link { 
        text-decoration: none !important; 
        font-size: 1.3rem; 
        font-weight: 800; 
        color: #007bff !important;
        width: 42px;
        height: 42px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f0f7ff;
        border-radius: 50%;
    }
</style>
""", unsafe_allow_html=True)

# 중앙 타이틀 출력
st.markdown('<div class="centered-title">성의교정 비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    try:
        return pd.read_csv(csv_url).fillna('')
    except:
        return pd.DataFrame()

SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

# 4. 검색창 (중앙 정렬됨)
term = st.text_input(
    "search", 
    placeholder="🔍 성함 또는 부서 검색", 
    label_visibility="collapsed"
).lower()

st.markdown('<div style="margin-bottom:20px;"></div>', unsafe_allow_html=True)

# 5. 리스트 출력
if not df.empty:
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
                <div class="icon-box">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("데이터를 불러오는 중입니다...")
