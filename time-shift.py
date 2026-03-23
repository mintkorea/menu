import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. 기본 설정 및 기기 인식 ---
DEVICE_MAP = {"S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원"}
PATTERN_START_DATE = datetime(2026, 3, 9).date()

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="wide")

# 한국 표준시(KST) 기준 시간 설정
now_kst = datetime.now(timezone(timedelta(hours=9)))
today_val = now_kst.date()
current_hour = now_kst.hour
current_min = now_kst.minute

# --- 2. 엑셀 이미지 속 진짜 실무 데이터 (07시~07시) ---
def get_official_schedule():
    data = [
        {"From": "07:00", "To": "08:00", "성희_조장": "안내실", "성희_대원": "로비", "의산_A": "로비", "의산_B": "휴게"},
        {"From": "08:00", "To": "09:00", "성희_조장": "안내실", "성희_대원": "휴게", "의산_A": "휴게", "의산_B": "로비"},
        {"From": "09:00", "To": "10:00", "성희_조장": "안내실", "성희_대원": "순찰", "의산_A": "휴게", "의산_B": "로비"},
        {"From": "10:00", "To": "11:00", "성희_조장": "휴게", "성희_대원": "안내실", "의산_A": "로비", "의산_B": "순찰/휴게"},
        {"From": "11:00", "To": "12:00", "성희_조장": "안내실", "성희_대원": "중식", "의산_A": "로비", "의산_B": "중식"},
        {"From": "12:00", "To": "13:00", "성희_조장": "중식", "성희_대원": "안내실", "의산_A": "중식", "의산_B": "로비"},
        {"From": "13:00", "To": "14:00", "성희_조장": "안내실", "성희_대원": "휴게", "의산_A": "순찰/휴게", "의산_B": "로비"},
        {"From": "14:00", "To": "15:00", "성희_조장": "순찰", "성희_대원": "안내실", "의산_A": "로비", "의산_B": "휴게"},
        {"From": "15:00", "To": "16:00", "성희_조장": "안내실", "성희_대원": "휴게", "의산_A": "로비", "의산_B": "휴게"},
        {"From": "16:00", "To": "17:00", "성희_조장": "휴게", "성희_대원": "안내실", "의산_A": "휴게", "의산_B": "로비"},
        {"From": "17:00", "To": "18:00", "성희_조장": "안내실", "성희_대원": "휴게", "의산_A": "휴게", "의산_B": "로비"},
        {"From": "18:00", "To": "19:00", "성희_조장": "안내실", "성희_대원": "석식", "의산_A": "로비", "의산_B": "석식"},
        {"From": "19:00", "To": "20:00", "성희_조장": "안내실", "성희_대원": "안내실", "의산_A": "석식", "의산_B": "로비"},
        {"From": "20:00", "To": "21:00", "성희_조장": "석식", "성희_대원": "안내실", "의산_A": "로비", "의산_B": "휴게"},
        {"From": "21:00", "To": "22:00", "성희_조장": "안내실", "성희_대원": "순찰", "의산_A": "로비", "의산_B": "휴게"},
        {"From": "22:00", "To": "23:00", "성희_조장": "순찰", "성희_대원": "휴게", "의산_A": "순찰", "의산_B": "로비"},
        {"From": "23:00", "To": "01:40", "성희_조장": "안내실", "성희_대원": "휴게", "의산_A": "휴게", "의산_B": "로비"},
        {"From": "01:40", "To": "05:00", "성희_조장": "휴게", "성희_대원": "안내실", "의산_A": "로비", "의산_B": "휴게"},
        {"From": "05:00", "To": "06:00", "성희_조장": "안내실", "성희_대원": "순찰", "의산_A": "로비", "의산_B": "순찰"},
        {"From": "06:00", "To": "07:00", "성희_조장": "안내실", "성희_대원": "안내실", "의산_A": "휴게", "의산_B": "로비"},
    ]
    return pd.DataFrame(data)

# --- 3. 사용자 및 현재 위치 계산 ---
ua = st_javascript("navigator.userAgent")
detected_name = "안 함"
if ua and ua != 0:
    for model, name in DEVICE_MAP.items():
        if model in str(ua).upper(): detected_name = name; break

with st.sidebar:
    st.header("👤 근무자 확인")
    user_name = st.selectbox("본인 성함", ["안 함", "황재업", "이정석", "김태언", "이태원"], index=["안 함", "황재업", "이정석", "김태언", "이태원"].index(detected_name))

st.markdown(f"### 🏛️ 성의교정 C조 당직 실무 안내 (현재: {now_kst.strftime('%H:%M')})")

# 4. [가장 중요한 강조 로직] 실시간 행 강조 함수
def apply_highlight(df):
    now_total = current_hour * 60 + current_min
    if now_total < 7 * 60: now_total += 24 * 60 # 07시 이전은 익일 취급

    def make_style(row):
        f_h, f_m = map(int, row['From'].split(':'))
        t_h, t_m = map(int, row['To'].split(':'))
        start, end = f_h * 60 + f_m, t_h * 60 + t_m
        if end < start: end += 24 * 60
        
        # 현재 시간이 From과 To 사이에 있으면 노란색 배경 적용
        if start <= now_total < end:
            return ['background-color: #FFF9C4; color: black; font-weight: bold'] * len(row)
        return [''] * len(row)
    
    return df.style.apply(make_style, axis=1)

# 5. 메인 화면 표시
diff_days = (today_val - PATTERN_START_DATE).days
if diff_days % 3 == 0:
    df_sched = get_official_schedule()
    
    # 강조가 적용된 데이터프레임 출력
    st.dataframe(apply_highlight(df_sched), use_container_width=True, hide_index=True)
    
    # 보직 확인 (선택 사항)
    if user_name != "안 함":
        st.success(f"🚩 **{user_name}**님, 노란색으로 표시된 시간대의 위치를 확인하세요!")
else:
    st.warning("오늘은 C조 비번입니다.")
