import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

# --- 1. 한국 표준시(KST) 강제 설정 (서버 시간 무시) ---
def get_now_kst():
    return datetime.now(timezone(timedelta(hours=9)))

# --- 2. 기본 설정 ---
# 엑셀 기준: 3/24(화) -> 황재업(조), 이태원(회), 이정석(A), 김태언(B)
PATTERN_START_DATE = datetime(2026, 3, 24).date()
TIME_TABLE_IMAGE = "KakaoTalk_20260324_052234899.png" 

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="wide") # 모바일 가독성을 위해 넓게 설정

def get_shift_workers(date):
    diff_days = (date - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        shift_num = diff_days // 3
        cycle = shift_num % 6
        # 엑셀 기반 조별 순환 로직
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

# --- 3. 실시간 상황판 ---
st.header("📍 실시간 근무 상황판")
st.write(f"🕒 현재 기준: **{now_kst.strftime('%Y-%m-%d %H:%M')}**")

workers = get_shift_workers(today_val)

if workers:
    st.success(f"✅ 오늘({today_val.strftime('%m/%d')})은 **C조 근무일**입니다.")
    cols = st.columns(4)
    for i, (pos, name) in enumerate(workers):
        with cols[i]:
            st.metric(label=pos, value=name)
else:
    st.warning(f"😴 오늘({today_val.strftime('%m/%d')})은 **비번/휴무**입니다.")
    # 다음 근무일 계산 로직
    days_diff = (today_val - PATTERN_START_DATE).days
    wait = 3 - (days_diff % 3) if days_diff % 3 > 0 else abs(days_diff % 3)
    st.info(f"📅 다음 근무일: **{(today_val + timedelta(days=wait)).strftime('%m/%d')}**")

st.divider()

# --- 4. 상세 당직 근무 시간표 (이미지 표출 부분) ---
st.subheader("📋 상세 근무 시간표 (세로 버전)")

# 파일 경로 확인 로그 (디버깅용 - 실제 운영시 삭제 가능)
if not os.path.exists(TIME_TABLE_IMAGE):
    st.error("❗ 시간표 이미지 파일을 찾을 수 없습니다.")
    st.info("파일명을 `KakaoTalk_20260324_052234899.png`로 수정하여 업로드하거나, 아래 텍스트 시간표를 확인하세요.")
    
    # [백업] 이미지 안 뜰 때 보여줄 텍스트 시간표
    with st.expander("📍 텍스트 버전 시간표 보기"):
        st.write("**08:00~18:00 (주간)**: 안내실/로비/휴게 순환")
        st.write("**18:00~08:00 (야간)**: 순찰/석식/대기 순환")
else:
    # 이미지가 있으면 표시 (가장자리 여백 제거)
    st.image(TIME_TABLE_IMAGE, use_container_width=True)

st.divider()

# --- 5. 메뉴 이동 (에러 방지용) ---
with st.sidebar:
    st.header("⚙️ 메뉴")
    st.radio("이동", ["실시간 상황판", "연차 신청", "근무 편성표(조회)"])
