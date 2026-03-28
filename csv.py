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
    # 선택된 건물의 로비/안내 시설 최우선(0)
    if selected_bldg != "전체보기" and row['building'] == selected_bldg:
        if any(k in name for k in ['안내', '인포', '데스크', '로비']): return 0
    # 주요 공용 시설(1)
    if any(k in name for k in ['마리아', '대강당', '강당', '홀', '도서관']): return 1
    # 기피 시설(3)
    if any(k in name.lower() for k in ['eps', 'tps', '공실', '창고']): return 3
    return 2

# --- 3. 메인 UI ---
def main():
    # 좁은 간격을 위해 padding 최적화
    st.set_page_config(page_title="성의안내", layout="centered")
    
    st.markdown("""
        <style>
        /* 타이틀 크기 절반 축소 및 상단 여백 제거 */
        .small-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 0.5rem; color: #333; }
        /* 리스트 항목 간격 최소화 */
        .info-row { 
            display: flex; align-items: center; border-bottom: 1px solid #eee; 
            padding: 4px 0; font-size: 0.85rem; line-height: 1.2;
        }
        .tag-bldg { color: #666; width: 60px; font-weight: bold; flex-shrink: 0; }
        .tag-floor { color: #004b9d; width: 35px; font-weight: bold; flex-shrink: 0; }
        .tag-name { flex-grow: 1; font-weight: 500; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
        .tag-room { color: #d63384; font-weight: bold; margin-left: 4px; flex-shrink: 0; }
        .tag-desc { color: #888; font-size: 0.75rem; margin-left: 8px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 30%; }
        /* 스트림릿 기본 여백 제거 */
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

        # 필터링 및 정렬
        view_df = data.copy()
        if selected_bldg != "전체보기":
            view_df = view_df[view_df['building'] == selected_bldg]
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df.apply(lambda r: q in f"{r['name']} {r.get('room','')} {r.get('description','')}".lower(), axis=1)]

        view_df['priority'] = view_df.apply(lambda r: get_priority(r, selected_bldg), axis=1)
        view_df['floor_int'] = pd.to_numeric(view_df['floor'].astype(str).str.extract('(\\d+)', expand=False), errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['priority', 'floor_int'], ascending=[True, False])

        st.caption(f"검색 결과: {len(view_df)}건")

        # 한 줄 출력 영역
        for _, row in view_df.iterrows():
            room_val = str(row.get('room', ''))
            room_str = f"{room_val}" if room_val and room_val != 'nan' else ""
            desc_val = str(row.get('description', ''))
            desc_str = f"| {desc_val}" if desc_val and desc_val != 'nan' else ""
            
            st.markdown(f"""
                <div class="info-row">
                    <span class="tag-bldg">{row['building']}</span>
                    <span class="tag-floor">{row['floor']}F</span>
                    <span class="tag-name">{row['name']}</span>
                    <span class="tag-room">{room_str}</span>
                    <span class="tag-desc">{desc_str}</span>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
