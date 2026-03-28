import pandas as pd
import streamlit as st

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
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'])

# --- 2. 우선순위 로직 ---
def get_priority(row, selected_bldg):
    name = str(row['name'])
    # 선택된 건물의 주요 시설(안내/인포)을 0순위로
    if selected_bldg != "전체보기" and row['building'] == selected_bldg:
        if any(k in name for k in ['안내', '인포', '데스크', '로비']): return 0
    # 공통 주요 시설
    if any(k in name for k in ['마리아', '대강당', '강당', '홀', '도서관']): return 1
    # 설비 및 공실
    if any(k in name.lower() for k in ['eps', 'tps', '공실', '창고']): return 3
    return 2

# --- 3. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # CSS: 타이트한 줄 간격 및 폰트 설정
    st.markdown("""
        <style>
        .small-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 0.8rem; color: #333; }
        .info-container { border-bottom: 1px solid #f0f0f0; padding: 6px 0; }
        /* 첫 번째 줄: 핵심 정보 전용 */
        .main-line { display: flex; align-items: center; font-size: 0.9rem; gap: 8px; }
        .b-tag { color: #666; font-weight: bold; min-width: 55px; }
        .f-tag { color: #004b9d; font-weight: bold; min-width: 30px; }
        .n-tag { font-weight: 600; color: #000; flex-shrink: 1; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
        .r-tag { color: #d63384; font-weight: bold; margin-left: auto; }
        /* 두 번째 줄: 비고 전용 */
        .sub-line { font-size: 0.8rem; color: #777; margin-top: 2px; padding-left: 8px; }
        .block-container { padding-top: 2rem !important; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="small-title">🏥 성의교정 시설 안내</div>', unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        c1, c2 = st.columns([1, 1.5])
        with c1:
            selected_bldg = st.selectbox("🏢 건물", options=["전체보기"] + sorted(data['building'].unique().tolist()), label_visibility="collapsed")
        with c2:
            search_query = st.text_input("🔍 검색", placeholder="시설/호실/이름", label_visibility="collapsed")

        view_df = data.copy()
        if selected_bldg != "전체보기":
            view_df = view_df[view_df['building'] == selected_bldg]
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df.apply(lambda r: q in f"{r['name']} {r.get('room','')} {r.get('description','')}".lower(), axis=1)]

        # 우선순위 정렬: 중요도 -> 건물 -> 층(내림차순)
        view_df['priority'] = view_df.apply(lambda r: get_priority(r, selected_bldg), axis=1)
        view_df['floor_int'] = pd.to_numeric(view_df['floor'].astype(str).str.extract('(\\d+)', expand=False), errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['priority', 'building', 'floor_int'], ascending=[True, True, False])

        st.caption(f"결과: {len(view_df)}건")

        # 결과 렌더링
        for _, row in view_df.iterrows():
            room_val = str(row.get('room', ''))
            room_str = f"{room_val}호" if room_val and room_val != 'nan' else ""
            desc_val = str(row.get('description', '')).strip()
            
            # HTML 출력
            main_line = f"""
                <div class="info-container">
                    <div class="main-line">
                        <span class="b-tag">{row['building']}</span>
                        <span class="f-tag">{row['floor']}F</span>
                        <span class="n-tag">{row['name']}</span>
                        <span class="r-tag">{room_str}</span>
                    </div>
            """
            
            # 비고가 있을 때만 두 번째 줄 추가
            sub_line = ""
            if desc_val and desc_val.lower() != 'nan' and desc_val != "":
                sub_line = f'<div class="sub-line">└ {desc_val}</div>'
            
            st.markdown(main_line + sub_line + "</div>", unsafe_allow_html=True)
            
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
