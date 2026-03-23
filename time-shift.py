import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 기본 설정 및 데이터 로드 ---
PATTERN_START_DATE = datetime(2026, 3, 9).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7", "연차": "#FFEBEE"}
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

# 연차 데이터 로드 함수
def load_vacation_data():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

# --- 2. CSS 스타일 ---
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 10px; }
    .stDataFrame { justify-content: center; display: flex; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 (설정) ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴 이동", ["📅 근무 편성표", "📍 실시간 상황판", "✍️ 연차 신청/현황"])
    st.divider()
    user_name = st.selectbox("👤 내 이름 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])
    
    if menu == "📅 근무 편성표":
        st.subheader("조회 설정")
        start_date = st.date_input("조회 시작일", datetime.now().date() - timedelta(days=3))
        duration = st.slider("조회 기간(일)", 7, 60, 30)

# --- 4. 메뉴별 로직 ---

# 데이터 미리 불러오기
df_vac = load_vacation_data()

# [함수] 특정 날짜/인원의 연차 여부 확인
def check_vacation(date, name):
    is_vac = df_vac[(df_vac['날짜'] == date) & (df_vac['이름'] == name)]
    return "연차" if not is_vac.empty else name

if menu == "📅 근무 편성표":
    st.markdown("<div class='main-title'>📅 성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    
    cal_list = []
    end_date = start_date + timedelta(days=duration)
    
    curr = start_date
    while curr <= end_date:
        diff_days = (curr - PATTERN_START_DATE).days
        if diff_days % 3 == 0:
            shift_count = diff_days // 3
            cycle_idx = (shift_count // 2) % 3 
            is_second_day = shift_count % 2 == 1
            
            # 패턴 기본 배정
            if cycle_idx == 0: h_p, a_p, b_p = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
            elif cycle_idx == 1: h_p, a_p, b_p = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
            else: h_p, a_p, b_p = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
            
            # 연차 데이터와 대조하여 이름 변환
            h = check_vacation(curr, h_p)
            a = check_vacation(curr, a_p)
            b = check_vacation(curr, b_p)
            jo = check_vacation(curr, "황재업")
            
            wd = curr.weekday()
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "조장": jo, "회관": h, "의산(A)": a, "의산(B)": b
            })
        curr += timedelta(days=1)

    df_display = pd.DataFrame(cal_list)
    
    def style_cells(val):
        if val == "연차": return 'background-color: #FFEBEE; color: #D32F2F; font-weight: bold;'
        if user_name != "안 함" and val == user_name: return f'background-color: {WORKER_COLORS.get(val)}; font-weight: bold;'
        if "(토)" in str(val): return 'color: #1E88E5;'
        if "(일)" in str(val): return 'color: #E53935;'
        return ''

    st.dataframe(df_display.style.applymap(style_cells), use_container_width=True, hide_index=True, height=500)

elif menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>📍 실시간 근무 상황</div>", unsafe_allow_html=True)
    today = datetime.now().date()
    
    # 오늘이 근무일인지 확인
    diff_days = (today - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        # 오늘 근무자 계산 (위 로직과 동일)
        shift_count = diff_days // 3
        cycle_idx = (shift_count // 2) % 3 
        is_second_day = shift_count % 2 == 1
        if cycle_idx == 0: h_p, a_p, b_p = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
        elif cycle_idx == 1: h_p, a_p, b_p = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
        else: h_p, a_p, b_p = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
        
        cols = st.columns(4)
        positions = [("조장", "황재업"), ("회관", h_p), ("의산(A)", a_p), ("의산(B)", b_p)]
        
        for i, (pos, name) in enumerate(positions):
            status = check_vacation(today, name)
            with cols[i]:
                st.metric(pos, status)
                if status == "연차":
                    st.error("❌ 부재중")
                else:
                    st.success("✅ 근무중")
    else:
        st.info("오늘은 정규 근무일이 아닙니다.")

elif menu == "✍️ 연차 신청/현황":
    st.markdown("<div class='main-title'>📂 연차 관리</div>", unsafe_allow_html=True)
    t1, t2 = st.tabs(["🗓️ 연차 현황판", "✍️ 연차 신청"])
    
    with t1:
        st.dataframe(df_vac.sort_values('날짜', ascending=False), use_container_width=True, hide_index=True)
        
    with t2:
        with st.form("vac_form", clear_on_submit=True):
            v_date = st.date_input("연차 날짜")
            v_name = st.selectbox("이름", ["황재업", "김태언", "이태원", "이정석"])
            v_reason = st.text_input("사유")
            if st.form_submit_button("신청하기"):
                new_row = pd.DataFrame({'날짜': [v_date], '이름': [v_name], '사유': [v_reason]})
                df_updated = pd.concat([df_vac, new_row], ignore_index=True)
                df_updated.to_csv(VACATION_FILE, index=False, encoding='utf-8-sig')
                st.success("연차가 등록되었습니다.")
                st.rerun()
