import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. 한국 시간(KST) 설정 로직 ---
def get_now_kst():
    # 서버 시간에 상관없이 한국 시간(UTC+9)으로 계산
    return datetime.now(timezone(timedelta(hours=9)))

# --- 2. 기본 설정 ---
DEVICE_MAP = {"S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원"}
PATTERN_START_DATE = datetime(2026, 3, 24).date() # 3/24 근무일 기준
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7", "연차": "#FFEBEE"}
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성희교정 C조 관리 시스템", layout="centered")

# --- 데이터 처리 함수 ---
def load_vacation_data():
    if os.path.exists(VACATION_FILE):
        try:
            df = pd.read_csv(VACATION_FILE)
            df['날짜'] = pd.to_datetime(df['날짜']).dt.date
            return df
        except: return pd.DataFrame(columns=['날짜', '이름', '사유'])
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

df_vac = load_vacation_data()

def check_vacation(date, name):
    is_vac = df_vac[(df_vac['날짜'] == date) & (df_vac['이름'] == name)]
    return "연차" if not is_vac.empty else name

def get_shift_workers(date):
    diff_days = (date - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        shift_count = diff_days // 3
        cycle_idx = (shift_count // 2) % 3 
        is_second_day = shift_count % 2 == 1
        if cycle_idx == 0: h_p, a_p, b_p = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
        elif cycle_idx == 1: h_p, a_p, b_p = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
        else: h_p, a_p, b_p = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
        return [("조장", "황재업"), ("회관", h_p), ("의산(A)", a_p), ("의산(B)", b_p)]
    return None

# --- 3. 사이드바 및 사용자 인식 ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 관리"])
    user_name = st.selectbox("👤 이름 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- 4. 메인 로직 ---
now_kst = get_now_kst()
today_val = now_kst.date()

if menu == "📍 실시간 상황판":
    st.markdown("### 📍 오늘의 근무 스케줄")
    
    # [시간 표시] 현재가 몇 시인지 상단에 명시 (오차 확인용)
    st.caption(f"🕒 현재 시각(KST): {now_kst.strftime('%Y-%m-%d %H:%M')}")

    # 1. 근무 시간표 (스케줄) 시각적 강조
    # 종이 근무표를 대체할 수 있도록 한눈에 들어오는 카드로 구성
    st.markdown("#### ⏰ 근무 타임라인")
    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1:
        st.info("**☀️ 주간**\n\n08:00 ~ 18:00\n\n회관/의산 정위치")
    with t_col2:
        st.info("**🌙 야간**\n\n18:00 ~ 08:00\n\n순찰 및 대기")
    with t_col3:
        st.info("**🔄 교대**\n\n08:00 정시\n\n인수인계 철저")

    st.divider()

    # 2. 오늘 근무 상태 (비번일 때도 스케줄 정보는 유지)
    workers = get_shift_workers(today_val)
    
    if workers:
        st.success(f"✅ 오늘({today_val.strftime('%m/%d')})은 **C조 근무일**입니다.")
        cols = st.columns(4)
        for i, (pos, name) in enumerate(workers):
            status = check_vacation(today_val, name)
            with cols[i]:
                st.metric(pos, status)
                if status == "연차": st.error("연차")
                else: st.success("근무")
    else:
        st.warning(f"😴 오늘({today_val.strftime('%m/%d')})은 **C조 비번**입니다.")
        # 다음 근무일 안내
        days_diff = (today_val - PATTERN_START_DATE).days
        wait_days = 3 - (days_diff % 3) if days_diff % 3 > 0 else abs(days_diff % 3)
        next_date = today_val + timedelta(days=wait_days)
        st.info(f"📅 다음 근무일: **{next_date.strftime('%m/%d')}** ({int(wait_days)}일 후)")

    st.divider()
    
    # 3. 추가 안내 (비상연락 등)
    st.markdown("#### 🚨 근무 유의사항")
    st.write("- 교대 시간 10분 전 도착 및 장비 점검 필수")
    st.write("- 야간 순찰 시 취약 지역(의산 지하 등) 철저 확인")

# [나머지 메뉴 로직 유지...]
