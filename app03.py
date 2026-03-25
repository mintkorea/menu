import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (모든 여백 제거 및 검색창 디자인)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }
    
    /* 검색창 디자인 */
    div[data-testid="stTextInput"] input {
        border-radius: 30px !important;
        padding-right: 40px !important;
        height: 45px !important;
        border: 1px solid #ddd !important;
    }

    /* 텍스트 형태의 X 버튼 (위젯 아님) */
    .custom-clear-btn {
        position: absolute;
        right: 15px;
        top: 10px;
        font-size: 20px;
        color: #ccc;
        cursor: pointer;
        z-index: 1000;
        font-weight: bold;
        text-decoration: none;
    }
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

# 4. 검색창 및 초기화 링크 (HTML Link 방식)
# 버튼 대신 하이퍼링크를 버튼처럼 보이게 하여 줄바꿈을 방지합니다.
search_area = st.container()
with search_area:
    # 검색어 입력 (Key를 활용)
    search_term = st.text_input(
        "search", 
        placeholder="🔍 성함, 부서, 업무 검색", 
        label_visibility="collapsed",
        key="search_key"
    )

    # 링크 형식을 버튼처럼 위치시킴 (X 버튼 역할)
    # 클릭 시 URL 파라미터를 비우거나 페이지를 새로고침하는 효과
    st.markdown(
        f'<div style="position: relative; width: 100%; margin-top: -42px;">'
        f'<a href="/" target="_self" class="custom-clear-btn">✕</a>'
        f'</div>', 
        unsafe_allow_html=True
    )
    # 간격 조절용
    st.markdown('<div style="margin-bottom: 25px;"></div>', unsafe_allow_html=True)

# 5. 리스트 출력
if not df.empty:
    term = search_term.lower() if search_term else ""
    
    for _, row in df.iterrows():
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

        if term and term not in f"{name}{dept}{work}{pos}".lower():
            continue

        t_clean = ext.replace("-", "").strip()
        m_clean = mobile.replace("-", "").strip()
        t_html = f'<a href="tel:{t_clean}" style="text-decoration:none; font-size:1.3rem; font-weight:800; color:#007bff; margin-right:15px;">T</a>' if t_clean else ""
        m_html = f'<a href="tel:{m_clean}" style="text-decoration:none; font-size:1.3rem; font-weight:800; color:#007bff;">M</a>' if m_clean else ""
        sep = " · " if pos and dept else ""
        
        st.markdown(f"""
            <div style="display: flex; justify-content: space-between; align-items: center; padding: 12px 0; border-bottom: 1px solid #eee;">
                <div>
                    <div style="display: flex; align-items: baseline; gap: 6px;">
                        <span style="font-weight: 700; font-size: 1.05rem;">{name}</span>
                        <span style="font-size: 0.85rem; color: #666;">{pos}{sep}{dept}</span>
                    </div>
                    <div style="font-size: 0.82rem; color: #888; margin-top: 3px;">{"- "+work if work.strip() else ""}</div>
                </div>
                <div style="flex-shrink: 0; display: flex;">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
