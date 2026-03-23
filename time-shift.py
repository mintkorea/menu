import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from streamlit_javascript import st_javascript

# --- 1. 기기-성함 매칭 데이터 (문자열 매칭 강화) ---
DEVICE_MAP = {
    "S918": "황재업",  # S23/24 Ultra 계열
    "A546": "김태언",  # A54 5G
    "N971": "이정석",  # Note 20 Ultra
    "G988": "이태원",  # S20 Ultra
}

# --- 2. 기본 설정 및 데이터 로드 ---
PATTERN_START_DATE = datetime(2026, 3, 9).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7", "연차": "#FFEBEE"}
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 관리", layout="centered")

# --- 3. 기기 감지 함수 (직접 호출 방식으로 변경) ---
def get_device_user():
    # 자바스크립트로 User-Agent 문자열 가져오기
    ua = st_javascript("navigator.userAgent")
    if ua and ua != 0:
        for model, name in DEVICE_MAP.items():
            if model in str(ua):
                return name
    return "안 함"

# --- 4. 데이터 로드 ---
@st.cache_data
def load_vacation():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

df_vac = load_vacation()

# --- 5. 사이드바 구성 (슬라이더 복구) ---
with st.sidebar:
    st.header("⚙️ 스마트 설정")
    menu = st.radio("메뉴", ["📅 근무 편성표", "📍 실시간 상황판", "✍️ 연차 관리"])
    
    st.divider()
    
    # [중요] 기기 감지 시도
    detected = get_device_user()
    
    user_list = ["안 함", "황재업", "김태언", "이태원", "이정석"]
    # 감지된 사용자가 있으면 그 순서로, 없으면 '안 함'으로 초기값 설정
    default_idx = user_list.index(detected) if detected in user_list else 0
    
    user_name = st.selectbox("👤 내 이름 강조", user_list, index=default_idx)
    
    if detected != "안 함":
        st.success(f"📱 기기 인식: **{detected}**님")
    
    # [슬라이더 복구] 모든 메뉴에서 보이게 하거나 '근무 편성표' 선택 시 보이게 설정
    if menu == "📅 근무 편성표":
        st.subheader("📅 조회 범위")
        start_date = st.date_input("조회 시작일", datetime.now().date() - timedelta(days=3))
        duration = st.slider("조회 기간(일)", min_value=7, max_value=60, value=30)

# --- 6. 근무 편성 로직 ---
def check_vacation(date, name):
    is_vac = df_vac[(df_vac['날짜'] == date) & (df_vac['이름'] == name)]
    return "연차" if not is_vac.empty else name

if menu == "📅 근무 편성표":
    st.markdown(f"### 📅 {user_name if user_name != '안 함' else 'C조'} 근무 편성표")
    
    cal_list = []
    curr = start_date
    end_date = start_date + timedelta(days=duration)
    
    while curr <= end_date:
        diff_days = (curr - PATTERN_START_DATE).days
        if diff_days % 3 == 0:
            shift_count = diff_days // 3
            cycle_idx = (shift_count // 2) % 3 
            is_second_day = shift_count % 2 == 1
            
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

    if cal_list:
        df_display = pd.DataFrame(cal_list)
        
        def style_cells(val):
            if val == "연차": return 'background-color: #FFEBEE; color: #D32F2F;'
            if val == user_name and user_name != "안 함": 
                return f'background-color: {WORKER_COLORS.get(val)}; font-weight: bold; border: 2px solid #1E3A8A;'
            return ''

        st.dataframe(df_display.style.applymap(style_cells), use_container_width=True, hide_index=True)
    else:
        st.info("조회 기간 내 근무일이 없습니다.")

# (나머지 실시간 상황판 및 연차 관리 메뉴 로직 유지)
