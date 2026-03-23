import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 근무 패턴 (이름 대신 역할 '회관', '의산A', '의산B'로 정의) ---
# 사용자님이 주신 1시간 단위 원칙 및 의산연 동시 휴게 불가 규칙 적용
BASE_PATTERN = [
    {"시간": "07:00-08:00", "조장": "안내실", "회관": "로비", "의산A": "로비", "의산B": "휴게"},
    {"시간": "08:00-09:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비"},
    {"시간": "09:00-10:00", "조장": "안내실", "회관": "순찰", "의산A": "휴게", "의산B": "로비"},
    {"시간": "10:00-11:00", "조장": "휴게", "회관": "안내실", "의산A": "로비", "의산B": "순찰(30)/휴게(30)"},
    {"시간": "11:00-12:00", "조장": "안내실", "회관": "중식", "의산A": "로비", "의산B": "중식"},
    {"시간": "12:00-13:00", "조장": "중식", "회관": "안내실", "의산A": "중식", "의산B": "로비"},
    {"시간": "13:00-14:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게(30)/순찰(30)", "의산B": "로비"},
    {"시간": "14:00-15:00", "조장": "순찰", "회관": "안내실", "의산A": "로비", "의산B": "휴게"},
    {"시간": "15:00-16:00", "조장": "안내실", "회관": "휴게", "의산A": "로비", "의산B": "휴게"},
    {"시간": "16:00-17:00", "조장": "휴게", "회관": "안내실", "의산A": "휴게", "의산B": "로비"},
    {"시간": "17:00-18:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비"},
    {"시간": "18:00-19:00", "조장": "로비", "회관": "안내실", "의산A": "로비", "의산B": "휴게"},
    {"시간": "19:00-20:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비"},
    {"시간": "20:00-21:00", "조장": "안내실", "회관": "석식", "의산A": "로비", "의산B": "석식"},
    {"시간": "21:00-22:00", "조장": "회관근무", "회관": "취침", "의산A": "로비", "의산B": "대기"},
    {"시간": "22:00-23:00", "조장": "회관근무", "회관": "취침", "의산A": "대기", "의산B": "로비"},
    {"시간": "23:00-00:00", "조장": "취침", "회관": "취침", "의산A": "회관근무", "의산B": "로비"},
    {"시간": "00:00-01:00", "조장": "취침", "회관": "취침", "의산A": "로비", "의산B": "회관근무"},
    {"시간": "01:00-02:00", "조장": "취침", "회관": "취침", "의산A": "회관근무", "의산B": "로비"},
    {"시간": "02:00-03:00", "조장": "취침", "회관": "취침", "의산A": "로비", "의산B": "회관근무"},
    {"시간": "03:00-04:00", "조장": "로비", "회관": "회관근무", "의산A": "취침", "의산B": "대기"},
    {"시간": "04:00-05:00", "조장": "대기", "회관": "회관근무", "의산A": "대기", "의산B": "취침"},
    {"시간": "05:00-06:00", "조장": "로비", "회관": "회관근무", "의산A": "취침", "의산B": "대기"},
    {"시간": "06:00-07:00", "조장": "대기", "회관": "회관근무", "의산A": "대기", "의산B": "취침"},
]

st.set_page_config(layout="wide")
st.title("🛡️ C조 성의 워크플레이스 허브")

# --- 2. 날짜에 따른 근무자 자동 배정 로직 ---
now = datetime.now()
selected_date = st.sidebar.date_input("조회 날짜", now.date())

# 기준일: 3/18 (C조 확정 근무일)
anchor_date = datetime(2026, 3, 18).date()
days_diff = (selected_date - anchor_date).days

if days_diff % 3 == 0:
    cycle_idx = days_diff // 3
    names = ["이태원", "이정석", "김태언"]
    
    # 3일 주기 로테이션 적용
    shift_offset = (cycle_idx // 2) % 3
    worker_h = names[shift_offset]  # 회관 역할
    remaining = [n for n in names if n != worker_h]
    worker_a, worker_b = (remaining[1], remaining[0]) if cycle_idx % 2 == 1 else (remaining[0], remaining[1])

    # --- 3. 데이터프레임 구성 (이름 동적 매칭) ---
    final_df_list = []
    for r in BASE_PATTERN:
        final_df_list.append({
            "시간": r["시간"],
            "황재업(조)": r["조장"],
            f"{worker_h}(회)": r["회관"],
            f"{worker_a}(A)": r["의산A"],
            f"{worker_b}(B)": r["의산B"]
        })
    df = pd.DataFrame(final_df_list)

    # --- 4. 스타일 적용 ---
    def style_table(row):
        start_h = int(row['시간'].split('-')[0].split(':')[0])
        is_now = (start_h == now.hour) and (selected_date == now.date())
        styles = []
        for col, val in row.items():
            base = 'color: black; font-weight: bold; '
            if is_now: base += 'background-color: #FFF9C4; border: 2px solid orange; '
            v = str(val)
            if '로비' in v: base += 'color: #D32F2F;'
            elif '순찰' in v: base += 'color: #1976D2;'
            elif '취침' in v or '대기' in v: base += 'color: #9E9E9E;'
            elif '중식' in v or '석식' in v: base += 'color: #EF6C00;'
            elif '안내실' in v or '회관근무' in v: base += 'color: #008B8B;'
            styles.append(base)
        return styles

    st.success(f"✅ {selected_date} 근무: {worker_h}(회), {worker_a}(A), {worker_b}(B)")
    st.table(df.style.apply(style_table, axis=1))

else:
    st.warning(f"C조 근무일이 아닙니다. 다음 근무: {selected_date + timedelta(days=3-(days_diff%3))}일")
