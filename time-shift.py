import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 50px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; display: flex; width: 100%; }
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; height: 45px; background-color: #f8f9fa; border: 1px solid #eee; border-radius: 10px 10px 0 0; padding: 5px !important; font-weight: 700; color: #888; }
    .stTabs [aria-selected="true"] { background-color: #ffffff !important; color: #2E4077 !important; border-bottom: 3px solid #2E4077 !important; }
    
    /* 카드 영역 스타일 */
    .status-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 15px; }
    .status-card { background: #F8F9FA; border: 1px solid #E0E0E0; border-radius: 12px; padding: 12px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    .worker-name { font-size: 13px; font-weight: 800; color: #666; margin-bottom: 4px; }
    .status-val { font-size: 16px; font-weight: 900; color: #2E4077; }

    /* 하이라이트: 굵은 빨간 테두리 */
    .row-highlight { background-color: #FFE5E5 !important; }
    .row-highlight td { border-top: 3px solid #E53935 !important; border-bottom: 3px solid #E53935 !important; font-weight: 900 !important; }
    .row-highlight .time-col { border-left: 3px solid #E53935 !important; }
    .row-highlight td:last-child { border-right: 3px solid #E53935 !important; }

    .status-msg-box { background: #2E4077; color: white; padding: 20px; border-radius: 15px; text-align: center; font-size: 17px; font-weight: 800; margin-bottom: 15px; line-height: 1.5; }
    
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 8px; overflow: hidden; margin-bottom: 15px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .custom-table th { background: #F2F4F7; color: #333; padding: 10px 2px; border: 1px solid #dee2e6; font-size: 11px; font-weight: 800; }
    .custom-table td { border: 1px solid #dee2e6; padding: 12px 2px; }
    .time-col { width: 90px !important; white-space: nowrap !important; font-weight: 700; background: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 설정 ---
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
    p = PATTERNS[(diff // 3) % 6]
    return ["황재업", p[0], p[1], p[2]]

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
    status_msg = ""; highlight_idx = -1

    # 실시간 인덱스 계산
    curr_m = (hr + 24 if hr < 7 else hr) * 60 + mn
    for i, r in enumerate(data_list):
        sh, sm = map(int, r[0].split(':')); eh, em = map(int, r[1].split(':'))
        s_total = (sh + 24 if sh < 7 else sh) * 60 + sm
        e_total = (eh + 24 if (eh < 7 or (eh==7 and em==0)) and sh != 7 else eh) * 60 + em
        if s_total <= curr_m < e_total:
            highlight_idx = i; break

    # 메시지 로직
    if is_c_day and 6 <= hr < 7:
        status_msg = "수고하셨습니다. 잘 마무리 하시고 A조와 근무 교대를 준비하십시오." if mn < 40 else "고생하셨습니다. 근무교대 시간입니다."
    elif is_c_day and hr == 7:
        status_msg = "✨ 밤새 고생 많으셨습니다. 안전하게 퇴근하십시오!"
    elif today_kst >= NEXT_WORK_DATE and hr < 7:
        status_msg = "🗓️ 오늘은 C조 근무일입니다. 즐겁고 보람 된 하루를 준비하십시오." if mn < 40 else "근무 교대 및 근무 준비 중..."
    else:
        status_msg = "😴 오늘은 휴무일입니다. 편안한 휴식 되세요."

    st.markdown(f'<div class="status-msg-box">{status_msg}</div>', unsafe_allow_html=True)

    # [추가] 카드 영역 표출
    work_date = today_kst if hr >= 7 or is_c_day else today_kst - timedelta(days=1)
    names = get_workers(work_date)
    if names:
        locs = data_list[highlight_idx][2:] if highlight_idx != -1 else ["대기", "대기", "대기", "대기"]
        st.markdown(f'''<div class="status-container">
            <div class="status-card"><div class="worker-name">{names[0]}</div><div class="status-val">{locs[0]}</div></div>
            <div class="status-card"><div class="worker-name">{names[1]}</div><div class="status-val">{locs[1]}</div></div>
            <div class="status-card"><div class="worker-name">{names[2]}</div><div class="status-val">{locs[2]}</div></div>
            <div class="status-card"><div class="worker-name">{names[3]}</div><div class="status-val">{locs[3]}</div></div>
        </div>''', unsafe_allow_html=True)
    
    h_names = names if names else ["조장", "성희", "당직A", "당직B"]
    rows_html = "".join([f"<tr{' class=\"row-highlight\"' if i==highlight_idx else ''}><td class='time-col'>{r[0]} ~ {r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(data_list)])
    st.markdown(f'<div class="table-container"><table class="custom-table"><tr><th class="time-col" rowspan="2">시간</th><th colspan="2">성의회관</th><th colspan="2">의과학산업연구원</th></tr><tr><th>{h_names[0]}</th><th>{h_names[1]}</th><th>{h_names[2]}</th><th>{h_names[3]}</th></tr>{rows_html}</table></div>', unsafe_allow_html=True)

# ... (tab2, tab3 생략 - 주신 소스 그대로 유지)
