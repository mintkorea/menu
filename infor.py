import pandas as pd
import streamlit as st
import re

# --- 1. 데이터 로드 및 통합 (원본 8개 파일 읽기) ---
@st.cache_data
def load_and_clean_data():
    target_files = [
        '의산연01.csv', '대학본관.csv', '의산연별관.csv', '성의회관.csv', 
        '병원별관.csv', '옴니버스A.csv', '옴니버스B.csv', '서울성모병원.CSV'
    ]
    all_dfs = []
    for file_path in target_files:
        try:
            # 인코딩 대응
            try: df = pd.read_csv(file_path, encoding='utf-8-sig')
            except: df = pd.read_csv(file_path, encoding='cp949')
            
            # 컬럼명 소문자화 및 표준화 (AttributeError 방지)
            df.columns = [str(c).strip().lower() for c in df.columns]
            rename_map = {'건물명': 'building', '시설명': 'name', '이름': 'name', '호실': 'room', '층': 'floor'}
            df = df.rename(columns=rename_map)
            
            # 파일명 기반 건물명 강제 할당 (데이터 누락 방지)
            if '의산연01' in file_path: df['building'] = '의산연본관'
            elif '대학본관' in file_path: df['building'] = '대학본관'
            elif '의산연별관' in file_path: df['building'] = '의산연별관'
            elif '성의회관' in file_path: df['building'] = '성의회관'
            elif '병원별관' in file_path: df['building'] = '병원별관'
            elif '옴니버스' in file_path: df['building'] = '옴니버스파크'
            elif 'building' not in df.columns: df['building'] = file_path.split('.')[0]
            
            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except: continue
            
    if not all_dfs: return None
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    
    # [데이터 클렌징] 제목행 중복 제거 및 .str.lower() 에러 방지
    if 'name' in combined.columns:
        combined = combined[combined['name'].astype(str).str.lower() != 'name']
    
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')

# --- 2. 유틸리티: 층 표시 정규화 및 영문 검색 매핑 ---
def format_floor(floor_val):
    if pd.isna(floor_val): return "-"
    # 숫자, B, L만 추출하여 'FF' 중복 현상 원천 차단
    clean_floor = re.sub(r'[^0-9BL]', '', str(floor_val).upper())
    return f"{clean_floor}F" if clean_floor else str(floor_val)

def get_search_tags(name):
    name_str = str(name).lower()
    tags = {'start': 'start center simulation cpx', '도서관': 'library', '식당': 'cafeteria', '회의실': 'meeting'}
    for key, val in tags.items():
        if key in name_str: return f"{name_str} {val}"
    return name_str

# --- 3. 안내판 기반 인덱스 우선순위 정렬 ---
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
    if selected_bldg != "전체보기" and selected_bldg in priority_map:
        for i, target in enumerate(priority_map[selected_bldg]):
            df.loc[df['name'].astype(str).str.contains(target, case=False, na=False), 'sort_idx'] = i
    return df.sort_values(by=['sort_idx', 'building', 'floor', 'name']).drop(columns=['sort_idx'])

# --- 4. 메인 UI 및 다운로드 기능 ---
def main():
    st.set_page_config(page_title="성의안내 관리자", layout="centered")
    
    # CSS 스타일 (리스트 가독성 최적화)
    st.markdown("""
        <style>
        .m-title { font-size: 1.15rem; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
        .result-row { padding: 10px 5px; border-bottom: 1px solid #f0f0f0; display: flex; align-items: center; }
        .loc-tag { background: #e7f1ff; border-radius: 4px; padding: 2px 5px; color: #007bff; font-weight: bold; font-size: 0.8rem; margin-right: 10px; min-width: 40px; text-align: center; }
        .bldg-info { font-size: 0.75rem; color: #888; margin-bottom: 2px; }
        .name-tag { font-weight: 500; color: #333; flex: 1; font-size: 0.92rem; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='m-title'>🏥 성의교정 통합 안내 (관리자 모드)</div>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    
    if data is not None:
        # [핵심] 일괄 다운로드 버튼 배치
        csv_bytes = data.to_csv(index=False, encoding='utf-8-sig').encode('utf-8-sig')
        st.download_button(
            label="📥 전체 데이터(8개 파일 합본) 다운로드",
            data=csv_bytes,
            file_name='성의교정_전체데이터_검수용.csv',
            mime='text/csv',
            help="클릭하면 8개 원본 파일이 합쳐진 전체 데이터를 엑셀용 CSV로 내려받습니다."
        )
        
        st.markdown("---")
        
        # 건물 선택 및 검색
        bldg_options = ["전체보기"] + sorted(data['building'].unique().tolist())
        selected_bldg = st.selectbox("🏢 건물을 선택하세요", options=bldg_options)
        search_query = st.text_input("🔍 시설명, 호실, 또는 영문(Start 등) 검색")
        
        # 데이터 필터링 로직
        view_df = data.copy() if selected_bldg == "전체보기" else data[data['building'] == selected_bldg].copy()
            
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df['name'].astype(str).str.lower().str.contains(q) | 
                             view_df['name'].apply(get_search_tags).str.contains(q) |
                             view_df['room'].astype(str).str.contains(q)]
        
        view_df = apply_priority(view_df, selected_bldg)
        st.caption(f"📍 현재 화면에 {len(view_df)}개의 정보가 노출 중입니다.")

        # 결과 리스트 출력
        for _, row in view_df.iterrows():
            name_str = str(row['name'])
            floor_display = format_floor(row.get('floor'))
            room_val = str(row.get('room', ''))
            bldg_name = str(row['building'])
            room_display = f"({room_val}호)" if room_val and room_val != 'nan' and room_val != '-' else ""
            
            is_info = any(kw in name_str.lower() for kw in ['센터', '연구소', '홀', '실', '팀', '식당'])
            icon = "📢" if is_info else "📍"
            
            st.markdown(f"""
                <div class='result-row'>
                    <div class='loc-tag'>{floor_display}</div>
                    <div class='name-tag'>
                        <div class='bldg-info'>[{bldg_name}]</div>
                        {icon} {name_str} {room_display}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error("데이터 로드 실패. CSV 파일들을 확인해 주세요.")

if __name__ == "__main__":
    main()
