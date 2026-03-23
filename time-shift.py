import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 엑셀 기반 데이터 (장소 및 시간 정밀 수정) ---
# 의산연 열에는 '안내실'이 없으며, 사용자님이 짚어주신 순찰/식사 로직을 반영
RAW_DATA = [
    {"No": "1", "시간": "07:00-08:00", "회관": "로비", "당직A": "로비", "당직B": "휴게", "분할": "60"},
    {"No": "2", "시간": "08:00-10:00", "회관": "휴게/순찰", "당직A": "휴게", "당직B": "로비", "분할": "120"},
    {"No": "3", "시간": "10:00-11:00", "회관": "안내실", "당직A": "로비", "당직B": "순찰(30)→휴게(30)", "분할": "30,30"},
    {"No": "4", "시간": "11:00-12:00", "회관": "안내실", "당직A": "순찰", "당직B": "로비", "분할": "60"},
    {"No": "5", "시간": "12:00-13:00", "회관": "휴게", "당직A": "중식", "당직B": "로비", "분할": "60"},
    {"No": "6", "시간": "13:00-14:00", "회관": "휴게", "당직A": "휴게(30)→순찰(30)", "당직B": "로비", "분할": "30,30"},
    {"No": "7", "시간": "14:00-15:00", "회관": "순찰", "당직A": "로비", "당직B": "휴게", "분할": "60"},
    {"No": "8", "시간": "15:00-16:00", "회관": "휴게", "당직A": "로비", "당직B": "휴게", "분할": "60"},
    {"No": "9", "시간": "16:00-17:00", "회관": "안내실", "당직A": "휴게", "당직B": "로비", "분할": "60"},
    {"No": "10", "시간": "17:00-18:00", "회관": "휴게", "당직A": "휴게", "당직B": "로비", "분할": "60"},
    {"No": "야1", "시간": "19:00-20:00", "회관": "휴게", "당직A": "휴게", "당직B": "로비", "분할": "60"},
    {"No": "2", "시간": "20:00-21:00", "회관": "석식", "당직A": "로비", "당직B": "석식", "분할": "60"},
]

st.set_page_config(layout="wide")
st.title("🗓️ 성의교정 C조 근무 상황판")

# --- 2. 날짜 및 인원 배정 (3/24 예시) ---
selected_date = st.sidebar.date_input("날짜", datetime(2026, 3, 24).date())
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    idx = days_diff // 3
    a_rotation = ["이태원", "김태언", "이정석"]
    a_worker = a_rotation[(idx // 2) % 3] 
    others = sorted([m for m in ["김태언", "이태원", "이정석"] if m != a_worker], key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x])
    b_worker, c_worker = (others[1], others[0]) if idx % 2 == 1 else (others[0], others[1])

    st.success(f"✅ **{selected_date}** | 회관: {a_worker} | 의산B: {b_worker} | 의산C: {c_worker}")

    # --- 3. 상황판 생성 ---
    display_data = []
    for r in RAW_DATA:
        display_data.append({
            "시간": r["시간"],
            f"{a_worker}(회관)": r["회관"],
            f"{b_worker}(의산B)": r["당직A"],
            f"{c_worker}(의산C)": r["당직B"],
            "분": r["분할"]
        })

    df = pd.DataFrame(display_data)

    # 근무지별 고유 색상 (사용자 지정 명칭 기준)
    def style_workplace(val):
        color = 'white'
        if '로비' in str(val): color = '#FF4B4B'
        elif '순찰' in str(val): color = '#1C83E1'
        elif '휴게' in str(val): color = '#2E7D32'
        elif '식' in str(val): color = '#F39C12'
        elif '안내실' in str(val): color = '#00C0F2'
        return f'color: {color}; font-weight: bold'

    st.table(df.style.applymap(style_workplace))

    st.markdown(f"""
    **📌 의산연 근무 핵심 요약**
    - 10:00-11:00: **{c_worker}** 순찰(30분) 후 휴게(30분)
    - 12:00-13:00: **{b_worker}** 중식 1시간
    - 13:00-14:00: **{b_worker}** 휴게(30분) 후 순찰(30분)
    - **{c_worker}**는 11:00부터 13:00까지 로비에서 **2시간 연속 근무**입니다.
    """)
else:
    st.warning("C조 근무일이 아닙니다.")
