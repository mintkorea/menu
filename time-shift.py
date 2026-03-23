import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. 기기-성함 매칭 데이터 ---
DEVICE_MAP = {
    "S918": "황재업",
    "N971": "이정석",
    "N970": "김태언",
    "V510": "김태언",
    "G988": "이태원",
}

# --- 2. 기본 설정 및 데이터 로드 ---
PATTERN_START_DATE = datetime(2026, 3, 9).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7", "연차": "#FFEBEE"}
VACATION_FILE = 'vacation.csv'
ADMIN_PASSWORD = "1234" 

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

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
            if model in ua_str:
                return name
    return "안 함"

df_vac = load_vacation_data()
now_kst = datetime.now(timezone(timedelta(hours=9)))
today_val = now_kst.date()

# --- 3. CSS 스타일 ---
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 10px; }
    .location-box { background-color: #f0f2f6; padding: 15px; border-radius: 10px; border-left: 5px solid #1E3A8A; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 사이드바 ---
with st.sidebar:
    st.header("⚙️ 스마트 설정")
    menu = st.radio("메뉴 이동", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 신청/관리"])
    st.divider()
    
    detected = get_device_user()
    user_list = ["안 함", "황재업", "김태언", "이태원", "이정석"]
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = detected if detected in user_list else "안 함"
    user_name = st.selectbox("👤 내 이름 강조", user_list, index=user_list.index(st.session_state.selected_user))

# --- 5. 메뉴별 로직 ---
def check_vacation(date, name):
    is_vac = df_vac[(df_vac['날짜'] == date) & (df_vac['이름'] == name)]
    return "연차" if not is_vac.empty else name

if menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>📍 실시간 근무 및 현장 안내</div>", unsafe_allow_html=True)
    st.caption(f"🕒 현재 시각(KST): {now_kst.strftime('%Y-%m-%d %H:%M')}")
    
    # [핵심 기능] 접속자 현재 근무 위치 자동 판별
    diff_days = (today_val - PATTERN_START_DATE).days
    my_location = None

    if diff_days % 3 == 0:
        shift_count = diff_days // 3
        cycle_idx = (shift_count // 2) % 3 
        is_second_day = shift_count % 2 == 1
        
        # 보직 매칭
        if cycle_idx == 0: h_p, a_p, b_p = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
        elif cycle_idx == 1: h_p, a_p, b_p = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
        else: h_p, a_p, b_p = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
        
        current_assignments = {"조장": "황재업", "성희관": h_p, "의산연(A)": a_p, "의산연(B)": b_p}
        
        # 강조된 이름이 현재 어디 있는지 찾기
        if user_name != "안 함":
            for loc, name in current_assignments.items():
                if name == user_name:
                    my_location = loc
                    break
        
        # 상단 안내 박스
        if my_location:
            st.markdown(f"""
            <div class='location-box'>
                <h4 style='margin:0;'>👋 <b>{user_name}</b>님, 반갑습니다!</h4>
                <p style='margin:5px 0 0 0;'>오늘 나의 근무지는 <b>[ {my_location} ]</b> 입니다.</p>
            </div>
            """, unsafe_allow_html=True)
        
        # 전체 상황판 표시
        cols = st.columns(4)
        for i, (pos, name) in enumerate(current_assignments.items()):
            status = check_vacation(today_val, name)
            with cols[i]:
                st.metric(pos, status)
                if status == "연차": st.error("부재중")
                else: st.success("근무중")
    else:
        st.info("오늘은 C조 정규 근무일이 아닙니다.")

# (이하 근무 편성표 및 연차 관리 로직은 이전과 동일...)
