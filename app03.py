import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 충무팀 연락망", layout="wide")

# 2. CSS 스타일
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding-top: 1rem !important; }
    .main-title { font-size: 1.6rem; font-weight: 800; text-align: center; margin-bottom: 15px; }
    .contact-card { display: flex; justify-content: space-between; align-items: center; padding: 10px 0px; border-bottom: 1px solid #eeeeee; width: 100%; }
    .info-section { flex: 1; min-width: 0; padding-right: 10px; }
    .name-row { display: flex; align-items: baseline; gap: 6px; }
    .name-text { font-weight: 700; font-size: 1.05rem; color: #000; white-space: nowrap; }
    .pos-dept { font-size: 0.85rem; color: #555; white-space: nowrap; }
    .work-text { font-size: 0.8rem; color: #777; margin-top: 3px; line-height: 1.3; word-break: keep-all; }
    .icon-section { min-width: 55px; display: flex; justify-content: flex-end; gap: 8px; flex-shrink: 0; }
    .icon-link { text-decoration: none !important; font-size: 1.15rem; font-weight: 800; color: #007bff !important; width: 24px; text-align: center; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">충무팀 비상연락망</div>', unsafe_allow_html=True)

# 3. 구글 시트 데이터 로드 함수
@st.cache_data(ttl=600)  # 10분마다 데이터 갱신
def load_data(sheets_url):
    # 시트 URL을 CSV 내보내기 형식으로 변환
    csv_url = sheets_url.replace('/edit?usp=sharing', '/export?format=csv')
    df = pd.read_csv(csv_url)
    return df.fillna('') # 결측치를 빈 문자열로 처리

# 제공된 구글 시트 주소 사용 
SHEET_URL = "https://docs.google.com/spreadsheets/d/1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0/edit?usp=sharing"

try:
    df = load_data(SHEET_URL)
    
    # 4. 검색창
    query = st.text_input("search", placeholder="성함, 부서 또는 업무 검색...", label_visibility="collapsed")

    # 5. 리스트 출력 로직
    for _, row in df.iterrows():
        # 데이터 추출 (시트 컬럼명 기준)
        dept = str(row.get('부서', ''))
        name = str(row.get('성명', ''))
        pos = str(row.get('직함', ''))
        ext = str(row.get('내선', ''))
        mobile = str(row.get('휴대폰', ''))
        work = str(row.get('담당업무', ''))

        # 검색 필터
        if query:
            search_target = f"{name}{dept}{work}{pos}".lower()
            if query.lower() not in search_target:
                continue

        # 아이콘 생성 (T: 내선, M: 휴대폰)
        t_html = ""
        if ext.strip():
            # 숫자만 추출하여 전화 링크 생성
            ext_num = ext.replace('-', '').replace(' ', '')
            t_html = f'<a href="tel:{ext_num}" class="icon-link">T</a>'

        m_html = ""
        if mobile.strip():
            m_num = mobile.replace('-', '').replace(' ', '')
            m_html = f'<a href="tel:{m_num}" class="icon-link">M</a>'

        # 텍스트 구성
        sep = " · " if pos and dept else ""
        work_display = f'<div class="work-text">- {work}</div>' if work else ""

        # HTML 카드 출력 (한 줄로 결합하여 깨짐 방지)
        card_html = (
            f'<div class="contact-card">'
            f'<div class="info-section">'
            f'<div class="name-row"><span class="name-text">{name}</span><span class="pos-dept">{pos}{sep}{dept}</span></div>'
            f'{work_display}'
            f'</div>'
            f'<div class="icon-section">{t_html}{m_html}</div>'
            f'</div>'
        )
        st.markdown(card_html, unsafe_allow_html=True)

except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.info("구글 시트가 '링크가 있는 모든 사용자에게 공개' 상태인지 확인해 주세요.")
