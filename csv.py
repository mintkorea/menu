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
            
            # 건물명 정규화
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

# --- 2. 우선순위 로직 함수 ---
def get_priority(row, selected_bldg):
    name = str(row['name'])
    desc = str(row.get('description', ''))
    
    # [0순위] 선택된 건물의 안내데스크/로비/주요시설 (가장 먼저 보여야 함)
    if selected_bldg != "전체보기" and row['building'] == selected_bldg:
        if any(k in name for k in ['안내', '인포', '로비', '센터', '데스크']):
            return 0
            
    # [1순위] 공통 주요 시설 (마리아홀, 대강당 등)
    if any(k in name for k in ['마리아', '대강당', '강당', '홀', '도서관', '은행', '편의점']):
        return 1
    
    # [3순위] 기계실, EPS, 공실 등 (가장 나중)
    if any(k in name.lower() for k in ['eps', 'tps', '공실', '창고', '기계실', '전기실']):
        return 3
        
    # [2순위] 일반 연구실 및 사무실
    return 2

# --- 3. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # 커스텀 CSS (카드 디자인 및 폰트 조절)
    st.markdown("""
        <style>
        .main { background-color: #f8f9fa; }
        .stActionButton { visibility: hidden; }
        .result-card {
            background-color: white; padding: 15px; border-radius: 10px;
            border-left: 5px solid #004b9d; margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }
        .bldg-tag { background-color: #e9ecef; padding: 2px 8px; border-radius: 4px; font-size: 0.8rem; color: #495057; font-weight: bold; }
        .floor-tag { color: #004b9d; font-weight: bold; font-size: 1rem; }
        </style>
    """, unsafe_allow_html=True)

    st.title("🏥 성의교정 스마트 인포")
    
    data = load_and_clean_data()
    if data is not None:
        # 필터 레이아웃
        col1, col2 = st.columns([1, 1])
        with col1:
            selected_bldg = st.selectbox("🏢 건물 선택", options=["전체보기"] + sorted(data['building'].unique().tolist()))
        with col2:
            search_query = st.text_input("🔍 시설명 검색", placeholder="예: 마리아홀, 교수실")

        # 필터링 로직
        view_df = data.copy()
        if selected_bldg != "전체보기":
            view_df = view_df[view_df['building'] == selected_bldg]
        
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df.apply(lambda r: q in f"{r['name']} {r.get('room','')} {r.get('description','')}".lower(), axis=1)]

        # 정렬 로직 적용
        view_df['priority'] = view_df.apply(lambda r: get_priority(r, selected_bldg), axis=1)
        view_df['floor_int'] = pd.to_numeric(view_df['floor'].astype(str).str.extract('(\\d+)', expand=False), errors='coerce').fillna(0)
        
        # 우선순위 -> 층수(높은순) 정렬
        view_df = view_df.sort_values(by=['priority', 'floor_int'], ascending=[True, False])

        st.caption(f"총 {len(view_df)}개의 시설이 검색되었습니다.")
        st.divider()

        # 결과 출력 (카드형 레이아웃)
        for _, row in view_df.iterrows():
            with st.container():
                room_val = str(row.get('room', ''))
                room_str = f"({room_val}호)" if room_val and room_val != 'nan' else ""
                
                # HTML을 활용한 카드 UI 구현
                st.markdown(f"""
                <div class="result-card">
                    <span class="bldg-tag">{row['building']}</span> <span class="floor-tag">{row['floor']}F</span>
                    <div style="margin-top: 8px;">
                        <span style="font-size: 1.1rem; font-weight: bold;">{row['name']}</span>
                        <span style="color: #d63384; font-weight: bold;">{room_str}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # 비고는 가독성을 위해 별도 표시
                desc = str(row.get('description', ''))
                if desc and desc != 'nan' and desc.strip() != "":
                    st.caption(f"&nbsp;&nbsp;&nbsp;&nbsp;└ {desc}")
                
    else:
        st.error("데이터 파일을 찾을 수 없습니다. CSV 파일들을 확인해주세요.")

if __name__ == "__main__":
    main()
