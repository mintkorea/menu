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
        
        # 4. 층수 보정 로직 (특히 성모병원 지하층: -6 -> B6F)
        def fix_floor(f):
            f = str(f).strip().upper()
            if f.startswith('-'): return f"B{f[1:]}F"
            if f.isdigit(): return f + "F"
            return f
            
        if 'floor' in df.columns:
            df['floor'] = df['floor'].apply(fix_floor)
        
        # 5. 건물명 기록
        df['building_name'] = file_path.split('.')[0]
        
        return df.reset_index(drop=True)
    except Exception as e:
        st.error(f"⚠️ {file_path} 처리 에러: {e}")
        return None

# --- 실행 부분 ---
df_list = []
# 이번엔 성모병원까지 포함합니다.
target_files = ['성의회관.csv', '의산연01.csv', '대학본관.csv', '병원별관.csv', '서울성모병원.CSV']

for f in target_files:
    temp_df = safe_clean_file(f)
    if temp_df is not None:
        df_list.append(temp_df)

if df_list:
    combined_df = pd.concat(df_list, ignore_index=True, sort=False)
    st.success(f"✅ 통합 성공! 총 {len(df_list)}개 건물")
    st.write(f"### 현재까지 총 {len(combined_df)}개 데이터 목록")
    st.dataframe(combined_df)
