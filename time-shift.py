import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 회관 60분 정박자 기준 데이터 (사용자 엑셀 의도 100% 반영) ---
# 회관이 1시간마다 교대하는 흐름을 행의 기준으로 삼았습니다.
# 의산연의 30분 단위 세부 업무(순찰, 휴게 등)를 칸 안에 명확히 표기했습니다.
FIXED_SCHEDULE = [
    {"No": "1", "시간": "07:00-08:00", "회관A": "로비", "의산B(A)": "로비", "의산C(B)": "휴게", "분": "60"},
    {"No": "2", "시간": "08:00-09:00", "회관A": "휴게", "의산B(A)": "휴게", "의산C(B)": "로비", "분": "60"},
    {"No": "3", "시간": "09:00-10:00", "회관A": "순찰", "의산B(A)": "휴게", "의산C(B)": "로비", "분": "60"},
    {"No": "4", "시간": "10:00-11:00", "회관A": "안내실", "의산B(A)": "로비", "의산C(B)": "순찰(30)/휴게(30)", "분": "30,30"},
    {"No": "5", "시간": "11:00-12:00", "회관A": "안내실", "의산B(A)": "순찰", "의산C(B)": "로비", "분": "60"},
    {"No": "6", "시간": "12:00-13:00", "회관A": "휴게", "의산B(A)": "중식", "의산C(B)": "로비", "분": "60"},
    {"No": "7", "시간": "13:00-14:00", "회관A": "휴게", "의산B(A)": "휴게(30)/순찰(30)", "의산C(B)": "로비", "분": "30,30"},
    {"No": "8", "시간": "14:00-15:00", "회관A": "순찰", "의산B(A)": "로비", "의산C(B)": "휴게", "분": "60"},
    {"No": "9", "시간": "15:00-16:00", "회관A": "휴게", "의산B(A)": "로비", "의산C(B)": "휴게", "분": "60"},
    {"No": "10", "시간": "16:00-17:00", "회관A": "안내실", "의산B(A)": "휴게", "의산C(B)": "로비", "분": "60"},
    {"No": "11", "시간": "17:00-18:00", "회관A": "휴게", "의산B(A)": "휴게", "의산C(B)": "로비", "분": "60"},
    {"No": "야1", "시간": "19:00-20:00", "회관A": "휴게", "의산B(A)": "휴게", "의산C(B)": "로비", "분": "60"},
    {"No": "야2", "시간": "20:00-21:00", "회관A": "석식", "의산B(A)": "로비", "의산C(B)": "석식", "분": "60"},
]

st.set_page_config(page_title="보안 통합 관리 시스템", layout="wide")
st.title("🗓️ C조 근무 상황판 (회관 기준)")

# --- 2. 날짜 및 인원 배정 로직 ---
selected_date = st.sidebar.date_input("날짜 선택", datetime(2026, 3, 24).date())
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    idx = days_diff // 3
    a_rotation = ["이태원", "김태언", "이정석"]
    a_worker = a_rotation[(idx // 2) % 3] 
    
    all_members = ["김태언", "이태원", "이정석"]
    others = [m for m in all_members if m != a_worker]
    others.sort(key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x])
    
    # B, C 교대 로직
    b_worker, c_worker = (others[1], others[0]) if idx % 2 == 1 else (others[0], others[1])

    st.success(f"✅ **{selected_date}** | 회관: {a_worker} | 의산B: {b_worker} | 의산C: {c_worker}")

    # --- 3. 표 데이터 구성 ---
    table_rows = []
    for r in FIXED_SCHEDULE:
        table_rows.append({
            "시간": r["시간"],
            f"{a_worker}(회관)": r["회관A"],
            f"{b_worker}(의산B)": r["의산B(A)"],
            f"{c_worker}(의산C)": r["의산C(B)"],
            "분": r["분"]
        })

    df = pd.DataFrame(table_rows)

    # --- 4. 스타일 함수 정의 (NameError 수정 완료) ---
    def style_workplace(val):
        color = 'white'
        val_str = str(val)
        if '로비' in val_str: color = '#FF4B4B'  # 빨강
        elif '순찰' in val_str: color = '#1C83E1' # 파랑
        elif '휴게' in val_str: color = '#2E7D32' # 초록
        elif '식' in val_str: color = '#F39C12'   # 주황
        elif '안내실' in val_str: color = '#00C0F2' # 하늘
        return f'color: {color}; font-weight: bold'

    # 스타일 적용하여 테이블 출력
    st.table(df.style.applymap(style_workplace))

    st.info(f"""
    **📌 표 구성 의도 (회관 60분 기준)**
    - **축**: 성의회관({a_worker})의 1시간 교차 흐름을 기준으로 정렬했습니다.
    - **의산연**: 회관 근무자가 바뀔 때, 의산연 근무자가 연속 근무 중인지(8-10시 로비 등) 한눈에 파악 가능합니다.
    - **세부**: 10:00와 13:00에 발생하는 의산연의 30분 단위 업무 전환을 명시했습니다.
    """)
else:
    st.warning("C조 근무일이 아닙니다.")
