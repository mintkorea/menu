import pandas as pd
import streamlit as st

def fix_building_names(df):
    # 1. '의산연01'이라는 명칭을 '의산연본관'으로 일괄 변경 (기본값)
    df.loc[df['building_name'] == '의산연01', 'building_name'] = '의산연본관'
    
    # 2. [추가 보정] 만약 별관 데이터가 층수나 호실로 구분 가능하다면 아래처럼 분리 가능합니다.
    # 예: 별관은 호실 번호가 특정 대역이거나 층수가 낮을 경우
    # df.loc[(df['building_name'] == '의산연본관') & (df['floor'].isin(['1F', '2F'])), 'building_name'] = '의산연별관'
    
    return df

# --- 메인 로직 적용 ---
final_df = get_integrated_data() # 이전 단계에서 정의한 통합 함수 호출

if final_df is not None:
    # 건물 명칭 교정 실행
    final_df = fix_building_names(final_df)
    
    st.title("🏢 가톨릭대학교 성의교정 시설 안내")
    st.success("✅ 건물 명칭 교정 완료: '의산연01' -> '의산연본관/별관'")

    # 현재 등록된 건물 목록 확인 (사이드바)
    st.sidebar.write("### 현재 등록된 건물")
    st.sidebar.write(final_df['building_name'].unique())

    # [검색창 및 통계 로직은 동일하게 유지]
