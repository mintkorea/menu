# --- 데이터 로드 및 전처리 ---
df = load_data(SHEET_CSV_URL)

# 에러 방지용 전처리: '건물' 컬럼이 없거나 비어있는 경우 대비
if not df.empty:
    # 1. '건물' 컬럼이 실제로 존재하는지 확인
    if '건물' in df.columns:
        # 2. 결측치(빈 칸)를 '미분류'로 채우고 문자열로 변환하여 에러 방지
        df['건물'] = df['건물'].fillna('미분류').astype(str)
        building_list = sorted(df['건물'].unique().tolist())
    else:
        st.error("⚠️ 구글 시트에 '건물' 컬럼이 없습니다. 첫 번째 줄의 제목을 확인해주세요.")
        building_list = []
else:
    building_list = []

# --- UI 레이아웃 ---
st.title("🏥 성의교정 & 성모병원 통합 안내")

if not df.empty:
    st.markdown(f"**현재 등록된 데이터:** {len(df)}건 (구글 시트 실시간 연동 중)")

    # 검색 섹션
    col1, col2 = st.columns([1, 2])
    with col1:
        # 데이터가 없을 경우를 대비해 building_list가 비어있지 않을 때만 실행
        selected_building = st.selectbox("🏢 건물 선택", ["전체"] + building_list)
    
    with col2:
        search_query = st.text_input("🔍 검색어 입력 (부서, 교수명, 호수 등)", placeholder="예: '서태석', '1416'...")

    # ... 이하 필터링 및 출력 로직 동일 ...
else:
    st.warning("데이터를 불러오는 중입니다. 잠시만 기다려주시거나 구글 시트 링크를 확인해주세요.")
