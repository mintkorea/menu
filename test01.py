import streamlit as st
import pandas as pd
from io import StringIO

# 1. 데이터 통합 설정 (하나의 리스트로 관리)
def get_combined_data():
    # 성의회관 데이터
    seongui_csv = """건물,층,호수,명칭,비고
성의회관,14F,1404호~1410호,게스트하우스 (포스텍 사용),기숙사 개념
성의회관,14F,1413호~1421호,게스트하우스 (학교관리),개인사용 개념
성의회관,13F,1304호,포스텍 서울공유오피스,
성의회관,11F,-,효원도서관,24시간 출입문 폐쇄
성의회관,1F,-,로비,마리아홀/매점/커피숍
"""
    # 의산연 데이터 (일부 예시, 전체 데이터를 여기에 추가하세요)
    uilsanyun_csv = """건물,층,호수,명칭,비고
의산연,지하1층,B101,서태석 교수,
의산연,1층,1009,연구기술지원팀,
의산연,2층,2014,대강당,
의산연,3층,3001,안과학교실,
의산연,5층,5017,류마티스센터,
"""
    df1 = pd.read_csv(StringIO(seongui_csv))
    df2 = pd.read_csv(StringIO(uilsanyun_csv))
    return pd.concat([df1, df2], ignore_index=True)

# 2. 페이지 레이아웃 설정
st.set_page_config(page_title="가톨릭대학교 성의교정 안내", page_icon="📍", layout="wide")

st.title("🏥 성의교정 입주현황 통합 안내 시스템")
st.info("찾으시는 건물, 부서명, 교수실 또는 호수를 입력하세요.")

# 데이터 로드
df = get_combined_data()

# 3. 검색 및 필터링 UI
col1, col2 = st.columns([2, 1])

with col1:
    search_query = st.text_input("🔍 통합 검색", placeholder="예: '도서관', '교수실', '1001', '의산연'")

with col2:
    building_filter = st.multiselect("건물 선택", options=["전체", "성의회관", "의산연"], default="전체")

# 4. 검색 로직
filtered_df = df.copy()

# 건물 필터 적용
if "전체" not in building_filter and building_filter:
    filtered_df = filtered_df[filtered_df['건물'].isin(building_filter)]

# 검색어 필터 적용
if search_query:
    # 명칭, 호수, 비고 등 모든 컬럼에서 검색
    mask = filtered_df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    filtered_df = filtered_df[mask]

# 5. 결과 출력
st.divider()

if not filtered_df.empty:
    st.write(f"✅ 총 **{len(filtered_df)}**개의 위치가 검색되었습니다.")
    
    # 결과를 표 형태로 출력 (내방객용)
    display_df = filtered_df[['건물', '층', '호수', '명칭', '비고']].fillna('-')
    
    # 데이터프레임 스타일링 (층별 정렬 등)
    st.dataframe(display_df, use_container_width=True, hide_index=True)
    
    # 상세 보기 (카드 형태 - 선택 사항)
    if len(filtered_df) <= 10: # 결과가 적을 때만 상세 카드 표시
        st.subheader("📍 상세 위치 정보")
        cols = st.columns(2)
        for idx, (_, row) in enumerate(filtered_df.iterrows()):
            with cols[idx % 2]:
                with st.expander(f"[{row['건물']}] {row['명칭']}", expanded=True):
                    st.write(f"🏢 **위치:** {row['층']} / {row['호수']}")
                    if pd.notna(row['비고']):
                        st.caption(f"📝 {row['비고']}")
else:
    st.error("❌ 검색 결과가 없습니다. 검색어를 다시 확인해 주세요.")

# 6. 하단 안내
st.sidebar.markdown("---")
st.sidebar.subheader("📌 이용 안내")
st.sidebar.write("1. 상단 검색창에 키워드를 입력하세요.")
st.sidebar.write("2. 건물별로 필터링하여 보실 수 있습니다.")
st.sidebar.write("3. 정보 수정이 필요한 경우 관리자에게 문의하세요.")
