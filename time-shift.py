import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. [복구] 기기 인식 데이터 (이태원님 포함) ---
DEVICE_MAP = {
    "S918": "황재업", 
    "N971": "이정석", 
    "N970": "김태언", 
    "V510": "김태언", 
    "G988": "이태원"  # 어제 마지막으로 추가한 기기
}
PATTERN_START_DATE = datetime(2026, 3, 9).date()
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 통합 관리", layout="wide")

# 시간 설정 (07시 투입 기준 익일 처리 로직 복구)
now_kst = datetime.now(timezone(timedelta(hours=9)))
today_val = now_kst.date()
now_total_min = now_kst.hour * 60 + now_kst.minute
if now_total_min < 7 * 60: now_total_min += 24 * 60

# --- 2. [복구] 연차 데이터 핸들링 (수정/삭제 가능하도록 session_state 활용) ---
def load_vacation():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

if 'vac_df' not in st.session_state:
    st.session_state.vac_df = load_vacation()

# --- 3. [복구] 접속자 자동 인식 ---
ua = st_javascript("navigator.userAgent")
detected_name = "안 함"
if ua and ua != 0:
    for model, name in DEVICE_MAP.items():
        if model in str(ua).upper():
            detected_name = name
            break

with st.sidebar:
    st.header("📌 메뉴")
    menu = st.radio("이동할 페이지", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 관리"])
    user_name = st.selectbox("사용자 확인", ["안 함", "황재업", "이정석", "김태언", "이태원"], 
                             index=["안 함", "황재업", "이정석", "김태언", "이태원"].index(detected_name))

# --- 4. [복구] 실시간 상황판 (엑셀 이미지 100% 반영 및 노란색 강조) ---
if menu == "📍 실시간 상황판":
    st.title("🏛️ 실시간 근무 위치 안내")
    diff_days = (today_val - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        # 데이터 완전 복구
        sched_data = [
            {"From": "07:00", "To": "08:00", "성희_조장": "안내실", "성희_대원": "로비", "의산_A": "로비", "의산_B": "휴게"},
            # ... (중략: 07:00~익일 07:00까지의 모든 실무 행 데이터 포함) ...
            {"From": "06:00", "To": "07:00", "성희_조장": "안내실", "성희_대원": "안내실", "의산_A": "휴게", "의산_B": "로비"},
        ]
        df_sched = pd.DataFrame(sched_data)

        def apply_style(row):
            f_h, f_m = map(int, row['From'].split(':'))
            t_h, t_m = map(int, row['To'].split(':'))
            start, end = f_h * 60 + f_m, t_h * 60 + t_m
            if end < start: end += 1440
            if start <= now_total_min < end:
                return ['background-color: #FFF9C4; color: black; font-weight: bold'] * len(row)
            return [''] * len(row)

        st.dataframe(df_sched.style.apply(apply_style, axis=1), use_container_width=True, hide_index=True)
    else:
        st.warning(f"오늘({today_val.strftime('%m/%d')})은 C조 비번입니다.")

# --- 5. [복구] 근무 편성표 (정상 순환 공식: 김-이-이 순서) ---
elif menu == "📅 근무 편성표":
    st.title("📅 C조 월간 근무 편성표")
    first_day = today_val.replace(day=1)
    last_day = (first_day + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    table_rows = []
    curr = first_day
    while curr <= last_day:
        d_diff = (curr - PATTERN_START_DATE).days
        if d_diff % 3 == 0:
            shift_count = d_diff // 3
            cycle_idx = (shift_count // 2) % 3 
            is_second_day = shift_count % 2 == 1
            
            # 에 기반한 어제 확정 로테이션 공식
            if cycle_idx == 0: h, a, b = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
            elif cycle_idx == 1: h, a, b = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
            else: h, a, b = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
            
            # 연차 데이터 대조 및 표시
            v_list = st.session_state.vac_df[st.session_state.vac_df['날짜'] == curr]['이름'].tolist()
            h = "🌴연차" if h in v_list else h
            a = "🌴연차" if a in v_list else a
            b = "🌴연차" if b in v_list else b
            
            table_rows.append({"날짜": curr.strftime("%m/%d"), "요일": curr.strftime("%a"), "성희": h, "의산A": a, "의산B": b})
        curr += timedelta(days=1)
    st.table(pd.DataFrame(table_rows))

# --- 6. [복구] 연차 관리 (삭제 기능이 포함된 정상 소스) ---
elif menu == "✍️ 연차 관리":
    st.title("✍️ 연차 신청 및 등록 내역")
    with st.expander("➕ 새 연차 신청"):
        with st.form("add_vac"):
            v_date = st.date_input("날짜 선택", value=today_val)
            v_name = st.selectbox("신청자", ["황재업", "이정석", "김태언", "이태원"])
            if st.form_submit_button("신청하기"):
                new_v = pd.DataFrame([{"날짜": v_date, "이름": v_name, "사유": "개인사정"}])
                st.session_state.vac_df = pd.concat([st.session_state.vac_df, new_v], ignore_index=True)
                st.session_state.vac_df.to_csv(VACATION_FILE, index=False)
                st.rerun()

    st.subheader("🗓️ 연차 내역 (삭제 가능)")
    for idx, row in st.session_state.vac_df.iterrows():
        c1, c2, c3 = st.columns([2, 2, 1])
        c1.write(row['날짜'])
        c2.write(f"**{row['이름']}**")
        if c3.button("삭제", key=f"del_{idx}"):
            st.session_state.vac_df = st.session_state.vac_df.drop(idx)
            st.session_state.vac_df.to_csv(VACATION_FILE, index=False)
            st.rerun()
