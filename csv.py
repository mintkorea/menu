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

            # 컬럼 표준화
            df.columns = [str(c).strip().lower() for c in df.columns]
            rename_dict = {'building_name': 'building', '건물명': 'building', '시설명': 'name', '이름': 'name'}
            df = df.rename(columns=rename_dict)
            
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

    # 불순물 제거 및 중복 제거
    if 'building' in combined.columns:
        combined = combined[combined['building'].astype(str).lower() != 'building']
    if 'name' in combined.columns:
        combined = combined[combined['name'].astype(str).lower() != 'name']
    
    subset_cols = [c for c in ['name', 'building', 'floor', 'room'] if c in combined.columns]
    combined = combined.drop_duplicates(subset=subset_cols, keep='first')
    
    return combined

# --- 2. [스마트 카테고리 분류] ---
def add_smart_category(df):
    def classify(val):
        val = str(val)
        if '교수' in val: return '👨‍🏫 교수연구실'
        elif '연구' in val or '연구소' in val: return '🧪 연구시설'
        elif '강의' in val or '세미나' in val: return '📖 교육시설'
        elif '실험' in val: return '🔬 실험시설'
        elif '회의' in val: return '🤝 회의실'
        elif '지원' in val or '사무' in val: return '📁 행정지원'
        return '🏢 기타시설'

    if 'name' in df.columns:
        df['category'] = df['name'].apply(classify)
    return df

# --- 3. [메인 화면 실행] ---
st.set_page_config(page_title="성의교정 시설 가이드", layout="wide")
st.title("🏥 성의교정 시설 통합 안내 시스템")

final_df = get_final_clean_data()

if final_df is not None:
    final_df = add_smart_category(final_df)
    
    # 상단 요약 지표 (1,158개 반영 확인)
    st.success(f"✅ 총 **{len(final_df)}개**의 시설 데이터가 성공적으로 통합되었습니다.")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("전체 시설", f"{len(final_df)}개")
    col2.metric("성의회관(갱신)", f"{len(final_df[final_df['building'] == '성의회관'])}개")
    col3.metric("교수/연구실", f"{len(final_df[final_df['category'].isin(['👨‍🏫 교수연구실', '🧪 연구시설'])])}개")

    # [A] 통합 검색 및 필터 구역
    st.write("---")
    c1, c2 = st.columns([1, 2])
    with c1:
        cat_list = ['전체'] + sorted(final_df['category'].unique().tolist())
        selected_cat = st.selectbox("📌 시설 유형 필터", options=cat_list)
    with c2:
        search_input = st.text_input("🔍 키워드 검색 (성함, 호실, 시설명 등)", placeholder="예: 김교수, 2016, 대강당")

    # 필터링 적용
    view_df = final_df.copy()
    if selected_cat != '전체':
        view_df = view_df[view_df['category'] == selected_cat]
    if search_input:
        s = search_input.lower()
        mask = view_df['name'].astype(str).str.lower().str.contains(s)
        if 'building' in view_df.columns: mask |= view_df['building'].astype(str).str.lower().str.contains(s)
        if 'room' in view_df.columns: mask |= view_df['room'].astype(str).str.lower().str.contains(s)
        view_df = view_df[mask]

    # [B] 결과 테이블
    st.write(f"조회 결과: **{len(view_df)}건**")
    show_cols = [c for c in ['name', 'building', 'floor', 'room', 'category', 'description'] if c in view_df.columns]
    st.dataframe(view_df[show_cols], use_container_width=True)

    # [C] 관리자용 데이터 내려받기
    st.write("---")
    csv_data = view_df.to_csv(index=False).encode('utf-8-sig')
    st.download_button(
        label="📥 현재 검색 결과 CSV로 저장하기",
        data=csv_data,
        file_name='성의교정_시설목록_추출.csv',
        mime='text/csv',
    )
else:
    st.error("데이터를 불러오지 못했습니다. CSV 파일명을 다시 확인해 주세요.")
