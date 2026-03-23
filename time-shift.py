import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 설정 및 데이터 관리 ---
st.set_page_config(page_title="보안 통합 관리 시스템", layout="wide")

def format_excel_time(t):
    if pd.isna(t) or isinstance(t, str): return ""
    total_seconds = int(round(t * 24 * 3600))
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    return f"{hours:02d}:{minutes:02d}"

# --- 2. C조 연속 근무 시간표 데이터 (셀 분할의 의미 반영) ---
# 120분 근무는 시각적으로 두 칸을 차지하는 느낌을 주도록 구성
RAW_TIMETABLE = [
    {"No": "1", "시간": "07:00-08:00", "구분": "60분", "조장": "안내실", "대원": "로비", "당직A": "로비", "당직B": "휴게"},
    # 2시간 근무 (셀 분할 반영)
    {"No": "2-1", "시간": "08:00-09:00", "구분": "120분", "조장": "안내실", "대원": "휴게", "당직A": "휴게", "당직B": "로비"},
    {"No": "2-2", "시간": "09:00-10:00", "구분": "연장", "조장": "안내실", "대원": "휴게", "당직A": "휴게", "당직B": "로비"},
    {"No": "3", "시간": "10:00-11:00", "구분": "60분", "조장": "안내실", "대원": "순찰", "당직A": "휴게", "당직B": "로비"},
    {"No": "4", "시간": "11:00-12:00", "구분": "60분", "조장": "휴게", "대원": "안내실", "당직A": "로비", "당직B": "순찰"},
    {"No": "5", "시간": "12:00-13:00", "구분": "60분", "조장": "로비", "대원": "안내실", "당직A": "순찰", "당직B": "휴게"},
    {"No": "6", "시간": "13:00-14:00", "구분": "60분", "조장": "순찰", "대원": "휴게", "당직A": "안내실", "당직B": "로비"},
    {"No": "7", "시간": "14:00-15:00", "구분": "60분", "조장": "안내실", "대원": "휴게", "당직A": "로비", "당직B": "휴게"},
    {"No": "8", "시간": "15:00-16:00", "구분": "60분", "조장": "로비", "대원": "순찰", "당직A": "휴게", "당직B": "안내실"},
    {"No": "9", "시간": "16:00-17:00", "구분": "60분", "조장": "안내실", "대원": "휴게", "당직A": "로비", "당직B": "휴게"},
    {"No": "10", "시간": "17:00-18:00", "구분": "60분", "조장": "휴게", "대원": "안내실", "당직A": "휴게", "당직B": "로비"},
    {"No": "야1", "시간": "19:00-20:00", "구분": "60분", "조장": "안내실", "대원": "휴게", "당직A": "휴게", "당직B": "로비"},
    {"No": "야2", "시간": "20:00-21:00", "구분": "60분", "조장": "안내실", "대원": "석식", "당직A": "로비", "당직B": "석식"},
]

menu = st.sidebar.selectbox("메뉴 선택", ["🗓️ 근무 상황판", "📱 비상연락망", "📝 연차 관리"])

if menu == "🗓️ 근무 상황판":
    st.subheader("🗓️ C조 실시간 근무 상황판")
    
    selected_date = st.sidebar.date_input("조회 날짜", datetime.now().date())
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

        # 근무자 상단 고정 바
        st.info(f"📍 **{selected_date} 편성** | 조장: 황재업 | A: {a_worker} | B: {b_worker} | C: {c_worker}")

        # 시간표 데이터프레임 구성
        display_data = []
        for row in RAW_TIMETABLE:
            display_data.append({
                "시간": row["시간"],
                "비고": row["구분"],
                "황재업": row["조장"],
                a_worker: row["대원"],
                b_worker: row["당직A"],
                c_worker: row["당직B"]
            })
        
        df = pd.DataFrame(display_data)

        # 2시간 근무(120분) 구간 시각적 강조 스타일 함수
        def highlight_long_shift(s):
            return ['background-color: #3e3e3e; border-left: 5px solid #ff4b4b' if s['비고'] in ['120분', '연장'] else '' for _ in s]

        st.dataframe(
            df.style.apply(highlight_long_shift, axis=1),
            use_container_width=True,
            hide_index=True,
            height=600
        )
        
        st.warning("⚠️ **빨간색 선**으로 표시된 구간은 **2시간 연속 근무** 구간입니다. 착오 없으시기 바랍니다.")

    else:
        st.warning("C조 근무일이 아닙니다.")
