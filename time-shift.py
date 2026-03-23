import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone

# 1. 한국 표준시(KST) 설정
def get_now_kst():
    return datetime.now(timezone(timedelta(hours=9)))

# 2. 기준 설정 (3/24 화요일 C조 근무 시작 기준)
PATTERN_START_DATE = datetime(2026, 3, 24).date()

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="wide")

# --- 당직 상세 스케줄 데이터 (주신 이미지 내용 그대로 구현) ---
def get_detail_schedule():
    # 주간(07:00~17:00) / 야간(17:00~07:00) 상세 로직
    # 표의 내용을 리스트화하여 모바일에서 보기 좋게 구성
    data = [
        ["07:00~08:00", "안내실", "로비", "로비", "휴게"],
        ["08:00~09:00", "안내실", "휴게", "휴게", "로비"],
        ["09:00~10:00", "안내실", "순찰", "휴게", "로비"],
        ["10:00~11:00", "휴게", "안내실", "로비", "순찰/휴게"],
        ["11:00~12:00", "안내실", "중식", "로비", "중식"],
        ["12:00~13:00", "중식", "안내실", "중식", "로비"],
        ["13:00~14:00", "안내실", "휴게", "휴게/순찰", "로비"],
        ["14:00~15:00", "순찰", "안내실", "로비", "휴게"],
        ["15:00~16:00", "안내실", "휴게", "로비", "휴게"],
        ["16:00~17:00", "휴게", "안내실", "휴게", "로비"],
        ["---", "---", "---", "---", "---"],
        ["17:00~18:00", "안내실", "휴게", "휴게", "로비"],
        ["18:00~19:00", "안내실", "석식", "로비", "석식"],
        ["19:00~20:00", "안내실", "안내실", "석식", "로비"],
        ["20:00~22:00", "석식/안내실", "안내실/순찰", "로비", "휴게"],
        ["22:00~23:00", "순찰", "휴게", "순찰", "로비"],
        ["23:00~01:40", "안내실", "휴게", "휴게", "로비"],
        ["01:40~05:00", "휴게", "안내실", "로비", "휴게"],
        ["05:00~06:00", "안내실", "순찰", "로비", "순찰"],
        ["06:00~07:00", "안내실", "안내실", "휴게", "로비"]
    ]
    return pd.DataFrame(data, columns=["시간", "조장", "대원(회관)", "당직A(의산)", "당직B(의산)"])

# 근무자 명단 계산
def get_shift_workers(date):
    diff_days = (date - PATTERN_START_DATE).days
    if diff_days % 3 == 0:
        shift_num = diff_days // 3
        cycle = shift_num % 6
        # 엑셀 순번 로직
        names = {
            0: ["황재업", "이태원", "이정석", "김태언"],
            1: ["황재업", "김태언", "이태원", "이정석"],
            2: ["황재업", "김태언", "이정석", "이태원"],
            3: ["황재업", "이정석", "김태언", "이태원"],
            4: ["황재업", "이정석", "이태원", "김태언"],
            5: ["황재업", "이태원", "김태언", "이정석"]
        }
        res = names[cycle]
        return {"조장": res[0], "회관": res[1], "의산A": res[2], "의산B": res[3]}
    return None

now_kst = get_now_kst()
today_val = now_kst.date()
workers = get_shift_workers(today_val)

# --- 화면 구현 ---
st.title("📍 성의교정 C조 당직 시스템")
st.write(f"🕒 현재 시각: **{now_kst.strftime('%H:%M')}**")

if workers:
    st.success(f"✅ 오늘은 **C조 근무일**입니다. ({workers['회관']}, {workers['의산A']}, {workers['의산B']})")
else:
    st.warning("😴 오늘은 **비번/휴무**입니다. 아래 시간표로 다음 일정을 확인하세요.")

st.divider()

# --- 핵심: 상세 근무 편성표 ---
st.subheader("📊 상세 당직 근무 편성표 (시간별 위치)")

df_detail = get_detail_schedule()

# 오늘 근무자가 있다면 이름을 매칭해서 보여줌
if workers:
    # 표의 헤더를 실제 이름으로 변경
    df_detail.columns = ["시간", f"조장({workers['조장']})", f"회관({workers['회관']})", f"의산A({workers['의산A']})", f"의산B({workers['의산B']})"]

# 표 출력 (이미지가 아니라 진짜 표입니다)
st.table(df_detail)

st.divider()

# 주간 날짜 확인용 (전체 흐름)
with st.expander("🗓️ 주간 날짜별 근무 조 확인"):
    week_list = []
    for i in range(-1, 8):
        d = today_val + timedelta(days=i)
        w = get_shift_workers(d)
        if w:
            week_list.append({"날짜": d.strftime('%m/%d(%a)'), "조장": w['조장'], "회관": w['회관'], "의산A": w['의산A'], "의산B": w['의산B']})
    st.dataframe(pd.DataFrame(week_list), use_container_width=True, hide_index=True)
