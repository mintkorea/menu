import pandas as pd
import streamlit as st

# --- 1. [함수 정의 구역] 최상단 배치 ---

def get_final_clean_data():
    """데이터 통합, 건물명 교정 및 오류 제거"""
    target_files = [
        '성의회관.csv', '의산연01.csv', '의산연별관.csv', '대학본관.csv', 
        '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv'
    ]
    
    all_dfs = []
    for file_path in target_files:
        try:
            # 파일 읽기
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')

            # 컬럼 표준화 (공백 제거 및 소문자화)
            df.columns = [c.strip().lower() for c in df.columns]
            rename_dict = {
                'building_name': 'building', 
                '건물명': 'building', 
                '시설명': 'name',
                '이름': 'name'
            }
            df = df.rename(columns=rename_dict)
            
            # 건물명 강제 교정 (의산연 본관/별관 분리)
            if '의산연01' in file_path:
                df['building'] = '의산연본관'
            elif '의산연별관' in file_path:
                df['building'] = '의산연별관'
            elif 'building' not in df.columns:
                df['building'] = file_path.split('.')[0]

            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except:
            continue
            
    if not all_dfs:
        return None
        
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)

    # [불순물 제거]
    if 'building' in combined.columns:
        combined = combined[combined['building'].astype(str).lower() != 'building']
    if 'name' in combined.columns:
        combined = combined[combined['name'].astype(str).lower() != 'name']
    
    # 중복 제거 및 성의회관 대강당 삭제
    subset_cols = [c for c in ['name', 'building', 'floor', 'room'] if c in combined.columns]
    combined = combined.drop_duplicates(subset=subset_cols, keep='first')
    combined = combined[~((combined['building'] == '성의회관') & (combined['name'] == '대강당'))]
    
    return combined

def add_category(df):
    """시설 명칭을 분석하여 교수실/연구실 카테고리 생성"""
    def classify(val):
        val = str(val)
        if '교수' in val: return '👨‍🏫 교수연구실'
        elif '연구실' in name or '연구' in val: return '🧪 일반연구실'
        elif '강의' in val or '세미나' in val: return '📖 교육시설'
        elif '실험' in val: return '🔬 실험시설'
        elif '회의' in val: return '🤝 회의실'
        return '🏢 기타시설'

    if 'name' in df.columns:
        df['category'] = df['name'].apply(classify)
    else:
        df['category'] = '🏢 기타시설'
    return df

# --- 2. [실행 구역] ---

st.set_page_config(page_title="성의교정 시설 가이드", layout="wide")
st.title("🏥 성의교정 시설 통합 가이드")

# 데이터 로드 및 카테고리 강화
final_df = get_final_clean_data()

if final_df is not None:
    final_df = add_category(final_df)
    
    # 상단 요약 정보
    st.success(f"✅ 총 **{len(final_df)}개**의 유효 시설 정보가 통합되었습니다.")
    
    # [A] 유형별 퀵 필터 (에러 방지를 위해 변수 직접 정의)
    st.write("### 📌 시설 유형별 모아보기")
    available_cats = ['전체'] + sorted(final_df['category'].unique().tolist())
    selected_cat = st.radio("유형을 선택하세요", options=available_cats, horizontal=True)

    # [B] 통합 검색창
    search_q = st.text_input("🔍 직접 검색 (교수님 성함, 호실 번호, 시설명)", placeholder="예: 홍길동, 2016, 세미나실")

    # 필터링 적용
    view_df = final_df.copy()
    if selected_cat != '전체':
        view_df = view_df[view_df['category'] == selected_cat]
        
    if search_q:
        q = search_q.lower()
        # 검색 대상 컬럼 안전하게 합치기
        mask = (view_df['name'].astype(str).str.lower().str.contains(q) | 
                view_df['building'].astype(str).str.lower().str.contains(q) |
                view_df['room'].astype(str).str.lower().str.contains(q))
        view_df = view_df[mask]

    # [C] 결과 출력
    st.write(f"검색 결과: **{len(view_df)}건**")
    # 보여줄 컬럼만 선택 (존재하는 컬럼만)
    cols_to_show = [c for c in ['name', 'building', 'floor', 'room', 'category', 'description'] if c in view_df.columns]
    st.dataframe(view_df[cols_to_show], use_container_width=True)

else:
    st.error("데이터를 불러오지 못했습니다. CSV 파일 목록과 파일명을 확인해 주세요.")
