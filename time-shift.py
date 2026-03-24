import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 기본 설정 ---
st.set_page_config(page_title="C조 근무 시스템", layout="wide")

# 상단 여백 및 기본 디자인 유지
st.markdown("""
    <style>
    .block-container { padding-top: 3.2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; }
    .title-sub { font-size: 14px !important; text-align: center; color: #666; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직: 7시 기준 날짜 설정 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

# ★ 핵심 수정: 07시 이전이면 '어제' 날짜를 target_date로 설정
if now.hour < 7:
    target_date = (now - timedelta(days=1)).date()
else:
    target_date = now.date()

PATTERN_START = datetime(2026, 3, 9).date()

def get_workers_by_date(d):
    diff = (d - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return "황재업", "김태언", "이태원", "이정석"

# 7시 기준으로 계산된 날짜의 근무자 호출
jojang, seonghui, uisanA, uisanB = get_workers_by_date(target_date)

# --- [3] 화면 출력 (최소화) ---
st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
st.markdown(f'<div class="title-sub">기준 날짜: {target_date.strftime("%Y-%m-%d")} (현재: {now.strftime("%H:%M")})</div>', unsafe_allow_html=True)

# 확인용 출력
st.success(f"현재 07시 기준 로직이 적용되었습니다.")
st.write(f"**오늘의 근무자:** {jojang}, {seonghui}, {uisanA}, {uisanB}")

# 데이터 프레임 생성을 위한 기본 데이터 (시간 설정)
time_data = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"],
    # ... (중략) ...
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"]
]
df_rt = pd.DataFrame(time_data, columns=["From", "To", jojang, seonghui, uisanA, uisanB])

st.table(df_rt.head(5)) # 우선 상위 5개만 출력하여 정상 작동 확인
