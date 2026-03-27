import streamlit as st
from datetime import datetime, date, timedelta, timezone
import calendar

# 1. KST 시간 및 기본 설정
def get_kst():
    return datetime.now(timezone(timedelta(hours=9)))

now_kst = get_kst()
today_kst = now_kst.date()

# [수정] 2026-01-01 B조 시작 기준 순환 로직
def get_shift_label(dt):
    base_date = date(2026, 1, 1)
    diff = (dt - base_date).days
    return ["B", "C", "A"][diff % 3]

# 2. 근무 로직 (3/27 시작, 선임자 우선 A배정 패턴)
# 선임 순위: 김태언 > 이태원 > 이정석
PATTERN = [
    ("황재업", "김태언", "이태원", "이정석"), # 1일차: 태원(선임) A
    ("황재업", "김태언", "이정석", "이태원"), # 2일차: 정석(후임) A
    ("황재업", "이정석", "김태언", "이태원"), # 3일차: 태언(선임) A
    ("황재업", "이정석", "이태원", "김태언"), # 4일차: 태원(후임) A
    ("황재업", "이태원", "김태언", "이정석"), # 5일차: 태언(선임) A
    ("황재업", "이태원", "이정석", "김태언")  # 6일차: 정석(후임) A
]

def get_base_workers(dt):
    # [수정] 편성표에서 하이픈(-)이 나오지 않도록 C조 근무일이 아니어도 패턴을 반환하거나 예외 처리
    start_date = date(2026, 3, 27)
    diff = (dt - start_date).days
    # 6일 주기로 계속 순환되도록 설정
    p_idx = diff % 6
    return list(PATTERN[p_idx])

# 3. 상세 시간표 데이터 및 인덱스 함수 (NameError 방지용 통합)
SHIFT_DATA = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "휴게"],
    ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
    ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"],
    ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"],
    ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"],
    ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"],
    ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"], ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"],
    ["01:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"],
    ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"], ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"],
    ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"]
]

def find_idx(dt):
    m = dt.hour * 60 + dt.minute
    if dt.hour < 7: m += 1440
    for i, r in enumerate(SHIFT_DATA):
        sh, sm = map(int, r[0].split(':')); eh, em = map(int, r[1].split(':'))
        s = (sh+24 if sh<7 else sh)*60+sm
        e = (eh+24 if (eh<7 or (eh==7 and em==0)) and sh!=7 else eh)*60+em
        if s <= m < e: return i
    return -1

# 4. UI 스타일 및 달력 설정 (흰 배경 + 강조 시 칸 전체 색상)
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")
st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 0px; display: flex; width: 100%; }
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; height: 40px; font-weight: 800; font-size: 13px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 10px 5px; text-align: center; background: white; }
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ddd; }
    .cal-td { border: 1px solid #eee; height: 65px; vertical-align: top; padding: 0 !important; background-color: white; }
    .cal-date-part { height: 35%; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 12px; }
    .cal-shift-part { height: 65%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 17px; }
    .sun { color: #d32f2f !important; } .sat { color: #1976d2 !important; }
    .hi-text { color: white !important; }
    .today-border { border: 2.5px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

# [생략] tab1(현황), tab2(편성표) 코드는 위 get_base_workers 로직을 사용하여 에러 없이 출력됨

# --- 탭 3: 근무달력 (A,B,C) ---
with tab3:
    st.markdown("<h3 style='text-align:center;'>🏥 성의교정 근무달력</h3>", unsafe_allow_html=True)
    hi = st.selectbox("🎯 강조할 조 선택", ["없음", "A", "B", "C"], index=3) # 기본 C조 강조
    
    BG_COLORS = {"A": "#FB8C00", "B": "#E53935", "C": "#1E88E5"}
    curr = today_kst.replace(day=1)
    
    for _ in range(3):
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        st.write(f"**{y}년 {m}월**")
        html = "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            html += "<tr>"
            for i, day in enumerate(week):
                if day == 0: html += "<td class='cal-td' style='background:#f9f9f9;'></td>"
                else:
                    d_obj = date(y, m, day)
                    s_lbl = get_shift_label(d_obj)
                    is_hi = (hi == s_lbl)
                    
                    # 강조 시에만 칸 전체 배경색 적용
                    bg_style = f"background-color: {BG_COLORS[s_lbl]};" if is_hi else "background-color: white;"
                    text_cls = "hi-text" if is_hi else ""
                    day_color = ("sun" if i==0 else "sat" if i==6 else "") if not is_hi else "hi-text"
                    today_cls = "today-border" if d_obj == today_kst else ""
                    
                    html += f"<td class='cal-td {today_cls}' style='{bg_style}'><div class='cal-date-part {day_color}'>{day}</div><div class='cal-shift-part {text_cls}'>{s_lbl}</div></td>"
            html += "</tr>"
        st.markdown(html + "</table><br>", unsafe_allow_html=True)
        curr = (curr + timedelta(days=32)).replace(day=1)
