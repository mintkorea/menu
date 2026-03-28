import pandas as pd
import streamlit as st
import re

# --- 1. 데이터 로드 및 전처리 ---
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
            
            # 파일명 기반으로 건물명 강제 매핑 (데이터 누락 대비)
            if '의산연본관' in file_path: df['building'] = '의산연본관'
            elif '성의회관' in file_path: df['building'] = '성의회관'
            elif '대학본관' in file_path: df['building'] = '대학본관'
            
            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except: continue
            
    if not all_dfs: return None
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')

# --- 2. 층 표시 정규화 ---
def format_floor(floor_val):
    if pd.isna(floor_val): return "-"
    clean_floor = re.sub(r'[^0-9BL]', '', str(floor_val).upper())
    return f"{clean_floor}F" if clean_floor else str(floor_val)

# --- 3. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    st.title("🏥 성의교정 통합 안내")
    
    data = load_and_clean_data()
    if data is not None:
        bldg_options = ["전체보기"] + sorted(data['building'].unique().tolist())
        selected_bldg = st.selectbox("🏢 건물 선택", options=bldg_options)
        search_query = st.text_input("🔍 시설명, 호실, 또는 검색어(교수님 성함 등) 입력")
        
        view_df = data.copy() if selected_bldg == "전체보기" else data[data['building'] == selected_bldg].copy()
        
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[
                view_df['name'].astype(str).str.lower().str.contains(q) | 
                view_df['room'].astype(str).str.lower().str.contains(q) | 
                view_df['description'].astype(str).str.lower().str.contains(q)
            ]
        
        # 정렬: 건물별 -> 층별(역순) -> 호실별
        view_df['floor_int'] = pd.to_numeric(view_df['floor'], errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['building', 'floor_int', 'room'], ascending=[True, False, True])

        st.info(f"📍 {len(view_df)}개의 결과를 찾았습니다.")

        for _, row in view_df.iterrows():
            with st.container():
                c1, c2 = st.columns([1, 6])
                
                with c1:
                    # 층수 표시
                    floor_txt = format_floor(row['floor'])
                    st.markdown(f"<div style='text-align: right; color: #007bff; font-weight: bold; margin-top: 5px;'>[{floor_txt}]</div>", unsafe_allow_html=True)
                
                with c2:
                    # [건물명] 시설명 (호실) 구조
                    bldg_name = f"<span style='color: #666; font-size: 0.8rem; font-weight: normal;'>[{row['building']}]</span> "
                    room_val = str(row.get('room', ''))
                    room_info = f" <span style='color: #d63384; font-size: 0.85rem; font-weight: bold;'>({room_val}호)</span>" if room_val and room_val != 'nan' else ""
                    
                    st.markdown(f"<div style='font-weight: 600; font-size: 1rem;'>{bldg_name}{row['name']}{room_info}</div>", unsafe_allow_html=True)
                    
                    # 비고(Description)
                    desc = str(row.get('description', ''))
                    if desc and desc != 'nan' and desc.strip() != "":
                        st.caption(f"└ {desc}")
                
                st.divider()
            
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
