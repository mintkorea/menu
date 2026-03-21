import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(page_title="성의교정 비상연락망", layout="wide")

# 1. 데이터 로드 (파일이 없을 경우 대비)
@st.cache_data
def load_data():
    try:
        # 통합 CSV 파일을 읽어옵니다.
        return pd.read_csv("contacts.csv")
    except:
        # 파일이 없을 경우 스크린샷에 보이는 기본 데이터만이라도 출력
        return pd.DataFrame([
            {"구분": "시설", "성명_부서": "전기팀", "직책": "지원", "연락처": "02-2258-5672", "표기번호": "*1-5672", "주요업무": "전기 시설 관리"},
            {"구분": "시설", "성명_부서": "성의회관", "직책": "건물", "연락처": "02-3147-8300", "표기번호": "8300", "주요업무": "성의회관 안내"},
            {"구분": "시설", "성명_부서": "통합관제", "직책": "지원", "연락처": "02-2258-5555", "표기번호": "2258-5555", "주요업무": "통합관제 센터"}
        ])

df = load_data()

st.title("📱 성의교정 비상연락망")

# 2. 검색창
search = st.text_input("🔍 이름이나 업무를 검색하세요", placeholder="예: 박현욱, 보안, 전기, 상황실")

# 3. 데이터 필터링 로직
if search:
    # 성명, 업무, 부서 어디든 검색어가 포함되면 출력
    mask = (
        df['성명_부서'].str.contains(search, na=False) | 
        df['주요업무'].str.contains(search, na=False) |
        df['구분'].str.contains(search, na=False)
    )
    display_df = df[mask]
else:
    display_df = df

# 4. 리스트 출력
if display_df.empty:
    st.warning("검색 결과가 없습니다.")
else:
    for _, row in display_df.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                # 인원일 경우와 시설일 경우를 구분해서 출력
                title = f"**{row['성명_부서']}**"
                if row['구분'] == "인원":
                    title += f" {row['직책']}"
                st.markdown(title)
                st.caption(f"내선/표기: {row['표기번호']}")
                st.caption(f"업무: {row['주요업무']}")
            with col2:
                # 전화연결 버튼
                st.markdown(f"""
                    <a href="tel:{row['연락처'].replace('-', '')}" style="text-decoration:none;">
                        <div style="background-color:#5cb85c; color:white; text-align:center; padding:12px; border-radius:8px; font-weight:bold; margin-top:10px;">
                            📞 연결
                        </div>
                    </a>
                """, unsafe_allow_html=True)
            st.divider()

# 5. 하단 관리용 메뉴
with st.sidebar:
    st.header("설정")
    st.download_button("📄 연락망 CSV 받기", df.to_csv(index=False).encode('utf-8-sig'), "contacts.csv", "text/csv")
