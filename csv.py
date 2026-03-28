import pandas as pd
import streamlit as st

# --- 1. [데이터 통합 및 컬럼 강제 교정] ---
def get_final_clean_data():
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

            # [핵심] 컬럼명에 있는 공백 제거 및 소문자 변환으로 일관성 확보
            df.columns = [c.strip().lower() for c in df.columns]
            
            # 유사한 컬럼명들 하나로 통일 (표준화)
            rename_dict = {
                'building_name': 'building', 
                '건물명': 'building',
                '시설명': 'name',
                '이름': 'name'
            }
            df = df.rename(columns=rename_dict)
            
            # 건물명 강제 교정 (파일명 우선순위)
            if '의산연01' in file_path:
                df['building'] = '의산연본관'
            elif '의산연별관' in file_path:
                df['building'] = '의산연별관'
            elif 'building' not in df.columns:
                df['building'] = file_path.split('.')[0]

            # 시설명(name) 컬럼이 없으면 빈 데이터로 간주
            if 'name' in df.columns:
                df = df.dropna(subset=['name'])
                all_dfs.append(df)
        except:
            continue
            
    if not all_dfs: return None
        
    # 데이터 통합
    combined = pd.concat(all_dfs, ignore_index=True, sort=False)

    # --- [불순물 제거: AttributeError 방어] ---
    # 컬럼이 확실히 존재하는지 확인 후 필터링
    if 'building' in combined.columns:
        # 건물명이 'building'인 제목행 제거
        combined = combined[combined['building'].astype(str).str.lower() != 'building']
    
    if 'name' in combined.columns:
        # 시설명이 'name'인 제목행 제거
        combined = combined[combined['name'].astype(str).str.lower() != 'name']
        combined = combined[combined['name'].astype(str).str.strip() != ""]

    # 중복 제거
    subset_cols = [c for c in ['name', 'building', 'floor', 'room'] if c in combined.columns]
    combined = combined.drop_duplicates(subset=subset_cols, keep='first')
    
    # 성의회관 대강당 오류 제거
    if 'building' in combined.columns and 'name' in combined.columns:
        ghost_mask = (combined['building'] == '성의회관') & (combined['name'] == '대강당')
        combined = combined[~ghost_mask]
    
    return combined

# --- 2. [메인 화면 구성] ---
st.title("🏢 성의교정 시설 통합 가이드")

final_df = get_final_clean_data()

if final_df is not None:
    st.success(f"✅ 총 **{len(final_df)}개**의 유효 시설 정보가 통합되었습니다.")

    # [A] 통합 검색바
    search_query = st.text_input("🔍 시설명, 건물명, 호실 번호로 검색", placeholder="예: 세포치료, 2016, 옴니버스")

    if search_query:
        q = search_query.lower()
        # 검색 대상 컬럼 안전하게 병합
        search_target = final_df['name'].astype(str) + final_df['building'].astype(str)
        if 'room' in final_df.columns:
            search_target += final_df['room'].astype(str)
            
        mask = search_target.str.lower().str.contains(q, na=False)
        res = final_df[mask]
        
        st.write(f"검색 결과 **{len(res)}건**")
        st.dataframe(res, use_container_width=True)

    # [B] 건물별 요약
    with st.expander("📊 건물별 시설 수 요약"):
        summary = final_df['building'].value_counts().reset_index()
        summary.columns = ['건물명', '시설 수']
        st.table(summary)

else:
    st.error("데이터를 불러오는 중 오류가 발생했습니다. CSV 파일 형식을 확인해 주세요.")
