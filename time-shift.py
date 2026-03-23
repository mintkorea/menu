import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. 한국 표준시(KST) 강제 설정 ---
def get_now_kst():
    # 세계 표준시(UTC)에 9시간을 더해 한국 시간으로 고정
    return datetime.now(timezone(timedelta(hours=9)))

# --- 2. 기준 데이터 설정 ---
# 3월 24일(화)이 C조 근무일인 기준점
PATTERN_START_DATE = datetime(2026, 3, 24).date()
DEVICE_MAP = {"S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원"}
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7", "연차": "#FFEBEE"}
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

# --- 데이터 처리 함수 ---
def load_vacation_data():
    if os.path.exists(VACATION_FILE):
        try:
            df = pd.read_csv(VACATION_FILE)
            df['날짜'] = pd.to_datetime(df['날짜']).dt.date
            return df
        except: return pd.DataFrame(columns=['날짜', '이름', '사유'])
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

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

df_vac = load_vacation_data()
now_kst = get_now_kst()
today_val = now_kst.date()

# --- 3. 사이드바 ---
with st.sidebar:
    st.header("⚙️ 스마트 설정")
    menu = st.radio("메뉴 이동", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 신청/관리"])
    user_name = st.selectbox("👤 내 이름 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- 4. 메뉴별 로직 ---

if menu == "📍 실시간 상황판":
    st.markdown("### 📍 오늘의 근무 스케줄")
    st.caption(f"🕒 현재 시각(한국): {now_kst.strftime('%Y-%m-%d %H:%M')}")

    # [중요] 근무 시간 안내 (스케줄표) - 비번일 때도 항상 최상단 노출
    st.info("🕒 **C조 표준 근무 시간**")
    t_col1, t_col2, t_col3 = st.columns(3)
    with t_col1: st.metric("☀️ 주간", "08:00~18:00")
    with t_col2: st.metric("🌙 야간", "18:00~08:00")
    with t_col3: st.metric("🔄 교대", "08:00 정시")
    
    st.divider()

    # 오늘 근무자 계산
    workers = get_shift_workers(today_val)
    
    if workers:
        st.success(f"✅ 오늘({today_val.strftime('%m/%d')})은 **C조 근무일**입니다.")
        cols = st.columns(4)
        for i, (pos, name) in enumerate(workers):
            is_vac = not df_vac[(df_vac['날짜'] == today_val) & (df_vac['이름'] == name)].empty
            display_name = "연차" if is_vac else name
            with cols[i]:
                st.metric(pos, display_name)
                if is_vac: st.error("❌ 휴무")
                else: st.success("✅ 근무")
    else:
        # 비번일 때 표시
        st.warning(f"😴 오늘({today_val.strftime('%m/%d')})은 **비번/휴무**입니다.")
        days_diff = (today_val - PATTERN_START_DATE).days
        wait_days = 3 - (days_diff % 3) if days_diff % 3 > 0 else abs(days_diff % 3)
        next_date = today_val + timedelta(days=wait_days)
        st.info(f"📅 다음 근무일: **{next_date.strftime('%m/%d')}** ({int(wait_days)}일 후)")

    st.divider()
    
    # [종이 근무표 대체] 주간 간이 편성표 상시 노출
    st.markdown("#### 🗓️ 주간 교대 흐름 (최근 7일)")
    week_list = []
    for i in range(-1, 6):
        d = today_val + timedelta(days=i)
        w = get_shift_workers(d)
        if w:
            row = {"날짜": d.strftime('%m/%d') + f"({['월','화','수','목','금','토','일'][d.weekday()]})"}
            for p, n in w:
                is_v = not df_vac[(df_vac['날짜'] == d) & (df_vac['이름'] == n)].empty
                row[p] = "연차" if is_v else n
            week_list.append(row)
    
    if week_list:
        df_w = pd.DataFrame(week_list)
        def style_df(val):
            if val == "연차": return 'color: red;'
            if val == user_name and user_name != "안 함": return f'background-color: {WORKER_COLORS.get(val)}; font-weight: bold;'
            return ''
        st.dataframe(df_w.style.applymap(style_df), use_container_width=True, hide_index=True)

elif menu == "📅 근무 편성표":
    st.markdown("### 📅 전체 근무 편성표 조회")
    # 시작일을 오늘(today_val)로 고정하여 NameError 방지
    s_date = st.date_input("조회 시작일", today_val)
    d_range = st.slider("조회 기간(일)", 7, 90, 30)
    
    full_list = []
    curr = s_date
    for _ in range(d_range):
        w = get_shift_workers(curr)
        if w:
            row = {"날짜": curr.strftime('%m/%d') + f"({['월','화','수','목','금','토','일'][curr.weekday()]})"}
            for p, n in w:
                is_v = not df_vac[(df_vac['날짜'] == curr) & (df_vac['이름'] == n)].empty
                row[p] = "연차" if is_v else n
            full_list.append(row)
        curr += timedelta(days=1)
    
    if full_list:
        st.dataframe(pd.DataFrame(full_list), use_container_width=True, hide_index=True, height=600)

elif menu == "✍️ 연차 신청/관리":
    st.markdown("### 📂 연차 관리 시스템")
    # ... (기존 연차 관리 로직 유지)
