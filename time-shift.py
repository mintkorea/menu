import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

# --- 1. 한국 표준시(KST) 설정 ---
def get_now_kst():
    return datetime.now(timezone(timedelta(hours=9)))

# --- 2. 기본 설정 ---
PATTERN_START_DATE = datetime(2026, 3, 24).date()
# 이미지 파일 경로 (사용자님의 환경에 맞춰 파일명을 확인하세요)
TIME_TABLE_IMAGE = "KakaoTalk_20260324_052234899.png" 

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

# --- 근무 계산 로직 ---
def get_shift_workers(date):
    diff_days = (date - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        # 3/24 기준 조별 순번 (엑셀 기준)
        shift_num = diff_days // 3
        cycle = shift_num % 6
        if cycle == 0:   res = ["황재업", "이태원", "이정석", "김태언"]
        elif cycle == 1: res = ["황재업", "김태언", "이태원", "이정석"]
        elif cycle == 2: res = ["황재업", "김태언", "이정석", "이태원"]
        elif cycle == 3: res = ["황재업", "이정석", "김태언", "이태원"]
        elif cycle == 4: res = ["황재업", "이정석", "이태원", "김태언"]
        else:            res = ["황재업", "이태원", "김태언", "이정석"]
        return [("조장", res[0]), ("성희관", res[1]), ("의산연(A)", res[2]), ("의산연(B)", res[3])]
    return None

now_kst = get_now_kst()
today_val = now_kst.date()

# --- 3. 실시간 상황판 (메인 화면) ---
st.markdown("### 📍 실시간 근무 및 안내")
st.caption(f"🕒 현재 시각: {now_kst.strftime('%Y-%m-%d %H:%M')}")

# 오늘 근무 여부 표시 (상단 요약)
workers = get_shift_workers(today_val)
if workers:
    st.success(f"✅ 오늘({today_val.strftime('%m/%d')})은 **C조 근무일**입니다.")
    cols = st.columns(4)
    for i, (pos, name) in enumerate(workers):
        with cols[i]: st.metric(pos, name)
else:
    st.warning(f"😴 오늘({today_val.strftime('%m/%d')})은 **비번/휴무**입니다.")
    days_diff = (today_val - PATTERN_START_DATE).days
    wait = 3 - (days_diff % 3) if days_diff % 3 > 0 else abs(days_diff % 3)
    st.info(f"📅 다음 근무: **{(today_val + timedelta(days=wait)).strftime('%m/%d')}**")

st.divider()

# --- 4. [핵심] 상세 당직 근무 시간표 이미지 띄우기 ---
st.markdown("#### 📋 상세 당직 근무 스케줄")
st.write("요일과 관계없이 고정된 시간별 근무 위치입니다.")

# 이미지가 해당 경로에 있는지 확인 후 표시
if os.path.exists(TIME_TABLE_IMAGE):
    st.image(TIME_TABLE_IMAGE, caption="성의교정 당직 근무편성표(C조)", use_column_width=True)
else:
    # 이미지가 없을 경우를 대비한 텍스트 안내 (에러 방지)
    st.error(f"시간표 이미지 파일({TIME_TABLE_IMAGE})을 찾을 수 없습니다. 파일명을 확인해 주세요.")

st.divider()

# --- 5. 주간 간이 편성표 (날짜 확인용) ---
with st.expander("🗓️ 주간 날짜별 근무자 확인"):
    week_data = []
    for i in range(-1, 8):
        d = today_val + timedelta(days=i)
        w = get_shift_workers(d)
        if w:
            row = {"날짜": d.strftime('%m/%d') + f"({['월','화','수','목','금','토','일'][d.weekday()]})"}
            for p, n in w: row[p] = n
            week_data.append(row)
    st.table(pd.DataFrame(week_data))
