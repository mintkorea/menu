import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

# --- 1. 한국 표준시(KST) 설정 (가장 중요한 수정 사항) ---
def get_now_kst():
    # 서버의 위치와 상관없이 한국 시간(UTC+9)을 강제로 가져옵니다.
    return datetime.now(timezone(timedelta(hours=9)))

# --- 2. 기준 설정 (C조 근무 패턴 시작일) ---
# 사용자님의 엑셀 데이터를 바탕으로 설정된 기준일입니다.
PATTERN_START_DATE = datetime(2026, 3, 24).date()

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

# --- 3. 근무자 계산 로직 (새벽 첫 소스 기준) ---
def get_shift_workers(date):
    diff_days = (date - PATTERN_START_DATE).days
    # 3일 주기 근무 체크
    if diff_days % 3 == 0:
        shift_num = diff_days // 3
        cycle = shift_num % 6
        # 엑셀에 명시된 C조 순환 파트너십 로직
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

# 현재 한국 시간 정보 가져오기
now_kst = get_now_kst()
today_val = now_kst.date()

# --- 4. 메인 화면 구현 ---
st.title("📍 실시간 근무 상황판")
st.write(f"🕒 현재 시각(KST): **{now_kst.strftime('%Y-%m-%d %H:%M')}**")

# 오늘 근무 여부 확인
workers = get_shift_workers(today_val)

if workers:
    st.success(f"✅ 오늘({today_val.strftime('%m/%d')})은 **C조 근무일**입니다.")
    # 근무자 명단 가로 배치
    cols = st.columns(4)
    for i, (pos, name) in enumerate(workers):
        with cols[i]:
            st.metric(label=pos, value=name)
else:
    st.warning(f"😴 오늘({today_val.strftime('%m/%d')})은 **C조 비번/휴무**입니다.")
    # 다음 근무일 계산
    days_diff = (today_val - PATTERN_START_DATE).days
    wait = 3 - (days_diff % 3) if days_diff % 3 > 0 else abs(days_diff % 3)
    next_work = today_val + timedelta(days=wait)
    st.info(f"📅 나의 다음 근무일: **{next_work.strftime('%m/%d')}** ({int(wait)}일 남음)")

st.divider()

# --- 5. 주간 근무 편성표 (조회 기능) ---
st.subheader("📅 주간 근무 일정 확인")
week_list = []
# 오늘 기준 전후 일정 표시
for i in range(-2, 10):
    target_d = today_val + timedelta(days=i)
    w_data = get_shift_workers(target_d)
    if w_data:
        row = {"날짜": target_d.strftime('%m/%d') + f"({['월','화','수','목','금','토','일'][target_d.weekday()]})"}
        for p, n in w_data:
            row[p] = n
        week_list.append(row)

if week_list:
    st.table(pd.DataFrame(week_list))
