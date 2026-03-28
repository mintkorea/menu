import pandas as pd
import streamlit as st

# --- 1. 데이터 통합 및 정제 함수 정의 ---
def get_integrated_data():
    target_files = [
        '성의회관.csv', '의산연01.csv', '대학본관.csv', 
        '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv'
    ]
    
    all_dfs = []
    for file_path in target_files:
        try:
            # 인코딩 처리
            try:
                df = pd.read_csv(file_path, encoding='utf-8-sig')
            except:
                df = pd.read_csv(file_path, encoding='cp949')

            # 중복 컬럼 제거
            df = df.loc[:, ~df.columns.duplicated()]
            
            # 제목행('name')이 데이터로 들어온 경우 제거
            if 'name' in df.columns:
                is_header = df['name'].astype(str).str.strip().str.lower() == 'name'
                df = df[~is_header]

            # 유효 데이터 필터링 (시설명이 없는 행 제외)
            df = df.dropna(subset=['name'])
            df = df[df['name'].astype(str).str.strip() != '']
            
            # 건물명 기록 (파일명 활용)
            df['building_name'] = file_path.split('.')[0]
            all_dfs.append(df)
        except:
            continue
            
    if not all_dfs:
        return None
        
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)
    
    # 기본 컬럼 보장
    for col in ['name', 'building_name', 'floor', 'room', 'description']:
        if col not in combined.columns: combined[col] = ""
    
    # --- [데이터 보정 로직 추가] ---
    # 1. 의산연 중복 제거 (이름, 건물, 층, 호실이 모두 같으면 하나만 남김)
    combined = combined.drop_duplicates(subset=['name', 'building_name', 'floor', 'room'], keep='first')
    
    # 2. 성의회관 유령 데이터 '대강당' 제거
    # 성의회관 2층 2014호가 대강당으로 잘못 나온 경우 필터링
    ghost_mask = (combined['building_name'] == '성의회관') & (combined['name'] == '대강당')
    combined = combined[~ghost_mask]
    
    return combined

# --- 2. 메인 화면 실행 (함수를 먼저 호출합니다) ---

# 페이지 설정
st.set_page_config(page_title="성의교정 시설 안내", layout="wide")

final_df = get_integrated_data()

if final_df is not None:
    st.title("🏢 가톨릭대학교 성의교정 시설 안내")
    st.info(f"현재 **{len(final_df)}개**의 유효 시설 정보가 통합되어 있습니다. (중복 및 오류 제거 완료)")

    # [A] 통합 검색 기능
    st.divider()
    st.subheader("🔍 시설 통합 검색")
    search_query = st.text_input("시설명, 건물명, 또는 호실 번호를 입력하세요.", placeholder="예: 기초의학실습실, 402호, 성모병원")

    if search_query:
        q = search_query.lower()
        # 검색 대상 컬럼 합치기 (이름, 건물, 층, 호실 포함)
        search_target = (final_df['name'].astype(str) + 
                         final_df['building_name'].astype(str) + 
                         final_df['floor'].astype(str) + 
                         final_df['room'].astype(str)).str.lower()
        
        results = final_df[search_target.str.contains(q, na=False)]
        
        if not results.empty:
            st.write(f"검색 결과 **{len(results)}건**")
            st.dataframe(results[['name', 'building_name', 'floor', 'room', 'description']], use_container_width=True)
        else:
            st.warning(f"'{search_query}'에 대한 검색 결과가 없습니다.")

    # [B] 건물별 데이터 분포 확인 (사이드바 혹은 접이식)
    with st.expander("📊 건물별 데이터 추출 현황 확인"):
        counts = final_df['building_name'].value_counts().reset_index()
        counts.columns = ['건물명', '시설 수']
        st.table(counts)

else:
    st.error("데이터를 불러오지 못했습니다. CSV 파일들을 확인해 주세요.")
