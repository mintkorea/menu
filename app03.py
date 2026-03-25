import streamlit as st
import pandas as pd

# 1. 페이지 설정 및 모바일 최적화 CSS
st.set_page_config(page_title="성의교정 연락망", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    /* 리스트 행 디자인: 간격 최소화 */
    .contact-card {
        padding: 8px 0;
        border-bottom: 1px solid #f1f1f1;
    }
    .main-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-decoration: none;
        color: inherit !important;
    }
    .name-text { font-size: 1.05rem; font-weight: bold; color: #111; }
    .dept-text { font-size: 0.8rem; color: #666; margin-left: 5px; }
    .work-text { font-size: 0.8rem; color: #888; display: block; margin-top: 2px; }
    .right-info { text-align: right; min-width: 100px; }
    .ext-text { font-size: 0.95rem; font-weight: bold; color: #007bff; }
    .mobile-text { font-size: 0.75rem; color: #aaa; }
    
    /* 별표 버튼 스타일 */
    .stButton > button {
        border: none !important; background: transparent !important;
        padding: 0 !important; color: #ffc107 !important; font-size: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 2. 데이터 로드 (KeyError 방지 로직 포함)
SHEET_ID = "1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0"
SHEET_NAME = "Sheet1"

@st.cache_data(ttl=60)
def load_data():
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
        df = pd.read_csv(url)
        df.columns = [c.strip() for c in df.columns] # 공백 제거
        return df
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("❌ 데이터를 불러올 수 없습니다. 구글 시트 공유 설정을 확인해주세요.")
    st.stop()

# 3. 검색 및 필터
col1, col2 = st.columns([2, 1])
with col1:
    keyword = st.text_input("🔍 이름/업무 검색", placeholder="예: 보안, 박현욱")
with col2:
    if "fav" not in st.session_state: st.session_state.fav = set()
    show_fav = st.checkbox("⭐ 즐겨찾기")

# 필터링 로직 (KeyError 안전장치)
filtered = df.copy()
name_col = '이름' if '이름' in df.columns else df.columns[0] # 컬럼명이 달라도 첫번째 컬럼 사용

if keyword:
    mask = filtered.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
    filtered = filtered[mask]

if show_fav:
    filtered = filtered[filtered.index.isin(st.session_state.fav)]

# 4. 리스트 출력 (초슬림 모드)
st.write(f"검색 결과: {len(filtered)}명")

for i, row in filtered.iterrows():
    is_fav = i in st.session_state.fav
    star = "★" if is_fav else "☆"
    
    # 폰트 및 데이터 매핑 (시트 컬럼명에 맞춰 조정 필요)
    dept = row.get('부서', '')
    name = row.get('성명', '이름없음')
    pos = row.get('직함', '')
    ext = row.get('내선', '')
    mobile = row.get('휴대폰', '')
    work = row.get('업무', '')
tel_link = str(mobile).replace("-", "")

    # 슬림 카드 레이아웃
    with st.container():
        c_star, c_content = st.columns([0.1, 0.9])
        with c_star:
            if st.button(star, key=f"btn_{i}"):
                if is_fav: st.session_state.fav.remove(i)
                else: st.session_state.fav.add(i)
                st.rerun()
        with c_content:
            st.markdown(f"""
                <div class="contact-card">
                    <a href="tel:{tel_link}" class="main-row">
                        <div style="flex: 1;">
                            <span class="name-text">{name}</span>
                            <span class="dept-text">{pos} ({dept})</span>
                            <span class="work-text">{work}</span>
                        </div>
                        <div class="right-info">
                            <div class="ext-text">{ext}</div>
                            <div class="mobile-text">{mobile}</div>
                        </div>
                    </a>
                </div>
            """, unsafe_allow_html=True)

# 5. 하단 관리 메뉴
with st.expander("⚙️ 데이터 관리"):
    if st.button("🔄 데이터 강제 새로고침"):
        st.cache_data.clear()
        st.rerun()
