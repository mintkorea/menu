import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. 기기-성함 매칭 및 설정 ---
DEVICE_MAP = {"S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원"}
PATTERN_START_DATE = datetime(2026, 3, 9).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7", "연차": "#FFEBEE"}
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

# [KST 시간 고정] - 새벽 오류 해결의 핵심
now_kst = datetime.now(timezone(timedelta(hours=9)))
today_val = now_kst.date()

# --- 2. 데이터 및 기기 인식 로직 ---
def load_vacation_data():
    if os.path.exists(VACATION_FILE):
        try:
            df = pd.read_csv(VACATION_FILE)
            df['날짜'] = pd.to_datetime(df['날짜']).dt.date
            return df
        except: return pd.DataFrame(columns=['날짜', '이름', '사유'])
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

def get_device_user():
    ua = st_javascript("navigator.userAgent")
    if ua and ua != 0:
        ua_str = str(ua).upper()
        for model, name in DEVICE_MAP.items():
            if model in ua_str: return name
    return "안 함"

df_vac = load_vacation_data()

# --- 3. 사이드바 ---
with st.sidebar:
    st.header("⚙️ 스마트 설정")
    menu = st.radio("메뉴 이동", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 신청/관리"])
    st.divider()
    detected = get_device_user()
    user_list = ["안 함", "황재업", "김태언", "이태원", "이정석"]
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = detected if detected in user_list else "안 함"
    user_name = st.selectbox("👤 내 이름 강조", user_list, index=user_list.index(st.session_state.selected_user))

# --- 4. 메뉴별 로직 ---
if menu == "📍 실시간 상황판":
    st.markdown("### 📍 실시간 근무 및 현장 안내")
    st.caption(f"🕒 현재 시각(KST): {now_kst.strftime('%Y-%m-%d %H:%M')}")

    # [이미지 속 바로 그 부분] 하루 근무 시간표
    with st.expander("⏰ C조 하루 근무 시간표 (상세)", expanded=True):
        schedule_df = pd.DataFrame([
            {"구분": "주간근무", "시간": "08:00 ~ 18:00", "비고": "성희관/의산연 거점"},
            {"구분": "휴게/식사", "시간": "12:00 ~ 13:00", "비고": "순번제 (지정장소)"},
            {"구분": "야간근무", "시간": "18:00 ~ 08:00", "비고": "교내 순찰 및 보안대기"},
            {"구분": "인수인계", "시간": "07:30 ~ 08:00", "비고": "D조와 업무교대"}
        ])
        st.table(schedule_df)

    # 근무 패턴 계산 및 내 위치 확인
    diff_days = (today_val - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        shift_count = diff_days // 3
        cycle_idx = (shift_count // 2) % 3 
        is_second_day = shift_count % 2 == 1
        
        if cycle_idx == 0: h_p, a_p, b_p = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
        elif cycle_idx == 1: h_p, a_p, b_p = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
        else: h_p, a_p, b_p = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
        
        assignments = {"조장": "황재업", "성희관": h_p, "의산연(A)": a_p, "의산연(B)": b_p}
        
        # 내 근무지 강조 안내
        if user_name != "안 함":
            my_loc = next((loc for loc, name in assignments.items() if name == user_name), None)
            if my_loc:
                st.info(f"💡 **{user_name}**님, 오늘 근무지는 **[{my_loc}]** 입니다.")

        # 실시간 상황판 (Metric 카드)
        cols = st.columns(4)
        for i, (pos, name) in enumerate(assignments.items()):
            is_vac = not df_vac[(df_vac['날짜'] == today_val) & (df_vac['이름'] == name)].empty
            with cols[i]:
                st.metric(pos, "연차" if is_vac else name)
                if is_vac: st.error("부재중")
                else: st.success("근무중")
    else:
        st.warning(f"😴 오늘({today_val.strftime('%m/%d')})은 C조 비번입니다.")

# (편성표/연차 메뉴는 기존 소스 그대로 유지)
