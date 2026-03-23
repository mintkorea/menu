import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

# --- 1. 한국 표준시(KST) 설정 (어제 소스에 이 부분만 추가되었습니다) ---
def get_now_kst():
    return datetime.now(timezone(timedelta(hours=9)))

# --- 2. 기본 설정 및 기준일 ---
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
        shift_num = diff_days // 3
        cycle = shift_num % 6
        names = {
            0: ["황재업", "이태원", "이정석", "김태언"],
            1: ["황재업", "김태언", "이태원", "이정석"],
            2: ["황재업", "김태언", "이정석", "이태원"],
            3: ["황재업", "이정석", "김태언", "이태원"],
            4: ["황재업", "이정석", "이태원", "김태언"],
            5: ["황재업", "이태원", "김태언", "이정석"]
        }
        res = names[cycle]
        return [("조장", res[0]), ("성희관", res[1]), ("의산연(A)", res[2]), ("의산연(B)", res[3])]
    return None

df_vac = load_vacation_data()
now_kst = get_now_kst()
today_val = now_kst.date()

# --- 3. 사이드바 메뉴 (어제 만드신 구성 그대로) ---
with st.sidebar:
    st.header("⚙️ 스마트 설정")
    menu = st.radio("메뉴 이동", ["📍 실시간 상황판", "📅 근무 편성표", "✍️ 연차 신청/관리"])
    user_name = st.selectbox("👤 내 이름 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- 4. 메뉴별 로직 ---

if menu == "📍 실시간 상황판":
    st.markdown("### 📍 실시간 근무 및 안내")
    st.caption(f"🕒 현재 시각: {now_kst.strftime('%Y-%m-%d %H:%M')}")
    
    # 상단 요약 안내 (어제 디자인)
    with st.expander("⏰ C조 표준 근무 시간 안내", expanded=False):
        st.table(pd.DataFrame([
            {"구분": "주간", "시간": "08:00 ~ 18:00", "비고": "회관/의산"},
            {"구분": "야간", "시간": "18:00 ~ 08:00", "비고": "순찰 및 대기"},
            {"구분": "교대", "시간": "08:00 정시", "비고": "인수인계"}
        ]))

    workers = get_shift_workers(today_val)
    if workers:
        st.success(f"✅ 오늘({today_val.strftime('%m/%d')})은 **C조 근무일**입니다.")
        cols = st.columns(4)
        for i, (pos, name) in enumerate(workers):
            is_vac = not df_vac[(df_vac['날짜'] == today_val) & (df_vac['이름'] == name)].empty
            display = "연차" if is_vac else name
            with cols[i]:
                st.metric(pos, display)
                if is_vac: st.error("휴무")
    else:
        st.warning(f"😴 오늘({today_val.strftime('%m/%d')})은 **[비번/휴무]**입니다.")
        days_diff = (today_val - PATTERN_START_DATE).days
        wait = 3 - (days_diff % 3) if days_diff % 3 > 0 else abs(days_diff % 3)
        st.info(f"📅 나의 다음 근무일: **{(today_val + timedelta(days=wait)).strftime('%m/%d')}**")

    st.divider()
    st.markdown("#### 🗓️ 주간 교대 일정")
    week_list = []
    for i in range(-1, 8):
        d = today_val + timedelta(days=i)
        w = get_shift_workers(d)
        if w:
            row = {"날짜": d.strftime('%m/%d(%a)')}
            for p, n in w: row[p] = n
            week_list.append(row)
    
    if week_list:
        df_w = pd.DataFrame(week_list)
        def style_df(val):
            if val == user_name and user_name != "안 함": return f'background-color: {WORKER_COLORS.get(val)}; font-weight: bold;'
            return ''
        st.dataframe(df_w.style.applymap(style_df), use_container_width=True, hide_index=True)

elif menu == "📅 근무 편성표":
    st.markdown("### 📅 전체 근무 편성표 조회")
    # 어제 발생했던 NameError(today 미정의)를 today_val로 수정하여 해결
    start_date = st.date_input("조회 시작일", today_val)
    
    full_list = []
    for i in range(30):
        curr = start_date + timedelta(days=i)
        w = get_shift_workers(curr)
        if w:
            row = {"날짜": curr.strftime('%Y-%m-%d(%a)')}
            for p, n in w: row[p] = n
            full_list.append(row)
    st.dataframe(pd.DataFrame(full_list), use_container_width=True, hide_index=True, height=500)

elif menu == "✍️ 연차 신청/관리":
    st.markdown("### ✍️ 연차 신청 및 관리")
    # 연차 파일 저장 및 관리 로직 (어제 버전 유지)
    with st.form("vacation_form"):
        v_date = st.date_input("연차 날짜", today_val)
        v_name = st.selectbox("신청자", ["황재업", "김태언", "이태원", "이정석"])
        v_reason = st.text_input("사유", "개인사정")
        if st.form_submit_button("신청하기"):
            new_data = pd.DataFrame([[v_date, v_name, v_reason]], columns=['날짜', '이름', '사유'])
            df_vac = pd.concat([df_vac, new_data]).drop_duplicates()
            df_vac.to_csv(VACATION_FILE, index=False)
            st.success(f"{v_name}님 {v_date} 연차 등록 완료!")
            st.rerun()
