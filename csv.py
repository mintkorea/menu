import pandas as pd
import streamlit as st
import os

# --- 0. 설정 파일 경로 및 로드 함수 ---
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

# --- 1. 초기 세션 상태 설정 ---
if 'admin_mode' not in st.session_state:
    st.session_state.admin_mode = False
# 앱 시작 시 파일에서 키워드 불러오기
if 'priority_keywords' not in st.session_state:
    st.session_state.priority_keywords = load_settings()

# --- [데이터 로드 및 우선순위 로직은 이전과 동일] ---
@st.cache_data
def load_and_clean_data():
    # (기존 데이터 로드 로직 동일...)
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

def get_priority(row, selected_bldg, admin_keywords):
    name = str(row['name'])
    keywords = [k.strip() for k in admin_keywords.split(',') if k.strip()]
    for i, kw in enumerate(keywords):
        if kw in name:
            return i if (selected_bldg != "전체보기" and row['building'] == selected_bldg) else i + 10
    if any(k in name.lower() for k in ['eps', 'tps', '공실', '창고']): return 200
    return 100

# --- 2. 메인 UI ---
def main():
    st.set_page_config(page_title="성의안내", layout="centered")
    
    # CSS (생략 - 이전과 동일)
    st.markdown("<style>.block-container { padding-top: 3.5rem !important; } .small-title { font-size: 1.1rem; font-weight: bold; margin-bottom: 1rem; color: #1e3a8a; border-left: 5px solid #1e3a8a; padding-left: 12px; }</style>", unsafe_allow_html=True)
    st.markdown('<div class="small-title">🏥 성의교정 시설 안내 시스템</div>', unsafe_allow_html=True)

    data = load_and_clean_data()
    if data is not None:
        c1, c2 = st.columns([1, 1.5])
        with c1: selected_bldg = st.selectbox("건물", options=["전체보기"] + sorted(data['building'].unique().tolist()), label_visibility="collapsed")
        with c2: search_query = st.text_input("검색", placeholder="시설명, 이름, 호실", label_visibility="collapsed")

        view_df = data.copy()
        if selected_bldg != "전체보기": view_df = view_df[view_df['building'] == selected_bldg]
        if search_query:
            q = search_query.lower().strip()
            view_df = view_df[view_df.apply(lambda r: q in f"{r['name']} {r.get('room','')} {r.get('description','')}".lower(), axis=1)]

        # 정렬 시 파일에서 불러온 키워드 사용
        view_df['priority'] = view_df.apply(lambda r: get_priority(r, selected_bldg, st.session_state.priority_keywords), axis=1)
        view_df['floor_int'] = pd.to_numeric(view_df['floor'].astype(str).str.extract('(\\d+)', expand=False), errors='coerce').fillna(0)
        view_df = view_df.sort_values(by=['priority', 'floor_int', 'name'], ascending=[True, False, True])

        # 리스트 출력 (중략 - 이전과 동일한 렌더링 로직)
        for _, row in view_df.iterrows():
            room_val = str(row.get('room', ''))
            room_html = f"<span style='color: #d63384; font-weight: bold; margin-left: 4px; font-size: 0.85rem;'>({room_val}호)</span>" if room_val and room_val != 'nan' else ""
            st.markdown(f"**{row['building']} {row['floor']}F** {row['name']}{room_html}", unsafe_allow_html=True)
            desc = str(row.get('description', ''))
            if desc and desc != 'nan': st.caption(f"└ {desc}")
            st.divider()

        # --- 관리자 모드 (하단) ---
        if not st.session_state.admin_mode:
            if st.button("🔒 관리자 모드"): st.session_state.admin_pw_input = True
            if st.session_state.get('admin_pw_input'):
                pw = st.text_input("비밀번호", type="password")
                if pw == "1234":
                    st.session_state.admin_mode = True
                    st.rerun()
        else:
            with st.expander("🛠 관리자 설정 (영구 저장)", expanded=True):
                new_keywords = st.text_area("우선순위 키워드 수정", value=st.session_state.priority_keywords)
                if st.button("💾 서버에 저장"):
                    st.session_state.priority_keywords = new_keywords
                    save_settings(new_keywords) # 파일에 쓰기
                    st.success("설정이 서버에 영구 저장되었습니다.")
                    st.rerun()
                if st.button("로그아웃"):
                    st.session_state.admin_mode = False
                    st.rerun()

if __name__ == "__main__":
    main()
