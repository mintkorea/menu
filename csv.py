import pandas as pd
import streamlit as st

# 데이터 로드 로직 (위의 get_verified_data 함수 포함 상태)
final_df = get_verified_data()

if final_df is not None:
    st.subheader("🚨 'building'이 '1'로 표시된 데이터 정밀 분석")
    
    # building 컬럼이 '1'이거나 숫자인 데이터만 필터링
    error_rows = final_df[final_df['building'].astype(str) == '1']
    
    if not error_rows.empty:
        st.warning(f"발견된 이상 데이터: {len(error_rows)}건")
        st.write("아래 표를 보고 이 데이터가 원래 어느 건물의 어떤 시설인지 확인해 주세요.")
        st.dataframe(error_rows) # 여기서 name, floor 등을 보면 정체를 알 수 있습니다.
        
        # [해결책] 만약 이 데이터가 '의산연별관' 것이라면 강제로 이름을 수정합니다.
        if st.button("🛠️ 이상 데이터 '의산연별관'으로 강제 교정하기"):
            final_df.loc[final_df['building'].astype(str) == '1', 'building'] = '의산연별관'
            st.success("교정이 완료되었습니다. 다시 집계해 보세요!")
    else:
        st.info("현재 '1'로 표시된 데이터가 필터링되지 않습니다. 전체 리스트를 확인해 주세요.")

    # 전체 통계 다시 보기
    st.divider()
    st.write("### 📊 현재 건물별 시설 수 (교정 전/후)")
    st.table(final_df['building'].value_counts())
