
import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 기본 설정 ---
st.set_page_config(page_title="C조 근무 시스템", layout="wide")

# --- [2] 07시 기준 날짜 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

# 07시 이전이면 '어제' 날짜를 기준으로 근무조 결정
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
        if ci == 0: return "황재업", "이태원", "이정석", "김태언"
        elif ci == 1: return "황재업", "이정석", "김태언", "이태원"
        else: return "황재업", "김태언", "이태원", "이정석"
    return "황재업", "이태원", "이정석", "김태언"

jojang, seonghui, uisanA, uisanB = get_workers_by_date(target_date)

# --- [3] 화면 출력 ---
st.title("C조 실시간 근무 현황 (진단용)")
st.write(f"**기준 날짜:** {target_date} | **현재 시간:** {now.strftime('%H:%M')}")
st.write(f"**오늘의 근무자:** {jojang}, {seonghui}, {uisanA}, {uisanB}")

time_data = [
    ["23:00", "01:40", "안내실", "휴게", "휴게", "로비"],
    ["01:40", "02:00", "안내실", "안내실", "로비", "로비"],
    ["02:00", "05:00", "휴게", "안내실", "로비", "휴게"],
    ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"],
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"]
]
df_rt = pd.DataFrame(time_data, columns=["From", "To", jojang, seonghui, uisanA, uisanB])
st.table(df_rt)
