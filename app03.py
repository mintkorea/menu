import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (기본 여백 제거 및 카드 디자인)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }
    .main-title { font-size: 1.5rem; font-weight: 800; text-align: center; margin-bottom: 15px; }
    
    /* 연락처 카드 디자인 */
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0px; border-bottom: 1px solid #eee; width: 100%; }
    .info-section { flex: 1; min-width: 0; }
    .name-row { display: flex; align-items: baseline; gap: 6px; }
    .name-text { font-weight: 700; font-size: 1.05rem; }
    .pos-dept { font-size: 0.85rem; color: #666; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 3px; line-height: 1.3; }
    .icon-section { display: flex; gap: 15px; flex-shrink: 0; margin-left: 10px; }
    .icon-link { text-decoration: none !important; font-size: 1.3rem; font-weight: 800; color: #007bff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드
@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

# 4. HTML/JS 커스텀 검색창 (이 부분이 핵심입니다)
# 검색어 입력을 실시간으로 감지하고 X 버튼을 누르면 즉시 초기화합니다.
if "search_val" not in st.session_state:
    st.session_state.search_val = ""

# 자바스크립트를 이용해 Streamlit의 세션 값을 업데이트하는 컴포넌트
search_html = f"""
<div style="position: relative; width: 100%; font-family: sans-serif;">
    <input type="text" id="search-input" value="{st.session_state.search_val}" 
        placeholder="🔍 성함, 부서, 업무 검색" 
        style="width: 100%; height: 45px; border-radius: 25px; border: 1px solid #ddd; padding: 0 40px 0 20px; font-size: 16px; outline: none; box-sizing: border-box;">
    <div id="clear-btn" style="position: absolute; right: 15px; top: 50%; transform: translateY(-50%); cursor: pointer; color: #ccc; font-weight: bold; font-size: 20px; display: { 'block' if st.session_state.search_val else 'none' };">✕</div>
</div>

<script>
    const input = document.getElementById('search-input');
    const btn = document.getElementById('clear-btn');

    // 입력 감지
    input.addEventListener('input', (e) => {{
        const val = e.target.value;
        btn.style.display = val ? 'block' : 'none';
        // 부모(Streamlit)에게 값 전달
        window.parent.postMessage({{type: 'streamlit:setComponentValue', value: val}}, '*');
    }});

    // X 버튼 클릭
    btn.addEventListener('click', () => {{
        input.value = '';
        btn.style.display = 'none';
        window.parent.postMessage({{type: 'streamlit:setComponentValue', value: ''}}, '*');
    }});
</script>
"""

# HTML 컴포넌트 실행 (높이 60px)
search_query = components.html(search_html, height=60)

# 컴포넌트에서 받은 값을 세션에 저장 (None일 경우 대비)
if search_query is not None:
    st.session_state.search_val = search_query

# 5. 리스트 출력
if not df.empty:
    search_term = st.session_state.search_val.lower()
    
    for _, row in df.iterrows():
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

        if search_term and search_term not in f"{name}{dept}{work}{pos}".lower():
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
