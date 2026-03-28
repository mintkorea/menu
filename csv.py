import pandas as pd
import streamlit as st
import re

# --- 1. 데이터 로드 (이전과 동일) ---
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

def format_floor(floor_val):
    if pd.isna(floor_val): return "-"
    clean_floor = re.sub(r'[^0-9BL]', '', str(floor_val).upper())
    return f"{clean_floor}F" if clean_floor else str(floor_val)

# --- 2. 메인 UI 및 스타일 ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # 모바일 대응 CSS: 타이틀 축소 및 결과 리스트 밀착
    st.markdown("""
        <style>
        /* 타이틀 크기 축소 */
        .main-title { font-size: 1.4rem !important; font-weight: bold; color: #1E3A8A; margin-bottom: 10px; }
        
        /* 결과 행 레이아웃 (플렉스박스) */
        .res-container { display: flex; align-items: flex-start; padding: 10px 0; border-bottom: 1px solid #f0f0f0; }
        .floor-box { 
            color: #007bff; font-weight: bold; font-size: 0.9rem; 
            min-width: 45px; margin-right: 10px; text-align: left; flex-shrink: 0;
        }
        .content-box { flex: 1; min-width: 0; }
        .name-txt { font-weight: 600; font-size: 0.95rem; color: #333; line-height: 1.3; }
        .bldg-txt { color: #888; font-size: 0.75rem; font-weight: normal; }
        .room-txt { color: #d63384; font-size: 0.85rem; font-weight: bold; }
        .desc-txt { color: #666; font-size: 0.8rem; margin-top: 2px; }
        </style>
    """, unsafe_allow_html=True)

    # 타이틀 (아이콘 크기도 소폭 조정)
    st.markdown("<div class='main-title'>🏥 성의교정 통합 안내</div>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        bldg_options = ["전체보기"] + sorted(data['building'].unique().tolist())
        selected_bldg = st.selectbox("🏢 건물", options=bldg_options)
        search_query = st.text_input("🔍 검색어(시설/호실/이름)", placeholder="예: 도서관, 1002, 김완욱")
        
        view_df = data.copy() if selected_bldg == "전체보기" else data[data['building'] == selected_bldg].copy()
        
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[
                view_df['name'].astype(str).str.lower().str.contains(q) | 
                view_df['room'].astype(str).str.lower().str.contains(q) | 
                view_df['description'].astype(str).str.lower().str.contains(q)
            ]
        
        view_df['floor_int'] = pd.to_numeric(view_df['floor'], errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['building', 'floor_int', 'room'], ascending=[True, False, True])

        st.caption(f"📍 {len(view_df)}개 결과")

        # --- 출력 (HTML 구조 개선) ---
        for _, row in view_df.iterrows():
            floor_disp = format_floor(row['floor'])
            bldg_disp = row['building']
            room_val = str(row.get('room', ''))
            room_disp = f" <span class='room-txt'>({room_val}호)</span>" if room_val and room_val != 'nan' else ""
            desc_val = str(row.get('description', ''))
            desc_disp = f"<div class='desc-txt'>└ {desc_val}</div>" if desc_val and desc_val != 'nan' and desc_val.strip() != "" else ""

            st.markdown(f"""
                <div class='res-container'>
                    <div class='floor-box'>[{floor_disp}]</div>
                    <div class='content-box'>
                        <div class='name-txt'>
                            <span class='bldg-txt'>[{bldg_disp}]</span> {row['name']}{room_disp}
                        </div>
                        {desc_disp}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
