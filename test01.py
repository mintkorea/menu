import streamlit as st
import pandas as pd

# 1. 구글 시트 URL 설정 (상단에 위치)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSGYiqRoXeOInxtwCEa_HXEEM3YVEtOWITy5jf83wkIg2CBHF6ttUKWpS2PtlPx4EOjjxsNJ2idTPzn/pub?gid=954211169&single=true&output=csv"

# 2. 함수 정의 (반드시 호출보다 먼저 정의되어야 함)
@st.cache_data(ttl=300)
def load_data(url):
    try:
        # 데이터 읽기 및 전처리
        df = pd.read_csv(url)
        # 모든 데이터를 문자열로 변환하고 앞뒤 공백 제거
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    except Exception as e:
        st.error(f"데이터 로드 중 오류 발생: {e}")
        return pd.DataFrame()

# 페이지 설정
st.set_page_config(page_title="성의교정 통합 안내 시스템", layout="wide")

# 3. 함수 호출 (정의된 이후에 실행)
df = load_data(SHEET_CSV_URL)

# --- UI 및 검색 로직 ---
st.title("🏥 성의교정 & 성모병원 통합 안내")

if not df.empty:
    # '건물' 컬럼 에러 방지 처리
    if '건물' in df.columns:
        df['건물'] = df['건물'].fillna('미분류').astype(str)
        building_list = sorted(df['건물'].unique().tolist())
    else:
        building_list = []

    st.markdown(f"**현재 등록된 데이터:** {len(df)}건 (실시간 연동 중)")

    col1, col2 = st.columns([1, 2])
    with col1:
        selected_building = st.selectbox("🏢 건물 선택", ["전체"] + building_list)
    with col2:
        search_query = st.text_input("🔍 검색어 입력", placeholder="예: 서태석, 1416, 산부인과")

    # 필터링
    filtered_df = df.copy()
    if selected_building != "전체":
        filtered_df = filtered_df[filtered_df['건물'] == selected_building]
    
    if search_query:
        mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
        filtered_df = filtered_df[mask]

    # 결과 출력
    st.dataframe(filtered_df, use_container_width=True, hide_index=True)
else:
    st.warning("데이터를 불러올 수 없습니다. 구글 시트 링크를 확인해주세요.")
