import streamlit as st
import pandas as pd

# 1. 페이지 설정 (제목 및 모바일 최적화 레이아웃)
st.set_page_config(page_title="성의교정 비상연락망", layout="wide")

# 2. 스타일 설정 (화면 낭비 최소화 및 리스트 디자인)
st.markdown("""
    <style>
    /* 상단 여백 제거 */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    /* 리스트 행 디자인: 간격 좁게 */
    .contact-row {
        padding: 8px 5px;
        border-bottom: 1px solid #f0f0f0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-decoration: none;
        color: inherit !important;
    }
    .contact-row:active { background-color: #f8f9fa; }
    .name-tag { font-size: 1.05rem; font-weight: bold; color: #111; }
    .info-tag { font-size: 0.8rem; color: #666; margin-top: 2px; }
    .right-section { text-align: right; }
    .ext-tag { font-size: 0.95rem; font-weight: bold; color: #007bff; }
    .phone-tag { font-size: 0.75rem; color: #aaa; }
    </style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 3. 데이터 로드 (구글 시트 연동)
SHEET_ID = "1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0"
SHEET_NAME = "Sheet1"

@st.cache_data(ttl=60)
def load_data():
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
        df = pd.read_csv(url)
        # 컬럼명 공백 제거
        df.columns = [c.strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

df = load_data()

# 4. 검색 기능
keyword = st.text_input("🔍 검색 (이름, 부서, 업무)", placeholder="예: 보안, 박현욱, 전기")

# 5. 결과 출력
if not df.empty:
    # 검색 필터링
    if keyword:
        # 모든 열에서 키워드 포함 여부 확인
        mask = df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
        display_df = df[mask]
    else:
        display_df = df

    # 슬림 리스트 출력
    for _, row in display_df.iterrows():
        # 연락처에서 하이픈 제거 (전화 걸기용)
        tel_val = str(row.get('휴대폰', ''))
        tel_link = tel_val.replace("-", "")
        
        # 이름/직급/부서/업무 및 내선번호 배치
        st.markdown(f"""
            <a href="tel:{tel_link}" class="contact-row">
                <div style="flex: 1;">
                    <div class="name-tag">{row.get('이름','')} <span style="font-size:0.8rem; font-weight:normal;">{row.get('직급','')}</span></div>
                    <div class="info-tag">{row.get('부서','')} | {row.get('업무','')}</div>
                </div>
                <div class="right-section">
                    <div class="ext-tag">{row.get('내선','')}</div>
                    <div class="phone-tag">{tel_val}</div>
                </div>
            </a>
        """, unsafe_allow_html=True)

    if display_df.empty:
        st.info("검색 결과가 없습니다.")
else:
    st.error("❌ 데이터를 불러올 수 없습니다. 구글 시트 설정을 확인해 주세요.")

# 6. 새로고침 버튼
if st.button("🔄 데이터 새로고침"):
    st.cache_data.clear()
    st.rerun()
