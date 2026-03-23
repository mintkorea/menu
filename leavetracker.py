import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 설정 및 데이터 로드 ---
VACATION_FILE = 'vacation.csv'

# 연차 데이터 불러오기 함수
def load_vacation_data():
    if os.path.exists(VACATION_FILE):
        return pd.read_csv(VACATION_FILE)
    else:
        return pd.DataFrame(columns=['날짜', '이름', '사유'])

# --- 2. UI 구성 (탭 메뉴) ---
st.title("📂 성의교정 연차 관리 시스템")
tabs = st.tabs(["🗓️ 연차 현황판", "✍️ 연차 신청"])

# --- 탭 1: 연차 현황판 ---
with tabs[0]:
    st.subheader("실시간 연차 내역")
    df_vac = load_vacation_data()
    
    if not df_vac.empty:
        # 날짜순 정렬 및 출력
        df_vac['날짜'] = pd.to_datetime(df_vac['날짜'])
        df_vac = df_vac.sort_values(by='날짜', ascending=False)
        
        # 표 형식으로 출력 (중앙 정렬 및 스타일 적용 가능)
        st.dataframe(df_vac, use_container_width=True, hide_index=True)
    else:
        st.info("등록된 연차 내역이 없습니다.")

# --- 탭 2: 연차 신청 ---
with tabs[1]:
    st.subheader("연차 신청서 작성")
    with st.form("vacation_form", clear_on_submit=True):
        vac_date = st.date_input("연차 날짜", datetime.now().date())
        vac_name = st.selectbox("신청자", ["김태언", "이태원", "이정석"])
        vac_reason = st.text_input("사유 (선택사항)", placeholder="개인사정 등")
        
        submitted = st.form_submit_button("신청하기")
        
        if submitted:
            new_data = pd.DataFrame({
                '날짜': [vac_date.strftime('%Y-%m-%d')],
                '이름': [vac_name],
                '사유': [vac_reason]
            })
            
            # 파일 저장
            if os.path.exists(VACATION_FILE):
                df_existing = pd.read_csv(VACATION_FILE)
                df_updated = pd.concat([df_existing, new_data], ignore_index=True)
            else:
                df_updated = new_data
            
            df_updated.to_csv(VACATION_FILE, index=False, encoding='utf-8-sig')
            st.success(f"✅ {vac_name}님의 {vac_date} 연차 신청이 완료되었습니다.")
            st.rerun()

# --- 3. 근무표 연동 가이드 (참고용) ---
st.sidebar.markdown("---")
st.sidebar.info("""
**💡 근무표 연동 팁:**
기본 근무 로직에서 `get_daily_layout` 함수를 실행할 때, 
`vacation.csv`에 해당 날짜와 이름이 있는지 체크하여 
이름 대신 **'연차'**라는 텍스트를 넣도록 구현했었습니다.
""")
