import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 및 데이터 ---
START_DATE = datetime(2026, 3, 24).date()
# 입사 순서 (선임 -> 후임)
RANK = ["김태언", "이태원", "이정석"]
# 회관 순번 (설명해주신 순서)
HALL_ROTATION = ["김태언", "이정석", "이태원"]
# 강조 색상
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "이정석": "#FFFDE7", "김태언": "#E8F5E9"}

# [고정] 시간표 패턴
BASE_PATTERN = [
    {"시간": "07:00", "조": "안내실", "회": "로비", "A": "휴게", "B": "로비"},
    {"시간": "08:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴게"},
    {"시간": "09:00", "조": "안내실", "회": "순찰", "A": "로비", "B": "휴게"},
    {"시간": "10:00", "조": "휴게", "회": "안내실", "A": "순찰/휴", "B": "로비"},
    {"시간": "11:00", "조": "안내실", "회": "중식", "A": "중식", "B": "로비"},
    {"시간": "12:00", "조": "중식", "회": "안내실", "A": "로비", "B": "중식"},
    {"시간": "13:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴/순"},
    {"시간": "14:00", "조": "순찰", "회": "안내실", "A": "휴게", "B": "로비"},
    {"시간": "15:00", "조": "안내실", "회": "휴게", "A": "휴게", "B": "로비"},
    {"시간": "16:00", "조": "휴게", "회": "안내실", "A": "로비", "B": "휴게"},
    {"시간": "17:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴게"},
    {"시간": "18:00", "조": "안내실", "회": "휴게", "A": "휴게", "B": "로비"},
    {"시간": "19:00", "조": "안내실", "회": "석식", "A": "로비", "B": "석식"},
    {"시간": "20:00", "조": "안내실", "회": "안내실", "A": "석식", "B": "로비"},
    {"시간": "21:00", "조": "석식", "회": "안내실", "A": "로비", "B": "휴게"},
    {"시간": "22:00", "조": "안내실", "회": "순찰", "A": "로비", "B": "휴게"},
    {"시간": "23:00", "조": "순찰", "회": "취침", "A": "순찰", "B": "로비"},
    {"시간": "00:00", "조": "안내실", "회": "취침", "A": "취침", "B": "로비"},
    {"시간": "01:00", "조": "안내실", "회": "취침", "A": "취침", "B": "로비"},
    {"시간": "02:00", "조": "안내실", "회": "취침", "A": "취침", "B": "로비"},
    {"시간": "03:00", "조": "취침", "회": "회관근무", "A": "로비", "B": "취침"},
    {"시간": "04:00", "조": "취침", "회": "회관근무", "A": "로비", "B": "취침"},
    {"시간": "05:00", "조": "취침", "회": "회관근무", "A": "로비", "B": "취침"},
    {"시간": "06:00", "조": "안내실", "회": "회관근무", "A": "로비", "B": "순찰"},
]

# --- 2. 핵심 로직 함수 ---
def get_roster(target_date):
    days_diff = (target_date - START_DATE).days
    if days_diff % 3 != 0: return None
    
    shift_idx = days_diff // 3
    # 회관 근무자 (3/24 이태원은 이전 패턴의 마지막이므로, 3/27부터 김태언 2회 시작 유도)
    # 실제 이미지 흐름에 맞춰 shift_idx를 조정합니다.
    hall_worker = HALL_ROTATION[(shift_idx + 2) // 2 % 3]
    
    # 나머지 인원 추출 및 선임순 정렬
    others = [w for w in RANK if w != hall_worker]
    # 선임자(먼저 입사)가 others[0], 후임자가 others[1]
    
    # 회관 1회차는 선임이 A, 2회차는 선임이 B (맞교대)
    if shift_idx % 2 == 0:
        return hall_worker, others[0], others[1] # 선임A, 후임B
    else:
        return hall_worker, others[1], others[0] # 후임A, 선임B

# --- 3. Streamlit UI ---
st.set_page_config(page_title="성의교정 C조", layout="centered")
st.markdown("<h2 style='text-align:center;'>성의교정 C조 근무 시스템</h2>", unsafe_allow_html=True)

with st.sidebar:
    menu = st.radio("메뉴", ["📅 근무 편성표", "📍 오늘 상황판"])
    user_name = st.selectbox("👤 이름 강조", ["안 함", "황재업"] + RANK)

if menu == "📅 근무 편성표":
    cal_list = []
    for i in range(45): # 45일치 계산
        d = START_DATE + timedelta(days=i)
        res = get_roster(d)
        if res:
            h, a, b = res
            cal_list.append({
                "날짜": f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][d.weekday()]})",
                "조장": "황재업", "회관": h, "의산A": a, "의산B": b
            })
    
    df = pd.DataFrame(cal_list)
    st.dataframe(df, use_container_width=True, hide_index=True)

elif menu == "📍 오늘 상황판":
    sel_date = st.date_input("날짜 선택", datetime.now().date())
    res = get_roster(sel_date)
    if res:
        h, a, b = res
        st.subheader(f"📅 {sel_date} 근무자: 조장(황재업), 회관({h}), A({a}), B({b})")
        board = pd.DataFrame([
            {"시간": r["시간"], "황재업(조)": r["조"], f"{h}(회)": r["회"], f"{a}(A)": r["A"], f"{b}(B)": r["B"]}
            for r in BASE_PATTERN
        ])
        st.dataframe(board, use_container_width=True, hide_index=True)
    else:
        st.info("비번입니다.")
