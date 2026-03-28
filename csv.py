import pandas as pd
import streamlit as st

# --- 1. [데이터 통합 함수] ---
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

            # 컬럼명 소문자화 및 공백 제거 (AttributeError 방지)
            df.columns = [str(c).strip().lower() for c in df.columns]
            
            rename_map = {
                'building_name': 'building', '건물명': 'building', 
                '시설명': 'name', '이름': 'name', '시설': 'name'
            }
            df = df.rename(columns=rename_map)
            
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
    
    # 제목행 제거 및 중복 제거
    if 'building' in combined.columns:
        combined = combined[combined['building'].astype(str).str.lower() != 'building']
    
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

# --- 3. [메인 실행 및 UI 최적화] ---
st.set_page_config(page_title="성의교정 안내", layout="centered") # 모바일을 위해 centered 설정

st.title("🏥 성의교정 시설 안내")

final_df = get_final_clean_data()

if final_df is not None:
    final_df = add_smart_category(final_df)
    
    # 모바일용 상단 간략 정보
    st.info(f"📍 총 **{len(final_df)}개** 시설 정보 통합 완료")
    
    # 검색 및 필터 (모바일은 세로 배치가 기본)
    selected_cat = st.selectbox("📌 유형 선택", options=['전체'] + sorted(final_df['category'].unique().tolist()))
    search_q = st.text_input("🔍 검색 (성함, 호실, 시설명)", placeholder="예: 홍길동, 2016")

    # 데이터 필터링
    view_df = final_df.copy()
    if selected_cat != '전체':
        view_df = view_df[view_df['category'] == selected_cat]
    if search_q:
        q = search_q.lower()
        mask = view_df['name'].astype(str).str.lower().str.contains(q)
        if 'building' in view_df.columns: mask |= view_df['building'].astype(str).str.lower().str.contains(s)
        if 'room' in view_df.columns: mask |= view_df['room'].astype(str).str.lower().str.contains(q)
        view_df = view_df[mask]

    # [C] 모바일 최적화 결과 보기
    st.write(f"결과: **{len(view_df)}건**")
    
    # 모바일에서 표가 너무 넓을 경우를 대비해 탭으로 구분하거나 간소화된 표 제공
    tab1, tab2 = st.tabs(["📋 간략히 보기", "📑 상세 표 보기"])
    
    with tab1:
        # 모바일용 카드 스타일 리스트 (주요 정보 위주)
        for _, row in view_df.head(50).iterrows(): # 성능을 위해 상위 50개만 카드형으로 표시
            with st.expander(f"📍 {row['name']}"):
                st.write(f"**건물:** {row.get('building', '-')}")
                st.write(f"**위치:** {row.get('floor', '-')}층 {row.get('room', '-')}호")
                st.write(f"**분류:** {row.get('category', '-')}")

    with tab2:
        # 기존 상세 표 (가로 스크롤 가능)
        show_cols = [c for c in ['name', 'building', 'floor', 'room'] if c in view_df.columns]
        st.dataframe(view_df[show_cols], use_container_width=True)

    # 하단 다운로드 버튼 (모바일에서도 작동)
    csv_data = view_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button("📥 검색 결과 저장", csv_data, "extract.csv", "text/csv", use_container_width=True)

else:
    st.error("데이터를 불러올 수 없습니다.")
