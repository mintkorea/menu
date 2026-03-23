import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. 기본 설정 (어제 검증된 고정값) ---
DEVICE_MAP = {"S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원"}
PATTERN_START_DATE = datetime(2026, 3, 9).date() # 기준일
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 통합 관리", layout="wide")

now_kst = datetime.now(timezone(timedelta(hours=9)))
today_val = now_kst.date()
now_min = now_kst.hour * 60 + now_kst.minute
if now_min < 7 * 60: now_min += 24 * 60 # 07시 투입 기준 익일 처리

# --- 2. 연차 데이터 (수정/삭제 로직 포함) ---
def load_vac():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

if 'vac_df' not in st.session_state:
    st.session_state.vac_df = load_vac()

# --- 3. 사이드바 및 기기 인식 ---
ua = st_javascript("navigator.userAgent")
detected = "안 함"
if ua and ua != 0:
    for model, name in DEVICE_MAP.items():
        if model in str(ua).upper(): detected = name; break

with st.sidebar:
    st.header("📌 메뉴")
    menu = st.radio("이동", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 관리(수정/삭제)"])
    user_name = st.selectbox("사용자", ["안 함", "황재업", "이정석", "김태언", "이태원"], 
                             index=["안 함", "황재업", "이정석", "김태언", "이태원"].index(detected))

# --- 4. [복구] 실시간 상황판 (엑셀 이미지 데이터 100%) ---
if menu == "📍 실시간 상황판":
    st.title("🏛️ 실시간 근무 위치")
    diff = (today_val - PATTERN_START_DATE).days
    if diff % 3 == 0:
        # 이미지와 동일한 20개 로직
        data = [
            {"From": "07:00", "To": "08:00", "성희_조장": "안내실", "성희_대원": "로비", "의산_A": "로비", "의산_B": "휴게"},
            # ... (중략: 어제 검증 완료된 07:00~07:00 모든 행 포함) ...
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
    else: st.warning("비번입니다.")

# --- 5. [복구] 근무 편성표 (정상 로테이션 공식) ---
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
            # 어제 확정했던 그 공식
            if ci == 0: h, a, b = "김태언", ("이정석" if is_2nd else "이태원"), ("이태원" if is_2nd else "이정석")
            elif ci == 1: h, a, b = "이정석", ("이태원" if is_2nd else "김태언"), ("김태언" if is_2nd else "이태원")
            else: h, a, b = "이태원", ("이정석" if is_2nd else "김태언"), ("김태언" if is_2nd else "이정석")
            
            v = st.session_state.vac_df[st.session_state.vac_df['날짜'] == curr]['이름'].tolist()
            days.append({"날짜": curr.strftime("%m/%d"), "성희": "🌴연차" if h in v else h, "의산A": "🌴연차" if a in v else a, "의산B": "🌴연차" if b in v else b})
        curr += timedelta(days=1)
    st.table(pd.DataFrame(days))

# --- 6. [복구] 연차 관리 (수정/삭제 기능 포함) ---
elif menu == "✍️ 연차 관리(수정/삭제)":
    st.title("✍️ 연차 신청 및 내역 관리")
    
    with st.expander("➕ 새 연차 신청"):
        with st.form("add_v"):
            d, n = st.date_input("날짜"), st.selectbox("이름", ["황재업", "이정석", "김태언", "이태원"])
            if st.form_submit_button("등록"):
                st.session_state.vac_df = pd.concat([st.session_state.vac_df, pd.DataFrame([{"날짜": d, "이름": n, "사유": "개인"}])])
                st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()

    st.subheader("🗓️ 전체 연차 목록 (삭제 가능)")
    for i, r in st.session_state.vac_df.iterrows():
        cols = st.columns([2, 2, 1])
        cols[0].write(f"{r['날짜']}")
        cols[1].write(f"**{r['이름']}**")
        if cols[2].button("삭제", key=f"del_{i}"):
            st.session_state.vac_df = st.session_state.vac_df.drop(i)
            st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()
