import streamlit as st
import pandas as pd

# [가정] 이전 단계에서 통합된 final_df가 있다고 가정합니다.
# 1. 화면 타이틀
st.title("🏢 가톨릭대학교 성의교정 시설 안내")
st.markdown(f"현재 **{len(final_df)}개**의 시설 정보가 등록되어 있습니다.")

# 2. 통합 검색창 레이아웃
st.divider()
search_query = st.text_input("🔍 찾으시는 시설명, 건물명, 또는 호실 번호를 입력하세요.", placeholder="예: 기초의학실습실, 옴니버스, 402호")

# 3. 검색 로직 (시설명, 건물명, 호실, 비고 전체에서 검색)
if search_query:
    # 대소문자 구분 없이 검색하기 위해 query를 소문자로 변환
    q = search_query.lower()
    
    # 여러 컬럼을 합쳐서 검색 대상 생성
    search_target = (
        final_df['name'].astype(str) + 
        final_df['building_name'].astype(str) + 
        final_df['floor'].astype(str) + 
        final_df['room'].astype(str) + 
        final_df['description'].astype(str)
    ).str.lower()
    
    results = final_df[search_target.str.contains(q, na=False)]
    
    if not results.empty:
        st.write(f"✅ **'{search_query}'**에 대한 검색 결과가 **{len(results)}건** 있습니다.")
        st.dataframe(results, use_container_width=True)
    else:
        st.warning(f"❌ '{search_query}'에 대한 검색 결과가 없습니다. 검색어를 확인해 주세요.")
else:
    st.info("검색어를 입력하시면 전체 건물에서 해당 시설을 즉시 찾아드립니다.")

# 4. 부가 기능: 건물별 필터 (사이드바)
st.sidebar.header("📍 건물별 필터")
selected_building = st.sidebar.multiselect(
    "특정 건물만 보기",
    options=final_df['building_name'].unique(),
    default=final_df['building_name'].unique()
)

# 필터 적용 로직은 필요시 추가 가능
