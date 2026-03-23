import streamlit as st
import pandas as pd

# 1. 사용자님이 제공하신 구글 시트 CSV 게시 링크
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSGYiqRoXeOInxtwCEa_HXEEM3YVEtOWITy5jf83wkIg2CBHF6ttUKWpS2PtlPx4EOjjxsNJ2idTPzn/pub?gid=954211169&single=true&output=csv"

# 페이지 설정
st.set_page_config(page_title="성의교정 통합 안내 시스템", page_icon="🏢", layout="wide")

@st.cache_data(ttl=300)  # 5분마다 데이터를 새로고침 (실시간성 유지)
def load_data(url):
    try:
        # 구글 시트 데이터 읽기
        df = pd.read_csv(url)
        # 데이터 앞뒤 공백 제거 (검색 정확도 향상)
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        return df
    except Exception as e:
        st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# 데이터 로드
df = load_data(SHEET_CSV_URL)

# --- UI 레이아웃 ---
st.title("🏥 성의교정 & 성모병원 통합 안내")
st.markdown(f"**현재 등록된 데이터:** {len(df)}건 (구글 시트 실시간 연동 중)")

# 검색 섹션
col1, col2 = st.columns([1, 2])
with col1:
    selected_building = st.selectbox("🏢 건물 선택", ["전체"] + sorted(df['건물'].unique().tolist()))
with col2:
    search_query = st.text_input("🔍 검색어 입력 (부서, 교수명, 호수, 시설명 등)", placeholder="예: '서태석', '1416', '산부인과'...")

# 필터링 로직
filtered_df = df.copy()

if selected_building != "전체":
    filtered_df = filtered_df[filtered_df['건물'] == selected_building]

if search_query:
    # 명칭, 호수, 비고 등 모든 열에서 검색어 포함 여부 확인 (대소문자 무시)
    mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

# --- 결과 출력 ---
if not filtered_df.empty:
    st.write(f"총 **{len(filtered_df)}**건의 정보가 검색되었습니다.")
    
    # 결과 테이블
    st.dataframe(
        filtered_df, 
        use_container_width=True, 
        hide_index=True,
        column_config={
            "건물": st.column_config.TextColumn("건물명", width="small"),
            "층": st.column_config.TextColumn("위치", width="small"),
            "호수": st.column_config.TextColumn("호수/동", width="small"),
            "명칭": st.column_config.TextColumn("상세 명칭", width="medium"),
            "비고": st.column_config.TextColumn("참고 사항", width="large")
        }
    )
    
    # 검색어가 있을 때 상세 카드 뷰 제공
    if search_query:
        st.markdown("---")
        for idx, row in filtered_df.iterrows():
            with st.expander(f"📍 {row['건물']} {row['층']} - {row['명칭']}"):
                st.write(f"**상세 위치:** {row['호수'] if pd.notna(row['호수']) else '-'}")
                st.write(f"**참고 사항:** {row['비고'] if pd.notna(row['비고']) else '내용 없음'}")
else:
    st.warning("일치하는 정보를 찾을 수 없습니다. 검색어를 확인해 주세요.")

# 하단 정보
st.sidebar.markdown("### 📊 데이터 요약")
st.sidebar.write(df['건물'].value_counts())
st.sidebar.info("데이터 수정이 필요한 경우 구글 시트 원본을 수정하세요. 수정 후 약 5분 뒤 앱에 반영됩니다.")
