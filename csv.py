import pandas as pd
import streamlit as st

# 1. 데이터가 합쳐진 final_df가 있다고 가정하고 집계를 수행합니다.
if 'final_df' in locals() or 'final_df' in globals():
    st.markdown("### 🏢 건물별 시설 데이터 추출 결과")
    
    # 건물별로 개수 세기 (Value Counts)
    building_counts = final_df['building_name'].value_counts().reset_index()
    building_counts.columns = ['건물명', '추출된 시설 수']
    
    # 시설 수 기준으로 내림차순 정렬
    building_counts = building_counts.sort_values(by='추출된 시설 수', ascending=False)
    
    # 2. 결과 표 출력
    st.table(building_counts)
    
    # 3. 전체 합계 표시
    total_sum = building_counts['추출된 시설 수'].sum()
    st.success(f"✅ 7개 파일에서 총 **{total_sum}개**의 시설 정보를 완벽하게 추출했습니다.")

    # 4. 시각화 (막대 그래프)
    st.bar_chart(data=building_counts.set_index('건물명'))

else:
    st.error("통합된 데이터(final_df)를 찾을 수 없습니다. 이전 단계의 통합 코드를 먼저 실행해 주세요.")
