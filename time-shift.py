import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 시간 포맷 함수 ---
def format_time(excel_val):
    if pd.isna(excel_val) or isinstance(excel_val, str): return ""
    total_seconds = int(round(excel_val * 24 * 3600))
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}"

# --- 2. 엑셀 시트 데이터 그대로 반영 (누락 없음) ---
# 엑셀의 From-To와 오른쪽 '시간' 열을 매칭하여 구성
RAW_DATA = [
    {"No": "1", "From": 0.2916, "To": 0.3125, "조장": "안내실", "회관": "로비", "의산A": "로비", "의산B": "휴게", "할당": "60"},
    {"No": "2", "From": 0.3333, "To": 0.3541, "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비", "할당": "120"},
    {"No": "3", "From": 0.3750, "To": 0.3958, "조장": "안내실", "회관": "순찰", "의산A": "휴게", "의산B": "로비", "할당": ""},
    {"No": "4", "From": 0.4166, "To": 0.4375, "조장": "휴게", "회관": "안내실", "의산A": "로비", "의산B": "순찰", "할당": "30"},
    {"No": "5", "From": 0.4583, "To": 0.4791, "조장": "로비", "회관": "안내실", "의산A": "순찰", "의산B": "식사", "할당": "120"},
    {"No": "6", "From": 0.5000, "To": 0.5208, "조장": "순찰", "회관": "휴게", "의산A": "안내실", "의산B": "로비", "할당": "60"},
    {"No": "7", "From": 0.5416, "To": 0.5625, "조장": "안내실", "회관": "휴게", "의산A": "로비", "의산B": "휴게", "할당": "60"},
    {"No": "8", "From": 0.5833, "To": 0.6041, "조장": "로비", "회관": "순찰", "의산A": "휴게", "의산B": "안내실", "할당": "60"},
    {"No": "9", "From": 0.6250, "To": 0.6458, "조장": "안내실", "회관": "휴게", "의산A": "로비", "의산B": "휴게", "할당": "60"},
    {"No": "10", "From": 0.6666, "To": 0.7291, "조장": "휴게", "회관": "안내실", "의산A": "휴게", "의산B": "로비", "할당": "60"},
    {"No": "야1", "From": 0.7083, "To": 0.7291, "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비", "할당": "60"},
    {"No": "야2", "From": 0.7500, "To": 0.7708, "조장": "안내실", "회관": "석식", "의산A": "로비", "의산B": "석식", "할당": "60"},
]

st.set_page_config(layout="wide")
st.title("🗓️ C조 근무 상황판 (최종 수정)")

# --- 3. 근무자 배정 로직 (3/24 예시) ---
selected_date = st.sidebar.date_input("날짜", datetime(2026, 3, 24).date())
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    idx = days_diff // 3
    a_rotation = ["이태원", "김태언", "이정석"]
    a_worker = a_rotation[(idx // 2) % 3] 
    
    all_members = ["김태언", "이태원", "이정석"]
    others = [m for m in all_members if m != a_worker]
    others.sort(key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x])
    
    b_worker, c_worker = (others[1], others[0]) if idx % 2 == 1 else (others[0], others[1])

    st.success(f"✅ **{selected_date}** | 회관(A): {a_worker} | 의산연(B): {b_worker} | 의산연(C): {c_worker}")

    # --- 4. 테이블 렌더링 ---
    table_list = []
    for r in RAW_DATA:
        table_list.append({
            "시작": format_time(r["From"]),
            "종료": format_time(r["To"]),
            "황재업": r["조장"],
            f"{a_worker}(A)": r["회관"],
            f"{b_worker}(B)": r["의산A"],
            f"{c_worker}(C)": r["의산B"],
            "시간": r["할당"]
        })

    df = pd.DataFrame(table_list)
    
    # 가독성을 위해 '시간' 열이 120인 경우 행 전체 강조
    def highlight_120(s):
        return ['background-color: #2c3e50' if s['시간'] == '120' else '' for _ in s]

    st.table(df) # 모바일에서 가장 깨지지 않는 기본 테이블 형태 사용

    st.markdown("""
    **※ 안내 사항**
    1. 회관(A)은 60분 단위로 로테이션 됩니다.
    2. 의산연(B, C)은 60분 또는 120분 단위로 연속 근무/휴게가 편성됩니다.
    3. 표의 **'휴게'**는 해당 시간대의 대기 또는 휴식 업무를 의미합니다.
    """)

else:
    st.warning("C조 근무일이 아닙니다.")
