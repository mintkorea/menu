import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (검색창과 카드 가독성에만 집중)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }
    
    /* 검색창 디자인: 둥글고 깔끔하게 */
    div[data-testid="stTextInput"] input {
        border-radius: 20px !important;
        height: 45px !important;
        border: 1px solid #ddd !important;
        background-color: #f9f9f9 !important;
        font-size: 16px !important;
    }

    /* 연락처 카드 디자인 */
    .contact-card { 
        display: flex; 
        justify-content: space-between; 
        align-items: center; 
        padding: 14px 0; 
        border-bottom: 1px solid #eee; 
    }
    .name-text { font-weight: 700; font-size: 1.1rem; color: #111; }
    .pos-dept { font-size: 0.85rem; color: #666; margin-left: 5px; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 4px; line-height: 1.4; }
    
    /* 전화 아이콘 스타일 */
    .icon-link { 
        text-decoration: none !important; 
        font-size: 1.4rem; 
        font-weight: 800; 
        color: #007bff !important; 
        margin-left: 18px; 
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div style="font-size:1.6rem; font-weight:800; text-align:center; margin-bottom:20px;">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

# 4. 심플 검색창
# 버튼이 없으므로 엔터를 치거나 글자를 입력하면 즉시 반영됩니다.
term = st.text_input(
    "search", 
    placeholder="🔍 성함, 부서, 업무 검색", 
    label_visibility="collapsed"
).lower()

# 5. 리스트 출력
if not df.empty:
    for _, row in df.iterrows():
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

        # 검색 필터링
        if term and term not in f"{name}{dept}{work}{pos}".lower():
            continue

        # 전화번호 링크 생성
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
                <div style="display:flex; align-items:center;">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("데이터를 불러올 수 없습니다.")
