import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 이미지 전수 대조 데이터 (수정본 반영) ---
# 주간(07-17): image_3e8d9d.png / 야간(18-07): image_49152b.png 기준
SCHEDULE_DATA = [
    {"시간": "07:00", "황(조)": "안내실", "이(회)": "로비", "김(A)": "휴게", "이(B)": "로비"},
    {"시간": "08:00", "황(조)": "안내실", "이(회)": "휴게", "김(A)": "로비", "이(B)": "휴게"},
    {"시간": "09:00", "황(조)": "안내실", "이(회)": "순찰", "김(A)": "로비", "이(B)": "휴게"},
    {"시간": "10:00", "황(조)": "휴게", "이(회)": "안내실", "김(A)": "순찰/휴", "이(B)": "로비"},
    {"시간": "11:00", "황(조)": "안내실", "이(회)": "중식", "김(A)": "중식", "이(B)": "로비"},
    {"시간": "12:00", "황(조)": "중식", "이(회)": "안내실", "김(A)": "로비", "이(B)": "중식"},
    {"시간": "13:00", "황(조)": "안내실", "이(회)": "휴게", "김(A)": "로비", "이(B)": "휴/순"},
    {"시간": "14:00", "황(조)": "순찰", "이(회)": "안내실", "김(A)": "휴게", "이(B)": "로비"},
    {"시간": "15:00", "황(조)": "안내실", "이(회)": "휴게", "김(A)": "휴게", "이(B)": "로비"},
    {"시간": "16:00", "황(조)": "휴게", "이(회)": "안내실", "김(A)": "로비", "이(B)": "휴게"},
    {"시간": "17:00", "황(조)": "안내실", "이(회)": "휴게", "김(A)": "로비", "이(B)": "휴게"},
    {"시간": "18:00", "황(조)": "안내실", "이(회)": "휴게", "김(A)": "휴게", "이(B)": "로비"},
    {"시간": "19:00", "황(조)": "안내실", "이(회)": "석식", "김(A)": "로비", "이(B)": "석식"},
    {"시간": "20:00", "황(조)": "안내실", "이(회)": "안내실", "김(A)": "석식", "이(B)": "로비"},
    {"시간": "21:00", "황(조)": "석식", "이(회)": "안내실", "김(A)": "로비", "이(B)": "휴게"},
    {"시간": "22:00", "황(조)": "안내실", "이(회)": "순찰", "김(A)": "로비", "이(B)": "휴게"},
    {"시간": "23:00", "황(조)": "순찰", "이(회)": "취침", "김(A)": "순찰", "이(B)": "로비"},
    {"시간": "00:00", "황(조)": "안내실", "이(회)": "취침", "김(A)": "취침", "이(B)": "로비"},
    {"시간": "01:00", "황(조)": "안내실", "이(회)": "취침", "김(A)": "취침", "이(B)": "로비"},
    {"시간": "02:00", "황(조)": "안내실", "이(회)": "취침", "김(A)": "취침", "이(B)": "로비"},
    {"시간": "03:00", "황(조)": "취침", "이(회)": "회관근무", "김(A)": "로비", "이(B)": "취침"},
    {"시간": "04:00", "황(조)": "취침", "이(회)": "회관근무", "김(A)": "로비", "이(B)": "취침"},
    {"시간": "05:00", "황(조)": "취침", "이(회)": "회관근무", "김(A)": "로비", "이(B)": "취침"},
    {"시간": "06:00", "황(조)": "안내실", "이(회)": "회관근무", "김(A)": "로비", "이(B)": "순찰"},
]

st.set_page_config(page_title="C조 상황판", layout="centered")

# --- 2. 모바일용 폰트 최소화 CSS ---
st.markdown("""
    <style>
    .reportview-container .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    table { font-size: 10px !important; width: 100% !important; table-layout: fixed; }
    th, td { padding: 2px !important; text-align: center !important; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .stDateInput { margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 근무 달력 표출 및 날짜 로직 ---
st.subheader("📅 근무 달력")
selected_date = st.date_input("날짜를 선택하세요", datetime.now().date())

# C조 기준일 (3월 24일 근무 확정)
anchor = datetime(2026, 3, 24).date()
diff = (selected_date - anchor).days

if diff % 3 == 0:
    st.success(f"✅ {selected_date} [C조 근무일]")
    
    df = pd.DataFrame(SCHEDULE_DATA)
    current_hour = datetime.now().hour

    def mobile_style(row):
        is_now = (int(row['시간'].split(':')[0]) == current_hour) and (selected_date == datetime.now().date())
        styles = []
        for val in row:
            base = 'font-weight: bold; '
            if is_now: base += 'background-color: #FFFFE0; border: 1px solid red; '
            v = str(val)
            if '로비' in v: base += 'color: red;'
            elif '순찰' in v: base += 'color: blue;'
            elif '취침' in v or '휴' in v: base += 'color: gray;'
            elif '식' in v: base += 'color: orange;'
            elif '안내' in v or '회관' in v: base += 'color: darkcyan;'
            styles.append(base)
        return styles

    # 표 출력 (st.table은 모바일에서 잘리지 않도록 정적 렌더링)
    st.table(df.style.apply(mobile_style, axis=1))
else:
    next_duty = selected_date + timedelta(days=3 - (diff % 3))
    st.warning(f"휴무일입니다. (다음 근무: {next_duty})")
