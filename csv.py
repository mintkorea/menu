import pandas as pd
import streamlit as st

def recover_omnibus():
    file_path = '옴니버스B.csv'
    try:
        # 1. 인코딩 및 읽기 (가장 원시적인 형태부터 시도)
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_path, encoding='cp949')

        # [복구 핵심 1] 전체 데이터 건수 확인 (필터링 전)
        raw_count = len(df)
        
        # [복구 핵심 2] 중복 컬럼 제거
        df = df.loc[:, ~df.columns.duplicated()]

        # [복구 핵심 3] 'name'이 없더라도 'room'이나 'floor'가 있으면 살림
        # 기존에는 name이 없으면 무조건 지웠으나, 이제는 내용이 하나라도 있으면 유지
        df = df.dropna(how='all') # 완전히 비어있는 행만 삭제
        
        # [복구 핵심 4] 제목 행('name')이 반복되는 경우만 조심스럽게 제거
        if 'name' in df.columns:
            df = df[df['name'].astype(str).str.strip().lower() != 'name']

        # 층수 보정 (B5~L8 등 다양한 표기 대응)
        def robust_fix_floor(f):
            f = str(f).strip().upper()
            if f in ['NAN', 'NONE', '']: return "층수미상"
            return f

        if 'floor' in df.columns:
            df['floor'] = df['floor'].apply(robust_fix_floor)

        df['building_name'] = '옴니버스B'
        
        final_count = len(df)
        return df.reset_index(drop=True), raw_count, final_count

    except Exception as e:
        st.error(f"❌ 옴니버스B 복구 중 에러: {e}")
        return None, 0, 0

# 실행 및 결과 확인
omni_df, raw_n, final_n = recover_omnibus()

if omni_df is not None:
    st.info(f"📊 [옴니버스B 검사 보고서]")
    st.write(f"- 원본 파일 행 수: {raw_n}개")
    st.write(f"- 정제 후 유효 데이터: {final_n}개")
    
    if final_n < 50: # 만약 데이터가 너무 적게 나오면 경고
        st.warning("⚠️ 데이터가 여전히 너무 적습니다. 파일의 첫 5줄을 확인해볼 필요가 있습니다.")
    
    st.dataframe(omni_df)
