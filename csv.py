import pandas as pd
import streamlit as st

def recover_omnibus_final():
    file_path = '옴니버스B.csv'
    try:
        # 1. 인코딩 해결 및 전체 읽기
        try:
            df = pd.read_csv(file_path, encoding='utf-8-sig')
        except:
            df = pd.read_csv(file_path, encoding='cp949')

        # [복구 핵심 1] 전체 데이터가 숫자로 인식되어도 문자로 강제 변환
        df = df.astype(str)
        
        # [복구 핵심 2] 중복 컬럼 제거
        df = df.loc[:, ~df.columns.duplicated()]

        # [복구 핵심 3] 'name' 행 제거 로직 수정 (에러 발생 지점 해결)
        if 'name' in df.columns:
            # .strAccessor를 사용하여 안전하게 비교
            mask = df['name'].str.strip().str.lower() != 'name'
            df = df[mask]

        # [복구 핵심 4] 진짜 데이터만 남기기 (nan이나 빈 칸 제외)
        # 'nan'이라는 문자열로 변한 빈 값들을 필터링
        df = df[~df['name'].str.contains('nan|None', case=False, na=False)]
        df = df[df['name'].str.strip() != '']

        # 층수 보정 (B5~L8 등)
        if 'floor' in df.columns:
            df['floor'] = df['floor'].str.strip().str.upper()
            df['floor'] = df['floor'].replace('NAN', '층수미상')

        df['building_name'] = '옴니버스B'
        
        return df.reset_index(drop=True)

    except Exception as e:
        st.error(f"❌ 옴니버스B 복구 중 에러 발생: {e}")
        return None

# 실행 및 결과 확인
omni_df = recover_omnibus_final()

if omni_df is not None:
    st.success(f"📊 옴니버스B 복구 완료: {len(omni_df)}개 행 발견")
    st.dataframe(omni_df)
