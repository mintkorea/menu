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
            
            if '의산연본관' in file_path: df['building'] = '의산연본관'
            elif '성의회관' in file_path: df['building'] = '성의회관'
            
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

# --- 3. 통합 검색용 텍스트 생성 ---
def get_search_corpus(row):
    fields = [row.get('name', ''), row.get('room', ''), row.get('description', ''), row.get('category', '')]
    return " ".join([str(f).lower() for f in fields if pd.notna(f)])

# --- 4. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # CSS 스타일 (박스 밀림 및 태그 노출 방지)
    st.markdown("""
        <style>
        .m-title { font-size: 1.15rem; font-weight: bold; color: #1E3A8A; margin-bottom: 15px; }
        .result-row { 
            padding: 12px 8px; 
            border-bottom: 1px solid #f0f0f0; 
            display: flex; 
            align-items: flex-start;
            width: 100%;
        }
        .loc-tag { 
            background: #e7f1ff; border-radius: 4px; padding: 2px 8px; 
            color: #007bff; font-weight: bold; font-size: 0.85rem; margin-right: 12px;
            min-width: 45px; text-align: center; flex-shrink: 0;
        }
        .info-container { flex: 1; min-width: 0; }
        .name-line { font-weight: 600; color: #333; font-size: 0.98rem; display: block; word-break: break-all; }
        .room-tag { color: #d63384; font-size: 0.85rem; margin-left: 6px; font-weight: bold; }
        .desc-line { 
            color: #666; font-size: 0.82rem; margin-top: 4px; 
            line-height: 1.4; border-left: 2px solid #ddd; padding-left: 8px;
            word-break: break-all;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='m-title'>🏥 성의교정 통합 안내</div>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        bldg_options = ["전체보기"] + sorted(data['building'].unique().tolist())
        selected_bldg = st.selectbox("🏢 건물 선택", options=bldg_options)
        search_query = st.text_input("🔍 시설명, 호실, 또는 검색어(교수님 성함 등) 입력")
        
        view_df = data.copy() if selected_bldg == "전체보기" else data[data['building'] == selected_bldg].copy()
        
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df.apply(lambda r: q in get_search_corpus(r), axis=1)]
        
        # 층수 정렬
        view_df['floor_int'] = pd.to_numeric(view_df['floor'], errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['building', 'floor_int', 'room'], ascending=[True, False, True])

        st.caption(f"📍 {len(view_df)}개의 결과를 찾았습니다.")
        st.markdown("---")

        for _, row in view_df.iterrows():
            floor_disp = format_floor(row.get('floor'))
            name_str = str(row['name'])
            room_val = str(row.get('room', ''))
            desc_val = str(row.get('description', ''))
            
            # 텍스트 정제 (HTML 깨짐 방지)
            room_text = f" <span class='room-tag'>{room_val}호</span>" if room_val and room_val != 'nan' else ""
            
            # description이 있을 때만 div를 생성하고, 없을 때는 아예 생성하지 않음
            desc_html = ""
            if desc_val and desc_val != 'nan' and desc_val.strip() != "":
                desc_html = f"<div class='desc-line'>{desc_val}</div>"
            
            # f-string 내부에 div 태그가 정확히 닫혔는지 확인
            st.markdown(f"""
                <div class='result-row'>
                    <div class='loc-tag'>{floor_disp}</div>
                    <div class='info-container'>
                        <div class='name-line'>{name_str}{room_text}</div>
                        {desc_html}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
