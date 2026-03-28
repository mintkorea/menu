import pandas as pd
import streamlit as st
import os

# --- 0. 설정 파일 관리 ---
SETTINGS_FILE = "admin_settings.txt"
DEFAULT_KEYWORDS = "안내, 인포, 로비, 마리아, 대강당, 행정팀"

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
            return f.read().strip()
    return DEFAULT_KEYWORDS

def save_settings(content):
    with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
        f.write(content)

# --- 1. 세션 상태 초기화 ---
if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False
if 'priority_keywords' not in st.session_state:
    st.session_state.priority_keywords = load_settings()

# --- 2. 데이터 로드 및 전처리 ---
@st.cache_data
def load_and_clean_data():
    target_files = ['의산연본관.csv', '대학본관.csv', '의산연별관.csv', '성의회관.csv', '병원별관.csv', '옴니버스A.csv', '옴니버스B.csv', '서울성모병원.CSV']
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
    return pd.concat(all_dfs, ignore_index=True).dropna(subset=['name']) if all_dfs else None

# --- 3. 우선순위 및 정렬 로직 ---
def get_priority(row, selected_bldg, admin_keywords):
    name = str(row['name'])
    keywords = [k.strip() for k in admin_keywords.split(',') if k.strip()]
    for i, kw in enumerate(keywords):
        if kw in name:
            return i if (selected_bldg != "전체보기" and row['building'] == selected_bldg) else i + 10
    if any(k in name.lower() for k in ['eps', 'tps', '공실', '창고']): return 200
    return 100

# --- 4. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # CSS: 줄간격 균일화 및 왼쪽 정렬 강화
    st.markdown("""
        <style>
        .block-container { padding-top: 2.5rem !important; padding-bottom: 1rem !important; }
        .small-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 1rem; color: #1e3a8a; }
        
        /* 한 줄 레이아웃 최적화 */
        .info-row { 
            display: flex; 
            align-items: center; 
            padding: 4px 0; /* 줄간격 균일하게 고정 */
            border-bottom: 1px solid #f0f0f0; 
            gap: 10px; /* 요소 간 간격 */
        }
        
        .tag-bldg { 
            background-color: #f1f3f5; color: #495057; 
            font-weight: bold; font-size: 0.75rem; 
            padding: 2px 6px; border-radius: 4px; 
            width: 55px; text-align: center; flex-shrink: 0;
        }
        
        .tag-floor { 
            color: #0061f2; font-weight: 800; 
            font-size: 0.9rem; width: 35px; flex-shrink: 0;
        }
        
        /* 시설명을 왼쪽으로 밀착 */
        .tag-name-box { 
            flex-grow: 1; 
            text-align: left; 
            font-weight: 700; color: #1a1a1a; font-size: 0.92rem; 
            display: flex; align-items: center;
        }
        
        .tag-room { color: #e83e8c; font-weight: bold; font-size: 0.82rem; margin-left: 5px; }
        
        .sub-desc { font-size: 0.8rem; color: #868e96; padding-left: 105px; margin-top: 1px; margin-bottom: 3px; }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="small-title">🏥 성의교정 시설 안내</div>', unsafe_allow_html=True)
    
    data = load_and_clean_data()
    if data is not None:
        c1, c2 = st.columns([1, 1.5])
        with c1: selected_bldg = st.selectbox("건물", options=["전체보기"] + sorted(data['building'].unique().tolist()), label_visibility="collapsed")
        with c2: search_query = st.text_input("검색", placeholder="시설명/호실/이름", label_visibility="collapsed")

        view_df = data.copy()
        if selected_bldg != "전체보기": view_df = view_df[view_df['building'] == selected_bldg]
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df.apply(lambda r: q in f"{r['name']} {r.get('room','')} {r.get('description','')}".lower(), axis=1)]

        view_df['priority'] = view_df.apply(lambda r: get_priority(r, selected_bldg, st.session_state.priority_keywords), axis=1)
        view_df['floor_int'] = pd.to_numeric(view_df['floor'].astype(str).str.extract('(\\d+)', expand=False), errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['priority', 'floor_int', 'name'], ascending=[True, False, True])

        # 리스트 출력
        for _, row in view_df.iterrows():
            room_val = str(row.get('room', ''))
            room_html = f"<span class='tag-room'>({room_val}호)</span>" if room_val and room_val != 'nan' and room_val.strip() != "" else ""
            desc_val = str(row.get('description', '')).strip()
            
            # 메인 행 (좌측 정렬 구조)
            st.markdown(f"""
                <div class="info-row">
                    <span class="tag-bldg">{row['building']}</span>
                    <span class="tag-floor">{row['floor']}F</span>
                    <div class="tag-name-box">{row['name']}{room_html}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # 비고 (있는 경우만)
            if desc_val and desc_val.lower() != 'nan' and desc_val != "":
                st.markdown(f'<div class="sub-desc">└ {desc_val}</div>', unsafe_allow_html=True)

        # 관리자 모드 버튼 (비밀번호 1234)
        st.markdown("<br>", unsafe_allow_html=True)
        if not st.session_state.admin_mode:
            if st.button("🔒 Admin"): st.session_state.admin_pw_input = True
            if st.session_state.get('admin_pw_input'):
                pw = st.text_input("Password", type="password")
                if pw == "1234":
                    st.session_state.admin_mode = True
                    st.rerun()
        else:
            with st.expander("🛠 정렬 키워드 관리 (영구 저장)", expanded=True):
                new_kw = st.text_area("우선순위 키워드", value=st.session_state.priority_keywords)
                if st.button("💾 서버 저장"):
                    st.session_state.priority_keywords = new_kw
                    save_settings(new_kw)
                    st.success("저장 완료")
                    st.rerun()
                if st.button("로그아웃"):
                    st.session_state.admin_mode = False
                    st.rerun()
    else:
        st.error("데이터를 불러올 수 없습니다.")

if __name__ == "__main__":
    main()
