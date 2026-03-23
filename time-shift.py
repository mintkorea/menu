import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

# 1. 한국 표준시(KST) 설정 (오전 5시에도 날짜 정확히 인식)
def get_now_kst():
    return datetime.now(timezone(timedelta(hours=9)))

# 2. 엑셀 기준 데이터 설정 (3/24 화요일 C조 근무 기준)
PATTERN_START_DATE = datetime(2026, 3, 24).date()
TIME_TABLE_IMAGE = "KakaoTalk_20260324_052234899.png" # 어제 말씀하신 상세 시간표 이미지

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

# 근무자 순환 로직
def get_shift_workers(date):
    diff_days = (date - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
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

# --- 메인 화면 ---
st.header("📍 실시간 근무 상황판")
st.caption(f"🕒 현재 시각(KST): {now_kst.strftime('%Y-%m-%d %H:%M')}")

# 오늘 근무자 요약 (상단)
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

# 3. [어제 요청하신 핵심] 상세 당직 근무 편성표 이미지 고정
st.subheader("📋 상세 당직 근무 스케줄 (세로 버전)")
if os.path.exists(TIME_TABLE_IMAGE):
    # 이미지가 있으면 크게 표시
    st.image(TIME_TABLE_IMAGE, use_container_width=True)
else:
    # 이미지가 없을 때만 뜨는 경고 (앱 멈춤 방지)
    st.error("❗ 시간표 이미지를 찾을 수 없습니다. 파일명을 확인해 주세요.")

st.divider()

# 4. 주간 날짜별 편성표 (접었다 펴기 가능)
with st.expander("🗓️ 주간 날짜별 근무자 확인 (전체)") :
    week_list = []
    for i in range(-2, 10):
        d = today_val + timedelta(days=i)
        w = get_shift_workers(d)
        if w:
            row = {"날짜": d.strftime('%m/%d') + f"({['월','화','수','목','금','토','일'][d.weekday()]})"}
            for p, n in w: row[p] = n
            week_list.append(row)
    st.table(pd.DataFrame(week_list))
