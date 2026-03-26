import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 3.5rem !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; justify-content: center; }
    .stTabs [data-baseweb="tab"] {
        height: 40px; background-color: #f0f2f6; border-radius: 8px 8px 0 0;
        padding: 0 20px; font-weight: 700; color: #333 !important;
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 14px !important; text-align: center; margin-bottom: 15px; color: #666; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 15px; }
    .status-card { border: 2px solid #2E4077; border-radius: 12px; padding: 12px 5px; text-align: center; background: white; }
    .worker-name { font-size: 14px !important; font-weight: 700; color: #555; }
    .status-val { font-size: 19px !important; font-weight: 900; color: #C04B41; }
    .off-card {
        grid-column: span 2; border-radius: 12px; padding: 20px 15px;
        text-align: center; background: #FFF5F5; border: 2px solid #C04B41; margin-bottom: 15px;
    }
    .table-wrapper { width: 100%; margin-top: 10px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12.5px; text-align: center; }
    .custom-table th, .custom-table td { border: 1px solid #dee2e6; padding: 8px 2px; }
    .highlight-row { background-color: #FFE5E5 !important; font-weight: bold; color: #C04B41; border: 2px solid #C04B41 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜 및 패턴 로직 ---
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
# 근무 기준일 계산 (07시 이전은 전날 근무의 연장)
work_date = (today - timedelta(days=1)) if now.hour < 7 else today
jojang, seonghui, uisanA, uisanB = get_workers_by_date(work_date)
if jojang is None: jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

# --- [3] 시간표 데이터 ---
combined_data = [
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
    ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"],
    ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"]
]

def get_current_idx(dt):
    curr_m = dt.hour * 60 + dt.minute
    # 00:00 ~ 06:59 사이면 24시간을 더해 비교 (예: 01:00 -> 25:00)
    if dt.hour < 7: curr_m += 1440
    
    for i, row in enumerate(combined_data):
        sh, sm = map(int, row[0].split(':'))
        eh, em = map(int, row[1].split(':'))
        s_m = (sh + 24 if sh < 7 else sh) * 60 + sm
        e_m = (eh + 24 if (eh < 7 or (eh == 7 and em == 0)) and sh != 7 else eh) * 60 + em
        if s_m <= curr_m < e_m: return i
    return -1

curr_idx = get_current_idx(now)

# --- [4] UI 출력 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    # 보기 모드 라디오 버튼
    view_mode = st.radio("🔍 보기 설정", ["현재 시간 우선", "전체 시간표"], horizontal=True)

    # 비번/휴무 로직
    is_today_work = get_workers_by_date(today)[0] is not None
    is_yesterday_work = get_workers_by_date(today - timedelta(days=1))[0] is not None
    
    if (is_yesterday_work and not is_today_work and now.hour >= 7) or (not is_yesterday_work and not is_today_work):
        nw = today
        while get_workers_by_date(nw)[0] is None: nw += timedelta(days=1)
        nj, ns, na, nb = get_workers_by_date(nw)
        st.markdown(f'<div class="off-card"><div style="font-size:20px; font-weight:900; color:#C04B41;">오늘은 휴무입니다.</div><div style="margin-top:8px; font-weight:700;">다음 근무: {nw.strftime("%m월 %d일")}<br>성희: {nj}, {ns} / 의산: {na}, {nb}</div></div>', unsafe_allow_html=True)
    elif curr_idx != -1:
        c = combined_data[curr_idx]
        st.markdown(f'<div class="status-container"><div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{c[2]}</div></div><div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{c[3]}</div></div><div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{c[4]}</div></div><div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{c[5]}</div></div></div>', unsafe_allow_html=True)

    # 테이블 렌더링 데이터 준비
    display_data = combined_data.copy()
    actual_highlight_idx = curr_idx

    # '현재 시간 우선'일 때 정렬 로직 (현재 인덱스를 맨 위로)
    if view_mode == "현재 시간 우선" and curr_idx != -1:
        # 현재 행을 맨 앞으로 가져오고 나머지를 뒤에 붙임
        display_data = [combined_data[curr_idx]] + combined_data[:curr_idx] + combined_data[curr_idx+1:]
        actual_highlight_idx = 0 # 이동했으므로 첫 번째 행이 하이라이트

    html_table = f"""
    <div class="table-wrapper"><table class="custom-table">
        <tr style="background:#f8f9fa; font-weight:bold;">
            <th colspan="2">시간</th><th colspan="2" style="background:#FFF2CC;">성의회관</th><th colspan="2" style="background:#D9EAD3;">의산연</th>
        </tr>
        <tr style="background:#eee; font-size:11px;">
            <td>From</td><td>To</td><td>{jojang}</td><td>{seonghui}</td><td>{uisanA}</td><td>{uisanB}</td>
        </tr>
    """
    for i, r in enumerate(display_data):
        row_cls = "highlight-row" if i == actual_highlight_idx else ""
        html_table += f'<tr class="{row_cls}"><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>'
    st.markdown(html_table + "</table></div>", unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1: s_date = st.date_input("📅 시작일", today)
    with c2: focus_u = st.selectbox("👤 강조 대상", ["안 함", "황재업", "김태언", "이태원", "이정석"])
    
    view_days = st.slider("📅 조회 기간 (일)", 7, 60, 31)
    
    cal_list = []
    for i in range(view_days):
        d = s_date + timedelta(days=i)
        w1, w2, w3, w4 = get_workers_by_date(d)
        if w1:
            wd = ['월','화','수','목','금','토','일'][d.weekday()]
            cal_list.append({"날짜": d.strftime('%m/%d'), "요일": wd, "조장": w1, "성희": w2, "의산A": w3, "의산B": w4})
    
    if cal_list:
        df = pd.DataFrame(cal_list)
        def style_df(row):
            styles = [''] * len(row)
            if row['요일'] == '일': styles[1] = 'color: red; font-weight: bold'
            elif row['요일'] == '토': styles[1] = 'color: blue; font-weight: bold'
            for i, val in enumerate(row):
                if focus_u != "안 함" and val == focus_u: styles[i] = 'background-color: #FFF2CC; font-weight: bold'
            return styles
        st.dataframe(df.style.apply(style_df, axis=1), use_container_width=True, hide_index=True)
