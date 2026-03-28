import pandas as pd
import streamlit as st
import re
import html

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
            
            # 건물명 강제 매핑 (파일명 기준)
            if '의산연본관' in file_path: df['building'] = '의산연본관'
            elif '성의회관' in file_path: df['building'] = '성의회관'
            
            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except: continue
    if not all_dfs: return None
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')

# --- 2. 메인 UI 및 스타일 (건물명 강조) ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    st.markdown("""
        <style>
        .main-title { font-size: 1.3rem !important; font-weight: bold; color: #1E3A8A; margin-bottom: 8px; }
        
        /* 건물명 강조 레이아웃 */
        .res-container { display: flex; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid #eee; }
        
        /* 건물명 박스: 가장 왼쪽, 배경색으로 강조 */
        .bldg-box { 
            background: #f1f3f5; color: #495057; font-weight: bold; font-size: 0.75rem; 
            padding: 3px 6px; border-radius: 4px; min-width: 75px; text-align: center;
            margin-right: 12px; flex-shrink: 0; line-height: 1.2;
        }
        
        .content-box { flex: 1; min-width: 0; }
        
        /* 층수와 시설명 배치 */
        .floor-txt { color: #007bff; font-weight: bold; font-size: 0.85rem; margin-right: 5px; }
        .name-txt { font-weight: 600; font-size: 1rem; color: #212529; }
        .room-txt { color: #d63384; font-size: 0.9rem; font-weight: bold; margin-left: 3px; }
        .desc-txt { color: #747d8c; font-size: 0.82rem; margin-top: 4px; border-left: 2px solid #e9ecef; padding-left: 8px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>🏥 성의교정 시설 안내</div>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        bldg_options = ["전체보기"] + sorted(data['building'].unique().tolist())
        selected_bldg = st.selectbox("🏢 건물 선택", options=bldg_options)
        search_query = st.text_input("🔍 시설명, 호실, 교수님 성함 검색", placeholder="예: 의산연본관 2016")
        
        view_df = data.copy() if selected_bldg == "전체보기" else data[data['building'] == selected_bldg].copy()
        
        if search_query:
            q = search_query.lower().strip()
            # 검색 범위: 건물명 포함
            view_df = view_df[
                view_df['building'].astype(str).str.lower().str.contains(q) |
                view_df['name'].astype(str).str.lower().str.contains(q) | 
                view_df['room'].astype(str).str.lower().str.contains(q) | 
                view_df['description'].astype(str).str.lower().str.contains(q)
            ]
        
        # 건물 -> 층(역순) -> 호실 순 정렬
        view_df['floor_int'] = pd.to_numeric(view_df['floor'].astype(str).str.extract('(\\d+)', expand=False), errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['building', 'floor_int', 'room'], ascending=[True, False, True])

        st.caption(f"📍 {len(view_df)}개 결과")

        for _, row in view_df.iterrows():
            # [HTML 보안] 데이터 내 특수문자가 태그로 해석되지 않도록 이스케이프 처리
            bldg = html.escape(str(row['building']))
            name = html.escape(str(row['name']))
            floor = html.escape(str(row.get('floor', '-')))
            room = html.escape(str(row.get('room', '')))
            desc = html.escape(str(row.get('description', '')))

            room_disp = f"<span class='room-txt'>({room}호)</span>" if room and room != 'nan' else ""
            desc_disp = f"<div class='desc-txt'>{desc}</div>" if desc and desc != 'nan' and desc.strip() != "" else ""

            st.markdown(f"""
                <div class='res-container'>
                    <div class='bldg-box'>{bldg}</div>
                    <div class='content-box'>
                        <div class='name-txt'>
                            <span class='floor-txt'>[{floor}]</span>{name}{room_disp}
                        </div>
                        {desc_disp}
                    </div>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
