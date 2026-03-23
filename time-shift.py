import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 설정 및 데이터 관리 ---
st.set_page_config(page_title="보안 통합 관리 시스템", layout="wide")

def load_leaves():
    if os.path.exists('leave_data.csv'):
        return pd.read_csv('leave_data.csv')
    return pd.DataFrame(columns=['날짜', '성명', '대근자'])

# 엑셀의 시간 숫자(float)를 "HH:mm" 문자열로 변환하는 함수
def format_excel_time(t):
    if pd.isna(t) or isinstance(t, str): return ""
    total_seconds = int(t * 24 * 3600)
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

# --- 2. C조 상세 시간표 (엑셀 '진한 색 To' 기준 반영) ---
# From 시각에 교대하여 To 시각까지 근무하는 구조
RAW_TIMETABLE = [
    {"구분": "주간1", "From": 0.291666, "To": 0.3125, "조장": "안내실", "대원": "로비", "당직A": "로비", "당직B": "휴게"},
    {"구분": "주간2", "From": 0.333333, "To": 0.354166, "조장": "안내실", "대원": "휴게", "당직A": "휴게", "당직B": "로비"},
    {"구분": "주간3", "From": 0.375, "To": 0.395833, "조장": "안내실", "대원": "순찰", "당직A": "휴게", "당직B": "로비"},
    {"구분": "주간4", "From": 0.416666, "To": 0.4375, "조장": "휴게", "대원": "안내실", "당직A": "로비", "당직B": "순찰"},
    {"구분": "주간5", "From": 0.458333, "To": 0.479166, "조장": "로비", "대원": "안내실", "당직A": "순찰", "당직B": "휴게"},
    {"구분": "주간6", "From": 0.5, "To": 0.520833, "조장": "순찰", "대원": "휴게", "당직A": "안내실", "당직B": "로비"},
    {"구분": "주간7", "From": 0.541666, "To": 0.5625, "조장": "안내실", "대원": "휴게", "당직A": "로비", "당직B": "휴게"},
    {"구분": "주간8", "From": 0.583333, "To": 0.604166, "조장": "로비", "대원": "순찰", "당직A": "휴게", "당직B": "안내실"},
    {"구분": "주간9", "From": 0.625, "To": 0.645833, "조장": "안내실", "대원": "휴게", "당직A": "로비", "당직B": "휴게"},
    {"구분": "주간10", "From": 0.666666, "To": 0.729166, "조장": "휴게", "대원": "안내실", "당직A": "휴게", "당직B": "로비"},
    {"구분": "야간1", "From": 0.708333, "To": 0.729166, "조장": "안내실", "대원": "휴게", "당직A": "휴게", "당직B": "로비"},
    {"구분": "야간2", "From": 0.75, "To": 0.770833, "조장": "안내실", "대원": "석식", "당직A": "로비", "당직B": "석식"},
]

menu = st.sidebar.selectbox("메뉴 선택", ["🗓️ 근무 상황판", "📱 비상연락망", "📝 연차 관리"])

if menu == "🗓️ 근무 상황판":
    st.subheader("🗓️ 오늘 근무 및 시간대별 상황")
    
    # 1. 날짜 및 인원 로직
    today = datetime.now().date()
    selected_date = st.sidebar.date_input("조회 날짜", today)
    
    # C조 근무 로직 (이태원 시작 기준)
    base_date = datetime(2026, 3, 3).date()
    days_diff = (selected_date - base_date).days
    
    if days_diff >= 0 and days_diff % 3 == 0:
        count_idx = days_diff // 3
        a_rotation = ["이태원", "김태언", "이정석"]
        staff_rank = {"김태언": 1, "이태원": 2, "이정석": 3}
        
        a_worker = a_rotation[(count_idx // 2) % 3]
        others = sorted([n for n in staff_rank.keys() if n != a_worker], key=lambda x: staff_rank[x])
        b_worker, c_worker = others[0], others[1]
        if count_idx % 2 == 1: b_worker, c_worker = c_worker, b_worker

        # 상단 현재 인원 카드
        st.markdown(f"""
            <div style="background:#262730; color:white; padding:15px; border-radius:10px; margin-bottom:20px;">
                <h4 style="margin:0; color:#00ff00;">● {selected_date} 근무 편성</h4>
                <div style="display:flex; justify-content:space-between; margin-top:10px; font-size:15px;">
                    <span><b>조장:</b> 황재업</span>
                    <span><b>회관(A):</b> {a_worker}</span>
                    <span><b>의산연(B):</b> {b_worker}</span>
                    <span><b>의산연(C):</b> {c_worker}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

        # 2. 실시간 근무 시간표 (From이 교대 시점)
        st.write("🕒 **시간대별 근무 위치 (From: 교대시간)**")
        
        table_rows = []
        for row in RAW_TIMETABLE:
            start_t = format_excel_time(row["From"])
            end_t = format_excel_time(row["To"])
            table_rows.append({
                "교대(From)": start_t,
                "종료(To)": end_t,
                "황재업(조장)": row["조장"],
                f"{a_worker}(A)": row["대원"],
                f"{b_worker}(B)": row["당직A"],
                f"{c_worker}(C)": row["당직B"]
            })
            
        df_time = pd.DataFrame(table_rows)
        
        # 강조 스타일: 현재 시간대에 해당하는 행 하이라이트 (옵션)
        st.dataframe(df_time, use_container_width=True, hide_index=True)
        st.info("💡 'From' 시각에 맞춰 해당 위치로 이동 및 교대하시면 됩니다.")
        
    else:
        st.warning("선택한 날짜는 C조 근무일이 아닙니다.")

# --- 나머지 메뉴 로직 생략 (이전과 동일) ---
