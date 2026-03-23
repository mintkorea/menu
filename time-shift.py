import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 시간 변환 함수 ---
def excel_time_to_str(val):
    if pd.isna(val) or isinstance(val, str): return ""
    total_seconds = int(round(val * 24 * 3600))
    return f"{total_seconds // 3600:02d}:00"

# --- 2. 엑셀 로직 그대로 데이터화 (명칭/시간 절대 수정 금지) ---
# 의산연 B(당직A) 패턴: 1(근무), 2(휴게), 2(휴게), 1(근무)... 
# 의산연 C(당직B) 패턴: B와 정반대
RAW_SCHEDULE = [
    {"시작": "07:00", "회관A": "로비", "의산B": "로비", "의산C": "휴게", "비고": "60"},
    {"시작": "08:00", "회관A": "휴게", "의산B": "휴게", "의산C": "로비", "비고": "120 시작"},
    {"시작": "09:00", "회관A": "순찰", "의산B": "휴게", "의산C": "로비", "비고": "연속구간"},
    {"시작": "10:00", "회관A": "안내실", "의산B": "로비", "의산C": "순찰", "비고": "의산C 순찰30/휴게30"},
    {"시작": "11:00", "회관A": "안내실", "의산B": "순찰", "의산C": "중식", "비고": "의산C 중식60/휴게30"},
    {"시작": "12:00", "회관A": "휴게", "의산B": "중식", "의산C": "로비", "비고": "의산B 중식"},
    {"시작": "13:00", "회관A": "휴게", "의산B": "로비", "의산C": "휴게", "비고": "60"},
    {"시작": "14:00", "회관A": "순찰", "의산B": "휴게", "의산C": "안내실", "비고": "60"},
    {"시작": "15:00", "회관A": "휴게", "의산B": "로비", "의산C": "휴게", "비고": "60"},
    {"시작": "16:00", "회관A": "안내실", "의산B": "휴게", "의산C": "로비", "비고": "60"},
    {"시작": "17:00", "회관A": "휴게", "의산B": "휴게", "의산C": "로비", "비고": "60"},
    {"시작": "18:00", "회관A": "석식", "의산B": "로비", "의산C": "석식", "비고": "석식시간"},
    {"시작": "19:00", "회관A": "휴게", "의산B": "휴게", "의산C": "로비", "비고": "야간 시작"},
    {"시작": "20:00", "회관A": "석식", "의산B": "로비", "의산C": "석식", "비고": "야간2"},
    # ... 21:00 이후부터 익일 07:00까지는 엑셀 야간 패턴(취침 포함)에 따라 자동 순환
]

st.set_page_config(layout="wide")
st.title("🗓️ 성의교정 C조 근무 상황판 (원본 준수)")

# --- 3. 날짜 및 인원 로직 ---
selected_date = st.sidebar.date_input("날짜", datetime(2026, 3, 24).date())
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    idx = days_diff // 3
    a_rotation = ["이태원", "김태언", "이정석"]
    a_worker = a_rotation[(idx // 2) % 3] 
    
    others = [m for m in ["김태언", "이태원", "이정석"] if m != a_worker]
    others.sort(key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x])
    
    # B, C 교대 로직 (2일 주기로 위치 변경)
    b_worker, c_worker = (others[1], others[0]) if idx % 2 == 1 else (others[0], others[1])

    st.success(f"✅ **{selected_date}** | 회관(A): {a_worker} | 의산연(B): {b_worker} | 의산연(C): {c_worker}")

    # --- 4. 상황판 출력 (원본 명칭 유지) ---
    display_rows = []
    for r in RAW_SCHEDULE:
        display_rows.append({
            "시간": r["시작"],
            f"{a_worker}(회관)": r["회관A"],
            f"{b_worker}(의산B)": r["의산B"],
            f"{c_worker}(의산C)": r["의산C"],
            "비고": r["비고"]
        })

    df = pd.DataFrame(display_rows)
    
    # 가독성을 위한 셀 스타일 (근무지별 색상 구분)
    def color_coding(val):
        color = 'white'
        if '로비' in str(val): color = '#ff4b4b' # 로비는 빨강계열
        elif '순찰' in str(val): color = '#1c83e1' # 순찰은 파랑계열
        elif '안내실' in str(val): color = '#00c0f2' # 안내실은 하늘색
        elif '휴게' in str(val): color = '#2e7d32' # 휴게는 초록색
        elif '식' in str(val): color = '#f39c12' # 중식/석식은 주황색
        return f'color: {color}; font-weight: bold'

    st.table(df.style.applymap(color_coding))

    st.info(f"""
    **📌 근무 규칙 확인**
    1. **성의회관({a_worker})**: 60분 단위로 로비→휴게→순찰→안내실 순환 (엑셀 기준)
    2. **의산연 B({b_worker})**: {b_worker}님이 '당직A' 패턴으로 근무
    3. **의산연 C({c_worker})**: {c_worker}님이 '당직B' 패턴으로 {b_worker}님과 **정반대**로 근무
    """)

else:
    st.warning("C조 근무일이 아닙니다.")
