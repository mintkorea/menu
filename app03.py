import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 최소한의 레이아웃 교정 (제목 중앙 및 간격만 유지)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 2rem 1rem !important; }
    
    /* 타이틀만 중앙 정렬 */
    .title-text {
        font-size: 1.6rem;
        font-weight: 800;
        text-align: center;
        margin-bottom: 20px;
    }

    /* 연락처 리스트 디자인 (순정 느낌 유지) */
    .contact-card { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 12px 0; 
        border-bottom: 1px solid #eee; 
    }
    .name-text { font-weight: 700; font-size: 1.1rem; }
    .pos-dept { font-size: 0.85rem; color: #666; margin-left: 5px; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 3px; }

    /* 통화 링크 아이콘 */
    .icon-box { display: flex; gap: 15px; }
    .icon-link { 
        text-decoration: none !important; 
        font-size: 1.3rem; 
        font-weight: 800; 
        color: #007bff !important;
    }
</style>
""", unsafe_allow_html=True)

# 중앙 타이틀
st.markdown('<div class="title-text">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

# 4. 순정 검색창 (st.text_input 기본값 사용)
term = st.text_input(
    label="검색어 입력", 
    placeholder="성함, 부서, 업무 등을 입력하세요", 
    label_visibility="collapsed"
).lower()

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
                    <div>
                        <span class="name-text">{name}</span>
                        <span class="pos-dept">{pos}{sep}{dept}</span>
                    </div>
                    <div class="work-text">{work}</div>
                </div>
                <div class="icon-box">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
