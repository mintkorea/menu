import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 엑셀 및 사용자 수정사항 100% 반영 데이터 ---
# 중식: 11시(조장/당직B), 12시(회관/당직A) -> 전원 식사 완료
# 순찰: 회관(09시, 14시), 의산연(10시 B순찰, 13시 A순찰)
SCHEDULE_DATA = [
    {"No": "1", "시작": "07:00", "종료": "08:00", "조장": "안내실", "회관": "로비", "의산A": "로비", "의산B": "휴게", "분": "60"},
    {"No": "2", "시작": "08:00", "종료": "09:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비", "분": "60"},
    {"No": "3", "시작": "09:00", "종료": "10:00", "조장": "안내실", "회관": "순찰", "의산A": "휴게", "의산B": "로비", "분": "60"}, # 회관 순찰
    {"No": "4", "시작": "10:00", "종료": "11:00", "조장": "휴게", "회관": "안내실", "의산A": "로비", "의산B": "순찰(30)/휴게(30)", "분": "30,30"}, # 의산B 순찰
    {"No": "5", "시작": "11:00", "종료": "12:00", "조장": "중식", "회관": "안내실", "의산A": "순찰", "의산B": "중식", "분": "60"}, # 조장/의산B 중식
    {"No": "6", "시작": "12:00", "종료": "13:00", "조장": "순찰", "회관": "중식", "의산A": "중식", "의산B": "로비", "분": "60"}, # 회관/의산A 중식
    {"No": "7", "시작": "13:00", "종료": "14:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게(30)/순찰(30)", "의산B": "로비", "분": "30,30"}, # 의산A 순찰
    {"No": "8", "시작": "14:00", "종료": "15:00", "조장": "로비", "회관": "순찰", "의산A": "휴게", "의산B": "안내실", "분": "60"}, # 회관 순찰
    {"No": "9", "시작": "15:00", "종료": "16:00", "조장": "안내실", "회관": "휴게", "의산A": "로비", "의산B": "휴게", "분": "60"},
    {"No": "10", "시작": "16:00", "종료": "17:00", "조장": "휴게", "회관": "안내실", "의산A": "휴게", "의산B": "로비", "분": "60"},
    {"No": "11", "시작": "17:00", "종료": "18:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비", "분": "60"},
    {"No": "야1", "시작": "19:00", "종료": "20:00", "조장": "안내실", "회관": "휴게", "의산A": "휴게", "의산B": "로비", "분": "60"},
    {"No": "야2", "시작": "20:00", "종료": "21:00", "조장": "안내실", "회관": "석식", "의산A": "로비", "의산B": "석식", "분": "60"},
]

st.set_page_config(layout="wide", page_title="C조 통합 상황판")
st.title("🛡️ 성의교정 C조 실시간 상황판")

# --- 2. 실시간 시간 및 근무자 자동 매칭 ---
now = datetime.now()
current_hour = now.hour
selected_date = st.sidebar.date_input("날짜 선택", now.date())

# C조 근무일 계산 (3/3 기준 3일 로테이션)
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
            "시간범위": f"{r['시작']}-{r['종료']}",
            "조장(황)": r["조장"],
            f"회관({a_worker})": r["회관"],
            f"의산A({b_worker})": r["의산A"],
            f"의산B({c_worker})": r["의산B"],
            "비고(분)": r["분"]
        })
    df = pd.DataFrame(df_list)

    # --- 4. 현재 시간 행 강조 및 명칭별 색상 스타일 ---
    def highlight_logic(row):
        start_h = int(row['시간범위'].split(':')[0])
        is_current = (start_h == current_hour)
        
        styles = []
        for col, val in row.items():
            base = 'color: black; font-weight: bold; '
            if is_current:
                base += 'background-color: #FFF9C4; border: 2.5px solid orange; ' # 현재 시각 행 강조
            
            # 근무지/업무별 텍스트 색상
            v = str(val)
            if '로비' in v: base += 'color: #D32F2F;'
            elif '순찰' in v: base += 'color: #1976D2;'
            elif '휴게' in v: base += 'color: #388E3C;'
            elif '식' in v: base += 'color: #EF6C00;'
            elif '안내실' in v: base += 'color: #008B8B;'
            
            styles.append(base)
        return styles

    st.success(f"📅 {selected_date} | 현재 {now.strftime('%H:%M')} 근무 상황 (노란색 강조)")
    st.table(df.style.apply(highlight_logic, axis=1))

else:
    st.warning("C조 근무일이 아닙니다. 날짜를 확인해주세요.")
