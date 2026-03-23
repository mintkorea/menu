import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 엑셀 원본 데이터 (이미지 기반 1:1 매칭) ---
# 문법 오류(SyntaxError)를 수정하고, 엑셀의 모든 열을 그대로 담았습니다.
SCHEDULE_DATA = [
    {"No": "1", "시작": "07:00", "종료": "08:00", "조장": "안내실", "회관": "로비", "의산A": "로비", "의산B": "휴게", "분": "60"},
    {"No": "2", "시작": "08:00", "종료": "09:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비", "분": "60"},
    {"No": "3", "시작": "09:00", "종료": "10:00", "조장": "안내실", "회관": "순찰", "의산A": "휴게", "의산B": "로비", "분": "60"},
    {"No": "4", "시작": "10:00", "종료": "11:00", "조장": "휴게", "회관": "안내실", "의산A": "로비", "의산B": "순찰(30)/휴게(30)", "분": "30,30"},
    {"No": "5", "시작": "11:00", "종료": "12:00", "조장": "로비", "회관": "안내실", "의산A": "순찰", "의산B": "로비", "분": "60"},
    {"No": "6", "시작": "12:00", "종료": "13:00", "조장": "순찰", "회관": "휴게", "의산A": "중식", "의산B": "로비", "분": "60"},
    {"No": "7", "시작": "13:00", "종료": "14:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게(30)/순찰(30)", "의산B": "로비", "분": "30,30"},
    {"No": "8", "시작": "14:00", "종료": "15:00", "조장": "로비", "회관": "순찰", "의산A": "로비", "의산B": "휴게", "분": "60"},
    {"No": "9", "시작": "15:00", "종료": "16:00", "조장": "안내실", "회관": "휴게", "의산A": "로비", "의산B": "휴게", "분": "60"},
    {"No": "10", "시작": "16:00", "종료": "17:00", "조장": "휴게", "회관": "안내실", "의산A": "휴게", "의산B": "로비", "분": "60"},
    {"No": "11", "시작": "17:00", "종료": "18:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비", "분": "60"},
    {"No": "야1", "시작": "19:00", "종료": "20:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비", "분": "60"},
    {"No": "야2", "시작": "20:00", "종료": "21:00", "조장": "안내실", "회관": "석식", "의산A": "로비", "의산B": "석식", "분": "60"},
]

st.set_page_config(layout="wide")
st.title("🗓️ C조 실시간 근무 상황판")

# --- 2. 실시간 시간 및 근무자 배정 ---
now = datetime.now()
current_hour = now.hour
selected_date = st.sidebar.date_input("날짜 선택", now.date())

# C조 근무일 로직 (3/3 기준 3일 주기)
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    idx = days_diff // 3
    a_rotation = ["이태원", "김태언", "이정석"]
    a_worker = a_rotation[(idx // 2) % 3] 
    others = sorted([m for m in ["김태언", "이태원", "이정석"] if m != a_worker], key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x])
    b_worker, c_worker = (others[1], others[0]) if idx % 2 == 1 else (others[0], others[1])

    # --- 3. 데이터프레임 구성 ---
    df_list = []
    for r in SCHEDULE_DATA:
        df_list.append({
            "시간": f"{r['시작']}-{r['종료']}",
            "조장(황)": r["조장"],
            f"회관({a_worker})": r["회관"],
            f"의산A({b_worker})": r["의산A"],
            f"의산B({c_worker})": r["의산B"],
            "분": r["분"]
        })
    df = pd.DataFrame(df_list)

    # --- 4. 현재 시간 행 강조 및 글자색 스타일링 ---
    def apply_style(row):
        # 시작 시간(HH) 추출하여 현재 시각과 비교
        start_h = int(row['시간'].split(':')[0])
        is_now = (start_h == current_hour)
        
        styles = []
        for col, val in row.items():
            # 기본 스타일: 검은색 글자, 배경 투명
            base = 'color: black; font-weight: bold; '
            if is_now:
                base += 'background-color: #FFF9C4; border-top: 2px solid orange; border-bottom: 2px solid orange; ' # 현재 시간 노란색 강조
            
            # 근무지 명칭별 색상 (빨강, 파랑, 초록, 주황)
            v = str(val)
            if '로비' in v: base += 'color: #D32F2F;'
            elif '순찰' in v: base += 'color: #1976D2;'
            elif '휴게' in v: base += 'color: #388E3C;'
            elif '식' in v: base += 'color: #EF6C00;'
            
            styles.append(base)
        return styles

    # 상단 요약 요약
    st.success(f"📅 {selected_date} C조 명단 | 회관: {a_worker} | 의산A: {b_worker} | 의산B: {c_worker}")

    # 표 출력
    st.table(df.style.apply(apply_style, axis=1))
    
    st.write(f"🕒 현재 시각: {now.strftime('%H:%M')} (노란색 줄이 현재 근무입니다.)")

else:
    st.warning("C조 근무일이 아닙니다.")
