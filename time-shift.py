import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. 기본 설정 및 기기 인식 ---
DEVICE_MAP = {"S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원"}
PATTERN_START_DATE = datetime(2026, 3, 9).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 관리", layout="wide")

# 한국 표준시(KST) 및 07시 투입 기준 시간 계산
now_kst = datetime.now(timezone(timedelta(hours=9)))
today_val = now_kst.date()
now_total_min = now_kst.hour * 60 + now_kst.minute
# 07:00 이전은 전날 근무의 연장선으로 처리
if now_total_min < 7 * 60: now_total_min += 1440 

# --- 2. 데이터 로드 및 관리자 권한 ---
def load_vac():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

if 'vac_df' not in st.session_state:
    st.session_state.vac_df = load_vac()

# --- 3. 사이드바 (조회 설정 및 기기 인식) ---
ua = st_javascript("navigator.userAgent")
detected = "안 함"
if ua and ua != 0:
    for model, name in DEVICE_MAP.items():
        if model in str(ua).upper(): detected = name; break

with st.sidebar:
    st.header("⚙️ 설정 및 조회")
    menu = st.radio("메뉴", ["📍 실시간 상황판", "📅 교대 근무표", "✍️ 연차 관리(관리자)"])
    user_name = st.selectbox("👤 이름 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"], 
                             index=["안 함", "황재업", "김태언", "이태원", "이정석"].index(detected))
    
    st.divider()
    st.subheader("📅 조회 기간 설정")
    start_date = st.date_input("시작일", value=today_val - timedelta(days=7))
    duration_days = st.slider("조회 범위(일)", min_value=7, max_value=180, value=30)
    end_date = start_date + timedelta(days=duration_days)

# --- 4. [페이지 1] 실시간 상황판 (현재 상태 표시) ---
if menu == "📍 실시간 상황판":
    st.title("🏛️ 실시간 근무 현황")
    
    diff_days = (today_val - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        # 엑셀 이미지 기반 근무 로직
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
        
        # 현재 근무자 명단 추출 (사용자 소스 로직 적용)
        shift_count = diff_days // 3
        cycle_idx = (shift_count // 2) % 3
        is_2nd = shift_count % 2 == 1
        if cycle_idx == 0: h, a, b = "김태언", ("이정석" if is_2nd else "이태원"), ("이태원" if is_2nd else "이정석")
        elif cycle_idx == 1: h, a, b = "이정석", ("이태원" if is_2nd else "김태언"), ("김태언" if is_2nd else "이태원")
        else: h, a, b = "이태원", ("이정석" if is_2nd else "김태언"), ("김태언" if is_2nd else "이정석")

        # 현재 상태 실시간 요약 (상단 카드 표시)
        current_row = None
        for r in sched_data:
            sh, sm = map(int, r['From'].split(':'))
            eh, em = map(int, r['To'].split(':'))
            s, e = sh*60+sm, eh*60+em
            if e < s: e += 1440
            if s <= now_total_min < e:
                current_row = r; break
        
        if current_row:
            cols = st.columns(4)
            cols[0].metric("조장 (황재업)", current_row['조장'])
            cols[1].metric(f"성희 ({h})", current_row['대원'])
            cols[2].metric(f"의산A ({a})", current_row['의산A'])
            cols[3].metric(f"의산B ({b})", current_row['의산B'])

        st.divider()
        st.subheader("⏱️ 24시간 상세 시간표")
        df_sched = pd.DataFrame(sched_data)
        def highlight_now(row):
            sh, sm = map(int, row['From'].split(':'))
            eh, em = map(int, row['To'].split(':'))
            s, e = sh*60+sm, eh*60+em
            if e < s: e += 1440
            return ['background-color: #FFF9C4; font-weight: bold'] * len(row) if s <= now_total_min < e else [''] * len(row)
        st.dataframe(df_sched.style.apply(highlight_now, axis=1), use_container_width=True, hide_index=True)
    else: st.warning("오늘은 비번입니다.")

# --- 5. [페이지 2] 교대 근무표 (과거/미래 조회 및 슬라이더) ---
elif menu == "📅 교대 근무표":
    st.title("📅 성의교정 C조 근무편성표")
    cal_list = []
    check_date = start_date
    while check_date <= end_date:
        diff = (check_date - PATTERN_START_DATE).days
        if diff % 3 == 0:
            sc = diff // 3
            ci = (sc // 2) % 3
            is_2nd = sc % 2 == 1
            # 사용자 소스 로직 100% 반영
            if ci == 0: h, a, b = "김태언", ("이정석" if is_2nd else "이태원"), ("이태원" if is_2nd else "이정석")
            elif ci == 1: h, a, b = "이정석", ("이태원" if is_2nd else "김태언"), ("김태언" if is_2nd else "이태원")
            else: h, a, b = "이태원", ("이정석" if is_2nd else "김태언"), ("김태언" if is_2nd else "이정석")
            
            # 연차 반영
            v = st.session_state.vac_df[st.session_state.vac_df['날짜'] == check_date]['이름'].tolist()
            wd = check_date.weekday()
            cal_list.append({
                "날짜": f"{check_date.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})",
                "조장": "황재업", "성희": "🌴연차" if h in v else h,
                "의산A": "🌴연차" if a in v else a, "의산B": "🌴연차" if b in v else b
            })
        check_date += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal_list)
    def style_cells(val):
        if "(토)" in str(val): return 'color: blue;'
        if "(일)" in str(val): return 'color: red;'
        if user_name != "안 함" and str(val) == user_name: return f'background-color: {WORKER_COLORS.get(user_name)};'
        return ''
    st.dataframe(df_cal.style.applymap(style_cells), use_container_width=True, hide_index=True)

# --- 6. [페이지 3] 연차 관리 (관리자 전용 수정/삭제) ---
elif menu == "✍️ 연차 관리(관리자)":
    st.title("✍️ 연차 및 휴가 관리")
    if user_name == "황재업": # 조장님만 수정 가능하도록 설정 예시
        with st.expander("➕ 새 연차 신청"):
            with st.form("add_v"):
                d, n = st.date_input("날짜"), st.selectbox("성함", ["이태원", "김태언", "이정석"])
                if st.form_submit_button("등록"):
                    st.session_state.vac_df = pd.concat([st.session_state.vac_df, pd.DataFrame([{"날짜": d, "이름": n}])])
                    st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()
        
        st.subheader("🗓️ 연차 목록 (수정/삭제)")
        for idx, row in st.session_state.vac_df.iterrows():
            c1, c2, c3 = st.columns([2, 2, 1])
            c1.write(row['날짜'])
            c2.write(f"**{row['이름']}**")
            if c3.button("삭제", key=f"del_{idx}"):
                st.session_state.vac_df = st.session_state.vac_df.drop(idx)
                st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()
    else: st.error("관리자(황재업 조장님)만 접근 가능합니다.")
