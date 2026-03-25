import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (모바일 최적화 및 검색창 디자인)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }
    
    /* 검색창을 둥글게 만들고 돋보기 아이콘 느낌 부여 */
    div[data-testid="stSelectbox"] div[data-baseweb="select"] {
        border-radius: 25px !important;
        height: 45px !important;
    }
    
    /* 연락처 카드 디자인 */
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0px; border-bottom: 1px solid #eee; width: 100%; }
    .name-text { font-weight: 700; font-size: 1.1rem; }
    .pos-dept { font-size: 0.85rem; color: #666; margin-left: 4px; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 4px; line-height: 1.3; }
    .icon-link { text-decoration: none !important; font-size: 1.3rem; font-weight: 800; color: #007bff !important; margin-left: 15px; }
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

# 4. 검색창 구현 (X 버튼이 내장된 selectbox 활용)
# 사용자가 직접 입력할 수 있도록 검색 기능을 활성화한 selectbox입니다.
if not df.empty:
    # 검색 후보군 (성함 위주로 보여주되, 실제 검색은 전체 필드 대상)
    options = [""] + sorted(df['성명'].unique().tolist())
    
    search_query = st.selectbox(
        "검색",
        options=options,
        index=0,
        placeholder="🔍 성함, 부서, 업무 검색...",
        label_visibility="collapsed"
    )

    # 5. 리스트 출력
    term = search_query.lower() if search_query else ""
    
    for _, row in df.iterrows():
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

        # 검색 로직: 이름뿐만 아니라 부서, 업무로도 검색 가능하게 설정
        if term and term not in f"{name}{dept}{work}{pos}".lower():
            continue

        t_num = ext.replace("-", "").strip()
        m_num = mobile.replace("-", "").strip()
        t_html = f'<a href="tel:{t_num}" class="icon-link">T</a>' if t_num else ""
        m_html = f'<a href="tel:{m_num}" class="icon-link">M</a>' if m_num else ""
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
else:
    st.info("데이터를 불러오는 중입니다...")
