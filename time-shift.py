import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 (여백 및 잘림 방지) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    /* 상단 여백 확보 및 글자 잘림 방지 */
    .block-container { padding-top: 50px !important; max-width: 500px; margin: auto; }
    
    .stTabs [data-baseweb="tab-list"] { 
        gap: 5px; 
        display: flex; 
        width: 100%;
        justify-content: space-around;
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1;
        text-align: center;
        height: 45px; /* 높이 상향 */
        background-color: #f0f2f6; 
        border-radius: 8px 8px 0 0;
        padding: 5px !important; 
        font-weight: 800; 
        font-size: 13px !important;
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    
    /* 타이틀 및 날짜 표시 */
    .main-title { text-align: center; font-size: 20px; font-weight: 900; color: #2E4077; margin-bottom: 5px; }
    .date-display { text-align: center; font-size: 14px; color: #666; margin-bottom: 15px; font-weight: 600; }

    /* 메시지 및 카드 */
    .status-msg { text-align: center; font-size: 14px; font-weight: 700; color: #C04B41; padding: 12px; border: 2px dashed #C04B41; border-radius: 10px; margin-bottom: 15px; background: #FFF5F5; line-height: 1.5; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 15px; }
    .status-card { border: 2px solid #2E4077; border-radius: 12px; padding: 10px 2px; text-align: center; background: white; box-shadow: 2px 2px 5px rgba(0,0,0,0.05); }
    .worker-name { font-size: 14px; font-weight: 800; color: #555; margin-bottom: 4px; }
    .status-val { font-size: 17px; font-weight: 900; color: #C04B41; }
    
    /* 테이블 스타일 (헤더 2중 구조 시각화) */
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 8px; margin-bottom: 25px; overflow: hidden; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .custom-table th { background: #2E4077; color: white; padding: 8px 2px; border: 1px solid #dee2e6; }
    .custom-table td { border: 1px solid #dee2e6; padding: 10px 2px; }
    
    /* 달력 (조 글자가 날짜보다 3pt 크게) */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; margin-bottom: 40px; }
    .cal-td { border: 1px solid #eee; height: 65px; vertical-align: top; padding: 0 !important; }
    .cal-date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 13px; }
    .cal-shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 16px; } /* 13+3=16px */
    .sun { color: #d32f2f !important; }
    .sat { color: #1976d2 !important; }
    .hi-text { color: white !important; }
    .today-border { border: 3px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 (순환/연차/시간) ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()
PATTERN_START = date(2026, 3, 9)

# 임시 연차 데이터 (실제 데이터 연동 가능 구조)
vaca_list = {date(2026, 3, 20): "이태원"} 

def get_workers(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 != 0: return None
    
    cycle_idx = (diff // 3)
    members = ["김태언", "김태언", "이정석", "이정석", "이태원", "이태원"] # 2회씩 성의회관
    chief = "황재업"
    hall_worker = members[cycle_idx % 6]
    
    # 입사순(김태언-이태원-이정석) 기반 나머지 2명 배정
    others = [m for m in ["김태언", "이태원", "이정석"] if m != hall_worker]
    res = [chief, hall_worker, others[0], others[1]] # 조장, 성희, 의산A, 의산B
    
    # 연차 로직: 의산연 근무자가 연차 시 성의회관 근무자와 스왑
    vaca_person = vaca_list.get(target_date)
    if vaca_person and vaca_person in [res[2], res[3]]:
        idx = res.index(vaca_person)
        res[1], res[idx] = res[idx], res[1]
    return res

def get_shift_simple(dt):
    diff = (dt - PATTERN_START).days
    return ["C", "A", "B"][diff % 3]

data_list = [["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"], ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "휴게"], ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"], ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"], ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"], ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"], ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"], ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"], ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"], ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"], ["01:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"], ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"], ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"], ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"], ["06:00", "07:00", "안내실", "정리", "로비", "정리"]]

# --- [3] 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">현재시간: {now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    hr, mn = now_kst.hour, now_kst.minute
    is_work_day = (get_shift_simple(today_kst) == "C")
    is_after_work = (get_shift_simple(today_kst - timedelta(days=1)) == "C")
    
    msg = ""; show_cards = False
    if is_work_day:
        if 0 <= hr < 6 or (hr == 6 and mn < 40): msg = "오늘 하루도 보람차고 즐거운 하루가 되도록 합시다."
        elif hr == 6 and 40 <= mn <= 59: msg = "카드 표출 및 근무 준비중입니다."; show_cards = True
        elif hr >= 7 or hr < 7: show_cards = True
    elif is_after_work and 0 <= hr < 7: show_cards = True
    
    if not msg and is_after_work and hr == 7: msg = "오늘도 수고하셨습니다. 다음 근무 때 뵙겠습니다."
    elif not msg and not is_work_day: msg = "오늘은 휴무일입니다."

    if msg: st.markdown(f'<div class="status-msg">{msg}</div>', unsafe_allow_html=True)
    
    work_date = today_kst if hr >= 7 or is_work_day else today_kst - timedelta(days=1)
    names = get_workers(work_date)
    
    def get_idx(dt):
        m = (dt.hour + 24 if dt.hour < 7 else dt.hour) * 60 + dt.minute
        for i, r in enumerate(data_list):
            sh, sm = map(int, r[0].split(':')); eh, em = map(int, r[1].split(':'))
            s, e = (sh+24 if sh<7 else sh)*60+sm, (eh+24 if (eh<7 or (eh==7 and em==0)) and sh!=7 else eh)*60+em
            if s <= m < e: return i
        return -1
    
    idx = get_idx(now_kst)
    if show_cards and names:
        st.markdown(f'''<div class="status-container">
            <div class="status-card"><div class="worker-name">{names[0]}</div><div class="status-val">{data_list[idx][2] if idx!=-1 else "대기"}</div></div>
            <div class="status-card"><div class="worker-name">{names[1]}</div><div class="status-val">{data_list[idx][3] if idx!=-1 else "대기"}</div></div>
            <div class="status-card"><div class="worker-name">{names[2]}</div><div class="status-val">{data_list[idx][4] if idx!=-1 else "대기"}</div></div>
            <div class="status-card"><div class="worker-name">{names[3]}</div><div class="status-val">{data_list[idx][5] if idx!=-1 else "대기"}</div></div>
        </div>''', unsafe_allow_html=True)

    show_all = st.radio("일정 보기", ["현재 이후", "전체"], horizontal=True)
    d_rows = data_list if show_all == "전체" else (data_list[idx:] if idx != -1 else data_list)
    
    rows_html = "".join([f"<tr{' style=\"background:#FFE5E5;font-weight:bold;\"' if (show_all=='전체' and i==idx) or (show_all=='현재 이후' and i==0) else ''}><td>{r[0]}~{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(d_rows)])
    st.markdown(f'''<div class="table-container"><table class="custom-table">
        <tr><th rowspan="2">시간</th><th colspan="2">성의회관</th><th colspan="2">의과학산업연구원</th></tr>
        <tr><th>조장</th><th>성희</th><th>당직A</th><th>당직B</th></tr>{rows_html}</table></div>''', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="main-title">📅 근무 편성표</div>', unsafe_allow_html=True)
    s_date = st.date_input("조회 기준일", today_kst)
    focus = st.selectbox("🎯 강조(색상)", ["없음", "황재업", "김태언", "이태원", "이정석"])
    
    t_html = '<div class="table-container"><table class="custom-table"><tr style="background:#f8f9fa;font-weight:800;"><td>날짜</td><td>조장</td><td>성희</td><td>의산A</td><td>의산B</td></tr>'
    for i in range(31): # 조회일 기준 1개월
        d = s_date + timedelta(days=i)
        ws = get_workers(d)
        if ws:
            wd = d.weekday(); lbl = f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})"
            cls = "sun" if wd==6 else ("sat" if wd==5 else "")
            t_html += f'<tr><td class="{cls}">{lbl}</td>'
            for w in ws:
                bg = {"황재업":"#D9EAD3","김태언":"#FFF2CC","이태원":"#EAD1DC","이정석":"#C9DAF8"}.get(w,"") if w==focus else ""
                t_html += f'<td style="background:{bg};">{w}</td>'
            t_html += '</tr>'
    st.markdown(t_html + '</table></div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="main-title">🏥 성의교정 근무 달력</div>', unsafe_allow_html=True)
    hi = st.selectbox("🎯 강조 조 선택", ["A", "B", "C"], index=["A", "B", "C"].index(get_shift_simple(today_kst)))
    
    B_COLS, S_COLS = {"A":"#FFE0B2","B":"#FFCDD2","C":"#BBDEFB"}, {"A":"#FB8C00","B":"#E53935","C":"#1E88E5"}
    cal_html = ""
    curr = today_kst.replace(day=1)
    
    for _ in range(12):
        y, m = curr.year, curr.month
        cal = calendar.monthcalendar(y, m)
        cal_html += f"<div style='text-align:center; font-weight:900; margin-bottom:8px;'>{y}년 {m}월</div>"
        cal_html += "<table class='cal-table'><tr><th class='sun'>일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class='sat'>토</th></tr>"
        for week in cal:
            cal_html += "<tr>"
            for i, day in enumerate(week):
                if day == 0: cal_html += "<td class='cal-td'></td>"
                else:
                    d_obj = date(y, m, day); s = get_shift_simple(d_obj); is_hi = (hi == s)
                    s_bg, d_bg = (S_COLS[s], S_COLS[s]) if is_hi else (B_COLS[s], "white")
                    td_cls = "today-border" if d_obj == today_kst else ""
                    txt_cls = "hi-text" if is_hi else ("sun" if i==0 else "sat" if i==6 else "")
                    cal_html += f"<td class='cal-td {td_cls}' style='background:{s_bg};'><div class='cal-date-part {txt_cls}' style='background:{d_bg};'>{day}</div><div class='cal-shift-part {txt_cls}'>{s}</div></td>"
            cal_html += "</tr>"
        cal_html += "</table>"
        curr = (curr.replace(day=1) + timedelta(days=32)).replace(day=1)
    st.markdown(cal_html, unsafe_allow_html=True)
