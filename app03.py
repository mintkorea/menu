import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (라디오 버튼 가로 정렬 및 카드 최적화)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding: 1rem 0.8rem !important; }
    
    /* 라디오 버튼 가로 정렬 강제 */
    div[role="radiogroup"] {
        flex-direction: row !important;
        flex-wrap: wrap !important;
        gap: 10px !important;
    }
    
    /* 라디오 버튼 항목 디자인 */
    div[data-testid="stMarkdownContainer"] > p { font-size: 0.9rem !important; }

    .main-title { font-size: 1.5rem; font-weight: 800; text-align: center; margin-bottom: 15px; }
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 12px 0px; border-bottom: 1px solid #eee; width: 100%; }
    .info-section { flex: 1; min-width: 0; }
    .name-row { display: flex; align-items: baseline; gap: 6px; }
    .name-text { font-weight: 700; font-size: 1.05rem; }
    .pos-dept { font-size: 0.85rem; color: #666; }
    .work-text { font-size: 0.82rem; color: #888; margin-top: 3px; line-height: 1.3; }
    .icon-section { display: flex; gap: 15px; flex-shrink: 0; margin-left: 10px; }
    .icon-link { text-decoration: none !important; font-size: 1.3rem; font-weight: 800; color: #007bff !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 구글 시트 데이터 로드
@st.cache_data(ttl=300)
def load_data(url):
    csv_url = url.replace('/edit?usp=sharing', '/export?format=csv')
    return pd.read_csv(csv_url).fillna('')

SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"
df = load_data(SHEET_URL)

# 4. 라디오 버튼 필터 (상단 배치)
# 시트의 '부서' 컬럼에서 유니크한 값들을 가져옵니다.
if not df.empty:
    depts = ["전체"] + sorted(df['부서'].unique().tolist())
    selected_dept = st.radio("부서 선택", depts, horizontal=True, label_visibility="collapsed")
    
    # 텍스트 검색창도 병행 (필요 없으면 삭제 가능)
    search_name = st.text_input("이름 검색", placeholder="성함 입력...", label_visibility="collapsed")

    # 5. 리스트 출력 로직
    for _, row in df.iterrows():
        name, dept, pos = str(row['성명']), str(row['부서']), str(row['직함'])
        ext, mobile, work = str(row['내선']), str(row['휴대폰']), str(row['담당업무'])

        # 필터 1: 라디오 버튼 (부서)
        if selected_dept != "전체" and dept != selected_dept:
            continue
            
        # 필터 2: 이름 검색
        if search_name and search_name not in name:
            continue

        # 전화번호 정제
        t_clean = ext.replace("-", "").replace(" ", "").strip()
        m_clean = mobile.replace("-", "").replace(" ", "").strip()
        t_html = f'<a href="tel:{t_clean}" class="icon-link">T</a>' if t_clean else ""
        m_html = f'<a href="tel:{m_clean}" class="icon-link">M</a>' if m_clean else ""
        sep = " · " if pos and dept else ""
        
        st.markdown(f"""
            <div class="contact-card">
                <div class="info-section">
                    <div class="name-row">
                        <span class="name-text">{name}</span>
                        <span class="pos-dept">{pos}{sep}{dept}</span>
                    </div>
                    {"<div class='work-text'>- "+work+"</div>" if work.strip() else ""}
                </div>
                <div class="icon-section">{t_html}{m_html}</div>
            </div>
        """, unsafe_allow_html=True)
else:
    st.info("데이터 로딩 중...")
