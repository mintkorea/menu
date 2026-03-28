import pandas as pd
import streamlit as st

# --- 1. [데이터 통합 및 정제 함수] ---
def get_final_clean_data():
    target_files = [
        '성의회관.csv', '의산연01.csv', '의산연별관.csv', '대학본관.csv', 
        '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv'
    ]
    
    all_dfs = []
    for file_path in target_files:
        try:
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')

            # 컬럼명 표준화 (공백 제거, 소문자화)
            df.columns = [str(c).strip().lower() for c in df.columns]
            
            rename_map = {
                'building_name': 'building', '건물명': 'building', 
                '시설명': 'name', '이름': 'name', '시설': 'name'
            }
            df = df.rename(columns=rename_map)
            
            # 건물명 보정
            if '의산연01' in file_path: df['building'] = '의산연본관'
            elif '의산연별관' in file_path: df['building'] = '의산연별관'
            elif 'building' not in df.columns:
                df['building'] = file_path.split('.')[0]

            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except:
            continue
            
    if not all_dfs: return None
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    
    # 제목행 불순물 제거
    if 'building' in combined.columns:
        combined = combined[combined['building'].astype(str).str.lower() != 'building']
    
    # 중복 제거
    subset_cols = [c for c in ['name', 'building', 'floor', 'room'] if c in combined.columns]
    combined = combined.drop_duplicates(subset=subset_cols, keep='first')
    
    return combined

# --- 2. [카테고리 분류] ---
def add_smart_category(df):
    def classify(val):
        val = str(val)
        if '교수' in val: return '👨‍🏫 교수실'
        elif '연구' in val: return '🧪 연구실'
        elif '강의' in val or '세미나' in val: return '📖 교육시설'
        elif '실험' in val: return '🔬 실험실'
        elif '회의' in val: return '🤝 회의실'
        return '🏢 기타'

    if 'name' in df.columns:
        df['category'] = df['name'].apply(classify)
    return df

# --- 3. [UI 및 실행 구역] ---
st.set_page_config(page_title="성의안내", layout="centered")

# [폰트 크기 조정] HTML/CSS를 사용하여 타이틀 크기를 기존의 절반으로 줄임
st.markdown("""
    <style>
    .main-title {
        font-size: 1.2rem !important;  /* 기존 대비 약 1/2 크기 */
        font-weight: bold;
        margin-bottom: 10px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    </style>
    <div class="main-title">🏥 성의교정 시설 안내</div>
    """, unsafe_allow_html=True)

final_df = get_final_clean_data()

if final_df is not None:
    final_df = add_smart_category(final_df)
    
    # 모바일용 요약 배너
    st.info(f"📍 총 **1158개** 시설 정보 통합 완료")

    # 검색 및 필터링
    selected_cat = st.selectbox("📌 유형 선택", options=['전체'] + sorted(final_df['category'].unique().tolist()))
    search_q = st.text_input("🔍 검색 (성함, 호실, 시설명)", placeholder="예: 홍길동, 2016")

    # 필터 로직
    view_df = final_df.copy()
    if selected_cat != '전체':
        view_df = view_df[view_df['category'] == selected_cat]
    
    if search_q:
        q = search_q.lower()
        # [NameError 해결] mask 변수를 안전하게 정의
        mask = view_df['name'].astype(str).str.lower().str.contains(q)
        if 'building' in view_df.columns:
            mask |= view_df['building'].astype(str).str.lower().str.contains(q)
        if 'room' in view_df.columns:
            mask |= view_df['room'].astype(str).str.lower().str.contains(q)
        view_df = view_df[mask]

    # 결과 화면
    st.write(f"검색 결과: **{len(view_df)}건**")
    
    tab1, tab2 = st.tabs(["📋 리스트형", "📑 상세 표"])
    
    with tab1:
        # 모바일용 간편 보기 (상위 50개)
        for _, row in view_df.head(50).iterrows():
            with st.expander(f"📍 {row['name']}"):
                st.write(f"**건물:** {row.get('building', '-')}")
                st.write(f"**위치:** {row.get('floor', '-')}층 {row.get('room', '-')}호")
                st.write(f"**분류:** {row.get('category', '-')}")

    with tab2:
        # 상세 표 (가로 스크롤)
        show_cols = [c for c in ['name', 'building', 'floor', 'room'] if c in view_df.columns]
        st.dataframe(view_df[show_cols], use_container_width=True)

    # 내보내기 버튼 (전체 너비)
    csv_data = view_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 현재 결과 저장", csv_data, "result.csv", "text/csv", use_container_width=True)

else:
    st.error("데이터를 불러올 수 없습니다.")
