import pandas as pd
import streamlit as st

def safe_clean_file(file_path):
    try:
        # 인코딩 해결
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_path, encoding='cp949')

        # 1. 중복 컬럼 제거 (InvalidIndexError 방지)
        df = df.loc[:, ~df.columns.duplicated()]

        # 2. 데이터 중간에 낀 'name' 행 제거
        if 'name' in df.columns:
            df = df[df['name'].astype(str).str.lower() != 'name']

        # 3. 필수 데이터(시설명) 없는 행 삭제
        df = df.dropna(subset=['name'])
        
        # 4. 건물명 기록 (파일명에서 가져옴)
        df['building_name'] = file_path.split('.')[0]
        
        return df.reset_index(drop=True)
    except Exception as e:
        st.error(f"❌ {file_path} 처리 중 에러: {e}")
        return None

# --- 실행 부분 ---
# 1. 성의회관 처리 (이미 성공한 것)
df1 = safe_clean_file('성의회관.csv')

# 2. 의과학연구원 처리 (새로 추가하는 것)
df2 = safe_clean_file('의산연01.csv')

# 3. 두 파일 합치기
if df1 is not None and df2 is not None:
    combined_df = pd.concat([df1, df2], ignore_index=True, sort=False)
    
    st.success(f"✅ 통합 성공! (성의회관: {len(df1)}건 + 의산연: {len(df2)}건)")
    st.write(f"### 총 {len(combined_df)}개 데이터 목록")
    st.dataframe(combined_df)
else:
    st.warning("일부 파일을 불러오지 못했습니다. 파일명을 다시 확인해주세요.")
