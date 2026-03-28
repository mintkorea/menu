import pandas as pd
import streamlit as st

# [추가] 데이터 후처리 함수
def clean_up_anomalies(df):
    # 1. 특정 건물의 잘못된 데이터(유령 시설) 삭제
    # '성의회관' 건물인데 '대강당'인 행을 찾아서 인덱스 드롭
    target_idx = df[(df['building_name'] == '성의회관') & (df['name'] == '대강당')].index
    df = df.drop(target_idx)
    
    # 2. 건물명, 층, 시설명, 호실이 완전히 똑같은 중복 데이터 합치기
    # 의산연01 대강당처럼 똑같은게 2개 있으면 하나만 남깁니다.
    df = df.drop_duplicates(subset=['name', 'building_name', 'floor', 'room'], keep='first')
    
    return df

# --- 메인 로직 내부에 삽입 ---
final_df = get_integrated_data()

if final_df is not None:
    # [수정] 위에서 정의한 정제 함수를 실행합니다.
    final_df = clean_up_anomalies(final_df)
    
    st.title("🏢 가톨릭대학교 성의교정 시설 안내")
    st.success(f"✅ 정제 완료: 총 **{len(final_df)}개**의 유효 시설 정보가 통합되었습니다.")

    # ... (이하 검색창 및 출력 코드는 동일)
