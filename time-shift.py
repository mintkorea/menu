import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. 설정 및 기기 인식 (기존 동일) ---
DEVICE_MAP = {"S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원"}
PATTERN_START_DATE = datetime(2026, 3, 9).date()
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="wide")

now_kst = datetime.now(timezone(timedelta(hours=9)))
today_val = now_kst.date()
now_total_min = now_kst.hour * 60 + now_kst.minute
if now_total_min < 7 * 60: now_total_min += 24 * 60

# --- 2. 연차 데이터 로드 ---
def load_vacation():
    if os.path.exists(VACATION_FILE):
        try:
            df = pd.read_csv(VACATION_FILE)
            df['날짜'] = pd.to_datetime(df['날짜']).dt.date
            return df
        except: return pd.DataFrame(columns=['날짜', '이름', '사유'])
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

df_vac = load_vacation()

# --- 3. 사이드바 및 사용자 인식 ---
ua = st_javascript("navigator.userAgent")
detected = "안 함"
if ua and ua != 0:
    for model, name in DEVICE_MAP.items():
        if model in str(ua).upper(): detected = name; break

with st.sidebar:
    menu = st.radio("메뉴", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 신청/관리"])
    user_name = st.selectbox("사용자", ["안 함", "황재업", "이정석", "김태언", "이태원"], 
                             index=["안 함", "황재업", "이정석", "김태언", "이태원"].index(detected))

# --- 4. 실시간 상황판 (엑셀 이미지 로직) ---
if menu == "📍 실시간 상황판":
    st.title("🏛️ C조 실시간 당직 안내")
    diff_days = (today_val - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        sched = [
            {"From": "07:00", "To": "08:00", "성희_조장": "안내실", "성희_대원": "로비", "의산_A": "로비", "의산_B": "휴게"},
            {"From": "08:00", "To": "09:00", "성희_조장": "안내실", "성희_대원": "휴게", "의산_A": "휴게", "의산_B": "로비"},
            {"From": "09:00", "To": "10:00", "성희_조장": "안내실", "성희_대원": "순찰", "의산_A": "휴게", "의산_B": "로비"},
            {"From": "10:00", "To": "11:00", "성희_조장": "휴게", "성희_대원": "안내실", "의산_A": "로비", "의산_B": "순찰/휴게"},
            {"From": "11:00", "To": "12:00", "성희_조장": "안내실", "성희_대원": "중식", "의산_A": "로비", "의산_B": "중식"},
            {"From": "12:00", "To": "13:00", "성희_조장": "중식", "성희_대원": "안내실", "의산_A": "중식", "의산_B": "로비"},
            {"From": "13:00", "To": "14:00", "성희_조장": "안내실", "성희_대원": "휴게", "의산_A": "순찰/휴게", "의산_B": "로비"},
            {"From": "14:00", "To": "15:00", "성희_조장": "순찰", "성희_대원": "안내실", "의산_A": "로비", "의산_B": "휴게"},
            {"From": "15:00", "To": "16:00", "성희_조장": "안내실", "성희_대원": "휴게", "의산_A": "로비", "의산_B": "휴게"},
            {"From": "16:00", "To": "17:00", "성희_조장": "휴게", "성희_대원": "안내실", "의산_A": "휴게", "의산_B": "로비"},
            {"From": "17:00", "To": "18:00", "성희_조장": "안내실", "성희_대원": "휴게", "의산_A": "휴게", "의산_B": "로비"},
            {"From": "18:00", "To": "19:00", "성희_조장": "안내실", "성희_대원": "석식", "의산_A": "로비", "의산_B": "석식"},
            {"From": "19:00", "To": "20:00", "성희_조장": "안내실", "성희_대원": "안내실", "의산_A": "석식", "의산_B": "로비"},
            {"From": "20:00", "To": "21:00", "성희_조장": "석식", "성희_대원": "안내실", "의산_A": "로비", "의산_B": "휴게"},
            {"From": "21:00", "To": "22:00", "성희_조장": "안내실", "성희_대원": "순찰", "의산_A": "로비", "의산_B": "휴게"},
            {"From": "22:00", "To": "23:00", "성희_조장": "순찰", "성희_대원": "휴게", "의산_A": "순찰", "의산_B": "로비"},
            {"From": "23:00", "To": "01:40", "성희_조장": "안내실", "성희_대원": "휴게", "의산_A": "휴게", "의산_B": "로비"},
            {"From": "01:40", "To": "05:00", "성희_조장": "휴게", "성희_대원": "안내실", "의산_A": "로비", "의산_B": "휴게"},
            {"From": "05:00", "To": "06:00", "성희_조장": "안내실", "성희_대원": "순찰", "의산_A": "로비", "의산_B": "순찰"},
            {"From": "06:00", "To": "07:00", "성희_조장": "안내실", "성희_대원": "안내실", "의산_A": "휴게", "의산_B": "로비"},
        ]
        df_sched = pd.DataFrame(sched)

        def style_now(row):
            f_h, f_m = map(int, row['From'].split(':'))
            t_h, t_m = map(int, row['To'].split(':'))
            start, end = f_h * 60 + f_m, t_h * 60 + t_m
            if end < start: end += 24 * 60
            if start <= now_total_min < end:
                return ['background-color: #FFF9C4; color: black; font-weight: bold'] * len(row)
            return [''] * len(row)

        st.dataframe(df_sched.style.apply(style_now, axis=1), use_container_width=True, hide_index=True)
    else:
        st.warning(f"오늘({today_val.strftime('%m/%d')})은 비번입니다.")

# --- 5. 근무 편성표 (에러 수정 지점!) ---
elif menu == "📅 근무 편성표":
    st.title("📅 C조 월간 근무 편성표")
    first_day = today_val.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    days_list = []
    curr = first_day
    while curr <= last_day:
        d_diff = (curr - PATTERN_START_DATE).days
        if d_diff % 3 == 0:
            shift_count = d_diff // 3
            cycle_idx = (shift_count // 2) % 3 
            is_second_day = shift_count % 2 == 1 # ◀ 여기서 변수명을 통일했습니다!
            
            # 어제 검증한 로직 그대로
            if cycle_idx == 0: h, a, b = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
            elif cycle_idx == 1: h, a, b = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
            else: h, a, b = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
            
            v_names = df_vac[df_vac['날짜'] == curr]['이름'].tolist()
            h = "🌴연차" if h in v_names else h
            a = "🌴연차" if a in v_names else a
            b = "🌴연차" if b in v_names else b
            
            days_list.append({"날짜": curr.strftime("%m/%d"), "요일": curr.strftime("%a"), "성희_대원": h, "의산_A": a, "의산_B": b})
        curr += timedelta(days=1)
    st.table(pd.DataFrame(days_list))

# --- 6. 연차 관리 ---
elif menu == "✍️ 연차 신청/관리":
    st.title("✍️ 연차 신청")
    with st.form("vac_form"):
        v_date = st.date_input("날짜", value=today_val)
        v_name = st.selectbox("이름", ["황재업", "이정석", "김태언", "이태원"])
        if st.form_submit_button("신청"):
            new_v = pd.DataFrame([{"날짜": v_date, "이름": v_name, "사유": "개인사정"}])
            df_vac = pd.concat([df_vac, new_v], ignore_index=True)
            df_vac.to_csv(VACATION_FILE, index=False)
            st.rerun()
    st.dataframe(df_vac)
