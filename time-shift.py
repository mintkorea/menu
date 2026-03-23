import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 시간 포맷 함수 ---
def format_time(excel_val):
    if pd.isna(excel_val) or isinstance(excel_val, str): return ""
    total_seconds = int(round(excel_val * 24 * 3600))
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}"

# --- 2. 로테이션 데이터 구성 ---
# 회관(대원)은 60분마다 바뀌고, 의산연(A, B)은 60분/120분 단위가 섞여 있음
RAW_DATA = [
    {"No": "1", "시작": 0.2916, "종료": 0.3125, "회관": "로비", "의산연A": "로비", "의산연B": "휴게", "비고": "60분"},
    {"No": "2-1", "시작": 0.3333, "종료": 0.3541, "회관": "휴게", "의산연A": "휴게", "의산연B": "로비", "비고": "의산연 120분 시작"},
    {"No": "2-2", "시작": 0.3750, "종료": 0.3958, "회관": "순찰", "의산연A": "휴게", "의산연B": "로비", "비고": "의산연 연속근무/휴게"},
    {"No": "4", "시작": 0.4166, "종료": 0.4375, "회관": "안내실", "의산연A": "로비", "의산연B": "순찰", "비고": "30분 단위 교차"},
    {"No": "5-1", "시작": 0.4583, "종료": 0.4791, "회관": "안내실", "의산연A": "순찰", "의산연B": "식사(60)", "비고": "의산연 120분(식사포함)"},
    {"No": "5-2", "시작": 0.5000, "종료": 0.5208, "회관": "휴게", "의산연A": "안내실", "의산연B": "로비", "비고": "회관 교대"},
    {"No": "7", "시작": 0.5416, "종료": 0.5625, "회관": "휴게", "의산연A": "로비", "의산연B": "휴게", "비고": "60분"},
    {"No": "8", "시작": 0.5833, "종료": 0.6041, "회관": "순찰", "의산연A": "휴게", "의산연B": "안내실", "비고": "60분"},
    {"No": "9", "시작": 0.6250, "종료": 0.6458, "회관": "휴게", "의산연A": "로비", "의산연B": "휴게", "비고": "60분"},
    {"No": "10", "시작": 0.6666, "종료": 0.7083, "회관": "안내실", "의산연A": "휴게", "의산연B": "로비", "비고": "60분"},
]

st.set_page_config(page_title="보안 통합 관리 시스템", layout="wide")
st.title("🗓️ C조 근무 상황판")

# --- 3. 날짜 및 인원 배정 (3/24 예시 적용) ---
selected_date = st.sidebar.date_input("날짜 선택", datetime(2026, 3, 24).date())
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    idx = days_diff // 3
    a_rotation = ["이태원", "김태언", "이정석"]
    a_worker = a_rotation[(idx // 2) % 3] # 2일 단위 회관(A) 고정
    
    others = [m for m in ["김태언", "이태원", "이정석"] if m != a_worker]
    others.sort(key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x]) # 선임순
    
    # B, C 교대 로직
    b_worker, c_worker = (others[1], others[0]) if idx % 2 == 1 else (others[0], others[1])

    st.success(f"✅ **{selected_date}** | 회관(A): {a_worker} | 의산연(B): {b_worker} | 의산연(C): {c_worker}")

    # --- 4. 상황판 테이블 생성 ---
    table_rows = []
    for r in RAW_DATA:
        table_rows.append({
            "시작": format_time(r["시작"]),
            "구분": r["비고"],
            f"{a_worker}(회관)": r["회관"],
            f"{b_worker}(의산B)": r["의산연A"],
            f"{c_worker}(의산C)": r["의산연B"]
        })

    df = pd.DataFrame(table_rows)

    # 연속 근무/휴게 시각적 강조 (배경색 동일화)
    def highlight_continuous(s):
        styles = [''] * len(s)
        if s['구분'] in ['의산연 120분 시작', '의산연 연속근무/휴게']:
            return ['background-color: #2e3b4e; color: #ffffff'] * len(s)
        if s['구분'] == '의산연 120분(식사포함)':
            return ['background-color: #4a3a1a; color: #ffffff'] * len(s)
        return styles

    st.dataframe(df.style.apply(highlight_continuous, axis=1), use_container_width=True, hide_index=True)

    st.markdown("""
    > **💡 로테이션 안내**
    > * **회관({a_worker})**은 60분마다 위치가 변경됩니다.
    > * **의산연({b_worker}, {c_worker})**은 회관이 바뀔 때 동일 위치에서 **연속 근무**하거나 **연속 휴게**하는 120분 주기가 포함되어 있습니다. (남색/갈색 표시 구간)
    """.format(a_worker=a_worker, b_worker=b_worker, c_worker=c_worker))

else:
    st.warning("C조 근무일이 아닙니다.")
