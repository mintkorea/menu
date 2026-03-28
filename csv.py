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
    
    # [데이터 정제] 제목행 제거 및 중복 제거
    if 'name' in combined.columns:
        combined = combined[combined['name'].astype(str).str.lower() != 'name']
    
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')

# --- 2. 층 표시 최적화 함수 (FF 중복 방지) ---
def format_floor(floor_val):
    if pd.isna(floor_val): return "-"
    # 숫자, B, L만 남기고 나머지(F 등) 제거 후 뒤에 F 붙임
    clean_floor = re.sub(r'[^0-9BL]', '', str(floor_val).upper())
    return f"{clean_floor}F" if clean_floor else str(floor_val)

# --- 3. 영문/별칭 매핑 ---
def get_search_tags(name):
    name_str = str(name).lower()
    tags = {'start': 'start center simulation cpx', '도서관': 'library', '식당': 'cafeteria', '회의실': 'meeting'}
    for key, val in tags.items():
        if key in name_str: return f"{name_str} {val}"
    return name_str

# --- 4. 안내판 기반 인덱스 우선순위 ---
def apply_priority(df, selected_bldg):
    priority_map = {
        '의산연본관': ['실험동물', '세포치료', '연구센터', '대강당', '창업보육', '관제실'],
        '성의회관': ['마리아홀', '안내실', '성당', '교목실', 'start', '도서관', '게스트'],
        '대학본관': ['행정실', '회의실', '식당', '교육실', '시설팀'],
        '의산연별관': ['술기교육', '응용해부', '실습실', '법의학'],
        '병원별관': ['암연구소', '백신바이오', '면역질환', '행정사무실'],
        '옴니버스파크': ['푸드코트', '이마트24', '컨벤션', '카페']
    }
    df['sort_idx'] = 999
    if selected_bldg in priority_map:
        for i, target in enumerate(priority_map[selected_bldg]):
            df.loc[df['name'].astype(str).str.contains(target, case=False, na=False), 'sort_idx'] = i
    return df.sort_values(by=['sort_idx', 'floor', 'name']).drop(columns=['sort_idx'])

# --- 5. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # 스타일 시트
    st.markdown("""
        <style>
        .m-title { font-size: 1.15rem; font-weight: bold; color: #1E3A8A; margin-bottom: 15px; }
        .result-row { 
            padding: 12px 8px; border-bottom: 1px solid #f0f0f0; display: flex; align-items: flex-start;
        }
        .loc-tag { 
            background: #e7f1ff; border-radius: 4px; padding: 2px 8px; 
            color: #007bff; font-weight: bold; font-size: 0.85rem; margin-right: 12px; white-space: nowrap;
            min-width: 40px; text-align: center;
        }
        .name-tag { font-weight: 500; color: #333; flex: 1; font-size: 0.95rem; }
        .room-info { color: #999; font-size: 0.8rem; margin-left: 6px; font-weight: normal; }
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
        
        view_df = apply_priority(view_df, selected_bldg)
        
        st.caption(f"📍 {len(view_df)}개 정보 로드됨")
        st.markdown("---")

        for _, row in view_df.iterrows():
            name_str = str(row['name'])
            # [수정] 층 표시 정규화 적용 (FF 방지)
            floor_display = format_floor(row.get('floor'))
            room_val = str(row.get('room', ''))
            
            room_display = f"{room_val}호" if room_val and room_val != 'nan' and room_val != '-' else ""
            
            is_info = any(kw in name_str.lower() for kw in ['센터', '연구소', '홀', '실', '팀', '식당'])
            icon = "📢" if is_info else "📍"
            
            st.markdown(f"""
                <div class='result-row'>
                    <div class='loc-tag'>{floor_display}</div>
                    <div class='name-tag'>
                        {icon} {name_str} <span class='room-info'>{room_display}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
