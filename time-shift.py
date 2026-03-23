import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 근무지 패턴 (이미지 전수 대조 완료) ---
# 3/24(화) 이태원(회관), 김태언(의산A), 이정석(의산B) 기준 패턴
BASE_PATTERN = [
    {"시간": 7, "표시": "07:00", "조장": "안내실", "회관": "로비", "의산A": "휴게", "의산B": "로비"},
    {"시간": 8, "표시": "08:00", "조장": "안내실", "회관": "휴게", "의산A": "로비", "의산B": "휴게"},
    {"시간": 9, "표시": "09:00", "조장": "안내실", "회관": "순찰", "의산A": "로비", "의산B": "휴게"},
    {"시간": 10, "표시": "10:00", "조장": "휴게", "회관": "안내실", "의산A": "순찰/휴", "의산B": "로비"},
    {"시간": 11, "표시": "11:00", "조장": "안내실", "회관": "중식", "의산A": "중식", "의산B": "로비"},
    {"시간": 12, "표시": "12:00", "조장": "중식", "회관": "안내실", "의산A": "로비", "의산B": "중식"},
    {"시간": 13, "표시": "13:00", "조장": "안내실", "회관": "휴게", "의산A": "로비", "의산B": "휴/순"},
    {"시간": 14, "표시": "14:00", "조장": "순찰", "회관": "안내실", "의산A": "휴게", "의산B": "로비"},
    {"시간": 15, "표시": "15:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비"},
    {"시간": 16, "표시": "16:00", "조장": "휴게", "회관": "안내실", "의산A": "로비", "의산B": "휴게"},
    {"시간": 17, "표시": "17:00", "조장": "안내실", "회관": "휴게", "의산A": "로비", "의산B": "휴게"},
    {"시간": 18, "표시": "18:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비"},
    {"시간": 19, "표시": "19:00", "조장": "안내실", "회관": "석식", "의산A": "로비", "의산B": "석식"},
    {"시간": 20, "표시": "20:00", "조장": "안내실", "회관": "안내실", "의산A": "석식", "의산B": "로비"},
    {"시간": 21, "표시": "21:00", "조장": "석식", "회관": "안내실", "의산A": "로비", "의산B": "휴게"},
    {"시간": 22, "표시": "22:00", "조장": "안내실", "회관": "순찰", "의산A": "로비", "의산B": "휴게"},
    {"시간": 23, "표시": "23:00", "조장": "순찰", "회관": "취침", "의산A": "순찰", "의산B": "로비"},
    {"시간": 0, "표시": "00:00", "조장": "안내실", "회관": "취침", "의산A": "취침", "의산B": "로비"},
    {"시간": 1, "표시": "01:00", "조장": "안내실", "회관": "취침", "의산A": "취침", "의산B": "로비"},
    {"시간": 2, "표시": "02:00", "조장": "안내실", "회관": "취침", "의산A": "취침", "의산B": "로비"},
    {"시간": 3, "표시": "03:00", "조장": "취침", "회관": "회관근무", "의산A": "로비", "의산B": "취침"},
    {"시간": 4, "표시": "04:00", "조장": "취침", "회관": "회관근무", "의산A": "로비", "의산B": "취침"},
    {"시간": 5, "표시": "05:00", "조장": "취침", "회관": "회관근무", "의산A": "로비", "의산B": "취침"},
    {"시간": 6, "표시": "06:00", "조장": "안내실", "회관": "회관근무", "의산A": "로비", "의산B": "순찰"},
]

# --- 2. 로테이션 설정 (3/24 기준) ---
START_DATE = datetime(2026, 3, 24).date()
WORKERS = ["이태원", "김태언", "이정석"] # 회관, 의산A, 의산B 순서

st.set_page_config(layout="centered")

# --- 3. 모바일 최적화 CSS (9px 폰트 및 고정 레이아웃) ---
st.markdown("""
    <style>
    html, body, [data-testid="stTable"] { font-size: 9px !important; font-family: 'Malgun Gothic'; }
    table { width: 100% !important; table-layout: fixed !important; border-collapse: collapse; }
    th, td { padding: 3px 1px !important; text-align: center !important; border: 1px solid #eee; overflow: hidden; }
    .stAlert { padding: 0.5rem !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 실시간 시간 및 날짜 계산 ---
now = datetime.now()
current_hour = now.hour
selected_date = st.date_input("📅 날짜 선택", now.date())

days_diff = (selected_date - START_DATE).days

# C조 근무일 판별 (3일 주기)
if days_diff % 3 == 0:
    # 근무 순서 로테이션 계산
    shift = (days_diff // 3) % 3
    h_man = WORKERS[(0 + shift) % 3]
    a_man = WORKERS[(1 + shift) % shift if shift != 0 else 1] # 리스트 순환 로직
    # 단순화된 순환 로직 적용
    lineup = [WORKERS[(0+shift)%3], WORKERS[(1+shift)%3], WORKERS[(2+shift)%3]]
    w_h, w_a, w_b = lineup[0], lineup[1], lineup[2]

    # --- 실시간 근무자 확인 헤더 ---
    st.subheader(f"✅ {selected_date.strftime('%m/%d')} C조 근무")
    
    # 현재 시간에 맞는 데이터 찾기
    cur_match = next((m for m in BASE_PATTERN if m["시간"] == current_hour), None)
    
    if cur_match and selected_date == now.date():
        st.info(f"📍 **현재({current_hour}시) 근무 위치**\n"
                f"• 조장(황): {cur_match['조장']} / 회관({w_h}): {cur_match['회관']}\n"
                f"• 의산A({w_a}): {cur_match['의산A']} / 의산B({w_b}): {cur_match['의산B']}")

    # --- 표 데이터 구성 ---
    final_df_list = []
    for row in BASE_PATTERN:
        final_df_list.append({
            "시간": row["표시"],
            "황재업(조)": row["조장"],
            f"{w_h}(회)": row["회관"],
            f"{w_a}(A)": row["의산A"],
            f"{w_b}(B)": row["의산B"]
        })
    
    df = pd.DataFrame(final_df_list)

    # 스타일 적용 (현재 시간 행 강조)
    def highlight_now(row):
        is_now = (int(row['시간'].split(':')[0]) == current_hour) and (selected_date == now.date())
        style = ['background-color: #FFF9C4; font-weight: bold; border: 1.2px solid red;' if is_now else '' for _ in row]
        return style

    st.table(df.style.apply(highlight_now, axis=1))
else:
    st.warning(f"⚠️ {selected_date}은(는) C조 휴무일입니다.")
