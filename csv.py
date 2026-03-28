import pandas as pd
import streamlit as st

# (위에서 정의한 final_df가 생성된 후 실행)
if 'final_df' in locals() or 'final_df' in globals():
    st.subheader("📊 건물별 최종 데이터 분포 (총 1,147개)")
    
    # 건물별 개수 집계
    check_stats = final_df['building'].value_counts().reset_index()
    check_stats.columns = ['건물명', '추출된 시설 수']
    
    # 표로 출력
    st.table(check_stats)
    
    # '의산연별관'이 목록에 있는지, 숫자가 0은 아닌지 확인
    if '의산연별관' in check_stats['건물명'].values:
        val = check_stats[check_stats['건물명'] == '의산연별관']['추출된 시설 수'].values[0]
        st.success(f"📍 의산연별관 데이터가 {val}개 포함되어 있습니다.")
    else:
        st.error("⚠️ 목록에 '의산연별관'이 없습니다. 파일명을 다시 확인해 주세요.")
else:
    st.error("데이터가 로드되지 않았습니다.")
