import pandas as pd
import streamlit as st

# --- 1. [데이터 통합 함수] ---
def get_final_clean_data():
    # 대상 파일 리스트 (성의회관.csv가 업데이트되었다면 그대로 진행)
    target_files = [
        '성의회관.csv', '의산연01.csv', '의산연별관.csv', '대학본관.csv', 
        '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv'
    ]
    
    all_dfs = []
    for file_path in target_files:
        try:
            # 파일 읽기 (인코딩 자동 대응)
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')

            # 컬럼명 표준화 (공백 제거, 소문자화)
            df.columns = [str(c).strip().lower() for c in df.columns]
            
            # 유사 컬럼명 통일
            rename_dict = {
                'building_name': 'building', '건물명': 'building', 
                '시설명': 'name', '이름': 'name'
            }
            df = df.rename(columns=rename_dict)
            
            # 건물명 강제 지정 (의산연 본관/별관 분리 및 기타 건물)
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

    # [불순물 제거] 제목행 데이터 삭제
    if 'building' in combined.columns:
        combined = combined[combined['building'].astype(str).str.lower() != 'building']
    if 'name' in combined.columns:
        combined = combined[combined['name'].astype(str).str.lower() != 'name']
    
    # 중복 제거 (이름, 건물, 층, 호실 기준)
    subset_cols = [c for c in ['name', 'building', 'floor', 'room'] if c in combined.columns]
    combined = combined.drop_duplicates(subset=subset_cols, keep='first')
    
    return combined

# --- 2. [카테고리 분류 함수] ---
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

# --- 3. [메인 실행 구역] ---
st.set_page_config(page_title="성의교정 시설 가이드", layout="wide")
st.title("🏥 성의교정 시설 통합 안내 (데이터 업데이트 완료)")

final_df = get_final_clean_data()

if final_df is not None:
    final_df = add_smart_category(final_df)
    
    # 1,146개(혹은 성의회관 수정후 개수) 상태 표시
    st.success(f"✅ 총 **{len(final_df)}개**의 시설 정보가 통합되었습니다.")
    
    # 유형별 퀵 필터
    st.write("### 📌 시설 유형별 모아보기")
    cat_list = ['전체'] + sorted(final_df['category'].unique().tolist())
    selected_cat = st.radio("필터를 선택하세요", options=cat_list, horizontal=True)

    # 통합 검색창
    search_input = st.text_input("🔍 검색 (교수님 성함, 호실 번호, 시설명 등)", placeholder="예: 홍길동, 2016, 세포치료")

    # 데이터 필터링
    view_df = final_df.copy()
    if selected_cat != '전체':
        view_df = view_df[view_df['category'] == selected_cat]
        
    if search_input:
        s = search_input.lower()
        mask = view_df['name'].astype(str).str.lower().str.contains(s)
        if 'building' in view_df.columns:
            mask |= view_df['building'].astype(str).str.lower().str.contains(s)
        if 'room' in view_df.columns:
            mask |= view_df['room'].astype(str).str.lower().str.contains(s)
        view_df = view_df[mask]

    # 결과 표 출력
    st.write(f"조회 결과: **{len(view_df)}건**")
    show_cols = [c for c in ['name', 'building', 'floor', 'room', 'category', 'description'] if c in view_df.columns]
    st.dataframe(view_df[show_cols], use_container_width=True)

else:
    st.error("데이터 로드 실패. CSV 파일들을 확인해 주세요.")
