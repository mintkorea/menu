import pandas as pd
import streamlit as st

# --- 1. [데이터 통합 및 최종 정제] ---
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
            df = df.rename(columns={'building_name': 'building', '시설명': 'name'})
            
            # 건물명 강제 교정 (의산연01 -> 의산연본관)
            if '의산연01' in file_path: df['building'] = '의산연본관'
            elif '의산연별관' in file_path: df['building'] = '의산연별관'
            elif 'building' not in df.columns: df['building'] = file_path.split('.')[0]

            all_dfs.append(df)
        except:
            continue
            
    if not all_dfs: return None
        
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)

    # --- [불순물 제거 로직] ---
    # 1. 제목행이 데이터로 들어온 경우 제거 (건물명이 'building'인 행 삭제)
    combined = combined[combined['building'].astype(str).lower() != 'building']
    
    # 2. 시설명이 비어있거나 'name'인 행 제거
    combined = combined.dropna(subset=['name'])
    combined = combined[combined['name'].astype(str).lower() != 'name']
    
    # 3. 중복 제거
    combined = combined.drop_duplicates(subset=['name', 'building', 'floor', 'room'], keep='first')
    
    # 4. 성의회관 대강당 등 특정 오류 제거
    combined = combined[~((combined['building'] == '성의회관') & (combined['name'] == '대강당'))]
    
    return combined

# --- 2. [화면 구성] ---
st.title("🏢 성의교정 시설 통합 가이드")

final_df = get_final_clean_data()

if final_df is not None:
    # 최종 개수 표시 (1,146개 예상)
    st.success(f"✅ 총 **{len(final_df)}개**의 유효 시설 정보가 통합되었습니다.")

    # [A] 통합 검색바
    search_query = st.text_input("🔍 시설명, 건물명, 호실 번호로 검색", placeholder="예: 세포치료, 2016, 옴니버스")

    if search_query:
        q = search_query.lower()
        # 검색 대상 설정
        mask = (final_df['name'].astype(str).str.lower().str.contains(q) | 
                final_df['building'].astype(str).str.lower().str.contains(q) |
                final_df['room'].astype(str).str.lower().str.contains(q))
        res = final_df[mask]
        st.write(f"검색 결과 **{len(res)}건**")
        st.dataframe(res[['name', 'building', 'floor', 'room', 'description']], use_container_width=True)

    # [B] 건물별 현황 요약
    with st.expander("📊 건물별 시설 수 요약"):
        summary = final_df['building'].value_counts().reset_index()
        summary.columns = ['건물명', '시설 수']
        st.table(summary)

else:
    st.error("데이터를 불러올 수 없습니다.")
