import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

# --- 1. 한국 표준시(KST) 설정 ---
# 서버 시간에 상관없이 한국 시간을 정확히 인식하게 합니다.
def get_now_kst():
    return datetime.now(timezone(timedelta(hours=9)))

# --- 2. 초기 설정 및 기준일 ---
# 3/24(화) C조 근무 기준 (엑셀 데이터 기반)
PATTERN_START_DATE = datetime(2026, 3, 24).date()

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

# --- 3. 근무자 로직 (새벽 초기 버전) ---
def get_shift_workers(date):
    diff_days = (date - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        shift_num = diff_days // 3
        cycle = shift_num % 6
        # 초기 설정된 성함 매칭 데이터
        names = {
            0: ["황재업", "이태원", "이정석", "김태언"],
            1: ["황재업", "김태언", "이태원", "이정석"],
            2: ["황재업", "김태언", "이정석", "이태원"],
            3: ["황재업", "이정석", "김태언", "이태원"],
            4: ["황재업", "이정석", "이태원", "김태언"],
            5: ["황재업", "이태원", "김태언", "이정석"]
        }
        res = names[cycle]
        return [("조장", res[0]), ("성희관", res[1]), ("의산연(A)", res[2]), ("의산연(B)", res[3])]
    return None

now_kst = get_now_kst()
today_val = now_kst.date()

# --- 4. 메인 화면 ---
st.title("📍 실시간 근무 및 안내")
st.write(f"🕒 현재 시각: **{now_kst.strftime('%Y-%m-%d %H:%M')}**")

# 오늘 근무 상태
workers = get_shift_workers(today_val)

if workers:
    st.success(f"✅ 오늘({today_val.strftime('%m/%d')})은 **C조 근무일**입니다.")
    cols = st.columns(4)
    for i, (pos, name) in enumerate(workers):
        with cols[i]:
            st.metric(pos, name)
else:
    st.warning(f"😴 오늘({today_val.strftime('%m/%d')})은 **비번/휴무**입니다.")
    # 다음 근무일 안내
    days_diff = (today_val - PATTERN_START_DATE).days
    wait = 3 - (days_diff % 3) if days_diff % 3 > 0 else abs(days_diff % 3)
    st.info(f"📅 다음 근무일: **{(today_val + timedelta(days=wait)).strftime('%m/%d')}**")

st.divider()

# --- 5. 주간 근무 편성표 ---
st.subheader("🗓️ 주간 근무 편성표")
week_list = []
for i in range(-2, 10):
    d = today_val + timedelta(days=i)
    w = get_shift_workers(d)
    if w:
        row = {"날짜": d.strftime('%m/%d(%a)')}
        for p, n in w: row[p] = n
        week_list.append(row)

if week_list:
    st.table(pd.DataFrame(week_list))
