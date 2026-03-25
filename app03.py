import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (현대적인 검색바 디자인)
st.markdown("""
<style>
    /* 헤더 제거 및 여백 조정 */
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1.5rem 1rem !important; }
    
    /* 🔍 검색창 입력칸 디자인 */
    div[data-testid="stTextInput"] input {
        border-radius: 12px !important; /* 부드러운 라운드 */
        height: 48px !important;
        border: 1.5px solid #eaeaea !important;
        background-color: #f2f2f7 !important; /* iOS 스타일 배경색 */
        font-size: 16px !important;
        padding-left: 15px !important;
        transition: all 0.2s ease-in-out;
    }

    /* 클릭(포커스) 시 디자인 */
    div[data-testid="stTextInput"] input:focus {
        border-color: #007bff !important;
        background-color: #ffffff !important;
        box-shadow: 0 0 0 3px rgba(0,123,255,0.1) !important;
    }

    /* 연락처 카드 디자인 */
    .contact-card { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 15px 5px; 
        border-bottom: 1px solid #f0f0f0; 
    }
    .name-text { font-weight: 700; font-size: 1.15rem; color: #1c1c1e; }
    .pos-dept { font-size: 0.88rem; color: #8e8e93; margin-left: 6px; }
    .work-text { font-size: 0.85rem; color: #636366; margin-top: 6px; line-height: 1.4; }
    
    /* T/M 아이콘 링크 */
    .icon-box { display: flex; gap: 12px; }
    .icon-link { 
        text-decoration: none !important; 
        font-size: 1.4rem; 
        font-weight: 800; 
        color: #007bff !important;
        width: 40px;
        height: 40px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: #f0f7ff;
        border-radius: 50%;
    }
</style>
""", unsafe_allow_html=True)

# 타이틀
st.markdown('<div style="font-size:1.7rem; font-weight:800; letter-spacing:-0.5px; margin-bottom:20px;">연락처 검색</div>', unsafe_allow_html=True)

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

# 4. 검색창 (버튼 없이 심플하게)
term = st.text_input(
    "search", 
    placeholder="🔍 성함, 부서, 업무로 찾기", 
    label_visibility="collapsed"
).lower()

# 5. 리스트 출력
if not df.empty:
    filtered_df = df.copy()
    if term:
        # 이름, 부서, 업무, 직함에서 모두 검색
        mask = df.apply(lambda row: term in f"{row['성명']}{row['부서']}{row['담당업무']}{row['직함']}".lower(), axis=1)
        filtered_df = df[mask]

    for _, row in filtered_df.iterrows():
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

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
