import pandas as pd
import streamlit as st

# --- 1. 데이터 로드 및 전처리 ---
@st.cache_data
def load_and_clean_data():
    target_files = [
        '성의회관.csv', '대학본관.csv', '의산연01.csv', '의산연별관.csv', 
        '병원별관.csv', '옴니버스A.csv', '옴니버스B.csv', '서울성모병원.CSV'
    ]
    all_dfs = []
    
    for file_path in target_files:
        try:
            try: df = pd.read_csv(file_path, encoding='utf-8-sig')
            except: df = pd.read_csv(file_path, encoding='cp949')
            
            df.columns = [str(c).strip().lower() for c in df.columns]
            rename_map = {'건물명': 'building', '시설명': 'name', '이름': 'name', '호실': 'room', '층': 'floor'}
            df = df.rename(columns=rename_map)
            
            # 건물명 강제 매칭
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
        except: continue
            
    if not all_dfs: return None
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    if 'name' in combined.columns:
        combined = combined[combined['name'].astype(str).str.lower() != 'name']
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')

# --- 2. 영문/별칭 매핑 ---
def get_search_tags(name):
    name_str = str(name).lower()
    tags = {'start': 'start center simulation cpx', '도서관': 'library', '식당': 'cafeteria', '회의실': 'meeting'}
    for key, val in tags.items():
        if key in name_str: return f"{name_str} {val}"
    return name_str

# --- 3. 안내판 기반 인덱스 우선순위 ---
def apply_priority(df, selected_bldg):
    priority_map = {
        '성의회관': ['마리아홀', '안내실', '성당', '교목실', 'start', '도서관', '게스트'],
        '대학본관': ['행정실', '회의실', '식당', '교육실', '시설팀'],
        '의산연본관': ['실험동물', '세포치료', '연구센터', '대강당', '관제실'],
        '의산연별관': ['술기교육', '응용해부', '실습실', '법의학'],
        '병원별관': ['암연구소', '백신바이오', '면역질환', '행정사무실', '학생회'],
        '옴니버스파크': ['푸드코트', '이마트24', '컨벤션', '카페']
    }
    df['sort_idx'] = 999
    if selected_bldg in priority_map:
        for i, target in enumerate(priority_map[selected_bldg]):
            df.loc[df['name'].astype(str).str.contains(target, case=False, na=False), 'sort_idx'] = i
    return df.sort_values(by=['sort_idx', 'floor', 'name']).drop(columns=['sort_idx'])

# --- 4. 메인 UI (리스트 노출 방식 수정) ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # CSS: 리스트 가독성 및 모바일 최적화
    st.markdown("""
        <style>
        .m-title { font-size: 1.15rem; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
        .result-row { 
            padding: 10px; border-bottom: 1px solid #eee; font-size: 0.95rem; line-height: 1.5;
        }
        .bldg-tag { color: #666; font-size: 0.8rem; margin-right: 5px; }
        .floor-tag { color: #007bff; font-weight: bold; margin-right: 8px; }
        .name-tag { font-weight: 500; color: #333; }
        .info-icon { color: #e67e22; margin-right: 4px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='m-title'>🏥 성의교정 시설 안내 시스템</div>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        bldg_list = sorted(data['building'].unique().tolist())
        selected_bldg = st.selectbox("🏢 건물을 선택하세요", options=bldg_list)
        search_query = st.text_input("🔍 시설명 또는 영문(Start 등) 검색")
        
        view_df = data[data['building'] == selected_bldg].copy()
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df['name'].astype(str).str.lower().str.contains(q) | 
                             view_df['name'].apply(get_search_tags).str.contains(q)]
        
        # 인덱스 우선순위 적용
        view_df = apply_priority(view_df, selected_bldg)
        
        st.caption(f"📍 {len(view_df)}개의 시설이 검색되었습니다.")
        st.markdown("---")

        # [수정] 펼치기 없이 바로 리스트 노출
        for _, row in view_df.iterrows():
            name_str = str(row['name'])
            floor_str = str(row.get('floor', '-'))
            bldg_str = str(row.get('building', '-'))
            
            # 안내판 항목 여부 확인 (아이콘 표시)
            is_info = any(kw in name_str.lower() for kw in ['센터', '연구소', '홀', '실', '팀', '식당'])
            icon = "📢" if is_info else "📍"
            
            # HTML을 이용한 한 줄 출력 (건물 | 층 | 시설명)
            st.markdown(f"""
                <div class='result-row'>
                    <span class='bldg-tag'>[{bldg_str}]</span>
                    <span class='floor-tag'>{floor_str}F</span>
                    <span class='name-tag'>{icon} {name_str}</span>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error("데이터를 불러올 수 없습니다.")

if __name__ == "__main__":
    main()
