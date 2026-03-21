import streamlit as st
import pandas as pd

# 1. 기본 설정 (모바일에서 꽉 차게 보이도록 설정)
st.set_page_config(page_title="비상연락망", layout="wide")

# CSS 주입: 불필요한 여백 줄이기 및 클릭 영역 최적화
st.markdown("""
    <style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .contact-row {
        padding: 10px 5px;
        border-bottom: 1px solid #eee;
        display: flex;
        justify-content: space-between;
        align-items: center;
        text-decoration: none;
        color: inherit;
    }
    .contact-row:active { background-color: #f8f9fa; }
    .name-tag { font-size: 1.1rem; font-weight: bold; color: #111; }
    .info-tag { font-size: 0.85rem; color: #666; margin-top: 2px; }
    .phone-tag { text-align: right; color: #007bff; font-weight: 600; font-size: 0.95rem; }
    .ext-tag { text-align: right; font-size: 0.8rem; color: #999; }
    </style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 2. 구글시트 설정 및 데이터 로드
SHEET_ID = "1sGpEFXLNsZm76lRPuyS4vLGmTQGkAYtNHt1f03mx0h0"
SHEET_NAME = "Sheet1"

@st.cache_data(ttl=60)
def load_data():
    try:
        url = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/gviz/tq?tqx=out:csv&sheet={SHEET_NAME}"
        return pd.read_csv(url)
    except:
        # 시트 로드 실패 시 PDF 기반 비상용 로컬 데이터 반환 (데이터 누락 방지)
        return pd.DataFrame([
            {"이름": "박현욱", "직급": "팀장", "부서": "총무팀", "휴대폰": "010-6245-0589", "내선": "8190", "업무": "부서업무 총괄"},
            {"이름": "윤호열", "직급": "UM", "부서": "안전관리U", "휴대폰": "010-2623-7963", "내선": "8199", "업무": "소방/방재, 시설관리"},
            {"이름": "이규용", "직급": "소장", "부서": "보안", "휴대폰": "010-8883-6580", "내선": "8300", "업무": "보안 총괄"}
        ])

df = load_data()

# 3. 검색 창 (슬림하게 배치)
keyword = st.text_input("🔍 이름/업무 검색", placeholder="예: 보안, 전기, 박현욱")

if keyword:
    mask = df.apply(lambda row: row.astype(str).str.contains(keyword, case=False).any(), axis=1)
    df = df[mask]

# 4. [span_7](start_span)[span_8](start_span)슬림 리스트 출력 (원본 PDF 느낌 유지[span_7](end_span)[span_8](end_span))
if not df.empty:
    for _, row in df.iterrows():
        # 전화연결용 번호 처리
        clean_tel = str(row['휴대폰']).replace("-", "")
        
        # 행 전체를 클릭하면 전화가 걸리도록 구성
        st.markdown(f"""
            <a href="tel:{clean_tel}" class="contact-row">
                <div style="flex: 1;">
                    <div class="name-tag">{row['이름']} <span style="font-size:0.8rem; font-weight:normal;">{row['직급']}</span></div>
                    <div class="info-tag">{row['부서']} | {row['업무']}</div>
                </div>
                <div>
                    <div class="phone-tag">{row['내선']}</div>
                    <div class="ext-tag">{row['휴대폰']}</div>
                </div>
            </a>
        """, unsafe_allow_html=True)
else:
    st.warning("검색 결과가 없습니다.")

# 5. 하단 메뉴 (데이터 새로고침 및 관리)
with st.sidebar:
    if st.button("🔄 데이터 새로고침"):
        st.cache_data.clear()
        st.rerun()
    st.info("구글 시트의 데이터가 자동으로 반영됩니다.")
