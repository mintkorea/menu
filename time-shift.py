import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (탭 가독성 및 표 통합 최적화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1rem !important; max-width: 500px; margin: auto; }
    
    /* [수정] 탭 글씨 가독성 강화 */
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        height: 45px; background-color: #f0f2f6; border-radius: 8px 8px 0 0;
        padding: 0 20px; font-weight: 700; color: #333 !important; /* 글씨 검정색 강제 */
    }
    .stTabs [aria-selected="true"] {
        background-color: #2E4077 !important; color: white !important; /* 선택된 탭은 남색 배경/흰 글씨 */
    }

    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 14px !important; text-align: center; margin-bottom: 15px; color: #666; }
    
    /* 근무 상태 카드 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 12px; padding: 12px 5px; 
        text-align: center; background: white;
    }
    .worker-name { font-size: 16px !important; font-weight: 700; color: #555; }
    .status-val { font-size: 20px !important; font-weight: 900; color: #C04B41; }
    
    /* 휴무 카드 */
    .off-card {
        grid-column: span 2; border-radius: 12px; padding: 20px 15px;
        text-align: center; background: #FFF5F5; border: 2px solid #C04B41; margin-bottom: 15px;
    }
    .off-title { font-size: 24px !important; font-weight: 900; color: #C04B41; margin-bottom: 8px; }

    /* 통합 실시간 테이블 */
    .table-wrapper { width: 100%; margin-top: 10px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 13px; text-align: center; }
    .custom-table th, .custom-table td { border: 1px solid #dee2e6; padding: 8px 1px; }
    .b-header { font-weight: bold; font-size: 14px; }
    .highlight-row { background-color: #FFE5E5 !important; font-weight: bold; color: #C04B41; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직부 (기존과 동일) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers_by_date(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

today = now.date()
is_today_work = get_workers_by_date(today)[0] is not None
is_yesterday_work = get_workers_by_date(today - timedelta(days=1))[0] is not None
is_off_display = (is_yesterday_work and not is_today_work and now.hour >= 7) or (not is_yesterday_work and not is_today_work)

# 시간표 데이터
combined_data = [
    ["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
    ["09:00", "10:00", "순찰", "안내실", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "순찰"],
    ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
    ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
    ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"],
    ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"],
    ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"],
    ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"],
    ["23:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"],
    ["02:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"],
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"]
]

def get_current_idx(dt):
    curr_m = dt.hour * 60 + dt.minute
    if dt.hour < 7: curr_m += 1440
    for i, row in enumerate(combined_data):
        sh, sm = map(int, row[0].split(':'))
        eh, em = map(int, row[1].split(':'))
        s_m, e_m = sh * 60 + sm, eh * 60 + em
        if sh < 7: s_m += 1440
        if eh < 7 or (eh == 7 and em == 0 and sh < 7): e_m += 1440
        if s_m <= curr_m < e_m: return i
    return -1

curr_idx = get_current_idx(now)
work_date = (today - timedelta(days=1)) if now.hour < 7 else today
jojang, seonghui, uisanA, uisanB = get_workers_by_date(work_date)
if jojang is None: jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

# --- [3] UI 출력 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    if is_off_display:
        nw = today; 
        while get_workers_by_date(nw)[0] is None: nw += timedelta(days=1)
        nj, ns, na, nb = get_workers_by_date(nw)
        st.markdown(f'<div class="off-card"><div class="off-title">오늘은 휴무입니다.</div><div style="font-weight:700;">다음 근무: {nw.strftime("%m/%d")}<br>성희: {nj}, {ns} / 의산: {na}, {nb}</div></div>', unsafe_allow_html=True)
    elif curr_idx != -1:
        c = combined_data[curr_idx]
        st.markdown(f'<div class="status-container"><div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{c[2]}</div></div><div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{c[3]}</div></div><div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{c[4]}</div></div><div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{c[5]}</div></div></div>', unsafe_allow_html=True)

    # 통합 실시간 시간표 (HTML)
    html_table = f"""
    <div class="table-wrapper"><table class="custom-table">
        <tr class="b-header">
            <th colspan="2" style="background:#f8f9fa;">구분 (시간)</th>
            <th colspan="2" style="background:#FFF2CC;">성의회관</th>
            <th colspan="2" style="background:#D9EAD3;">의산연</th>
        </tr>
        <tr style="background:#eee; font-weight:bold;">
            <td>From</td><td>To</td><td>{jojang}</td><td>{seonghui}</td><td>{uisanA}</td><td>{uisanB}</td>
        </tr>
    """
    for i, r in enumerate(combined_data):
        row_cls = "highlight-row" if i == curr_idx else ""
        html_table += f'<tr class="{row_cls}"><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>'
    st.markdown(html_table + "</table></div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: s_date = st.date_input("📅 시작일", today)
    with c2: focus_u = st.selectbox("👤 강조 대상", ["안 함", "황재업", "김태언", "이태원", "이정석"])
    days_cnt = st.slider("📆 확인 일수", 7, 60, 15)

    cal_list = []
    for i in range(days_cnt):
        d = s_date + timedelta(days=i)
        w1, w2, w3, w4 = get_workers_by_date(d)
        if w1:
            weekday_str = ['월','화','수','목','금','토','일'][d.weekday()]
            cal_list.append({"날짜": d.strftime('%m/%d'), "요일": weekday_str, "조장": w1, "성희": w2, "의산A": w3, "의산B": w4})
    
    if cal_list:
        df = pd.DataFrame(cal_list)
        # [수정] 요일 칼라 적용 및 강조 로직
        def style_df(row):
            styles = [''] * len(row)
            # 일요일(빨간색), 토요일(파란색)
            if row['요일'] == '일': styles[1] = 'color: red; font-weight: bold'
            elif row['요일'] == '토': styles[1] = 'color: blue; font-weight: bold'
            # 강조 대상 배경색
            for i, val in enumerate(row):
                if focus_u != "안 함" and val == focus_u:
                    styles[i] = 'background-color: #FFF2CC; font-weight: bold'
            return styles

        st.dataframe(df.style.apply(style_df, axis=1), use_container_width=True, hide_index=True)
