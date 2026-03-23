import streamlit as st
import pandas as pd
from datetime import datetime, time

# --- 1. 엑셀 원본 데이터 (CSV 파일 내용과 1:1 매칭) ---
# 중식: 12:00~13:00 (당직A) / 석식: 18:00~19:00 및 20:00~21:00 반영
# 근무지 명칭: 안내실, 로비, 휴게, 순찰, 중식, 석식 (엑셀 명칭 그대로)
RAW_DATA = [
    {"No": "1", "시작": "07:00", "종료": "08:00", "조장": "안내실", "회관": "로비", "당직A": "로비", "당직B": "휴게", "분": "60"},
    {"No": "2", "시작": "08:00", "종료": "09:00", "조장": "안내실", "회관": "휴게", "당직A": "휴게", "당직B": "로비", "분": "60"},
    {"No": "3", "시작": "09:00", "종료": "10:00", "조장": "안내실", "회관": "순찰", "당직A": "휴게", "당직B": "로비", "분": "60"},
    {"No": "4", "시작": "10:00", "종료": "11:00", "조장": "휴게", "회관": "안내실", "당직A": "로비", "당직B": "순찰(30)/휴게(30)", "분": "30,30"},
    {"No": "5", "시작": "11:00", "종료": "12:00", "조장": "로비", "회관": "안내실", "당직A": "순찰", "당직B": "로비", "분": "60"},
    {"No": "6", "시작": "12:00", "종료": "13:00", "조장": "순찰", "회관": "휴게", "당직A": "중식", "당직B": "로비", "분": "60"},
    {"No": "7", "시작": "13:00", "종료": "14:00", "조장": "안내실", "회관": "휴게", "당직A": "휴게(30)/순찰(30)", "당직B": "로비", "분": "30,30"},
    {"No": "8", "시작": "14:00", "종료": "15:00", "조장": "로비", "회관": "순찰", "당직A": "로비", "당직B": "휴게", "분": "60"},
    {"No": "9", "시작": "15:00", "종료": "16:00", "조장": "안내실", "회관": "휴게", "당직A": "로비", "당직B": "휴게", "분": "60"},
    {"No": "10", "시작": "16:00", "종료": "17:00", "조장": "휴게", "회관": "안내실", "당직A": "휴게", "당직B": "로비", "분": "60"},
    {"No": "11", "시작": "17:00", "종료": "18:00", "조장": "안내실", "회관": "휴게", "당직A": "휴게", "당직B": "로비", "분": "60"},
    {"No": "야1", "시작": "19:00", "종료": "20:00", "조장": "안내실", "회관": "휴게", "당직A": "휴게", "당직B": "로비", "분": "60"},
    {"No": "야2", "시작": "20:00", "종료": "21:00", "조장": "안내실", "회관": "석식", "당직A": "로비", "당직B": "석식", "분": "60"},
]

st.set_page_config(layout="wide", page_title="성의교정 근무 상황판")
st.title("🗓️ C조 실시간 근무 상황판")

# --- 2. 실시간 시간 및 근무자 계산 ---
now = datetime.now()
current_time_str = now.strftime("%H:%M")
current_hour = now.hour
selected_date = st.sidebar.date_input("근무 날짜", now.date())

# C조 근무일 로직 (3/3 기준 3일 주기)
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    idx = days_diff // 3
    a_rotation = ["이태원", "김태언", "이정석"]
    a_worker = a_rotation[(idx // 2) % 3] 
    others = sorted([m for m in ["김태언", "이태원", "이정석"] if m != a_worker], key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x])
    b_worker, c_worker = (others[1], others[0]) if idx % 2 == 1 else (others[0], others[1])

    # 상단 현재 상황 대시보드
    st.subheader(f"🕒 현재 시각: {current_time_str}")
    
    # --- 3. 데이터프레임 구성 ---
    df_list = []
    for r in RAW_DATA:
        df_list.append({
            "시간": f"{r['시작']}-{r['종료']}",
            "황재업(조)": r["조장"],
            f"{a_worker}(회)": r["회관"],
            f"{b_worker}(B)": r["당직A"],
            f"{c_worker}(C)": r["당직B"],
            "소요(분)": r["분"]
        })
    df = pd.DataFrame(df_list)

    # --- 4. 현재 시간 행 강조 및 명칭별 색상 스타일링 ---
    def highlight_row(row):
        # 현재 시간(시)에 해당하는 행 배경색 노란색 강조
        row_start_hour = int(row['시간'].split(':')[0])
        is_now = row_start_hour == current_hour
        
        styles = []
        for col, val in row.items():
            # 기본 설정: 검은색 글자, 흰색 배경
            style = 'color: black; font-weight: bold; background-color: white;'
            
            # 1. 현재 시간 행 전체 노란색 배경 강조
            if is_now:
                style = 'color: black; font-weight: bold; background-color: #FFFFE0; border: 2px solid orange;'
            
            # 2. 근무지 명칭별 글자색 강조 (엑셀 명칭 기준)
            val_s = str(val)
            if '로비' in val_s: style += 'color: red;'
            elif '순찰' in val_s: style += 'color: blue;'
            elif '휴게' in val_s: style += 'color: green;'
            elif '중식' in val_s or '석식' in val_s: style += 'color: #FF8C00;' # 진한 주황
            elif '안내실' in val_s: style += 'color: #008B8B;' # 다크 시안
            
            styles.append(style)
        return styles

    # 테이블 표출
    st.table(df.style.apply(highlight_row, axis=1))

    st.markdown(f"""
    **💡 실시간 안내**
    - 현재 **노란색**으로 표시된 줄이 지금 시간대 근무 상황입니다.
    - **중식시간**: 12:00~13:00에 **{b_worker}(B)** 근무자의 '중식'이 정확히 반영되었습니다.
    - **명칭 준수**: 엑셀에 명시된 모든 근무지 명칭을 그대로 사용하였습니다.
    """)

else:
    st.warning("C조 근무일이 아닙니다. 날짜를 변경해 확인해 보세요.")
