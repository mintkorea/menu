import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. [복구] 사용자 지정 기기 및 패턴 설정 ---
DEVICE_MAP = {"S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원"}
PATTERN_START_DATE = datetime(2026, 3, 9).date()
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 통합 관리", layout="wide")

# 시간 설정 (07시 투입 기준 익일 처리)
now_kst = datetime.now(timezone(timedelta(hours=9)))
today_val = now_kst.date()
now_total_min = now_kst.hour * 60 + now_kst.minute
if now_total_min < 7 * 60: now_total_min += 24 * 60

# --- 2. [복구] 연차 데이터 로드 및 삭제 로직 ---
def load_vacation():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

if 'vac_df' not in st.session_state:
    st.session_state.vac_df = load_vacation()

# --- 3. 사이드바 및 사용자 자동 인식 ---
ua = st_javascript("navigator.userAgent")
detected_name = "안 함"
if ua and ua != 0:
    for model, name in DEVICE_MAP.items():
        if model in str(ua).upper(): detected_name = name; break

with st.sidebar:
    st.header("📌 메뉴")
    menu = st.radio("이동", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 관리"])
    user_name = st.selectbox("사용자 확인", ["안 함", "황재업", "이정석", "김태언", "이태원"], 
                             index=["안 함", "황재업", "이정석", "김태언", "이태원"].index(detected_name))

# --- 4. [복구] 실시간 상황판 (엑셀 이미지 데이터 100%) ---
if menu == "📍 실시간 상황판":
    st.title("🏛️ C조 실시간 근무 위치")
    diff_days = (today_val - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        # 엑셀 이미지와 동일한 20개 시간대 데이터
        sched_data = [
            {"From": "07:00", "To": "08:00", "조장": "안내실", "대원": "로비", "의산A": "로비", "의산B": "휴게"},
            {"From": "08:00", "To": "09:00", "조장": "안내실", "대원": "휴게", "의산A": "휴게", "의산B": "로비"},
            {"From": "09:00", "To": "10:00", "조장": "안내실", "대원": "순찰", "의산A": "휴게", "의산B": "로비"},
            {"From": "10:00", "To": "11:00", "조장": "휴게", "대원": "안내실", "의산A": "로비", "의산B": "순찰/휴게"},
            {"From": "11:00", "To": "12:00", "조장": "안내실", "대원": "중식", "의산A": "로비", "의산B": "중식"},
            {"From": "12:00", "To": "13:00", "조장": "중식", "대원": "안내실", "의산A": "중식", "의산B": "로비"},
            {"From": "13:00", "To": "14:00", "조장": "안내실", "대원": "휴게", "의산A": "순찰/휴게", "의산B": "로비"},
            {"From": "14:00", "To": "15:00", "조장": "순찰", "대원": "안내실", "의산A": "로비", "의산B": "휴게"},
            {"From": "15:00", "To": "16:00", "조장": "안내실", "대원": "휴게", "의산A": "로비", "의산B": "휴게"},
            {"From": "16:00", "To": "17:00", "조장": "휴게", "대원": "안내실", "의산A": "휴게", "의산B": "로비"},
            {"From": "17:00", "To": "18:00", "조장": "안내실", "대원": "휴게", "의산A": "휴게", "의산B": "로비"},
            {"From": "18:00", "To": "19:00", "조장": "안내실", "대원": "석식", "의산A": "로비", "의산B": "석식"},
            {"From": "19:00", "To": "20:00", "조장": "안내실", "대원": "안내실", "의산A": "석식", "의산B": "로비"},
            {"From": "20:00", "To": "21:00", "조장": "석식", "대원": "안내실", "의산A": "로비", "의산B": "휴게"},
            {"From": "21:00", "To": "22:00", "조장": "안내실", "대원": "순찰", "의산A": "로비", "의산B": "휴게"},
            {"From": "22:00", "To": "23:00", "조장": "순찰", "대원": "휴게", "의산A": "순찰", "의산B": "로비"},
            {"From": "23:00", "To": "01:40", "조장": "안내실", "대원": "휴게", "의산A": "휴게", "의산B": "로비"},
            {"From": "01:40", "To": "05:00", "조장": "휴게", "대원": "안내실", "의산A": "로비", "의산B": "휴게"},
            {"From": "05:00", "To": "06:00", "조장": "안내실", "대원": "순찰", "의산A": "로비", "의산B": "순찰"},
            {"From": "06:00", "To": "07:00", "조장": "안내실", "대원": "안내실", "의산A": "휴게", "의산B": "로비"},
        ]
        df_sched = pd.DataFrame(sched_data)

        def style_row(row):
            f_h, f_m = map(int, row['From'].split(':'))
            t_h, t_m = map(int, row['To'].split(':'))
            s, e = f_h * 60 + f_m, t_h * 60 + t_m
            if e < s: e += 1440
            return ['background-color: #FFF9C4; color: black; font-weight: bold'] * len(row) if s <= now_total_min < e else [''] * len(row)

        st.dataframe(df_sched.style.apply(style_row, axis=1), use_container_width=True, hide_index=True)
    else:
        st.warning("비번입니다.")

# --- 5. [중요] 사용자가 주신 '정상 로직' 기반 근무 편성표 ---
elif menu == "📅 근무 편성표":
    st.markdown("### 📅 성의교정 C조 근무편성표")
    cal_list = []
    # 3/9부터 말일까지 계산
    check_date = today_val.replace(day=1)
    end_date = (check_date + timedelta(days=32)).replace(day=1) - timedelta(days=1)
    
    while check_date <= end_date:
        diff_days = (check_date - PATTERN_START_DATE).days
        if diff_days % 3 == 0:
            shift_count = diff_days // 3  # 패턴 시작점부터 몇 번째 근무일인가
            cycle_idx = (shift_count // 2) % 3 # 회관 담당 2회씩 순환
            is_second_day = shift_count % 2 == 1 # 2회 중 두 번째 날인가
            
            # 사용자님의 정상 로직 100% 복구: 김태언(0) -> 이정석(1) -> 이태원(2) 순서
            if cycle_idx == 0:
                h = "김태언"
                a, b = ("이정석", "이태원") if is_second_day else ("이태원", "이정석")
            elif cycle_idx == 1:
                h = "이정석"
                a, b = ("이태원", "김태언") if is_second_day else ("김태언", "이태원")
            else:
                h = "이태원"
                a, b = ("이정석", "김태언") if is_second_day else ("김태언", "이정석")
            
            # 연차 반영
            v = st.session_state.vac_df[st.session_state.vac_df['날짜'] == check_date]['이름'].tolist()
            wd = check_date.weekday()
            cal_list.append({
                "날짜": f"{check_date.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "조장": "황재업",
                "성희(회관)": "🌴연차" if h in v else h,
                "의산(A)": "🌴연차" if a in v else a,
                "의산(B)": "🌴연차" if b in v else b
            })
        check_date += timedelta(days=1)
    
    st.table(pd.DataFrame(cal_list))

# --- 6. [복구] 연차 관리 (삭제 기능 포함) ---
elif menu == "✍️ 연차 관리":
    st.title("✍️ 연차 신청 및 관리")
    with st.form("add_v"):
        d, n = st.date_input("날짜"), st.selectbox("이름", ["황재업", "이정석", "김태언", "이태원"])
        if st.form_submit_button("등록"):
            st.session_state.vac_df = pd.concat([st.session_state.vac_df, pd.DataFrame([{"날짜": d, "이름": n, "사유": "개인"}])])
            st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()

    st.subheader("🗓️ 등록된 연차 (삭제)")
    for idx, row in st.session_state.vac_df.iterrows():
        c1, c2, c3 = st.columns([2, 2, 1])
        c1.write(row['날짜'])
        c2.write(f"**{row['이름']}**")
        if c3.button("삭제", key=f"del_{idx}"):
            st.session_state.vac_df = st.session_state.vac_df.drop(idx)
            st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()
