# --- [데이터 보정 로직에 추가할 내용] ---
def enhance_data(df):
    # 'name' 컬럼을 분석하여 카테고리(category) 부여
    def classify(name):
        name = str(name)
        if '교수' in name or '연구실' in name:
            if '연구실' in name and '교수' not in name:
                return '일반연구실'
            return '교수연구실'
        elif '강의' in name or '세미나' in name:
            return '교육시설'
        elif '실험' in name:
            return '실험시설'
        return '기타'

    df['category'] = df['name'].apply(classify)
    return df

# --- [메인 화면 구성 업데이트] ---
final_df = get_final_clean_data()
if final_df is not None:
    final_df = enhance_data(final_df) # 카테고리 강화 실행
    
    st.title("🏢 성의교정 시설 통합 가이드")
    
    # 1. 상단 요약 카드 (Metric)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("전체 시설", f"{len(final_df)}개")
    with col2:
        prof_rooms = len(final_df[final_df['category'] == '교수연구실'])
        st.metric("교수/연구실", f"{prof_rooms}개")
    with col3:
        edu_rooms = len(final_df[final_df['category'] == '교육시설'])
        st.metric("강의/세미나실", f"{edu_rooms}개")

    # 2. 퀵 필터 버튼
    st.write("### 📌 유형별 모아보기")
    cats = ['교수연구실', '일반연구실', '교육시설', '실험시설']
    selected_cat = st.segmented_control("원하시는 시설 유형을 선택하세요", options=cats)

    if selected_cat:
        filtered_res = final_df[final_df['category'] == selected_cat]
        st.write(f"**{selected_cat}** 검색 결과: {len(filtered_res)}건")
        st.dataframe(filtered_res[['name', 'building', 'floor', 'room', 'description']], use_container_width=True)
    
    # 3. 자유 검색창 (기존 로직)
    st.write("---")
    search_q = st.text_input("🔍 직접 검색 (교수님 성함, 호실 등)", placeholder="예: 김OO 교수, 2016, 나노연구")
    # ... (검색 로직 생략)
