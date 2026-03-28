import pandas as pd
import streamlit as st

# --- 1. [함수 정의 구역] 반드시 최상단에 위치해야 합니다 ---

def get_final_clean_data():
    """데이터 통합 및 기본 정제 함수"""
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

            # 컬럼 표준화 (공백 제거 및 소문자화)
            df.columns = [c.strip().lower() for c in df.columns]
            rename_dict = {'building_name': 'building', '건물명': 'building', '시설명': 'name'}
            df = df.rename(columns=rename_dict)
            
            # 건물명 강제 교정
            if '의산연01' in file_path: df['building'] = '의산연본관'
            elif '의산연별관' in file_path: df['building'] = '의산연별관'
            elif 'building' not in df.columns: df['building'] = file_path.split('.')[0]

            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except:
            continue
            
    if not all_dfs: return None
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)

    # 유령 데이터 및 제목행 제거
    if 'building' in combined.columns:
        combined = combined[combined['building'].astype(str).lower() != 'building']
    if 'name' in combined.columns:
        combined = combined[combined['name'].astype(str).lower() != 'name']
    
    # 중복 제거 (이름, 건물, 층, 호실 기준)
    subset_cols = [c for c in ['name', 'building', 'floor', 'room'] if c in combined.columns]
    combined = combined.drop_duplicates(subset=subset_cols, keep='first')
    
    # 성의회관 대강당 삭제
    combined = combined[~((combined['building'] == '성의회관') & (combined['name'] == '대강당'))]
    
    return combined

def enhance_data(df):
    """교수실, 연구실 등을 자동으로 분류하는 함수"""
    def classify(name):
        name = str(name)
        if '교수' in name: return '교수연구실'
        elif '연구실' in name: return '일반연구실'
        elif '강의' in name or '세미나' in name: return '교육시설'
        elif '실험' in name: return '실험시설'
        elif '진료' in name or '센터' in name: return '의료/지원시설'
        return '기타'

    df['category'] = df['name'].apply(classify)
    return df

# --- 2. [실행 구역] 함수 정의가 끝난 후 시작합니다 ---

st.set_page_config(page_title="성의교정 시설 가이드", layout="wide")
st.title("🏢 성의교정 시설 통합 가이드")

# 데이터 로드 및 강화
final_df = get_final_clean_data()

if final_df is not None:
    final_df = enhance_data(final_df) # 카테고리 부여
    
    # 상단 요약 대시보드
    st.success(f"✅ 총 **{len(final_df)}개**의 유효 시설 정보가 통합되었습니다.")
    
    m1, m2, m3 = st.columns(3)
    m1.metric("전체 시설", f"{len(final_df)}개")
    m2.metric("교수/연구실", f"{len(final_df[final_df['category'].isin(['교수연구실', '일반연구실'])])}개")
    m3.metric("기타 시설", f"{len(final_df[final_df['category'] == '기타'])}개")

    # [A] 유형별 퀵 필터 (Segmented Control)
    st.write("### 📌 유형별 모아보기")
    cat_options = ['전체'] + sorted(final_df['category'].unique().tolist())
    selected_cat = st.radio("시설 유형을 선택하세요", options=cat_options, horizontal=True)

    # [B] 통합 검색창
    search_query = st.text_input("🔍 검색 (교수님 성함, 호실 번호, 시설명)", placeholder="예: 홍길동, 2016, 세미나실")

    # 데이터 필터링 로직
    display_df = final_df.copy()
    
    if selected_cat != '전체':
        display_df = display_df[display_df['category'] == selected_cat]
        
    if search_query:
        q = search_query.lower()
        mask = (display_df['name'].astype(str).str.lower().str.contains(q) | 
                display_df['building'].astype(str).str.lower().str.contains(q) |
                display_df['room'].astype(str).str.lower().str.contains(q))
        display_df = display_df[mask]

    # 결과 출력
    st.write(f"검색 결과: **{len(display_df)}건**")
    st.dataframe(display_df[['name', 'building', 'floor', 'room', 'category', 'description']], use_container_width=True)

else:
    st.error("데이터 로드 실패. 파일 목록과 함수 순서를 확인해 주세요.")
