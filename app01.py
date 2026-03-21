import streamlit as st
import pandas as pd

# 1. 페이지 설정 (모바일 브라우저 최적화)
st.set_page_config(page_title="성의교정 비상연락망", layout="wide")

# 2. 스타일 설정 (화면 여백 최소화 및 리스트 디자인)
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .contact-row {
        padding: 12px 8px;
        border-bottom: 1px solid #eee;
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-decoration: none;
        color: inherit !important;
    }
    .contact-row:active { background-color: #f0f2f6; }
    .name-tag { font-size: 1.1rem; font-weight: bold; color: #111; }
    .info-tag { font-size: 0.85rem; color: #666; margin-top: 3px; line-height: 1.2; }
    .right-section { text-align: right; min-width: 100px; }
    .ext-tag { font-size: 1rem; font-weight: bold; color: #007bff; }
    .phone-tag { font-size: 0.8rem; color: #999; margin-top: 2px; }
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
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

df = load_data()

# 4. 검색창
keyword = st.text_input("🔍 이름이나 업무로 검색", placeholder="예: 보안, 박현욱, 전기")

# 5. 검색 로직 및 출력
if not df.empty:
    # 검색어 필터링
    if keyword:
        df = df[
            df["이름"].astype(str).str.contains(keyword, case=False, na=False) |
            df["업무"].astype(str).str.contains(keyword, case=False, na=False) |
            df["부서"].astype(str).str.contains(keyword, case=False, na=False)
        ]

    # 리스트 출력
    for _, row in df.iterrows():
        # 휴대폰 번호에서 하이픈 제거 (전화 걸기 용)
        tel_link = str(row["휴대폰"]).replace("-", "")
        
        # 한 줄 형태의 슬림한 리스트 (전체 클릭 시 전화 연결)
        st.markdown(f"""
            <a href="tel:{tel_link}" class="contact-row">
                <div style="flex: 1; padding-right: 10px;">
                    <div class="name-tag">{row['이름']} <span style="font-size:0.85rem; font-weight:normal;">{row['직급']}</span></div>
                    <div class="info-tag">{row['부서']} | {row['업무']}</div>
                </div>
                <div class="right-section">
                    <div class="ext-tag">{row['내선']}</div>
                    <div class="phone-tag">{row['휴대폰']}</div>
                </div>
            </a>
        """, unsafe_allow_html=True)

    if df.empty:
        st.info("검색 결과가 없습니다.")
else:
    st.error("❌ 데이터를 불러올 수 없습니다. 구글 시트 ID와 공유 설정을 확인해주세요.")

# 6. 하단 새로고침 기능
st.divider()
if st.button("🔄 데이터 새로고침"):
    st.cache_data.clear()
    st.rerun()
