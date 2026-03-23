import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. 기본 설정 및 기기 인식 ---
DEVICE_MAP = {"S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원"}
PATTERN_START_DATE = datetime(2026, 3, 9).date() 
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="wide")

now_kst = datetime.now(timezone(timedelta(hours=9)))
today_val = now_kst.date()
now_min = now_kst.hour * 60 + now_kst.minute
if now_min < 7 * 60: now_min += 24 * 60 # 07시 투입 기준 익일 처리

# --- 2. 연차 데이터 로드 및 삭제 기능 ---
def load_vac():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

if 'vac_df' not in st.session_state:
    st.session_state.vac_df = load_vac()

# --- 3. 사이드바 및 사용자 자동 인식 ---
ua = st_javascript("navigator.userAgent")
detected = "안 함"
if ua and ua != 0:
    for model, name in DEVICE_MAP.items():
        if model in str(ua).upper(): detected = name; break

with st.sidebar:
    st.header("📌 메뉴")
    menu = st.radio("이동", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 관리"])
    user_name = st.selectbox("사용자", ["안 함", "황재업", "이정석", "김태언", "이태원"], 
                             index=["안 함", "황재업", "이정석", "김태언", "이태원"].index(detected))

# --- 4. [복구] 실시간 상황판 (엑셀 이미지 100% 반영) ---
if menu == "📍 실시간 상황판":
    st.title("🏛️ 실시간 근무 위치")
    diff = (today_val - PATTERN_START_DATE).days
    if diff % 3 == 0:
        # 엑셀 이미지 데이터
        data = [
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
        df_sched = pd.DataFrame(data)
        
        def highlight(row):
            f_h, f_m = map(int, row['From'].split(':'))
            t_h, t_m = map(int, row['To'].split(':'))
            s, e = f_h*60+f_m, t_h*60+t_m
            if e < s: e += 1440
            return ['background-color: #FFF9C4; color: black; font-weight: bold'] * len(row) if s <= now_min < e else [''] * len(row)

        st.dataframe(df_sched.style.apply(highlight, axis=1), use_container_width=True, hide_index=True)
    else: st.warning("오늘은 비번입니다.")

# --- 5. [복구] 근무 편성표 (사용자 캡처 로직 100% 반영) ---
elif menu == "📅 근무 편성표":
    st.title("📅 C조 월간 편성표")
    days = []
    curr = today_val.replace(day=1)
    last = (curr + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    while curr <= last:
        d_diff = (curr - PATTERN_START_DATE).days
        if d_diff % 3 == 0:
            sc = d_diff // 3
            ci = (sc // 2) % 3
            is_2nd = sc % 2 == 1
            # 캡처 로직 복구 (이태원-김태언-이정석 순환)
            if ci == 0: h, a, b = ("김태언" if not is_2nd else "김태언"), ("이태원" if not is_2nd else "이정석"), ("이정석" if not is_2nd else "이태원")
            elif ci == 1: h, a, b = ("이정석" if not is_2nd else "이정석"), ("김태언" if not is_2nd else "이태원"), ("이태원" if not is_2nd else "김태언")
            else: h, a, b = ("이태원" if not is_2nd else "이태원"), ("이정석" if not is_2nd else "김태언"), ("김태언" if not is_2nd else "이정석")
            
            v = st.session_state.vac_df[st.session_state.vac_df['날짜'] == curr]['이름'].tolist()
            days.append({"날짜": curr.strftime("%m/%d"), "성희": "🌴연차" if h in v else h, "의산A": "🌴연차" if a in v else a, "의산B": "🌴연차" if b in v else b})
        curr += timedelta(days=1)
    st.table(pd.DataFrame(days))

# --- 6. [복구] 연차 관리 (삭제 기능) ---
elif menu == "✍️ 연차 관리":
    st.title("✍️ 연차 신청 및 내역")
    with st.form("add_v"):
        d, n = st.date_input("날짜", value=today_val), st.selectbox("신청자", ["황재업", "이정석", "김태언", "이태원"])
        if st.form_submit_button("등록"):
            st.session_state.vac_df = pd.concat([st.session_state.vac_df, pd.DataFrame([{"날짜": d, "이름": n, "사유": "개인"}])])
            st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()

    st.subheader("🗓️ 목록 (삭제)")
    for idx, row in st.session_state.vac_df.iterrows():
        c1, c2, c3 = st.columns([2, 2, 1])
        c1.write(row['날짜'])
        c2.write(f"**{row['이름']}**")
        if c3.button("삭제", key=f"del_{idx}"):
            st.session_state.vac_df = st.session_state.vac_df.drop(idx)
            st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()
