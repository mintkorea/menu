import pandas as pd
import streamlit as st
import re

# --- 1. 데이터 로드 및 건물명 단축/세분화 ---
@st.cache_data
def load_and_clean_data():
    target_files = [
        '의산연본관.csv', '대학본관.csv', '의산연별관.csv', '성의회관.csv', 
        '병원별관.csv', '옴니버스A.csv', '옴니버스B.csv', '서울성모병원.CSV'
    ]
    all_dfs = []
    for file_path in target_files:
        try:
            # 인코딩 처리
            try: df = pd.read_csv(file_path, encoding='utf-8-sig')
            except: df = pd.read_csv(file_path, encoding='cp949')
            
            df.columns = [str(c).strip().lower() for c in df.columns]
            rename_map = {'건물명': 'building', '시설명': 'name', '이름': 'name', '호실': 'room', '층': 'floor', '비고': 'description'}
            df = df.rename(columns=rename_map)
            
            # 건물명 단축 및 옴니버스 A/B 분리 로직
            f_name = file_path.upper()
            if '의산연본관' in f_name: b_name = "의산연본"
            elif '성의회관' in f_name: b_name = "성의회관"
            elif '대학본관' in f_name: b_name = "대학본관"
            elif '서울성모병원' in f_name: b_name = "성모병원"
            elif '옴니버스A' in f_name: b_name = "옴니버스A"
            elif '옴니버스B' in f_name: b_name = "옴니버스B"
            elif '병원별관' in f_name: b_name = "병원별관"
            else: b_name = df['building'].iloc[0][:4] if 'building' in df.columns else "기타"
            
            df['building'] = b_name
            
            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except: continue
    
    if not all_dfs: return None
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')

# --- 2. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # 타이틀 크기 축소 (모바일 대응)
    st.markdown("<h3 style='margin-bottom:0;'>🏥 성의교정 시설 안내</h3>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        # 필터 영역
        bldg_options = ["전체보기"] + sorted(data['building'].unique().tolist())
        c_f1, c_f2 = st.columns([1, 2])
        with c_f1:
            selected_bldg = st.selectbox("🏢 건물", options=bldg_options)
        with c_f2:
            search_query = st.text_input("🔍 검색(시설/호실/성함)", placeholder="예: 옴니버스 2016")
        
        view_df = data.copy() if selected_bldg == "전체보기" else data[data['building'] == selected_bldg].copy()
        
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[
                view_df['building'].astype(str).str.lower().str.contains(q) |
                view_df['name'].astype(str).str.lower().str.contains(q) | 
                view_df['room'].astype(str).str.lower().str.contains(q) | 
                view_df['description'].astype(str).str.lower().str.contains(q)
            ]
        
        # 정렬: 건물명 -> 층(숫자추출 정렬) -> 호실
        view_df['floor_int'] = pd.to_numeric(view_df['floor'].astype(str).str.extract('(\\d+)', expand=False), errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['building', 'floor_int', 'room'], ascending=[True, False, True])

        st.caption(f"📍 {len(view_df)}개 결과")
        st.divider()

        # --- 3. 출력 영역 (HTML 노출 원천 차단 방식) ---
        for _, row in view_df.iterrows():
            # 층수/건물명(중요정보)와 시설상세로 분리
            col_left, col_right = st.columns([1, 3])
            
            with col_left:
                # 건물명(4글자)을 굵게 강조
                st.write(f"**:{row['building']}**")
                # 층 정보는 아래에 작게
                st.caption(f"[{row['floor']}]")
            
            with col_right:
                # 시설명과 호실 정보
                r_val = str(row.get('room', ''))
                r_info = f" ({r_val}호)" if r_val and r_val != 'nan' else ""
                st.markdown(f"**{row['name']}**{r_info}")
                
                # 비고(Description) - st.text는 HTML을 절대 해석하지 않음
                desc = str(row.get('description', ''))
                if desc and desc != 'nan' and desc.strip() != "":
                    st.text(f"└ {desc}")
            
            st.divider()
            
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
