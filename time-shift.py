import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. 기본 설정 및 기기 인식 ---
DEVICE_MAP = {"S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원"}
PATTERN_START_DATE = datetime(2026, 3, 9).date()
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 통합 관리", layout="wide")

# 시간 설정 (KST)
now_kst = datetime.now(timezone(timedelta(hours=9)))
today_val = now_kst.date()
now_total_min = now_kst.hour * 60 + now_kst.minute
if now_total_min < 7 * 60: now_total_min += 24 * 60

# --- 2. 데이터 로드 및 저장 (연차 관리용) ---
def load_vacation():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

def save_vacation(df):
    df.to_csv(VACATION_FILE, index=False)

df_vac = load_vacation()

# --- 3. 사이드바 메뉴 ---
with st.sidebar:
    st.header("📋 메뉴 선택")
    menu = st.radio("이동할 페이지", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 신청/관리"])
    
    # 기기 자동 인식
    ua = st_javascript("navigator.userAgent")
    detected = "안 함"
    if ua and ua != 0:
        for model, name in DEVICE_MAP.items():
            if model in str(ua).upper(): detected = name; break
    user_name = st.selectbox("사용자 확인", ["안 함", "황재업", "이정석", "김태언", "이태원"], 
                             index=["안 함", "황재업", "이정석", "김태언", "이태원"].index(detected))

# --- 4. [페이지 1] 실시간 상황판 (이미지 로직 + 강조) ---
if menu == "📍 실시간 상황판":
    st.title("🏛️ C조 실시간 당직 안내")
    
    diff_days = (today_val - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        # 어제 맞춘 20개 시간대 데이터
        sched = [
            {"From": "07:00", "To": "08:00", "성희_조장": "안내실", "성희_대원": "로비", "의산_A": "로비", "의산_B": "휴게"},
            {"From": "08:00", "To": "09:00", "성희_조장": "안내실", "성희_대원": "휴게", "의산_A": "휴게", "의산_B": "로비"},
            # ... (중략 - 어제 입력한 모든 데이터 동일) ...
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
        st.warning("오늘은 C조 비번입니다.")

# --- 5. [페이지 2] 근무 편성표 (3일 로테이션 자동 계산) ---
elif menu == "📅 근무 편성표":
    st.title("📅 C조 월간 근무 편성표")
    year, month = today_val.year, today_val.month
    
    # 이번 달 날짜 리스트 생성
    first_day = today_val.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    days_list = []
    curr = first_day
    while curr <= last_day:
        d_diff = (curr - PATTERN_START_DATE).days
        is_working = "근무" if d_diff % 3 == 0 else "비번"
        
        # 로테이션 계산
        shift_count = d_diff // 3
        cycle_idx = (shift_count // 2) % 3 
        is_second = shift_count % 2 == 1
        
        if is_working == "근무":
            if cycle_idx == 0: h, a, b = "김태언", ("이정석" if is_second else "이태원"), ("이태원" if is_second else "이정석")
            elif cycle_idx == 1: h, a, b = "이정석", ("이태원" if is_second else "김태언"), ("김태언" if is_second_day else "이태원")
            else: h, a, b = "이태원", ("이정석" if is_second else "김태언"), ("김태언" if is_second else "이정석")
            
            # 연차 체크
            v_names = df_vac[df_vac['날짜'] == curr]['이름'].tolist()
            h = "🌴연차" if h in v_names else h
            a = "🌴연차" if a in v_names else a
            b = "🌴연차" if b in v_names else b
            
            days_list.append({"날짜": curr.strftime("%m/%d"), "요일": curr.strftime("%A"), "성희_대원": h, "의산_A": a, "의산_B": b})
        curr += timedelta(days=1)

    st.table(pd.DataFrame(days_list))

# --- 6. [페이지 3] 연차 신청/관리 ---
elif menu == "✍️ 연차 신청/관리":
    st.title("✍️ 연차 신청 및 내역")
    
    with st.form("연차신청"):
        v_date = st.date_input("연차 날짜 선택", value=today_val)
        v_name = st.selectbox("신청자", ["황재업", "이정석", "김태언", "이태원"])
        v_reason = st.text_input("사유", "개인사정")
        if st.form_submit_button("신청하기"):
            new_v = pd.DataFrame([{"날짜": v_date, "이름": v_name, "사유": v_reason}])
            df_vac = pd.concat([df_vac, new_v], ignore_index=True)
            save_vacation(df_vac)
            st.success(f"{v_name}님 {v_date} 연차 신청 완료!")
            st.rerun()

    st.markdown("---")
    st.subheader("🗓️ 등록된 연차 명단")
    st.dataframe(df_vac.sort_values("날짜"), use_container_width=True)
    if st.button("연차 내역 초기화(주의)"):
        if os.path.exists(VACATION_FILE): os.remove(VACATION_FILE)
        st.rerun()
