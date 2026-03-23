import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 엑셀 원본 데이터 (조장/회관/의산A/의산B 열 및 시간 완벽 복구) ---
# 엑셀의 'From-To'를 60분 단위로 정렬하되, 의산연의 세부 분할(30분) 내용을 포함
SCHEDULE_DATA = [
    {"시간": "07:00", "조장": "안내실", "회관A": "로비", "의산B": "로비", "의산C": "휴게", "분": "60"},
    {"시간": "08:00", "조장": "안내실", "회관A": "휴게", "의산B": "휴게", "의산C": "로비", "분": "60"},
    {"시간": "09:00", "조장": "안내실", "회관A": "순찰", "의산B": "휴게", "의산C": "로비", "분": "60"},
    {"시간": "10:00", "조장": "휴게", "회관A": "안내실", "의산B": "로비", "의산C": "순찰(30)/휴게(30)", "분": "30,30"},
    {"시간": "11:00", "조장": "로비", "회관A": "안내실", "의산B": "순찰", "의산C": "로비", "분": "60"},
    {"시간": "12:00", "조장": "순찰", "회관A": "휴게", "의산B": "중식", "의산C": "로비", "분": "60"},
    {"시간": "13:00", "조장": "안내실", "회관A": "휴게", "의산B": "휴게(30)/순찰(30)", "의산C": "로비", "분": "30,30"},
    {"시간": "14:00", "조장": "로비", "회관A": "순찰", "의산B": "로비", "의산C": "휴게", "분": "60"},
    {"시간": "15:00", "조장": "안내실", "회관A": "휴게", "의산B": "로비", "의산C": "휴게", "분": "60"},
    {"시간": "16:00", "조장": "휴게", "회관A": "안내실", "의산B": "휴게", "의산C": "로비", "분": "60"},
    {"시간": "17:00", "조장": "안내실", "회관A": "휴게", "의산B": "휴게", "의산C": "로비", "분": "60"},
    {"시간": "18:00", "조장": "안내실", "회관A": "석식", "의산B": "로비", "의산C": "석식", "분": "60"},
    {"시간": "19:00", "조장": "안내실", "회관A": "휴게", "의산B": "휴게", "의산C": "로비", "분": "60"},
    {"시간": "20:00", "조장": "안내실", "회관A": "석식", "의산B": "로비", "의산C": "석식", "분": "60"},
]

st.set_page_config(layout="wide", page_title="C조 근무 상황판")
st.title("🛡️ 성의교정 C조 통합 상황판")

# --- 2. 실시간 시간 및 근무자 자동 계산 ---
now = datetime.now()
current_hour = now.hour
selected_date = st.sidebar.date_input("날짜", now.date())

# C조 근무일 로직 (3/3 기준 3일 주기)
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    idx = days_diff // 3
    a_rotation = ["이태원", "김태언", "이정석"]
    a_worker = a_rotation[(idx // 2) % 3] 
    others = sorted([m for m in ["김태언", "이태원", "이정석"] if m != a_worker], key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x])
    b_worker, c_worker = (others[1], others[0]) if idx % 2 == 1 else (others[0], others[1])

    # 상단 요약 정보 (접속하자마자 보임)
    st.subheader(f"📅 {selected_date} 근무 명단")
    col1, col2, col3 = st.columns(3)
    col1.metric("성의회관(A)", a_worker)
    col2.metric("의산연(B)", b_worker)
    col3.metric("의산연(C)", c_worker)

    # --- 3. 데이터프레임 구성 ---
    df_list = []
    for r in SCHEDULE_DATA:
        df_list.append({
            "시작시간": r["시간"],
            "황재업(조)": r["조장"],
            f"{a_worker}(회)": r["회관A"],
            f"{b_worker}(B)": r["의산B"],
            f"{c_worker}(C)": r["의산C"],
            "소요분": r["분"]
        })
    df = pd.DataFrame(df_list)

    # --- 4. 현재 시간 행 강조 및 스타일링 ---
    def highlight_current_and_work(row):
        # 현재 시간에 해당하는 행 배경색 강조
        row_hour = int(row['시작시간'].split(':')[0])
        is_current = row_hour == current_hour
        
        styles = []
        for col, val in row.items():
            base_style = 'color: black; font-weight: bold;'
            if is_current:
                base_style += 'background-color: #FFF9C4;' # 현재 시간 노란색 강조
            
            # 장소별 글자색
            if '로비' in str(val): base_style += 'color: #D32F2F;'
            elif '순찰' in str(val): base_style += 'color: #1976D2;'
            elif '휴게' in str(val): base_style += 'color: #388E3C;'
            elif '식' in str(val): base_style += 'color: #F57C00;'
            
            styles.append(base_style)
        return styles

    # 테이블 출력 (글자 잘 보이게 스타일 적용)
    st.table(df.style.apply(highlight_current_and_work, axis=1))

    st.write(f"🕒 현재 시각: {now.strftime('%H:%M')} (표에서 노란색으로 강조된 행이 현재 근무입니다.)")

else:
    st.warning("C조 근무일이 아닙니다. 날짜를 확인해 주세요.")
