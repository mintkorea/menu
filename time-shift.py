import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; max-width: 800px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { width: 100%; justify-content: space-around; }
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; font-weight: 800; font-size: 14px; }
    
    /* 현황판 카드 스타일 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 10px; }
    .status-card { border: 2px solid #2E4077; border-radius: 12px; padding: 10px; text-align: center; background: white; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
    .worker-name { font-size: 16px; font-weight: 800; color: #333; }
    .status-val { font-size: 18px; font-weight: 900; color: #C04B41; margin-top: 4px;}
    .single-card { grid-column: span 2; padding: 25px; font-size: 18px; font-weight: 800; color: #2E4077; border: 3px solid #2E4077; }
    
    /* 테이블 공통 */
    .table-container { width: 100%; margin-top: 10px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: center; }
    .custom-table th, .custom-table td { border: 1px solid #dee2e6; padding: 10px 5px; }
    
    /* 달력 스타일 */
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; margin-bottom: 30px; }
    .cal-td { border: 1px solid #ddd; height: 70px; vertical-align: top; padding: 0 !important; position: relative; }
    .cal-date { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 15px; } /* 15px */
    .cal-shift { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 12px; } /* 3pt 차이(12px) */
    .sun { color: #d32f2f; } .sat { color: #1976d2; }
    .today-border { border: 4px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 (근무 규칙) ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_date = now_kst.date()

# 패턴 기준일 (C조가 성의회관 근무를 시작하는 임의의 기준일)
PATTERN_START = date(2024, 1, 1) 

def get_c_crew_assignment(target_date):
    """C조의 6일 주기 로직 적용"""
    # 조원: 김태언(입사1), 이태원(입사2), 이정석(입사3)
    # 규칙: 조장은 고정. 조원은 2회씩 회관 근무. 나머지 2명은 선임순 당직A, 당직B
    crew = ["김태언", "이태원", "이정석"] # 입사순 정렬
    days_diff = (target_date - PATTERN_START).days
    cycle_idx = days_diff % 6  # 6일 주기 (각 조원당 2회씩 회관 근무)
    
    leader = "황재업"
    hall_worker = crew[cycle_idx // 2]  # 0,1일차:김태언 / 2,3일차:이태원 / 4,5일차:이정석
    others = [p for p in crew if p != hall_worker] # 선임순 유지됨
    
    # 1일차: 당직A(선임1), 당직B(선임2) / 2일차: 당직B(선임1), 당직A(선임2) 교대? 
    # 요청사항: 선임이 첫날 당직A, 둘째날 당직B
    if cycle_idx % 2 == 0:
        dj_a, dj_b = others[0], others[1]
    else:
        dj_a, dj_b = others[1], others[0]
        
    return [leader, hall_worker, dj_a, dj_b]

def get_shift_group(target_date):
    """전체 조(A,B,C) 배정용 (달력용)"""
    days = (target_date - PATTERN_START).days
    groups = ["C", "A", "B"] # 가상 패턴
    return groups[days % 3]

# --- [3] 탭 구현 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무 현황판", "📅 근무 편성표", "🏥 근무 달력"])

# 1. 근무 현황판 탭
with tab1:
    # 시간 적용 로직 (오전 7시 기준 투입/철수)
    is_after_7am = now_kst.hour >= 7
    current_work_date = today_date if is_after_7am else today_date - timedelta(days=1)
    
    # 메시지 및 카드 표출 조건
    curr_hour = now_kst.hour
    curr_min = now_kst.minute
    total_min = curr_hour * 60 + curr_min
    
    st.subheader(f"📅 {now_kst.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 근무 스케줄 데이터 (예시 데이터)
    schedule_data = [
        ["07:00", "09:00", "보안실", "로비", "순찰", "휴게"],
        ["09:00", "11:00", "로비", "순찰", "휴게", "보안실"],
        ["11:00", "13:00", "순찰", "중식", "보안실", "로비"],
        ["13:00", "15:00", "휴게", "보안실", "로비", "순찰"],
        ["15:00", "17:00", "중식", "로비", "순찰", "휴게"],
        ["17:00", "19:00", "보안실", "순찰", "휴게", "석식"],
        ["19:00", "21:00", "로비", "석식", "보안실", "순찰"],
        ["21:00", "23:00", "순찰", "보안실", "로비", "휴게"],
        ["23:00", "01:00", "휴게", "로비", "순찰", "보안실"],
        ["01:00", "01:40", "보안실", "순찰", "휴게", "로비"],
        ["01:40", "04:00", "교대휴게", "보안실", "로비", "순찰"], # 01:40 교대 반영
        ["04:00", "07:00", "순찰", "로비", "보안실", "휴게"]
    ]

    # 메시지 판별 로직
    if not is_after_7am and curr_hour < 7: # 새벽 시간대
        if total_min < 400: # 00:00 ~ 06:40
            st.markdown('<div class="status-card single-card">오늘 하루도 보람차고 즐거운 하루가 되도록 합시다.</div>', unsafe_allow_html=True)
        elif 400 <= total_min < 420: # 06:40 ~ 07:00
            st.markdown('<div class="status-card single-card">근무 준비중입니다. (교대 대기)</div>', unsafe_allow_html=True)
    
    # 실시간 근무자 카드 (마. 근무 중 상황)
    names = get_c_crew_assignment(current_work_date)
    
    # 현재 시간 인덱스 찾기
    current_idx = -1
    display_min = total_min if is_after_7am else total_min + 1440
    for i, row in enumerate(schedule_data):
        start_h, start_m = map(int, row[0].split(':'))
        end_h, end_m = map(int, row[1].split(':'))
        s_total = (start_h if start_h >= 7 else start_h + 24) * 60 + start_m
        e_total = (end_h if end_h >= 7 or (end_h==7 and end_m==0) else end_h + 24) * 60 + end_m
        if s_total <= display_min < e_total:
            current_idx = i
            break

    cols = st.columns(2)
    card_titles = ["성의 조장", "성의 회관", "의산연 당직A", "의산연 당직B"]
    for i in range(4):
        status = schedule_data[current_idx][i+2] if current_idx != -1 else "대기/휴게"
        with cols[i % 2]:
            st.markdown(f'''<div class="status-card">
                <div style="font-size:12px; color:gray;">{card_titles[i]}</div>
                <div class="worker-name">{names[i]}</div>
                <div class="status-val">{status}</div>
            </div>''', unsafe_allow_html=True)

    # 근무 테이블 가. 나. 다. 라.
    st.write("---")
    view_all = st.radio("일정 보기", ["현재 이후", "전체 보기"], horizontal=True)
    
    display_rows = schedule_data[current_idx:] if (view_all == "현재 이후" and current_idx != -1) else schedule_data
    
    table_html = '<table class="custom-table"><tr style="background:#f8f9fa;"><th>시간</th><th>성의(조장)</th><th>성의(회관)</th><th>의산A</th><th>의산B</th></tr>'
    for i, row in enumerate(display_rows):
        is_highlight = "background:#FFF5F5; font-weight:bold;" if (view_all == "현재 이후" and i == 0) else ""
        table_html += f'<tr style="{is_highlight}"><td>{row[0]}~{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td><td>{row[4]}</td><td>{row[5]}</td></tr>'
    table_html += '</table>'
    st.markdown(table_html, unsafe_allow_html=True)

# 2. 근무편성표 탭
with tab2:
    st.subheader("📅 C조 근무 편성표 (1개월)")
    
    # 조회기간 설정 슬라이더 (-12 ~ +12)
    month_offset = st.select_slider("조회 월 변경 (현재 기준)", options=list(range(-12, 13)), value=0)
    base_month = (today_date.replace(day=1) + timedelta(days=month_offset * 31)).replace(day=1)
    
    focus_worker = st.selectbox("본인 강조 선택", ["없음", "황재업", "김태언", "이태원", "이정석"])
    
    # 연차 시뮬레이션 (라. 연차 프로그램 연동 가정)
    st.info("💡 연차 발생 시 해당 인원은 야간 성의회관으로 투입되며 근무지가 자동 변경됩니다.")
    
    t_html = '<table class="custom-table"><tr style="background:#f8f9fa;"><td>날짜</td><td>성의(조장)</td><td>성의(회관)</td><td>의산연A</td><td>의산연B</td></tr>'
    
    # 한 달치 생성
    num_days = calendar.monthrange(base_month.year, base_month.month)[1]
    for d in range(1, num_days + 1):
        curr = date(base_month.year, base_month.month, d)
        crew = get_c_crew_assignment(curr)
        
        # 주말 색상
        wd = curr.weekday()
        date_cls = "sun" if wd == 6 else ("sat" if wd == 5 else "")
        
        t_html += f'<tr><td class="{date_cls}">{curr.strftime("%m/%d")}({["월","화","수","목","금","토","일"][wd]})</td>'
        for name in crew:
            # 본인 하이라이트 (가.)
            bg_color = ""
            if name == focus_worker:
                bg_color = "background:#D1E7DD;" # 연한 초록 강조
            t_html += f'<td style="{bg_color}">{name}</td>'
        t_html += '</tr>'
    st.markdown(t_html + '</table>', unsafe_allow_html=True)

# 3. 근무달력 탭
with tab3:
    st.subheader("🏥 12개월 근무 달력")
    
    # 하이라이트 기능 (나. 다.)
    hi_group = st.radio("강조할 근무조 선택", ["A", "B", "C"], index=2, horizontal=True)
    
    B_COLORS = {"A": "#FFE0B2", "B": "#FFCDD2", "C": "#E3F2FD"} # 연한 배경
    S_COLORS = {"A": "#FB8C00", "B": "#D32F2F", "C": "#1976D2"} # 진한 강조색
    
    cal_container = st.container()
    
    # 오늘부터 12개월치 출력
    start_month = today_date.replace(day=1)
    for m_inc in range(12):
        curr_m = (start_month + timedelta(days=m_inc * 31)).replace(day=1)
        st.write(f"#### {curr_m.year}년 {curr_m.month}월")
        
        month_cal = calendar.monthcalendar(curr_m.year, curr_m.month)
        cal_html = '<table class="cal-table"><tr><th class="sun">일</th><th>월</th><th>화</th><th>수</th><th>목</th><th>금</th><th class="sat">토</th></tr>'
        
        for week in month_cal:
            cal_html += '<tr>'
            for idx, day in enumerate(week):
                if day == 0:
                    cal_html += '<td class="cal-td"></td>'
                else:
                    d_obj = date(curr_m.year, curr_m.month, day)
                    group = get_shift_group(d_obj)
                    is_today = (d_obj == today_date)
                    is_hi = (group == hi_group)
                    
                    # 스타일 결정 (다. 라.)
                    bg = S_COLORS[group] if is_hi else B_COLORS[group]
                    text_color = "white" if is_hi else "black"
                    border = "today-border" if is_today else ""
                    
                    # 날짜(15px)와 조(12px) 3pt 차이 반영
                    cal_html += f'''<td class="cal-td {border}" style="background:{bg}; color:{text_color};">
                        <div class="cal-date">{day}</div>
                        <div class="cal-shift" style="font-size:12px;">{group}조</div>
                    </td>'''
            cal_html += '</tr>'
        cal_html += '</table>'
        st.markdown(cal_html, unsafe_allow_html=True)

