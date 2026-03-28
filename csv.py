import pandas as pd
import streamlit as st

# --- 1. [함수 정의] 가장 윗부분에 배치하여 NameError 방지 ---

def get_final_clean_data():
    """데이터 통합 및 모든 중복/오류 제거"""
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

            # 컬럼명 표준화 (공백 제거 및 소문자화)
            df.columns = [c.strip().lower() for c in df.columns]
            
            # 유사 컬럼명 통일
            rename_dict = {
                'building_name': 'building', 
                '건물명': 'building', 
                '시설명': 'name',
                '이름': 'name'
            }
            df = df.rename(columns=rename_dict)
            
            # 건물명 강제 지정 (의산연 본관/별관 분리)
            if '의산연01' in file_path:
                df['building'] = '의산연본관'
            elif '의산연별관' in file_path:
                df['building'] = '의산연별관'
            elif 'building' not in df.columns:
                df['building'] = file_path.split('.')[0]

            # 시설명(name)이 있는 행만 추가
            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except:
            continue
            
    if not all_dfs:
        return None
        
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)

    # [불순물 제거] 'building'이나 'name'이라는 글자가 데이터로 들어온 경우 삭제
    if 'building' in combined.columns:
        combined = combined[combined['building'].astype(str).lower() != 'building']
    if 'name' in combined.columns:
        combined = combined[combined['name'].astype(str).lower() != 'name']
    
    # 중복 데이터 제거 (이름, 건물, 층, 호실 기준)
    subset_cols = [c for c in ['name', 'building', 'floor', 'room'] if c in combined.columns]
    combined = combined.drop_duplicates(subset=subset_cols, keep='first')
    
    # 성의회관 2014호 대강당 유령 데이터 삭제
    if 'building' in combined.columns and 'name' in combined.columns:
        ghost_mask = (combined['building'] == '성의회관') & (combined['name'] == '대강당')
        combined = combined[~ghost_mask]
    
    return combined

def add_smart_category(df):
    """시설 명칭을 분석하여 교수실/연구실 등을 자동 분류"""
    def classify(row_name):
        text = str(row_name)
        if '교수' in text: return '👨‍🏫 교수연구실'
        elif '연구실' in text or '연구소' in text: return '🧪 일반연구실'
        elif '강의' in text or '세미나' in text: return '📖 교육시설'
        elif '실험' in text: return '🔬 실험시설'
        elif '회의' in text: return '🤝 회의실'
        return '🏢 기타시설'

    if 'name' in df.columns:
        df['category'] = df['name'].apply(classify)
    else:
        df['category'] = '🏢 기타시설'
    return df

# --- 2. [실행 구역] ---

st.set_page_config(page_title="성의교정 시설 가이드", layout="wide")
st.title("🏥 성의교정 시설 통합 가이드")

# 데이터 로드 및 카테고리 부여
final_df = get_final_clean_data()

if final_df is not None:
    final_df = add_smart_category(final_df)
    
    # 상단 요약 정보
    st.success(f"✅ 총 **{len(final_df)}개**의 유효 시설 정보가 통합되었습니다. (본관/별관 분리 완료)")
    
    # [A] 유형별 퀵 필터
    st.write("### 📌 시설 유형별 모아보기")
    # 카테고리 목록을 안전하게 생성
    cat_list = ['전체'] + sorted(final_df['category'].unique().tolist())
    selected_cat = st.radio("유형을 선택하세요", options=cat_list, horizontal=True)

    # [B] 통합 검색창
    search_q = st.text_input("🔍 직접 검색 (교수님 성함, 호실 번호, 시설명)", placeholder="예: 홍길동, 2016, 세미나실")

    # 필터링 적용
    view_df = final_df.copy()
    
    # 1. 카테고리 필터
    if selected_cat != '전체':
        view_df = view_df[view_df['category'] == selected_cat]
        
    # 2. 검색어 필터
    if search_q:
        q = search_q.lower()
        # 모든 컬럼을 합쳐서 검색 (에러 방지를 위해 존재하는 컬럼만)
        mask = view_df['name'].astype(str).str.lower().str.contains(q)
        if 'building' in view_df.columns:
            mask |= view_df['building'].astype(str).str.lower().str.contains(q)
        if 'room' in view_df.columns:
            mask |= view_df['room'].astype(str).str.lower().str.contains(q)
        view_df = view_df[mask]

    # [C] 결과 출력
    st.write(f"검색 결과: **{len(view_df)}건**")
    
    # 보여줄 컬럼 설정 (존재하는 것만)
    display_cols = [c for c in ['name', 'building', 'floor', 'room', 'category', 'description'] if c in view_df.columns]
    st.dataframe(view_df[display_cols], use_container_width=True)

else:
    st.error("데이터 로드 실패. CSV 파일이 서버에 존재하는지 확인해 주세요.")
