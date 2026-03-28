import pandas as pd
import streamlit as st

def safe_read_and_clean(file_path):
    try:
        # 1. 인코딩 처리
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_path, encoding='cp949')

        # 2. 중복 컬럼 제거 및 제목행 방어
        df = df.loc[:, ~df.columns.duplicated()]
        if 'name' in df.columns:
            is_header = df['name'].astype(str).str.strip().str.lower() == 'name'
            df = df[~is_header]

        # 3. 빈 데이터 제거
        df = df.dropna(subset=['name'])
        df = df[df['name'].astype(str).str.strip() != '']
        
        # 4. 건물명 기록
        df['building_name'] = file_path.split('.')[0]
        
        return df.reset_index(drop=True)
    except Exception as e:
        return None

# --- [메인 실행부] ---
target_files = [
    '성의회관.csv', '의산연01.csv', '대학본관.csv', 
    '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv'
]

all_dfs = []
for f in target_files:
    temp_df = safe_read_and_clean(f)
    if temp_df is not None:
        all_dfs.append(temp_df)

if all_dfs:
    # 1. 데이터 통합
    final_df = pd.concat(all_dfs, ignore_index=True, sort=False)
    
    # 2. 화면 출력
    st.success(f"🎊 총 {len(all_dfs)}개 건물, 전체 {len(final_df)}개 데이터 통합 완료!")
    
    st.divider()
    
    # 3. [핵심] 건물별 추출 개수 통계
    st.subheader("🏢 건물별 시설 데이터 추출 현황")
    
    # 개수 집계 및 정렬
    counts = final_df['building_name'].value_counts().reset_index()
    counts.columns = ['건물명', '추출된 시설 수']
    
    # 표와 차트 나란히 배치
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.write("#### 데이터 상세 수치")
        st.table(counts)
        
    with col2:
        st.write("#### 시각화 그래프")
        st.bar_chart(data=counts.set_index('건물명'))

    # 4. 데이터 미리보기
    with st.expander("🔍 전체 데이터 리스트 보기"):
        st.dataframe(final_df)
else:
    st.error("파일을 하나도 불러오지 못했습니다. 파일명이 정확한지 확인해 주세요.")
