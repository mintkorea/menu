import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (검색창 내부에 X를 강제 고정)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }

    /* 통합 검색바 컨테이너 */
    .search-wrapper {
        position: relative;
        display: flex;
        align-items: center;
        width: 100%;
        height: 45px;
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 25px;
        padding: 0 15px;
        margin-bottom: 20px;
    }

    /* 실제 입력창: 테두리 없애고 컨테이너에 맞춤 */
    .search-input {
        flex: 1;
        border: none !important;
        background: transparent !important;
        outline: none !important;
        font-size: 16px;
        height: 100%;
        color: #333;
    }

    /* X 버튼: 입력창 우측 끝에 절대 좌표로 고정 */
    .search-clear-btn {
        color: #aaa;
        font-size: 22px;
        font-weight: bold;
        text-decoration: none;
        cursor: pointer;
        padding-left: 10px;
    }
    
    .search-clear-btn:hover { color: #666; }

    /* 리스트 카드 디자인 */
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee; }
    .name-text { font-weight: 700; font-size: 1.05rem; }
    .pos-dept { font-size: 0.85rem; color: #666; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 3px; }
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

# 4. 쿼리 파라미터를 이용한 검색 제어 (깜빡임 최소화)
query_params = st.query_params
current_search = query_params.get("q", "")

# HTML로 구현된 통합 검색바 (X 버튼 포함)
# X를 누르면 URL 파라미터를 날려서 초기화하는 원리입니다.
st.markdown(f"""
    <div class="search-wrapper">
        <form action="/" method="get" style="display:flex; width:100%; align-items:center;">
            <input type="text" name="q" class="search-input" value="{current_search}" placeholder="🔍 성함, 부서, 업무 검색">
            {f'<a href="/" target="_self" class="search-clear-btn">✕</a>' if current_search else ''}
            <input type="submit" style="display:none;">
        </form>
    </div>
""", unsafe_allow_html=True)

# 5. 리스트 출력
if not df.empty:
    term = current_search.lower()
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
                    <div style="display: flex; align-items: baseline; gap: 6px;">
                        <span class="name-text">{name}</span>
                        <span class="pos-dept">{pos}{sep}{dept}</span>
                    </div>
                    <div class="work-text">{"- "+work if work.strip() else ""}</div>
                </div>
                <div style="display:flex;">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
