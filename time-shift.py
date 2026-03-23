import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from streamlit_javascript import st_javascript  # pip install streamlit-javascript 필요

# --- 1. 기기-성함 매칭 데이터 ---
# 모델 번호의 일부를 키워드로 매칭합니다.
DEVICE_MAP = {
    "S918": "황재업",  # S23 Ultra (S918) - 정보주신 S21 Ultra는 보통 G998이나, 적어주신 S918 기준으로 세팅
    "A546": "김태언",  # A54 5G
    "N971": "이정석",  # Note 20 Ultra (실제 모델명 N986 가능성 있으나 적어주신 N971 기준)
    "G988": "이태원",  # S20 Ultra
}

# --- 2. 기본 설정 및 데이터 로드 ---
PATTERN_START_DATE = datetime(2026, 3, 9).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7", "연차": "#FFEBEE"}
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 관리", layout="centered")

# --- 3. 기기 감지 로직 ---
def get_user_by_device():
    # 브라우저의 User-Agent 정보를 가져옴
    ua = st_javascript("navigator.userAgent")
    if not ua or ua == 0:
        return "안 함"
    
    for model, name in DEVICE_MAP.items():
        if model in ua:
            return name
    return "안 함"

# --- 4. 데이터 로드 및 초기화 ---
if os.path.exists(VACATION_FILE):
    df_vac = pd.read_csv(VACATION_FILE)
    df_vac['날짜'] = pd.to_datetime(df_vac['날짜']).dt.date
else:
    df_vac = pd.DataFrame(columns=['날짜', '이름', '사유'])

# 기기 감지를 통한 초기 이름 설정
if "detected_user" not in st.session_state:
    st.session_state.detected_user = get_user_by_device()

# --- 5. 사이드바 ---
with st.sidebar:
    st.header("⚙️ 스마트 설정")
    menu = st.radio("메뉴", ["📅 근무 편성표", "📍 실시간 상황판", "✍️ 연차 관리"])
    
    st.divider()
    # 기기 감지 결과가 있으면 기본값으로 설정, 없으면 수동 선택
    user_list = ["안 함", "황재업", "김태언", "이태원", "이정석"]
    default_idx = user_list.index(st.session_state.detected_user) if st.session_state.detected_user in user_list else 0
    
    user_name = st.selectbox("👤 내 이름 강조", user_list, index=default_idx)
    
    if st.session_state.detected_user != "안 함":
        st.success(f"📱 기기 인식: **{st.session_state.detected_user}**님")
    else:
        st.caption("기기가 자동 인식되지 않았습니다.")

# --- 6. 근무 편성 로직 (기존 연차 연동 포함) ---
def check_vacation(date, name):
    is_vac = df_vac[(df_vac['날짜'] == date) & (df_vac['이름'] == name)]
    return "연차" if not is_vac.empty else name

if menu == "📅 근무 편성표":
    st.markdown("### 📅 C조 근무 편성표")
    start_date = st.date_input("조회 시작일", datetime.now().date() - timedelta(days=3))
    
    cal_list = []
    curr = start_date
    for _ in range(30): # 30일치 계산
        diff_days = (curr - PATTERN_START_DATE).days
        if diff_days % 3 == 0:
            shift_count = diff_days // 3
            cycle_idx = (shift_count // 2) % 3 
            is_second_day = shift_count % 2 == 1
            
            # 패턴 배정
            if cycle_idx == 0: h_p, a_p, b_p = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
            elif cycle_idx == 1: h_p, a_p, b_p = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
            else: h_p, a_p, b_p = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
            
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][curr.weekday()]})",
                "조장": check_vacation(curr, "황재업"),
                "회관": check_vacation(curr, h_p),
                "의산(A)": check_vacation(curr, a_p),
                "의산(B)": check_vacation(curr, b_p)
            })
        curr += timedelta(days=1)

    df_display = pd.DataFrame(cal_list)
    
    def style_cells(val):
        if val == "연차": return 'background-color: #FFEBEE; color: #D32F2F;'
        if val == user_name and user_name != "안 함": 
            return f'background-color: {WORKER_COLORS.get(val)}; font-weight: bold; border: 2px solid #1E3A8A;'
        return ''

    st.dataframe(df_display.style.applymap(style_cells), use_container_width=True, hide_index=True)

# ... (실시간 상황판 및 연차 관리 로직은 이전과 동일하게 유지)
