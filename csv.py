import pandas as pd
import streamlit as st
import re

# --- 1. 데이터 로드 및 전처리 ---
@st.cache_data
def load_and_clean_data():
    target_files = [
        '의산연01.csv', '대학본관.csv', '의산연별관.csv', '성의회관.csv', 
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
            
            # 건물명 수동 매핑
            if '의산연01' in file_path: df['building'] = '의산연본관'
            elif '대학본관' in file_path: df['building'] = '대학본관'
            elif '의산연별관' in file_path: df['building'] = '의산연별관'
            elif '성의회관' in file_path: df['building'] = '성의회관'
            elif '병원별관' in file_path: df['building'] = '병원별관'
            elif '옴니버스' in file_path: df['building'] = '옴니버스파크'
            
            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except: continue
    if not all_dfs: return None
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    if 'name' in combined.columns:
        combined = combined[combined['name'].astype(str).str.lower() != 'name']
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')

# --- 2. 유틸리티 함수 (층 표시 & 영문 매핑) ---
def format_floor(floor_val):
    if pd.isna(floor_val): return "-"
    clean_floor = re.sub(r'[^0-9BL]', '', str(floor_val).upper())
    return f"{clean_floor}F" if clean_floor else str(floor_val)

def get_search_tags(name):
    name_str = str(name).lower()
    tags = {'start': 'start center simulation cpx', '도서관': 'library', '식당': 'cafeteria', '회의실': 'meeting'}
    for key, val in tags.items():
        if key in name_str: return f"{name_str} {val}"
    return name_str

# --- 3. 안내판 우선순위 적용 ---
def apply_priority(df, selected_bldg):
    priority_map = {
        '의산연본관': ['실험동물', '세포치료', '연구센터', '대강당', '창업보육'],
        '성의회관': ['마리아홀', '안내실', '성당', '교목실', 'start', '도서관'],
        '대학본관': ['행정실', '회의실', '식당', '교육실', '시설팀'],
        '의산연별관': ['술기교육', '응용해부', '실습실', '법의학'],
        '병원별관': ['암연구소', '백신바이오', '면역질환', '행정사무실'],
        '옴니버스파크': ['푸드코트', '이마트24', '컨벤션', '카페']
    }
    df['sort_idx'] = 999
    # '전체보기'가 아닐 때만 특정 건물의 안내판 우선순위 적용
    if selected_bldg != "전체보기" and selected_bldg in priority_map:
        for i, target in enumerate(priority_map[selected_bldg]):
            df.loc[df['name'].astype(str).str.contains(target, case=False, na=False), 'sort_idx'] = i
    return df.sort_values(by=['sort_idx', 'building', 'floor', 'name']).drop(columns=['sort_idx'])

# --- 4. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # 세션 상태 초기화 (장바구니 기능)
    if 'favorites' not in st.session_state:
        st.session_state.favorites = []

    st.markdown("""
        <style>
        .m-title { font-size: 1.15rem; font-weight: bold; color: #1E3A8A; margin-bottom: 15px; }
        .result-row { padding: 10px 5px; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; }
        .loc-tag { background: #e7f1ff; border-radius: 4px; padding: 2px 5px; color: #007bff; font-weight: bold; font-size: 0.8rem; margin-right: 10px; min-width: 40px; text-align: center; }
        .bldg-info { font-size: 0.75rem; color: #888; margin-bottom: 2px; }
        .name-tag { font-weight: 500; color: #333; flex: 1; font-size: 0.92rem; }
        .fav-btn { cursor: pointer; border: none; background: none; font-size: 1.1rem; padding: 0 10px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='m-title'>🏥 성의교정 통합 안내 시스템</div>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        # 건물 선택 (전체보기 추가)
        bldg_options = ["전체보기"] + sorted(data['building'].unique().tolist())
        selected_bldg = st.selectbox("🏢 건물을 선택하세요", options=bldg_options)
        
        search_query = st.text_input("🔍 시설명, 호실, 또는 영문(Start 등) 검색")
        
        # 데이터 필터링
        if selected_bldg == "전체보기":
            view_df = data.copy()
        else:
            view_df = data[data['building'] == selected_bldg].copy()
            
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df['name'].astype(str).str.lower().str.contains(q) | 
                             view_df['name'].apply(get_search_tags).str.contains(q) |
                             view_df['room'].astype(str).str.contains(q)]
        
        view_df = apply_priority(view_df, selected_bldg)

        # --- 장바구니(관심 시설) 영역 ---
        if st.session_state.favorites:
            with st.expander("⭐ 관심 시설 (장바구니)", expanded=True):
                for fav in st.session_state.favorites:
                    st.write(f"[{fav['bldg']}] {fav['floor']} {fav['name']}")
                if st.button("장바구니 비우기"):
                    st.session_state.favorites = []
                    st.rerun()

        st.caption(f"📍 {len(view_df)}개 정보 검색됨")
        st.markdown("---")

        # 결과 리스트 출력
        for i, row in view_df.iterrows():
            name_str = str(row['name'])
            floor_display = format_floor(row.get('floor'))
            room_val = str(row.get('room', ''))
            bldg_name = str(row['building'])
            
            room_display = f"({room_val}호)" if room_val and room_val != 'nan' and room_val != '-' else ""
            
            # 한 줄 구성
            col1, col2 = st.columns([0.85, 0.15])
            with col1:
                st.markdown(f"""
                    <div class='result-row'>
                        <div class='loc-tag'>{floor_display}</div>
                        <div class='name-tag'>
                            <div class='bldg-info'>{bldg_name}</div>
                            {name_str} {room_display}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
            with col2:
                # 장바구니 담기 버튼
                if st.button("⭐", key=f"fav_{i}"):
                    fav_item = {"name": name_str, "bldg": bldg_name, "floor": floor_display}
                    if fav_item not in st.session_state.favorites:
                        st.session_state.favorites.append(fav_item)
                        st.rerun()
            
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
