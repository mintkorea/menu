import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 회관 60분 정박자 기준 데이터 (엑셀 시트 의도 완벽 반영) ---
# 모든 행은 회관의 교대 시간인 60분 단위로 고정합니다.
# 의산연은 이 흐름에 맞춰 연속 근무나 세부 업무(30분 단위)를 표시합니다.
FIXED_SCHEDULE = [
    {"No": "1", "시간": "07:00-08:00", "회관A": "로비", "의산B(A)": "로비", "의산C(B)": "휴게", "비고": "60"},
    {"No": "2", "시간": "08:00-09:00", "회관A": "휴게", "의산B(A)": "휴게", "의산C(B)": "로비", "비고": "120분 시작"},
    {"No": "3", "시간": "09:00-10:00", "회관A": "순찰", "의산B(A)": "휴게", "의산C(B)": "로비", "비고": "의산연 연속"},
    {"No": "4", "시간": "10:00-11:00", "회관A": "안내실", "의산B(A)": "로비", "의산C(B)": "순찰(30)/휴게(30)", "비고": "30,30"},
    {"No": "5", "시간": "11:00-12:00", "회관A": "안내실", "의산B(A)": "순찰", "의산C(B)": "로비", "비고": "60"},
    {"No": "6", "시간": "12:00-13:00", "회관A": "휴게", "의산B(A)": "중식", "의산C(B)": "로비", "비고": "60"},
    {"No": "7", "시간": "13:00-14:00", "회관A": "휴게", "의산B(A)": "휴게(30)/순찰(30)", "의산C(B)": "로비", "비고": "30,30"},
    {"No": "8", "시간": "14:00-15:00", "회관A": "순찰", "의산B(A)": "로비", "의산C(B)": "휴게", "비고": "60"},
    {"No": "9", "시간": "15:00-16:00", "회관A": "휴게", "의산B(A)": "로비", "의산C(B)": "휴게", "비고": "60"},
    {"No": "10", "시간": "16:00-17:00", "회관A": "안내실", "의산B(A)": "휴게", "의산C(B)": "로비", "비고": "60"},
    {"No": "11", "시간": "17:00-18:00", "회관A": "휴게", "의산B(A)": "휴게", "의산C(B)": "로비", "비고": "60"},
    {"No": "야1", "시간": "19:00-20:00", "회관A": "휴게", "의산B(A)": "휴게", "의산C(B)": "로비", "비고": "60"},
    {"No": "야2", "시간": "20:00-21:00", "회관A": "석식", "의산B(A)": "로비", "의산C(B)": "석식", "비고": "60"},
]

st.set_page_config(layout="wide")
st.title("🗓️ 성의교정 C조 근무 상황판 (회관 기준)")

# --- 2. 날짜 및 인원 배정 로직 (3/24 예시) ---
selected_date = st.sidebar.date_input("날짜", datetime(2026, 3, 24).date())
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    idx = days_diff // 3
    a_rotation = ["이태원", "김태언", "이정석"]
    a_worker = a_rotation[(idx // 2) % 3] 
    
    # 선임순 정렬 및 B, C 배정
    all_members = ["김태언", "이태원", "이정석"]
    others = [m for m in all_members if m != a_worker]
    others.sort(key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x])
    
    b_worker, c_worker = (others[1], others[0]) if idx % 2 == 1 else (others[0], others[1])

    st.success(f"✅ **{selected_date}** | 회관: {a_worker} | 의산B: {b_worker} | 의산C: {c_worker}")

    # --- 3. 표 생성 ---
    table_rows = []
    for r in FIXED_SCHEDULE:
        table_rows.append({
            "시간": r["시간"],
            f"{a_worker}(회관)": r["회관A"],
            f"{b_worker}(의산B)": r["의산B(A)"],
            f"{c_worker}(의산C)": r["의산C(B)"],
            "비고": r["비고"]
        })

    df = pd.DataFrame(table_rows)

    # 근무지별 색상 강조 (가독성)
    def style_row(val):
        color = 'white'
        if '로비' in str(val): color = '#FF4B4B'
        elif '순찰' in str(val): color = '#1C83E1'
        elif '휴게' in str(val): color = '#2E7D32'
        elif '식' in str(val): color = '#F39C12'
        elif '안내실' in str(val): color = '#00C0F2'
        return f'color: {color}; font-weight: bold'

    st.table(df.style.applymap(style_workplace))

    st.info(f"""
    **💡 표 구성 의도 (회관 기준 60분 정박자)**
    - 모든 행은 **회관 근무자({a_worker})**의 1시간 교대 주기에 맞춰져 있습니다.
    - 의산연 근무자는 회관이 한 번 바뀔 때 같이 바뀌거나, 혹은 동일 위치에서 120분간 유지되는 모습이 명확히 보입니다.
    - 10:00와 13:00의 세부 업무 분할(30분 단위)은 비고란과 해당 칸에 명시하였습니다.
    """)
else:
    st.warning("C조 근무일이 아닙니다.")
