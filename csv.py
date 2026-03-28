import pandas as pd
import streamlit as st
import re

# --- 1. 데이터 로드 및 전처리 (건물명 단축 및 핵심 시설 우선순위 강제 부여) ---
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
            
            # 건물명 4글자 제한 (성모병원, 의산연본, 성의회관, 옴니버스A/B)
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
    
    # [핵심 우선순위 로직] 방문객들이 가장 많이 찾는 시설(인포메이션) 최상단 고정
    def get_core_priority(row):
        name = str(row['name'])
        room = str(row.get('room', ''))
        # 0순위: 마리아홀, 대강당, 1002호 및 주요 대관/회의 시설
        if any(k in name for k in ['마리아', '대강당', '홀', '회의', '팀', '사무', '강의', '도서관']):
            return 0
        if '1002' in room:
            return 0
        # 2순위: 단순 설비 공간 (EPS, TPS, 공실 등)
        if any(k in name.lower() for k in ['eps', 'tps', '공실', '창고']):
            return 2
        # 1순위: 일반 연구실 및 기타
        return 1
        
    combined['priority'] = combined.apply(get_core_priority, axis=1)
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'])

# --- 2. 메인 UI ---
def main():
    # 모바일에서 타이틀이 개행되지 않도록 크기 축소
    st.set_page_config(page_title="성의안내", layout="centered")
    st.markdown("<h3 style='margin-bottom: 0.5rem;'>🏥 성의교정 시설 안내 (인포메이션)</h3>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        c_f1, c_f2 = st.columns([1, 1.5])
        with c_f1:
            selected_bldg = st.selectbox("🏢 건물", options=["전체보기"] + sorted(data['building'].unique().tolist()))
        with c_f2:
            search_query = st.text_input("🔍 검색(시설/호실/이름)", placeholder="예: 마리아홀, 김완욱")
        
        view_df = data.copy()
        if selected_bldg != "전체보기":
            view_df = view_df[view_df['building'] == selected_bldg]
            
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df.apply(lambda r: q in f"{r['name']} {r['room']} {r['description']} {r['building']}".lower(), axis=1)]
        
        # 정렬: 핵심순위 -> 건물명 -> 층(숫자 추출 정렬)
        view_df['floor_int'] = pd.to_numeric(view_df['floor'].astype(str).str.extract('(\\d+)', expand=False), errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['priority', 'building', 'floor_int'], ascending=[True, True, False])

        st.caption(f"📍 {len(view_df)}개의 결과를 찾았습니다.")
        st.divider()

        # --- 3. 출력 영역 (HTML 완전 제거 버전) ---
        for _, row in view_df.iterrows():
            with st.container():
                # [레이아웃 고정] [1: 3.5] 비율로 왼쪽 건물/층 정보와 오른쪽 시설 정보를 나눔
                c1, c2 = st.columns([1, 3.5])
                
                with c1:
                    # 건물명(4글자)을 굵게 강조
                    st.write(f"**:{row['building']}**")
                    # 층 표시에 'F'를 붙여 명확하게 표시 (예: 13F)
                    st.caption(f"{row['floor']}F")
                
                with c2:
                    # 시설명 + 호실 정보
                    room_val = str(row.get('room', ''))
                    # 호실 정보를 핑크색 굵은 글씨로 강조
                    room_info = f" <span style='color: #d63384; font-weight: bold; font-size: 0.85rem;'>({room_val}호)</span>" if room_val and room_val != 'nan' else ""
                    # 시설명은 굵게, 호실 정보와 함께 배치 (개행 방지)
                    st.markdown(f"**{row['name']}**{room_info}", unsafe_allow_html=True)
                    
                    # 비고(Description)가 있는 경우에만 '└' 표시와 함께 출력
                    desc = str(row.get('description', ''))
                    if desc and desc != 'nan' and desc.strip() != "":
                        # st.text는 HTML을 절대 해석하지 않으므로 보안상 가장 안전함
                        st.text(f"└ {desc}")
                
                st.divider() # 각 결과 사이 구분선
            
    else:
        st.error("데이터 로드 실패")

if __name__ == "__main__":
    main()
