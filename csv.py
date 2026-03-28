import pandas as pd
import streamlit as st

# --- 1. 데이터 로드 및 전처리 (에러 방지 로직 포함) ---
@st.cache_data
def load_and_clean_data():
    # 관리 중인 모든 CSV 파일 리스트
    target_files = [
        '성의회관.csv', '대학본관.csv', '의산연01.csv', '의산연별관.csv', 
        '병원별관.csv', '옴니버스A.csv', '옴니버스B.csv', '서울성모병원.CSV'
    ]
    all_dfs = []
    
    for file_path in target_files:
        try:
            # 인코딩 에러 방지 (utf-8-sig -> cp949 순차 시도)
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')
            
            # 컬럼명 표준화 (소문자화 및 공백 제거로 AttributeError 방지)
            df.columns = [str(c).strip().lower() for c in df.columns]
            rename_map = {'건물명': 'building', '시설명': 'name', '이름': 'name', '호실': 'room', '층': 'floor'}
            df = df.rename(columns=rename_map)
            
            # 파일명 기반 건물명 강제 매칭
            if '성의회관' in file_path: df['building'] = '성의회관'
            elif '대학본관' in file_path: df['building'] = '대학본관'
            elif '의산연01' in file_path: df['building'] = '의산연본관'
            elif '의산연별관' in file_path: df['building'] = '의산연별관'
            elif '병원별관' in file_path: df['building'] = '병원별관'
            elif '옴니버스' in file_path: df['building'] = '옴니버스파크'
            elif 'building' not in df.columns: df['building'] = file_path.split('.')[0]
            
            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except Exception as e:
            continue
            
    if not all_dfs:
        return None
        
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    # 데이터 불순물(제목행 반복 등) 제거
    combined = combined[combined['name'].astype(str).lower() != 'name']
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')

# --- 2. 영문/별칭 매핑 함수 (영문 검색 지원) ---
def get_search_tags(name):
    name_str = str(name).lower()
    # START센터, 도서관 등 주요 시설 영문 매핑
    tags = {
        'start': 'start center simulation cpx 시뮬레이션',
        '도서관': 'library',
        '식당': 'cafeteria restaurant food court',
        '회의실': 'conference meeting room',
        '행정실': 'office administration'
    }
    for key, val in tags.items():
        if key in name_str:
            return f"{name_str} {val}"
    return name_str

# --- 3. 안내판 기반 인덱스 우선순위 설정 ---
def apply_priority(df, selected_bldg):
    # 이미지 분석을 통해 추출한 건물별 안내판 핵심 키워드 리스트
    priority_map = {
        '성의회관': ['마리아홀', '안내실', '성당', '교목실', 'start', '도서관', '게스트', '강의실'],
        '대학본관': ['행정실', '회의실', '식당', '교육실', '시설팀', '교수실'],
        '의산연본관': ['실험동물', '세포치료', '연구센터', '대강당', '창업보육', '관제실'],
        '의산연별관': ['술기교육', '응용해부', '실습실', '법의학', '조직은행', '한센병'],
        '병원별관': ['암연구소', '백신바이오', '면역질환', '행정사무실', '옴니헬스', '학생회'],
        '옴니버스파크': ['푸드코트', '이마트24', '컨벤션', '박물관', '카페', '마스터센터']
    }
    
    df['sort_idx'] = 999  # 기본값 (일반 항목)
    
    if selected_bldg in priority_map:
        targets = priority_map[selected_bldg]
        for i, target in enumerate(targets):
            # 안내판 키워드 포함 시 인덱스 상단(0~n) 배정
            df.loc[df['name'].str.contains(target, case=False, na=False), 'sort_idx'] = i
            
    # 우선순위 -> 층수 -> 이름순 정렬
    return df.sort_values(by=['sort_idx', 'floor', 'name']).drop(columns=['sort_idx'])

# --- 4. Streamlit UI 메인 루프 ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # 타이틀 폰트 1/2 축소 (모바일 최적화)
    st.markdown("<style>.m-title{font-size:1.15rem; font-weight:bold; color:#1E3A8A;}</style>", unsafe_allow_html=True)
    st.markdown("<div class='m-title'>🏥 성의교정 시설 안내 시스템</div>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    
    if data is not None:
        # 건물 선택
        bldg_list = sorted(data['building'].unique().tolist())
        selected_bldg = st.selectbox("🏢 건물을 선택하세요", options=bldg_list)
        
        # 검색어 입력 (영문 검색 지원)
        search_query = st.text_input("🔍 시설명, 성함, 또는 영문(Start 등) 검색", placeholder="비워두면 안내판 정보가 먼저 나옵니다.")
        
        # 필터링 로직
        view_df = data[data['building'] == selected_bldg].copy()
        
        if search_query:
            q = search_query.lower().strip()
            # 이름 혹은 영문 매핑 태그에서 검색
            view_df = view_df[
                view_df['name'].str.lower().str.contains(q) | 
                view_df['name'].apply(get_search_tags).str.contains(q)
            ]
        
        # 인덱스 우선순위 적용 (건물 선택 시 자동 실행)
        view_df = apply_priority(view_df, selected_bldg)
        
        st.caption(f"📍 {selected_bldg}: {len(view_df)}건 검색됨")
        
        # 결과 출력 (Expanders)
        for _, row in view_df.iterrows():
            # 안내판 항목은 아이콘으로 구분
            is_info = any(kw in str(row['name']).lower() for kw in ['센터', '연구소', '홀', '실', '팀', '식당'])
            icon = "📢" if is_info else "📍"
            
            with st.expander(f"{icon} {row['name']}"):
                st.write(f"**위치:** {row.get('floor','-')}층 {row.get('room','-')}호")
    else:
        st.error("데이터 파일이 없거나 로드할 수 없습니다.")

if __name__ == "__main__":
    main()
