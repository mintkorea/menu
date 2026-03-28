import pandas as pd
import streamlit as st
import re

# --- 1. 데이터 로드 및 전처리 (건물명 단축 및 우선순위 부여) ---
@st.cache_data
def load_and_clean_data():
    target_files = [
        '의산연본관.csv', '대학본관.csv', '의산연별관.csv', '성의회관.csv', 
        '병원별관.csv', '옴니버스A.csv', '옴니버스B.csv', '서울성모병원.CSV'
    ]
    all_dfs = []
    for file_path in target_files:
        try:
            try: df = pd.read_csv(file_path, encoding='utf-8-sig')
            except: df = pd.read_csv(file_path, encoding='cp949')
            df.columns = [str(c).strip().lower() for c in df.columns]
            rename_map = {'건물명': 'building', '시설명': 'name', '이름': 'name', '호실': 'room', '층': 'floor', '비고': 'description'}
            df = df.rename(columns=rename_map)
            
            # 건물명 단축 로직
            f_name = file_path.upper()
            if '의산연본관' in f_name: b_name = "의산연본"
            elif '성의회관' in f_name: b_name = "성의회관"
            elif '서울성모병원' in f_name: b_name = "성모병원"
            elif '옴니버스A' in f_name: b_name = "옴니버스A"
            elif '옴니버스B' in f_name: b_name = "옴니버스B"
            else: b_name = df['building'].iloc[0][:4] if 'building' in df.columns else "기타"
            df['building'] = b_name
            
            all_dfs.append(df)
        except: continue
    
    if not all_dfs: return None
    combined = pd.concat(all_dfs, ignore_index=True, sort=False).dropna(subset=['name'])
    
    # [우선순위 로직] 사람들이 자주 찾는 시설(교수실, 사무실, 강의실 등)에 가중치 부여
    def get_priority(row):
        name = str(row['name'])
        desc = str(row.get('description', ''))
        # 중요 키워드가 포함되면 0순위, 단순 시설(EPS, TPS 등)은 1순위
        if any(k in name or k in desc for k in ['교수', '실장', '사무', '강의', '팀', '센터']):
            return 0
        return 1
        
    combined['priority'] = combined.apply(get_priority, axis=1)
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'])

# --- 2. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # 모바일에서 한 줄 유지를 위한 강제 CSS
    st.markdown("""
        <style>
        .main-title { font-size: 1.2rem !important; font-weight: bold; margin-bottom: 10px; }
        .row-container { display: flex; align-items: flex-start; padding: 10px 0; border-bottom: 1px solid #eee; }
        .left-info { width: 85px; flex-shrink: 0; margin-right: 10px; }
        .bldg-label { font-weight: bold; font-size: 0.8rem; color: #495057; display: block; }
        .floor-label { font-size: 0.75rem; color: #007bff; }
        .right-info { flex: 1; min-width: 0; }
        .name-label { font-weight: 600; font-size: 0.95rem; display: block; }
        .room-label { color: #d63384; font-size: 0.85rem; font-weight: bold; }
        .desc-label { font-size: 0.8rem; color: #666; margin-top: 2px; line-height: 1.2; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>🏥 성의교정 시설 안내</div>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        col1, col2 = st.columns([1, 1.5])
        with col1:
            selected_bldg = st.selectbox("🏢 건물", options=["전체보기"] + sorted(data['building'].unique().tolist()))
        with col2:
            search_query = st.text_input("🔍 검색", placeholder="교수님 성함, 호실 등")
        
        view_df = data.copy()
        if selected_bldg != "전체보기":
            view_df = view_df[view_df['building'] == selected_bldg]
            
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df.apply(lambda r: q in f"{r['name']} {r['room']} {r['description']}".lower(), axis=1)]
        
        # [정렬 기준 변경] 우선순위(교수실 등) -> 건물명 -> 층(내림차순)
        view_df['floor_int'] = pd.to_numeric(view_df['floor'].astype(str).str.extract('(\\d+)', expand=False), errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['priority', 'building', 'floor_int'], ascending=[True, True, False])

        st.caption(f"📍 {len(view_df)}개 결과")

        # --- 3. 출력 (Flexbox를 사용하여 모바일 한 줄 유지) ---
        for _, row in view_df.iterrows():
            room_info = f"<span class='room-label'>({row['room']}호)</span>" if pd.notna(row['room']) and str(row['room']) != 'nan' else ""
            desc_info = f"<div class='desc-label'>└ {row['description']}</div>" if pd.notna(row['description']) and str(row['description']).strip() != "" and str(row['description']) != 'nan' else ""
            
            # st.markdown 하나에 모든 구조를 담아 태그 깨짐 방지
            st.markdown(f"""
                <div class='row-container'>
                    <div class='left-info'>
                        <span class='bldg-label'>{row['building']}</span>
                        <span class='floor-label'>[{row['floor']}]</span>
                    </div>
                    <div class='right-info'>
                        <span class='name-label'>{row['name']}{room_info}</span>
                        {desc_info}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
