import streamlit as st
import pandas as pd
from datetime import datetime

# --- 1. 정밀 대조 데이터 (수정본 100% 반영) ---
# 주간: image_3efde2 외 / 야간: image_49152b 기준 데이터
SCHEDULE_DATA = [
    {"시간": "07:00", "황재업(조)": "안내실", "이태원(회)": "로비", "김태언(A)": "휴게", "이정석(B)": "로비"},
    {"시간": "08:00", "황재업(조)": "안내실", "이태원(회)": "휴게", "김태언(A)": "로비", "이정석(B)": "휴게"},
    {"시간": "09:00", "황재업(조)": "안내실", "이태원(회)": "순찰", "김태언(A)": "로비", "이정석(B)": "휴게"},
    {"시간": "10:00", "황재업(조)": "휴게", "이태원(회)": "안내실", "김태언(A)": "순찰/휴", "이정석(B)": "로비"},
    {"시간": "11:00", "황재업(조)": "안내실", "이태원(회)": "중식", "김태언(A)": "중식", "이정석(B)": "로비"},
    {"시간": "12:00", "황재업(조)": "중식", "이태원(회)": "안내실", "김태언(A)": "로비", "이정석(B)": "중식"},
    {"시간": "13:00", "황재업(조)": "안내실", "이태원(회)": "휴게", "김태언(A)": "로비", "이정석(B)": "휴/순"},
    {"시간": "14:00", "황재업(조)": "순찰", "이태원(회)": "안내실", "김태언(A)": "휴게", "이정석(B)": "로비"},
    {"시간": "15:00", "황재업(조)": "안내실", "이태원(회)": "휴게", "김태언(A)": "휴게", "이정석(B)": "로비"},
    {"시간": "16:00", "황재업(조)": "휴게", "이태원(회)": "안내실", "김태언(A)": "로비", "이정석(B)": "휴게"},
    {"시간": "17:00", "황재업(조)": "안내실", "이태원(회)": "휴게", "김태언(A)": "로비", "이정석(B)": "휴게"},
    {"시간": "18:00", "황재업(조)": "안내실", "이태원(회)": "휴게", "김태언(A)": "휴게", "이정석(B)": "로비"},
    {"시간": "19:00", "황재업(조)": "안내실", "이태원(회)": "석식", "김태언(A)": "로비", "이정석(B)": "석식"},
    {"시간": "20:00", "황재업(조)": "안내실", "이태원(회)": "안내실", "김태언(A)": "석식", "이정석(B)": "로비"},
    {"시간": "21:00", "황재업(조)": "석식", "이태원(회)": "안내실", "김태언(A)": "로비", "이정석(B)": "휴게"},
    {"시간": "22:00", "황재업(조)": "안내실", "이태원(회)": "순찰", "김태언(A)": "로비", "이정석(B)": "휴게"},
    {"시간": "23:00", "황재업(조)": "순찰", "이태원(회)": "취침", "김태언(A)": "순찰", "이정석(B)": "로비"},
    {"시간": "00:00", "황재업(조)": "안내실", "이태원(회)": "취침", "김태언(A)": "취침", "이정석(B)": "로비"},
    {"시간": "01:00", "황재업(조)": "안내실", "이태원(회)": "취침", "김태언(A)": "취침", "이정석(B)": "로비"},
    {"시간": "02:00", "황재업(조)": "안내실", "이태원(회)": "취침", "김태언(A)": "취침", "이정석(B)": "로비"},
    {"시간": "03:00", "황재업(조)": "취침", "이태원(회)": "회관근무", "김태언(A)": "로비", "이정석(B)": "취침"},
    {"시간": "04:00", "황재업(조)": "취침", "이태원(회)": "회관근무", "김태언(A)": "로비", "이정석(B)": "취침"},
    {"시간": "05:00", "황재업(조)": "취침", "이태원(회)": "회관근무", "김태언(A)": "로비", "이정석(B)": "취침"},
    {"시간": "06:00", "황재업(조)": "안내실", "이태원(회)": "회관근무", "김태언(A)": "로비", "이정석(B)": "순찰"},
]

st.set_page_config(layout="centered")

# --- 2. 폰트 최소화 및 모바일 가로 너비 고정 CSS ---
st.markdown("""
    <style>
    /* 전체 폰트 크기 극소화 및 간격 제거 */
    html, body, [data-testid="stTable"] { 
        font-size: 9px !important; 
        font-family: 'Malgun Gothic', sans-serif;
    }
    /* 표 레이아웃 강제 고정 */
    table { 
        width: 100% !important; 
        table-layout: fixed !important; 
        border-collapse: collapse !important;
    }
    th, td { 
        padding: 2px 1px !important; 
        text-align: center !important; 
        border: 1px solid #eee !important;
        white-space: nowrap !important;
        overflow: hidden !important;
    }
    /* 헤더 폰트 강조 */
    th { background-color: #f8f9fa; font-weight: bold; }
    /* 현재 시간 강조 행 */
    .current-row { background-color: #FFF9C4 !important; border: 1.5px solid red !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 실시간 연동 헤더 ---
now = datetime.now()
current_hour = now.hour
st.subheader(f"📅 {now.strftime('%m/%d')} C조 실시간 현황")

# 상단 요약 바 (현재 인원 실시간 연동)
cur = next((item for item in SCHEDULE_DATA if int(item["시간"].split(':')[0]) == current_hour), None)
if cur:
    st.info(f"📍 **현재({current_hour}시):** 조-{cur['황재업(조)']} / 회-{cur['이태원(회)']} / A-{cur['김태언(A)']} / B-{cur['이정석(B)']}")

# --- 4. 데이터프레임 스타일 적용 및 출력 ---
df = pd.DataFrame(SCHEDULE_DATA)

def apply_mobile_style(row):
    is_now = int(row['시간'].split(':')[0]) == current_hour
    styles = []
    for col, val in row.items():
        base = ''
        if is_now:
            base = 'background-color: #FFF9C4; color: black; font-weight: bold; border-top: 1.5px solid red; border-bottom: 1.5px solid red;'
        else:
            v = str(val)
            if '로비' in v: base = 'color: #D32F2F;'
            elif '순찰' in v: base = 'color: #1976D2;'
            elif '취침' in v or '휴' in v: base = 'color: #757575;'
            elif '식' in v: base = 'color: #F57C00;'
            else: base = 'color: #212121;'
        styles.append(base)
    return styles

st.table(df.style.apply(apply_mobile_style, axis=1))
