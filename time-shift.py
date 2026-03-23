import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 데이터 및 로테이션 설정 (이미지 순서 및 규칙 완벽 반영) ---
# 규칙: 한 사람이 회관을 2회 연속하고, 나머지 2명은 A, B를 교대함.
START_DATE = datetime(2026, 3, 24).date()
# 인원 리스트 (패턴 계산을 위한 고정 순서)
WORKERS = ["이태원", "이정석", "김태언"] 
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "이정석": "#FFFDE7", "김태언": "#E8F5E9"}

# 시간대별 상세 업무 (기존 이미지 기준 고정)
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

# --- 2. 로직 함수 (회관 2연속 패턴 계산) ---
def get_daily_workers(target_date):
    days_diff = (target_date - START_DATE).days
    if days_diff % 3 != 0:
        return None  # 비번일
    
    # 근무일 회차 (0, 1, 2, 3...)
    shift_no = days_diff // 3
    
    # 1. 회관 근무자 결정 (2회마다 변경)
    # 3/24, 3/27(김태언) / 3/30, 4/2(이정석) / 4/5, 4/8(이태원) 등의 순서로 가도록 인덱스 조정
    # 이미지 4b61ae 기준: 3/24(이태원), 3/27, 3/30(김태언), 4/2, 4/5(이정석), 4/8, 4/11(이태원)
    # 3/24은 예외적으로 1번만 수행된 시점이라면:
    h_idx = ((shift_no + 1) // 2) % 3
    main_worker = ["이태원", "김태언", "이정석"][h_idx]
    
    # 2. 나머지 2명 결정
    others = [w for w in WORKERS if w != main_worker]
    # 회차에 따라 A, B 교대
    if shift_no % 2 == 0:
        w_a, w_b = others[0], others[1]
    else:
        w_a, w_b = others[1], others[0]
        
    return main_worker, w_a, w_b

# --- 3. Streamlit UI 설정 ---
st.set_page_config(page_title="성의교정 C조", layout="centered")
st.markdown("<style>.main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; }</style>", unsafe_allow_html=True)

with st.sidebar:
    menu = st.radio("메뉴", ["📅 교대 근무표", "📍 실시간 상황판"])
    user_focus = st.selectbox("👤 이름 강조", ["안 함", "황재업"] + WORKERS)

now = datetime.now().date()

if menu == "📅 교대 근무표":
    st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    cal_list = []
    # 3/24부터 45일간 계산
    for i in range(45):
        d = START_DATE + timedelta(days=i)
        res = get_daily_workers(d)
        if res:
            h, a, b = res
            cal_list.append({
                "날짜": f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][d.weekday()]})",
                "조장": "황재업", "회관": h, "의산A": a, "의산B": b
            })
    
    df = pd.DataFrame(cal_list)
    st.dataframe(df, use_container_width=True, hide_index=True)

elif menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>실시간 근무 상황판</div>", unsafe_allow_html=True)
    sel_d = st.date_input("날짜 선택", now)
    res = get_daily_workers(sel_d)
    if res:
        h, a, b = res
        board = pd.DataFrame([
            {"시간": r["시간"], "황재업(조)": r["조"], f"{h}(회)": r["회"], f"{a}(A)": r["A"], f"{b}(B)": r["B"]}
            for r in BASE_PATTERN
        ])
        st.dataframe(board, use_container_width=True, hide_index=True)
    else:
        st.info("💡 오늘은 C조 비번입니다.")
