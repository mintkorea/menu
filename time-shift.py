import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 (기존 디자인 복구 + 하이라이트 강화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 50px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; display: flex; width: 100%; }
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; height: 45px; background-color: #f8f9fa; border: 1px solid #eee; border-radius: 10px 10px 0 0; font-weight: 700; color: #888; }
    .stTabs [aria-selected="true"] { background-color: #ffffff !important; color: #2E4077 !important; border-bottom: 3px solid #2E4077 !important; }
    
    .main-title { text-align: center; font-size: 20px; font-weight: 900; color: #2E4077; margin-bottom: 5px; }
    .date-display { text-align: center; font-size: 18px; color: #333; margin-bottom: 15px; font-weight: 700; }
    
    /* [지시사항] 하이라이트 강화: 시간 포함 + 굵은 테두리 */
    .row-highlight { background-color: #FFE5E5 !important; }
    .row-highlight td { 
        border-top: 3px solid #E53935 !important; 
        border-bottom: 3px solid #E53935 !important;
        font-weight: 900 !important; 
    }
    .row-highlight .time-col { border-left: 3px solid #E53935 !important; }
    .row-highlight td:last-child { border-right: 3px solid #E53935 !important; }

    /* 격려 문구 박스 */
    .status-msg-box { background: #2E4077; color: white; padding: 20px; border-radius: 15px; text-align: center; font-size: 18px; font-weight: 800; margin-bottom: 15px; line-height: 1.5; }
    
    /* 시간표/편성표 공통 */
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden; margin-bottom:20px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .custom-table th { background: #F2F4F7; color: #333; padding: 10px 2px; border: 1px solid #dee2e6; font-size: 11px; font-weight: 800; }
    .custom-table td { border: 1px solid #dee2e6; padding: 12px 2px; }
    .time-col { width: 90px !important; white-space: nowrap !important; font-weight: 700; background: #fafafa; }
    
    /* 달력 디자인 복구 */
    .month-title { background: #2E4077; color: white; padding: 8px; border-radius: 5px; font-size: 16px; font-weight: 800; margin-top: 25px; margin-bottom: 10px; text-align: center; }
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; margin-bottom: 10px; }
    .cal-table th, .cal-table td { border: 1px solid #eee; padding: 8px 2px; text-align: center; font-size: 12px; }
    .cal-table th { background: #f8f9fa; font-weight: 800; color: #555; }
    .cal-day { font-weight: 700; margin-bottom: 4px; }
    .cal-worker { font-size: 10px; color: #C04B41; font-weight: 800; line-height: 1.2; }
    .sun { color: #d32f2f !important; } .sat { color: #1976d2 !important; }
    .today-box { background-color: #FFF9C4 !important; border: 2px solid #FBC02D !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()
hr, mn = now_kst.hour, now_kst.minute
PATTERN_START = date(2026, 3, 9)
NEXT_WORK_DATE = date(2026, 3, 30)

PATTERNS = [["김태언", "이태원", "이정석"], ["김태언", "이정석", "이태원"], ["이정석", "김태언", "이태원"], ["이정석", "이태원", "김태언"], ["이태원", "김태언", "이정석"], ["이태원", "이정석", "김태언"]]

def get_workers(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 != 0: return None
    return ["황재업", PATTERNS[(diff // 3) % 6][0], PATTERNS[(diff // 3) % 6][1], PATTERNS[(diff // 3) % 6][2]]

def get_shift_simple(dt):
    return ["C", "A", "B"][(dt - PATTERN_START).days % 3]

data_list = [["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"], ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "휴게"], ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"], ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"], ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"], ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"], ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"], ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"], ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"], ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"], ["01:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"], ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"], ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"], ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"], ["06:00", "07:00", "안내실", "정리", "로비", "정리"]]

# --- [3] 화면 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    weekdays = ['월','화','수','목','금','토','일']
    st.markdown(f'<div class="date-display">{now_kst.strftime("%Y-%m-%d")}({weekdays[now_kst.weekday()]}) {now_kst.strftime("%H:%M:%S")}</div>', unsafe_allow_html=True)
    
    is_c_day = (get_shift_simple(today_kst) == "C")
    status_msg = ""
    highlight_idx = -1

    # 시간별 격려 문구 로직
    if is_c_day and 6 <= hr < 7:
        status_msg = "수고하셨습니다. 잘 마무리 하시고 A조와 근무 교대를 준비하십시오." if mn < 40 else "고생하셨습니다. 근무교대 시간입니다."
        highlight_idx = 24
    elif is_c_day and hr == 7:
        status_msg = "✨ 밤새 고생 많으셨습니다. 안전하게 퇴근하십시오!"
    elif today_kst >= NEXT_WORK_DATE and hr < 7:
        status_msg = "🗓️ 오늘은 C조 근무일입니다. 즐겁고 보람 된 하루를 준비하십시오." if mn < 40 else "근무 교대 및 근무 준비 중(인수인계 사항을 잘 확인하시기 바랍니다.)"
    else:
        status_msg = "😴 오늘은 휴무일입니다. 편안한 휴식 되세요."

    st.markdown(f'<div class="status-msg-box">{status_msg}</div>', unsafe_allow_html=True)

    if highlight_idx == -1:
        st.info(f"📍 다음 근무는 **{NEXT_WORK_DATE.strftime('%Y-%m-%d')}(월)**입니다. 아래와 같이 근무하시면 됩니다.")

    h_names = get_workers(NEXT_WORK_DATE) if get_workers(NEXT_WORK_DATE) else ["조장", "성희", "의산A", "의산B"]
    rows_html = "".join([f"<tr{' class=\"row-highlight\"' if i==highlight_idx else ''}><td class='time-col'>{r[0]}~{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(data_list)])
    st.markdown(f'<div class="table-container"><table class="custom-table"><tr><th class="time-col" rowspan="2">시간</th><th colspan="2">성의회관</th><th colspan="2">의과학산업연구원</th></tr><tr><th>{h_names[0]}</th><th>{h_names[1]}</th><th>{h_names[2]}</th><th>{h_names[3]}</th></tr>{rows_html}</table></div>', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="main-title">🗓️ 근무 편성표</div>', unsafe_allow_html=True)
    # 슬라이더 미노출 문제 해결: 기준일 입력창 복구
    s_date = st.date_input("조회 기준일 선택", today_kst)
    t_html = '<div class="table-container"><table class="custom-table"><tr><th>날짜</th><th>조장</th><th>성희</th><th>의산A</th><th>의산B</th></tr>'
    for i in range(30):
        d = s_date + timedelta(days=i)
        ws = get_workers(d)
        if ws:
            wd = d.weekday(); lbl = f"{d.strftime('%m/%d')}({weekdays[wd]})"; cls = "sun" if wd==6 else ("sat" if wd==5 else "")
            t_html += f'<tr><td class="{cls}">{lbl}</td><td>{ws[0]}</td><td>{ws[1]}</td><td>{ws[2]}</td><td>{ws[3]}</td></tr>'
    st.markdown(t_html + '</table></div>', unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="main-title">🏥 성의교정 근무 달력</div>', unsafe_allow_html=True)
    curr = today_kst.replace(day=1)
    for _ in range(3): # 3개월치 표출
        y, m = curr.year, curr.month
        st.markdown(f'<div class="month-title">{y}년 {m}월</div>', unsafe_allow_html=True)
        html = '<table class="cal-table"><tr><th class="sun">일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class="sat">토</th></tr><tr>'
        
        cal = calendar.monthcalendar(y, m)
        for week in cal:
            for day_idx, day in enumerate(week):
                if day == 0: html += '<td></td>'
                else:
                    d_obj = date(y, m, day)
                    ws = get_workers(d_obj)
                    cls = "sun" if day_idx==0 else ("sat" if day_idx==6 else "")
                    today_cls = " today-box" if d_obj == today_kst else ""
                    content = f'<div class="cal-worker">{"<br>".join(ws)}</div>' if ws else ""
                    html += f'<td class="{today_cls}"><div class="cal-day {cls}">{day}</div>{content}</td>'
            html += '</tr><tr>'
        st.markdown(html + '</tr></table>', unsafe_allow_html=True)
        curr = (curr + timedelta(days=32)).replace(day=1)
