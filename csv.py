import pandas as pd
import streamlit as st

# --- 1. 데이터 로드 및 전처리 ---
@st.cache_data
def load_and_clean_data():
    # 실제 환경에 맞는 파일명 리스트
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
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'])

# --- 2. 우선순위 계산 로직 (관리자 설정 반영) ---
def get_priority(row, selected_bldg, admin_keywords):
    name = str(row['name'])
    
    # 관리자가 입력한 키워드 순서대로 우선순위 부여 (쉼표 구분 입력)
    keywords = [k.strip() for k in admin_keywords.split(',') if k.strip()]
    
    for i, kw in enumerate(keywords):
        if kw in name:
            # 선택된 건물의 핵심 시설인 경우 최상단(0~), 타 건물은 뒤로(+10)
            return i if (selected_bldg != "전체보기" and row['building'] == selected_bldg) else i + 10
            
    # 비선호 시설 (항상 최하단)
    if any(k in name.lower() for k in ['eps', 'tps', '공실', '창고', '기계실']):
        return 200
        
    return 100 # 일반 시설

# --- 3. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # CSS: 레이아웃 및 여백 최적화
    st.markdown("""
        <style>
        .block-container { padding-top: 4rem !important; }
        .small-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 1rem; color: #1e3a8a; border-left: 5px solid #1e3a8a; padding-left: 12px; line-height: 1; }
        .info-container { border-bottom: 1px solid #eee; padding: 6px 0; }
        .main-line { display: flex; align-items: baseline; font-size: 0.9rem; gap: 8px; }
        .tag-bldg { color: #666; font-weight: bold; min-width: 55px; font-size: 0.8rem; }
        .tag-floor { color: #004b9d; font-weight: 800; min-width: 32px; }
        .tag-name-room { font-weight: 600; color: #000; flex-grow: 1; display: flex; align-items: center; }
        .tag-room-inline { color: #d63384; font-weight: bold; margin-left: 5px; font-size: 0.85rem; }
        .sub-line { font-size: 0.8rem; color: #777; margin-top: 2px; padding-left: 12px; }
        </style>
    """, unsafe_allow_html=True)

    # --- 관리자 설정 사이드바 ---
    with st.sidebar:
        st.header("⚙️ 관리자 설정")
        admin_keywords = st.text_area(
            "우선순위 키워드 (쉼표 구분)", 
            value="안내, 인포, 로비, 마리아, 대강당, 행정팀",
            help="여기에 적힌 순서대로 검색 결과 상단에 노출됩니다."
        )
        st.info("💡 위 키워드가 포함된 시설이 건물 선택 시 최상단에 배치됩니다.")

    st.markdown('<div class="small-title">🏥 성의교정 시설 안내 시스템</div>', unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        c1, c2 = st.columns([1, 1.5])
        with c1:
            selected_bldg = st.selectbox("건물", options=["전체보기"] + sorted(data['building'].unique().tolist()), label_visibility="collapsed")
        with c2:
            search_query = st.text_input("검색", placeholder="시설명, 이름, 호실 검색", label_visibility="collapsed")

        view_df = data.copy()
        
        # 필터링
        if selected_bldg != "전체보기":
            view_df = view_df[view_df['building'] == selected_bldg]
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df.apply(lambda r: q in f"{r['name']} {r.get('room','')} {r.get('description','')}".lower(), axis=1)]

        # 정렬 로직 (관리자 지정 키워드 반영)
        view_df['priority'] = view_df.apply(lambda r: get_priority(r, selected_bldg, admin_keywords), axis=1)
        view_df['floor_int'] = pd.to_numeric(view_df['floor'].astype(str).str.extract('(\\d+)', expand=False), errors='coerce').fillna(0)
        
        # 우선순위 -> 층수(내림차순) 순 정렬
        view_df = view_df.sort_values(by=['priority', 'floor_int', 'name'], ascending=[True, False, True])

        st.caption(f"📍 총 {len(view_df)}개의 정보가 검색되었습니다.")

        # 결과 렌더링
        for _, row in view_df.iterrows():
            room_val = str(row.get('room', ''))
            room_html = f"<span class='tag-room-inline'>({room_val}호)</span>" if room_val and room_val != 'nan' else ""
            desc_val = str(row.get('description', '')).strip()
            
            st.markdown(f"""
                <div class="info-container">
                    <div class="main-line">
                        <span class="tag-bldg">{row['building']}</span>
                        <span class="tag-floor">{row['floor']}F</span>
                        <div class="tag-name-room">{row['name']}{room_html}</div>
                    </div>
                """, unsafe_allow_html=True)
            
            if desc_val and desc_val.lower() != 'nan' and desc_val != "":
                st.markdown(f'<div class="sub-line">└ {desc_val}</div>', unsafe_allow_html=True)
            
            st.markdown("</div>", unsafe_allow_html=True)
            
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
