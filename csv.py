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

        # 2. 데이터 중간에 낀 'name' 행 제거 (필터링)
        if 'name' in df.columns:
            df = df[df['name'].astype(str).str.lower() != 'name']

        # 3. 필수 데이터(시설명) 없는 행 삭제
        df = df.dropna(subset=['name'])
        
        # 4. 건물명 기록 (파일명에서 가져옴)
        df['building_name'] = file_path.split('.')[0]
        
        return df.reset_index(drop=True)
    except Exception as e:
        # 파일이 없거나 에러가 나면 화면에 표시
        st.error(f"⚠️ {file_path}를 찾을 수 없거나 에러가 났습니다: {e}")
        return None

# --- 실행 부분 ---
# 1. 기존 성공 파일들
df_list = []
target_files = ['성의회관.csv', '의산연01.csv', '대학본관.csv', '병원별관.csv']

for f in target_files:
    temp_df = safe_clean_file(f)
    if temp_df is not None:
        df_list.append(temp_df)

# 2. 파일들 합치기
if df_list:
    combined_df = pd.concat(df_list, ignore_index=True, sort=False)
    
    st.success(f"✅ 통합 성공! 총 {len(df_list)}개 건물 데이터 합쳐짐")
    st.write(f"### 현재까지 총 {len(combined_df)}개 데이터 목록")
    st.dataframe(combined_df)
else:
    st.error("데이터를 하나도 불러오지 못했습니다.")
