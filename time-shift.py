import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from streamlit_javascript import st_javascript

# --- 1. 기기-성함 매칭 데이터 ---
DEVICE_MAP = {
    "S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원",
}

# --- 2. 기준 설정 (3/24 근무일 기준) ---
PATTERN_START_DATE = datetime(2026, 3, 24).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7", "연차": "#FFEBEE"}
VACATION_FILE = 'vacation.csv'
ADMIN_PASSWORD = "1234"

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

# --- 데이터 처리 함수들 ---
def load_vacation_data():
    if os.path.exists(VACATION_FILE):
        try:
            df = pd.read_csv(VACATION_FILE)
            df['날짜'] = pd.to_datetime(df['날짜']).dt.date
            return df
        except: return pd.DataFrame(columns=['날짜', '이름', '사유'])
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

def save_vacation_data(df):
    df.to_csv(VACATION_FILE, index=False, encoding='utf-8-sig')

def get_device_user():
    ua = st_javascript("navigator.userAgent")
    if ua and ua != 0:
        ua_str = str(ua).upper()
        for model, name in DEVICE_MAP.items():
            if model in ua_str: return name
    return "안 함"

df_vac = load_vacation_data()

def check_vacation(date, name):
    is_vac = df_vac[(df_vac['날짜'] == date) & (df_vac['이름'] == name)]
    return "연차" if not is_vac.empty else name

def get_shift_workers(date):
    diff_days = (date - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        shift_count = diff_days // 3
        cycle_idx = (shift_count // 2) % 3 
        is_second_day = shift_count % 2 == 1
        if cycle_idx == 0: h_p, a_p, b_p = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
        elif cycle_idx == 1: h_p, a_p, b_p = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
        else: h_p, a_p, b_p = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
        return [("조장", "황재업"), ("회관", h_p), ("의산(A)", a_p), ("의산(B)", b_p)]
    return None

# --- 3. 사이드바 ---
with st.sidebar:
    st.header("⚙️ 스마트 설정")
    menu = st.radio("메뉴 이동", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 신청/관리"])
    st.divider()
    detected = get_device_user()
    user_list = ["안 함", "황재업", "김태언", "이태원", "이정석"]
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = detected if detected in user_list else "안 함"
    user_name = st.selectbox("👤 내 이름 강조", user_list, index=user_list.index(st.session_state.selected_user))

today_val = datetime.now().date()

# --- 4. 메뉴별 로직 ---

if menu == "📍 실시간 상황판":
    st.markdown("### 📍 실시간 근무 및 안내")
    
    # [시간표 고정] 종이 근무표 대신 상시 확인용
    with st.expander("⏰ C조 표준 근무 시간 안내", expanded=True):
        time_table = pd.DataFrame({
            "구분": ["주간", "야간", "교대"],
            "시간": ["08:00 ~ 18:00", "18:00 ~ 08:00", "08:00 정시"],
            "비고": ["회관/의산", "순찰 및 대기", "인수인계"]
        })
        st.table(time_table)

    st.divider()

    # 오늘 근무 상태 확인
    current_workers = get_shift_workers(today_val)
    
    if current_workers:
        st.success(f"✅ 오늘({today_val.strftime('%m/%d')})은 **[C조 근무일]**입니다.")
    else:
        st.warning(f"😴 오늘({today_val.strftime('%m/%d')})은 **[비번/휴무]**입니다.")
        # 다음 근무일 계산
        days_diff = (today_val - PATTERN_START_DATE).days
        wait_days = 3 - (days_diff % 3) if days_diff % 3 > 0 else abs(days_diff % 3)
        next_work = today_val + timedelta(days=wait_days)
        st.info(f"📅 나의 다음 근무일: **{next_work.strftime('%m/%d')}** ({int(wait_days)}일 남음)")
        
        # 비번이어도 오늘 전체 편성표를 보려면 이 날짜의 근무자를 가져옴
        current_workers = get_shift_workers(today_val)

    # 근무자 명단 (비번일 때도 하단에 상시 표시 가능하도록 로직 구성)
    st.markdown("#### 👤 현재 시간대 근무자")
    # 오늘이 근무일이든 아니든, C조의 '오늘 순번'을 보여줍니다.
    # 만약 다른 조 정보를 넣으려면 get_shift_workers 로직을 확장해야 합니다.
    display_workers = get_shift_workers(today_val)
    if display_workers:
        cols = st.columns(4)
        for i, (pos, name) in enumerate(display_workers):
            status = check_vacation(today_val, name)
            with cols[i]:
                st.metric(pos, status)
                if status == "연차": st.error("부재중")
                else: st.success("근무중")
    else:
        st.info("오늘은 C조 전체 비번입니다. 하단 편성표에서 다음 일정을 확인하세요.")

    st.divider()
    
    # 주간 편성표 (종이 근무표 대체 핵심)
    st.markdown("#### 🗓️ 주간 교대 일정")
    week_data = []
    for i in range(-2, 7): # 전후 1주일치
        target_d = today_val + timedelta(days=i)
        target_w = get_shift_workers(target_d)
        if target_w:
            row = {"날짜": target_d.strftime('%m/%d') + f"({['월','화','수','목','금','토','일'][target_d.weekday()]})"}
            for p, n in target_w: row[p] = check_vacation(target_d, n)
            week_data.append(row)
    
    if week_data:
        df_week = pd.DataFrame(week_data)
        def style_highlight(val):
            if val == "연차": return 'color: red; font-weight: bold;'
            if val == user_name and user_name != "안 함": return f'background-color: {WORKER_COLORS.get(val)}; font-weight: bold; border: 1px solid blue;'
            return ''
        st.dataframe(df_week.style.applymap(style_highlight), use_container_width=True, hide_index=True)

elif menu == "📅 근무 편성표":
    st.markdown("### 📅 전체 근무 편성표 조회")
    s_date = st.date_input("조회 시작일", today_val)
    d_range = st.slider("조회 기간(일)", 7, 90, 30)
    
    full_list = []
    curr = s_date
    for _ in range(d_range):
        w = get_shift_workers(curr)
        if w:
            row = {"날짜": curr.strftime('%m/%d') + f"({['월','화','수','목','금','토','일'][curr.weekday()]})"}
            for pos, name in w: row[pos] = check_vacation(curr, name)
            full_list.append(row)
        curr += timedelta(days=1)
    
    if full_list:
        df_full = pd.DataFrame(full_list)
        st.dataframe(df_full.style.applymap(lambda x: f'background-color: {WORKER_COLORS.get(x)}' if x in WORKER_COLORS and x == user_name else ''), use_container_width=True, hide_index=True, height=600)

elif menu == "✍️ 연차 신청/관리":
    st.markdown("### 📂 연차 관리 시스템")
    t1, t2, t3 = st.tabs(["현황", "신청", "관리자"])
    with t1: st.dataframe(df_vac.sort_values('날짜', ascending=False), use_container_width=True)
    with t2:
        with st.form("v_form"):
            d, n, r = st.date_input("날짜", today_val), st.selectbox("성명", ["황재업", "김태언", "이태원", "이정석"]), st.text_input("사유")
            if st.form_submit_button("신청"):
                df_vac = pd.concat([df_vac, pd.DataFrame({'날짜':[d],'이름':[n],'사유':[r]})], ignore_index=True)
                save_vacation_data(df_vac); st.rerun()
    with t3:
        if st.text_input("암호", type="password") == ADMIN_PASSWORD:
            if not df_vac.empty:
                idx = st.number_input("삭제 ID", 0, len(df_vac)-1)
                if st.button("삭제"):
                    df_vac = df_vac.drop(idx).reset_index(drop=True)
                    save_vacation_data(df_vac); st.rerun()
