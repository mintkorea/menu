import pandas as pd
import streamlit as st
import re

# --- 1. 데이터 로드 및 전처리 (파일명 변경 반영) ---
@st.cache_data
def load_and_clean_data():
    # 관리자님이 지정하신 최신 파일명 체계
    target_files = [
        '의산연본관.csv', '대학본관.csv', '의산연별관.csv', '성의회관.csv', 
        '병원별관.csv', '옴니버스A.csv', '옴니버스B.csv', '서울성모병원.CSV'
    ]
    all_dfs = []
    
    for file_path in target_files:
        try:
            try: df = pd.read_csv(file_path, encoding='utf-8-sig')
            except: df = pd.read_csv(file_path, encoding='cp949')
            
            # 컬럼명 표준화
            df.columns = [str(c).strip().lower() for c in df.columns]
            rename_map = {'건물명': 'building', '시설명': 'name', '이름': 'name', '호실': 'room', '층': 'floor'}
            df = df.rename(columns=rename_map)
            
            # 건물명 수동 매핑 (데이터 내 building 컬럼이 틀릴 경우 대비)
            if '의산연본관' in file_path: df['building'] = '의산연본관'
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
    
    # [중복 제거] 시설명, 건물, 층, 호실이 모두 일치하는 완전 중복만 제거
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')

# --- 2. 층 표시 및 검색 태그 ---
def format_floor(floor_val):
    if pd.isna(floor_val): return "-"
    # 숫자/B/L만 추출하여 FF 중복 방지
    clean_floor = re.sub(r'[^0-9BL]', '', str(floor_val).upper())
    return f"{clean_floor}F" if clean_floor else str(floor_val)

def get_search_tags(row):
    # 시설명 + 호실 + 비고(description)를 모두 합쳐 검색 가능하게 함
    name = str(row.get('name', '')).lower()
    room = str(row.get('room', '')).lower()
    desc = str(row.get('description', '')).lower()
    return f"{name} {room} {desc}"

# --- 3. 메인 UI ---
def main():
    st.set_page_config(page_title="성의교정 안내", layout="centered")
    
    st.markdown("""
        <style>
        .m-title { font-size: 1.15rem; font-weight: bold; color: #1E3A8A; margin-bottom: 15px; }
        .result-row { padding: 12px 8px; border-bottom: 1px solid #f0f0f0; display: flex; align-items: flex-start; }
        .loc-tag { 
            background: #e7f1ff; border-radius: 4px; padding: 2px 8px; 
            color: #007bff; font-weight: bold; font-size: 0.85rem; margin-right: 12px;
            min-width: 45px; text-align: center;
        }
        .name-tag { font-weight: 500; color: #333; flex: 1; font-size: 0.95rem; }
        .room-info { color: #d63384; font-size: 0.85rem; font-weight: bold; margin-left: 5px; }
        .desc-text { color: #888; font-size: 0.8rem; display: block; margin-top: 2px; font-weight: normal; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='m-title'>🏥 성의교정 통합 안내 시스템 (최신본)</div>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        bldg_options = ["전체보기"] + sorted(data['building'].unique().tolist())
        selected_bldg = st.selectbox("🏢 건물을 선택하세요", options=bldg_options)
        search_query = st.text_input("🔍 시설명, 호실, 또는 인물(교수님 등) 검색")
        
        view_df = data.copy() if selected_bldg == "전체보기" else data[data['building'] == selected_bldg].copy()
        
        if search_query:
            q = search_query.lower().strip()
            # 이름, 호실, 설명(교수명 등)에서 모두 검색
            view_df = view_df[view_df.apply(lambda r: q in get_search_tags(r), axis=1)]
        
        # 층별 정렬
        view_df = view_df.sort_values(by=['building', 'floor', 'room'])
        
        st.caption(f"📍 {len(view_df)}개의 장소를 찾았습니다.")
        st.markdown("---")

        for _, row in view_df.iterrows():
            floor_display = format_floor(row.get('floor'))
            name_str = str(row['name'])
            room_val = str(row.get('room', ''))
            desc_val = str(row.get('description', ''))
            
            room_display = f"<span class='room-info'>{room_val}호</span>" if room_val and room_val != 'nan' else ""
            desc_display = f"<span class='desc-text'>{desc_val}</span>" if desc_val and desc_val != 'nan' else ""
            
            st.markdown(f"""
                <div class='result-row'>
                    <div class='loc-tag'>{floor_display}</div>
                    <div class='name-tag'>
                        {name_str} {room_display}
                        {desc_display}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("데이터 파일을 읽을 수 없습니다. 파일명을 확인해 주세요.")

if __name__ == "__main__":
    main()
