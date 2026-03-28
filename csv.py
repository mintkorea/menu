import pandas as pd
import streamlit as st

# --- 1. [데이터 통합 및 표준화 함수] ---
def get_final_clean_data():
    target_files = [
        '성의회관.csv', '의산연01.csv', '의산연별관.csv', '대학본관.csv', 
        '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv'
    ]
    
    all_dfs = []
    for file_path in target_files:
        try:
            # 파일 읽기 (인코딩 대응)
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')

            # [해결책] 컬럼명의 공백을 제거하고 모두 소문자로 변경
            df.columns = [str(c).strip().lower() for c in df.columns]
            
            # 유사 컬럼명들을 'building'과 'name'으로 강제 통일
            rename_map = {
                'building_name': 'building', '건물명': 'building', 
                '시설명': 'name', '이름': 'name', '시설': 'name'
            }
            df = df.rename(columns=rename_map)
            
            # 건물명 보정 (의산연 본관/별관 분리 및 누락 보정)
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
        
    # 데이터 통합
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)

    # [에러 방어] 'building' 컬럼이 확실히 있을 때만 제목행 제거 로직 실행
    if 'building' in combined.columns:
        combined = combined[combined['building'].astype(str).str.lower() != 'building']
    
    # 중복 데이터 제거
    subset_cols = [c for c in ['name', 'building', 'floor', 'room'] if c in combined.columns]
    combined = combined.drop_duplicates(subset=subset_cols, keep='first')
    
    return combined

# --- 2. [교수실/연구실 자동 카테고리화] ---
def add_smart_category(df):
    def classify(val):
        val = str(val)
        if '교수' in val: return '👨‍🏫 교수연구실'
        elif '연구' in val or '연구소' in val: return '🧪 연구시설'
        elif '강의' in val or '세미나' in val: return '📖 교육시설'
        elif '실험' in val: return '🔬 실험시설'
        elif '회의' in val: return '🤝 회의실'
        return '🏢 기타시설'

    if 'name' in df.columns:
        df['category'] = df['name'].apply(classify)
    return df

# --- 3. [메인 화면 구성] ---
st.set_page_config(page_title="성의교정 시설 가이드", layout="wide")
st.title("🏥 성의교정 시설 통합 안내 시스템")

final_df = get_final_clean_data()

if final_df is not None:
    final_df = add_smart_category(final_df)
    
    # 상단 요약 지표 (1,158개 확인용)
    st.success(f"✅ 총 **{len(final_df)}개**의 시설 데이터가 통합되었습니다.")
    
    # [A] 검색 및 필터링
    st.write("### 🔍 시설 통합 검색")
    col1, col2 = st.columns([1, 2])
    with col1:
        # 카테고리 필터
        cat_list = ['전체'] + sorted(final_df['category'].unique().tolist())
        selected_cat = st.selectbox("유형 필터", options=cat_list)
    with col2:
        # 자유 검색어
        search_q = st.text_input("검색어 입력 (교수님 성함, 호실, 시설명)", placeholder="예: 홍길동, 2016, 대강당")

    # 필터링 적용
    view_df = final_df.copy()
    if selected_cat != '전체':
        view_df = view_df[view_df['category'] == selected_cat]
    if search_q:
        q = search_q.lower()
        mask = view_df['name'].astype(str).str.lower().str.contains(q)
        if 'building' in view_df.columns: mask |= view_df['building'].astype(str).str.lower().str.contains(q)
        if 'room' in view_df.columns: mask |= view_df['room'].astype(str).str.lower().str.contains(q)
        view_df = view_df[mask]

    # [B] 결과 테이블 출력
    st.write(f"결과: **{len(view_df)}건**")
    show_cols = [c for c in ['name', 'building', 'floor', 'room', 'category', 'description'] if c in view_df.columns]
    st.dataframe(view_df[show_cols], use_container_width=True)

    # [C] 데이터 추출 기능
    st.write("---")
    csv_data = view_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 현재 목록 CSV로 저장",
        data=csv_data,
        file_name='성의교정_시설목록.csv',
        mime='text/csv',
    )
else:
    st.error("데이터를 불러올 수 없습니다. CSV 파일들을 확인해 주세요.")
