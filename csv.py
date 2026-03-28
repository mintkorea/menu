import pandas as pd
import streamlit as st

# --- 1. [데이터 통합 및 컬럼 강제 표준화] ---
def get_final_clean_data():
    target_files = [
        '옴니버스A.csv', '옴니버스B.csv', '성의회관.csv', '병원별관.csv', 
        '대학본관.csv', '의산연01.csv', '의산연별관.csv', '서울성모병원.CSV'
    ]
    all_dfs = []
    for file_path in target_files:
        try:
            try: df = pd.read_csv(file_path, encoding='utf-8-sig')
            except: df = pd.read_csv(file_path, encoding='cp949')
            
            # [핵심] 컬럼명 표준화 및 공백 제거 (AttributeError 방지)
            df.columns = [str(c).strip().lower() for c in df.columns]
            rename_map = {'건물명': 'building', '시설명': 'name', '이름': 'name'}
            df = df.rename(columns=rename_map)
            
            # 건물명 강제 할당 (파일명 기준)
            if '옴니버스' in file_path: df['building'] = '옴니버스파크'
            elif '성의회관' in file_path: df['building'] = '성의회관'
            elif '병원별관' in file_path: df['building'] = '병원별관'
            elif '대학본관' in file_path: df['building'] = '대학본관'
            elif '의산연01' in file_path: df['building'] = '의산연본관'
            elif '의산연별관' in file_path: df['building'] = '의산연별관'
            elif 'building' not in df.columns: df['building'] = file_path.split('.')[0]
            
            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except: continue
    
    if not all_dfs: return None
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    # [NameError 방지] 'building' 컬럼 존재 보장
    if 'building' not in combined.columns: combined['building'] = '기타'
    return combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')

# --- 2. [전 건물 통합 인덱스 우선순위 로직] ---
def apply_global_priority(df, selected_bldg):
    # 안내판 이미지 기반 인덱스 우선순위 맵
    priority_map = {
        '옴니버스파크': [
            '푸드코트', '플레이그라운드', '컨벤션홀', '이마트24', '카페', '돈까스', '파스타', 
            '박물관', '인포멀러닝스페이스', '마스터센터', '공동연구지원센터', '기업 입주공간'
        ],
        '성의회관': [
            '마리아홀', '안내실', '매점', '카페', '화원', '성당', '교목실', '강의실', 
            '학생휴게실', '동아리방', '방송반', '효원도서관', 'START의학시뮬레이션센터', '게스트하우스'
        ],
        '병원별관': [
            '암연구소', '백신바이오연구소', '면역질환융합연구소', '의료원 행정사무실', '옴니헬스실', '학생회'
        ],
        '의산연본관': [
            '실험동물연구센터', '세포치료사업단', '대강당', '통합관제실', '기능세포치료센터'
        ],
        '대학본관': [
            '행정실', '회의실', '식당', '교육실', '시설팀'
        ]
    }
    
    df['sort_val'] = 999
    if selected_bldg in priority_map:
        for i, target in enumerate(priority_map[selected_bldg]):
            # 안내판 키워드 포함 시 인덱스 최상단(0~n) 배치
            df.loc[df['name'].str.contains(target, na=False), 'sort_val'] = i

    # [정렬] 가중치 -> 층수 -> 이름 순
    return df.sort_values(by=['sort_val', 'floor', 'name']).drop(columns=['sort_val'])

# --- 3. [Streamlit UI] ---
st.set_page_config(page_title="성의교정 안내", layout="centered")

# 모바일 대응 폰트 축소
st.markdown("<style>.main-title{font-size:1.15rem; font-weight:bold; color:#004A99; margin-bottom:12px;}</style>", unsafe_allow_html=True)
st.markdown("<div class='main-title'>🏥 가톨릭대학교 성의교정 시설 안내</div>", unsafe_allow_html=True)

all_data = get_final_clean_data()

if all_data is not None:
    # 1. 건물 선택
    bldg_list = sorted(all_data['building'].unique().tolist())
    selected_bldg = st.selectbox("🏢 건물 선택", options=bldg_list)

    # 2. 검색 (선택사항)
    search_query = st.text_input("🔍 시설명/성함 검색 (안내판 시설 우선 노출)", placeholder="예: 푸드코트, 마리아홀")

    # 데이터 필터링
    view_df = all_data[all_data['building'] == selected_bldg].copy()
    if search_query:
        view_df = view_df[view_df['name'].str.contains(search_query, case=False, na=False)]

    # 3. [핵심] 인덱스 우선순위 적용
    view_df = apply_global_priority(view_df, selected_bldg)

    # 4. 결과 출력 (모바일 최적화)
    st.info(f"📍 {selected_bldg}: {len(view_df)}개 시설 정보")
    
    for _, row in view_df.iterrows():
        # 인덱스 상위 항목(안내판 시설)에 강조 아이콘 부여
        icon = "📢" if any(kw in str(row['name']) for kw in ['식당', '카페', '홀', '센터', '연구소', '실']) else "📍"
        with st.expander(f"{icon} {row['name']}"):
            st.write(f"**위치:** {row.get('floor','-')}층 {row.get('room','-')}호")
else:
    st.error("데이터 로딩 중 오류가 발생했습니다.")
