import pandas as pd
import streamlit as st

# --- 1. 데이터 로드 및 전처리 (에러 완벽 방지) ---
@st.cache_data
def load_and_clean_data():
    target_files = [
        '성의회관.csv', '대학본관.csv', '의산연01.csv', '의산연별관.csv', 
        '병원별관.csv', '옴니버스A.csv', '옴니버스B.csv', '서울성모병원.CSV'
    ]
    all_dfs = []
    
    for file_path in target_files:
        try:
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')
            
            # 컬럼명 표준화 (AttributeError 방지용 소문자화)
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
        except:
            continue
            
    if not all_dfs:
        return None
        
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    
    # [에러 해결] .str.lower()를 사용하여 Series 문자열 처리
    if 'name' in combined.columns:
        combined = combined[combined['name'].astype(str).str.lower() != 'name']
        
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')

# --- 2. 영문/별칭 매핑 함수 (START센터 등 대응) ---
def get_search_tags(name):
    name_str = str(name).lower()
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

# --- 3. 안내판 기반 인덱스 우선순위 설정 (이미지 데이터 반영) ---
def apply_priority(df, selected_bldg):
    priority_map = {
        '성의회관': ['마리아홀', '안내실', '성당', '교목실', 'start', '도서관', '게스트', '강의실'],
        '대학본관': ['행정실', '회의실', '식당', '교육실', '시설팀', '교수실'],
        '의산연본관': ['실험동물', '세포치료', '연구센터', '대강당', '창업보육', '관제실'],
        '의산연별관': ['술기교육', '응용해부', '실습실', '법의학', '조직은행', '한센병'],
        '병원별관': ['암연구소', '백신바이오', '면역질환', '행정사무실', '옴니헬스', '학생회'],
        '옴니버스파크': ['푸드코트', '이마트24', '컨벤션', '박물관', '카페', '마스터센터']
    }
    
    df['sort_idx'] = 999
    
    if selected_bldg in priority_map:
        targets = priority_map[selected_bldg]
        for i, target in enumerate(targets):
            # 안내판 키워드 포함 시 인덱스 상단 배치
            df.loc[df['name'].astype(str).str.contains(target, case=False, na=False), 'sort_idx'] = i
            
    return df.sort_values(by=['sort_idx', 'floor', 'name']).drop(columns=['sort_idx'])

# --- 4. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    st.markdown("<style>.m-title{font-size:1.15rem; font-weight:bold; color:#1E3A8A;}</style>", unsafe_allow_html=True)
    st.markdown("<div class='m-title'>🏥 성의교정 시설 안내 시스템</div>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    
    if data is not None:
        bldg_list = sorted(data['building'].unique().tolist())
        selected_bldg = st.selectbox("🏢 건물을 선택하세요", options=bldg_list)
        
        search_query = st.text_input("🔍 시설명, 성함, 또는 영문(Start 등) 검색", placeholder="비워두면 안내판 정보가 먼저 노출됩니다.")
        
        # 1차 필터링 (건물 기준)
        view_df = data[data['building'] == selected_bldg].copy()
        
        # 2차 필터링 (검색어 기준)
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[
                view_df['name'].astype(str).str.lower().str.contains(q) | 
                view_df['name'].apply(get_search_tags).str.contains(q)
            ]
        
        # [핵심] 인덱스 우선순위 적용 (검색 전/후 모두 적용)
        view_df = apply_priority(view_df, selected_bldg)
        
        st.caption(f"📍 {selected_bldg}: {len(view_df)}건 검색됨")
        
        for _, row in view_df.iterrows():
            name_str = str(row['name'])
            is_info = any(kw in name_str.lower() for kw in ['센터', '연구소', '홀', '실', '팀', '식당'])
            icon = "📢" if is_info else "📍"
            
            with st.expander(f"{icon} {name_str}"):
                st.write(f"**위치:** {row.get('floor','-')}층 {row.get('room','-')}호")
    else:
        st.error("데이터를 불러올 수 없습니다. CSV 파일들을 확인해주세요.")

if __name__ == "__main__":
    main()
