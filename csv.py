import pandas as pd
import streamlit as st
import re
import html

# --- 1. 데이터 로드 및 방문객 우선순위 부여 ---
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
            
            # 건물명 4글자 제한 (사용자 요청 반영)
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
    
    # [방문객 우선순위 로직] 인포메이션 게시용 대관/공용시설 최우선
    def get_visitor_priority(row):
        target = f"{row['name']} {row.get('description', '')}".lower()
        # 0순위: 외부인 방문 목적 (강당, 회의실, 홀, 센터, 사무실, 도서관)
        if any(k in target for k in ['강당', '회의', '홀', '센터', '사무', '팀', '강의', '도서', '식당', '카페']):
            return 0
        # 2순위: 단순 설비 및 비공개 공간 (EPS, TPS, 공실 등)
        if any(k in target for k in ['eps', 'tps', '공실', 'ps', '창고', '휀룸', '비트']):
            return 2
        # 1순위: 일반 연구실 및 기타
        return 1
        
    combined['priority'] = combined.apply(get_visitor_priority, axis=1)
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'])

# --- 2. 메인 UI 및 밀착 레이아웃 ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # CSS: 건물명-시설명 밀착 및 개행 방지
    st.markdown("""
        <style>
        .main-title { font-size: 1.25rem !important; font-weight: bold; color: #1E3A8A; margin-bottom: 15px; }
        .res-row { display: flex; align-items: flex-start; padding: 12px 0; border-bottom: 1px solid #eee; width: 100%; }
        /* 접두사(건물/층) 영역 너비를 75px로 줄여 시설명과 밀착 */
        .prefix-area { flex-shrink: 0; width: 75px; margin-right: 12px; line-height: 1.3; }
        .bldg-label { font-weight: bold; font-size: 0.82rem; color: #333; display: block; }
        .floor-label { font-size: 0.78rem; color: #007bff; font-weight: bold; }
        .main-area { flex: 1; min-width: 0; }
        .name-label { font-weight: 600; font-size: 1rem; color: #111; word-break: keep-all; }
        .room-label { color: #d63384; font-size: 0.88rem; font-weight: bold; }
        .desc-label { font-size: 0.82rem; color: #666; margin-top: 4px; border-left: 3px solid #f0f0f0; padding-left: 8px; line-height: 1.4; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='main-title'>🏥 성의교정 시설 안내 (인포메이션)</div>", unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        c1, c2 = st.columns([1, 1.2])
        with c1:
            selected_bldg = st.selectbox("🏢 건물 선택", options=["전체보기"] + sorted(data['building'].unique().tolist()))
        with c2:
            search_query = st.text_input("🔍 시설/호실/교수님 검색", placeholder="예: 마리아홀, 2016")
        
        view_df = data.copy()
        if selected_bldg != "전체보기":
            view_df = view_df[view_df['building'] == selected_bldg]
            
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df.apply(lambda r: q in f"{r['name']} {r['room']} {r['description']} {r['building']}".lower(), axis=1)]
        
        # [정렬 기준] 우선순위(방문객 시설) -> 건물명 -> 층(내림차순)
        view_df['floor_int'] = pd.to_numeric(view_df['floor'].astype(str).str.extract('(\\d+)', expand=False), errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['priority', 'building', 'floor_int'], ascending=[True, True, False])

        st.caption(f"📍 {len(view_df)}개의 시설이 검색되었습니다.")

        # --- 3. 데이터 출력 (HTML 노출 방지 처리) ---
        for _, row in view_df.iterrows():
            # 텍스트 안전 처리
            s_bldg = html.escape(str(row['building']))
            s_floor = html.escape(str(row['floor']))
            s_name = html.escape(str(row['name']))
            s_room = html.escape(str(row.get('room', '')))
            s_desc = html.escape(str(row.get('description', '')))

            room_tag = f" <span class='room-label'>({s_room}호)</span>" if s_room and s_room != 'nan' else ""
            
            # 상세정보(비고)가 있을 때만 렌더링
            desc_tag = ""
            if s_desc and s_desc != 'nan' and s_desc.strip() != "":
                desc_tag = f"<div class='desc-label'>{s_desc}</div>"

            st.markdown(f"""
                <div class='res-row'>
                    <div class='prefix-area'>
                        <span class='bldg-label'>{s_bldg}</span>
                        <span class='floor-label'>[{s_floor}]</span>
                    </div>
                    <div class='main-area'>
                        <div class='name-label'>{s_name}{room_tag}</div>
                        {desc_tag}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
    else:
        st.error("데이터를 불러올 수 없습니다.")

if __name__ == "__main__":
    main()
