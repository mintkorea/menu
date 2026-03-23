import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 근무 패턴 (이미지 전수 대조 완료) ---
# 위치명은 가변적으로 처리하기 위해 인덱스로 관리
BASE_PATTERN = [
    {"시간": "07:00", "조장": "안내실", "회관": "로비", "의산A": "휴게", "의산B": "로비"},
    {"시간": "08:00", "조장": "안내실", "회관": "휴게", "의산A": "로비", "의산B": "휴게"},
    {"시간": "09:00", "조장": "안내실", "회관": "순찰", "의산A": "로비", "의산B": "휴게"},
    {"시간": "10:00", "조장": "휴게", "회관": "안내실", "의산A": "순찰/휴", "의산B": "로비"},
    {"시간": "11:00", "조장": "안내실", "회관": "중식", "의산A": "중식", "의산B": "로비"},
    {"시간": "12:00", "조장": "중식", "회관": "안내실", "의산A": "로비", "의산B": "중식"},
    {"시간": "13:00", "조장": "안내실", "회관": "휴게", "의산A": "로비", "의산B": "휴/순"},
    {"시간": "14:00", "조장": "순찰", "회관": "안내실", "의산A": "휴게", "의산B": "로비"},
    {"시간": "15:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비"},
    {"시간": "16:00", "조장": "휴게", "회관": "안내실", "의산A": "로비", "의산B": "휴게"},
    {"시간": "17:00", "조장": "안내실", "회관": "휴게", "의산A": "로비", "의산B": "휴게"},
    {"시간": "18:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비"},
    {"시간": "19:00", "조장": "안내실", "회관": "석식", "의산A": "로비", "의산B": "석식"},
    {"시간": "20:00", "조장": "안내실", "회관": "안내실", "의산A": "석식", "의산B": "로비"},
    {"시간": "21:00", "조장": "석식", "회관": "안내실", "의산A": "로비", "의산B": "휴게"},
    {"시간": "22:00", "조장": "안내실", "회관": "순찰", "의산A": "로비", "의산B": "휴게"},
    {"시간": "23:00", "조장": "순찰", "회관": "취침", "의산A": "순찰", "의산B": "로비"},
    {"시간": "00:00", "조장": "안내실", "회관": "취침", "의산A": "취침", "의산B": "로비"},
    {"시간": "01:00", "조장": "안내실", "회관": "취침", "의산A": "취침", "의산B": "로비"},
    {"시간": "02:00", "조장": "안내실", "회관": "취침", "의산A": "취침", "의산B": "로비"},
    {"시간": "03:00", "조장": "취침", "회관": "회관근무", "의산A": "로비", "의산B": "취침"},
    {"시간": "04:00", "조장": "취침", "회관": "회관근무", "의산A": "로비", "의산B": "취침"},
    {"시간": "05:00", "조장": "취침", "회관": "회관근무", "의산A": "로비", "의산B": "취침"},
    {"시간": "06:00", "조장": "안내실", "회관": "회관근무", "의산A": "로비", "의산B": "순찰"},
]

# --- 2. 로테이션 로직 설정 ---
# 3/24일 기준: 이태원(회관), 김태언(의산A), 이정석(의산B)
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"]

st.set_page_config(layout="centered")

# --- 3. 모바일 최적화 CSS (9px 폰트) ---
st.markdown("""
    <style>
    html, body, [data-testid="stTable"] { font-size: 9px !important; }
    table { width: 100% !important; table-layout: fixed !important; }
    th, td { padding: 2px !important; text-align: center !important; border: 1px solid #eee !important; white-space: nowrap !important; }
    .current-time { background-color: #FFF9C4 !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 날짜 선택 및 인원 배치 ---
selected_date = st.date_input("근무일 선택", datetime.now().date())
days_diff = (selected_date - START_DATE).days

if days_diff % 3 == 0:
    # 3일마다 인원이 한 칸씩 밀리는 로테이션 (0:이, 1:김, 2:이 순서)
    shift = (days_diff // 3) % 3
    # 로테이션 결과: [회관 담당, 의산A 담당, 의산B 담당]
    current_lineup = [WORKERS[(0+shift)%3], WORKERS[(1+shift)%3], WORKERS[(2+shift)%3]]
    
    w_h, w_a, w_b = current_lineup[0], current_lineup[1], current_lineup[2]
    
    st.success(f"📅 {selected_date} 근무: {w_h}(회), {w_a}(A), {w_b}(B)")

    # 데이터 재구성
    final_list = []
    for row in BASE_PATTERN:
        final_list.append({
            "시간": row["시간"],
            "황재업(조)": row["조장"],
            f"{w_h}(회)": row["회관"],
            f"{w_a}(A)": row["의산A"],
            f"{w_b}(B)": row["의산B"]
        })
    
    df = pd.DataFrame(final_list)
    current_hour = datetime.now().hour

    def row_style(row):
        is_now = (int(row['시간'].split(':')[0]) == current_hour) and (selected_date == datetime.now().date())
        styles = []
        for val in row:
            base = 'background-color: #FFF9C4; border: 1px solid red;' if is_now else ''
            v = str(val)
            if '로비' in v: base += 'color: red;'
            elif '순찰' in v: base += 'color: blue;'
            elif '취침' in v or '휴' in v: base += 'color: gray;'
            styles.append(base)
        return styles

    st.table(df.style.apply(row_style, axis=1))
else:
    st.warning("C조 근무일이 아닙니다.")
