import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from streamlit_javascript import st_javascript

# --- 1. 기기-성함 매칭 데이터 ---
DEVICE_MAP = {
    "S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원",
}

# --- 2. 기준 날짜 설정 (3월 24일 근무일 기준) ---
PATTERN_START_DATE = datetime(2026, 3, 24).date() 

WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7", "연차": "#FFEBEE"}
VACATION_FILE = 'vacation.csv'
ADMIN_PASSWORD = "1234"

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

# --- 데이터 처리 함수들 ---
def load_vacation_data():
    if os.path.exists(VACATION_FILE):
        try:
            df = pd.read_csv(VACATION_FILE)
            df['날짜'] = pd.to_datetime(df['날짜']).dt.date
            return df
        except:
            return pd.DataFrame(columns=['날짜', '이름', '사유'])
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

def save_vacation_data(df):
    df.to_csv(VACATION_FILE, index=False, encoding='utf-8-sig')

def get_device_user():
    ua = st_javascript("navigator.userAgent")
    if ua and ua != 0:
        ua_str = str(ua).upper()
        for model, name in DEVICE_MAP.items():
            if model in ua_str: return name
    return "안 함"

df_vac = load_vacation_data()

def check_vacation(date, name):
    is_vac = df_vac[(df_vac['날짜'] == date) & (df_vac['이름'] == name)]
    return "연차" if not is_vac.empty else name

# --- 3. 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 스마트 설정")
    menu = st.radio("메뉴 이동", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 신청/관리"])
    
    st.divider()
    detected = get_device_user()
    user_list = ["안 함", "황재업", "김태언", "이태원", "이정석"]
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = detected if detected in user_list else "안 함"
    user_name = st.selectbox("👤 내 이름 강조", user_list, index=user_list.index(st.session_state.selected_user))

# --- 4. 공통 근무 계산 로직 ---
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

# --- 5. 메뉴별 메인 로직 ---

if menu == "📍 실시간 상황판":
    st.markdown("### 📍 실시간 근무 및 안내")
    today = datetime.now().date()
    
    # 상단 안내 (휴무/근무 여부)
    workers = get_shift_workers(today)
    
    if workers:
        st.success(f"✅ 오늘({today.strftime('%m/%d')})은 **C조 근무일**입니다.")
        cols = st.columns(4)
        for i, (pos, name) in enumerate(workers):
            status = check_vacation(today, name)
            with cols[i]:
                st.metric(pos, status)
                if status == "연차": st.error("❌ 부재중")
                else: st.success("✅ 근무중")
    else:
        st.warning(f"😴 오늘({today.strftime('%m/%d')})은 **비번/휴무**입니다.")
        next_work_date = today + timedelta(days=(3 - (today - PATTERN_START_DATE).days % 3) % 3)
        st.info(f"다음 근무 예정일: **{next_work_date.strftime('%m/%d')}**")

    st.divider()
    
    # [요청사항] 실제 근무시간표(편성표)를 아래쪽에 항상 표출
    st.subheader("🗓️ 주간 근무 편성표")
    # 오늘 포함 전후 7일간의 근무일을 보여줌
    cal_list = []
    start_point = today - timedelta(days=2)
    for i in range(10):
        target_date = start_point + timedelta(days=i)
        target_workers = get_shift_workers(target_date)
        if target_workers:
            row = {"날짜": target_date.strftime('%m/%d') + f"({['월','화','수','목','금','토','일'][target_date.weekday()]})"}
            for pos, name in target_workers:
                row[pos] = check_vacation(target_date, name)
            cal_list.append(row)
    
    df_week = pd.DataFrame(cal_list)
    def style_cells(val):
        if val == "연차": return 'background-color: #FFEBEE; color: #D32F2F;'
        if val == user_name and user_name != "안 함": return f'background-color: {WORKER_COLORS.get(val)}; font-weight: bold; border: 1.5px solid #1E3A8A;'
        return ''
    st.dataframe(df_week.style.applymap(style_cells), use_container_width=True, hide_index=True)

elif menu == "📅 근무 편성표":
    # (기존 상세 조회 로직 유지)
    st.markdown("### 📅 전체 근무 편성표 조회")
    start_date = st.date_input("조회 시작일", today)
    duration = st.slider("조회 기간(일)", 7, 90, 30)
    # ... (생략된 기존 루프 로직)

elif menu == "✍️ 연차 신청/관리":
    # (기존 연차 관리 로직 유지)
    st.markdown("### 📂 연차 관리 시스템")
