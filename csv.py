import pandas as pd
import streamlit as st

# --- 1. 데이터 통합 및 정제 함수 ---
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

            # 중복 컬럼 및 제목행 제거
            df = df.loc[:, ~df.columns.duplicated()]
            if 'name' in df.columns:
                is_header = df['name'].astype(str).str.strip().str.lower() == 'name'
                df = df[~is_header]

            # 유효 데이터 필터링
            df = df.dropna(subset=['name'])
            df = df[df['name'].astype(str).str.strip() != '']
            
            # 건물명 기록
            df['building_name'] = file_path.split('.')[0]
            all_dfs.append(df)
        except:
            continue
            
    if all_dfs:
        combined = pd.concat(all_dfs, ignore_index=True, sort=False)
        # 필수 컬럼 보장
        for col in ['name', 'building_name', 'floor', 'room', 'description']:
            if col not in combined.columns: combined[col] = "정보없음"
        return combined
    return None

# --- 2. 메인 화면 구성 (순서 중요!) ---

# 데이터를 먼저 가져옵니다 (이게 1번이어야 에러가 안 납니다)
final_df = get_integrated_data()

if final_df is not None:
    # 제목 및 상단 통계
    st.title("🏢 가톨릭대학교 성의교정 시설 안내")
    st.success(f"✅ 총 **{len(final_df)}개**의 시설 정보가 통합되었습니다.")

    # [A] 통합 검색 기능
    st.divider()
    st.subheader("🔍 시설 통합 검색")
    search_query = st.text_input("시설명, 건물명, 또는 호실 번호를 입력하세요.", placeholder="예: 기초의학실습실, 402호, 성모병원")

    if search_query:
        q = search_query.lower()
        # 검색 대상 컬럼 합치기
        search_target = (final_df['name'].astype(str) + final_df['building_name'].astype(str) + 
                         final_df['floor'].astype(str) + final_df['room'].astype(str)).str.lower()
        
        results = final_df[search_target.str.contains(q, na=False)]
        
        if not results.empty:
            st.write(f"검색 결과 **{len(results)}건**")
            st.dataframe(results[['name', 'building_name', 'floor', 'room', 'description']], use_container_width=True)
        else:
            st.warning("검색 결과가 없습니다.")

    # [B] 건물별 통계 (접어두기 기능)
    with st.expander("📊 건물별 데이터 분포 확인"):
        counts = final_df['building_name'].value_counts().reset_index()
        counts.columns = ['건물명', '시설 수']
        st.table(counts)
        st.bar_chart(data=counts.set_index('건물명'))

else:
    st.error("데이터 파일을 찾을 수 없습니다. CSV 파일들이 올바른 위치에 있는지 확인해 주세요.")
