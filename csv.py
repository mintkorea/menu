import pandas as pd
import streamlit as st

def robust_read(file_path):
    try:
        # 1. 인코딩 처리
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_path, encoding='cp949')

        # 2. 모든 데이터를 문자로 변환 (에러 방지)
        df = df.astype(str)
        
        # 3. 중복 컬럼 제거
        df = df.loc[:, ~df.columns.duplicated()]

        # 4. 제목행('name')이 반복되는 경우 제거
        if 'name' in df.columns:
            df = df[df['name'].str.strip().lower() != 'name']

        # 5. 유효한 데이터만 남기기 (nan 제외)
        df = df[~df['name'].str.contains('nan|None', case=False, na=False)]
        df = df[df['name'].str.strip() != '']

        # 6. 건물명 기록
        df['building_name'] = file_path.split('.')[0]
        
        return df.reset_index(drop=True)
    except Exception as e:
        st.error(f"⚠️ {file_path} 읽기 실패: {e}")
        return None

# --- 실행: 모든 파일 합치기 ---
target_files = [
    '성의회관.csv', '의산연01.csv', '대학본관.csv', 
    '병원별관.csv', '서울성모병원.CSV', '옴니버스B.csv', '옴니버스A.csv' # A 추가!
]

all_dfs = []
for f in target_files:
    clean_df = robust_read(f)
    if clean_df is not None:
        all_dfs.append(clean_df)

if all_dfs:
    final_db = pd.concat(all_dfs, ignore_index=True, sort=False)
    
    # 필수 컬럼 정리
    cols = ['name', 'building_name', 'floor', 'room', 'category', 'description']
    for col in cols:
        if col not in final_db.columns: final_db[col] = "정보없음"
    
    final_db = final_db[cols]
    
    # CSV 저장
    final_db.to_csv('integrated_campus_db_v2.csv', index=False, encoding='utf-8-sig')
    
    st.success(f"🎊 [최종 통합 성공] 총 {len(all_dfs)}개 건물을 합쳤습니다!")
    st.info(f"📊 현재 전체 데이터 개수: {len(final_db)}개")
    st.dataframe(final_db)
