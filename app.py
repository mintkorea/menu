import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정 (한국 시간)
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단", page_icon="🍽️", layout="centered")

# 2. 데이터 로드
@st.cache_data(ttl=600)
def load_data(url):
    try:
        df = pd.read_csv(url)
        result = {}
        for _, r in df.iterrows():
            d = str(r['date']).strip()
            m = str(r['meal_type']).strip()
            result.setdefault(d, {})[m] = {"menu": str(r['menu']), "side": str(r['side'])}
        return result
    except: return {}

URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
data = load_data(URL)

# 3. 파라미터 및 상태 관리
params = st.query_params
today = get_now().date()
try:
    d = datetime.strptime(params.get("d", str(today)), "%Y-%m-%d").date()
except:
    d = today

# 식사 시간 정의 및 남은 시간 계산
meal_times = {"조식": time(8, 0), "간편식": time(10, 0), "중식": time(13, 30), "석식": time(19, 0), "야식": time(23, 59)}

def get_status_msg():
    now = get_now()
    now_t = now.time()
    next_meal = None
    for m, t in meal_times.items():
        if now_t < t:
            next_meal = (m, t)
            break
    if next_meal:
        target_dt = datetime.combine(now.date(), next_meal[1], tzinfo=KST)
        diff = target_dt - now
        mins = int(diff.total_seconds() // 60)
        h, m = divmod(mins, 60)
        t_str = f"{h}시간 {m}분" if h > 0 else f"{m}분"
        return f"💡 {next_meal[0]} 시간까지 <span style='color:#E95444;'>{t_str}</span> 남았습니다."
    return "🌙 오늘 모든 배식이 종료되었습니다."

selected = params.get("meal", "중식")

# 4. 근무조 및 요일 설정
def get_shift(target_d):
    anchor = datetime(2026, 3, 13).date()
    arr = [{"n":"A조","bg":"#FF9800"}, {"n":"B조","bg":"#E91E63"}, {"n":"C조","bg":"#2196F3"}]
    return arr[(target_d - anchor).days % 3]

# 요일 색상 결정
weekday_names = ["월", "화", "수", "목", "금", "토", "일"]
wd = d.weekday() # 5:토, 6:일
wd_name = weekday_names[wd]
wd_color = "#2196F3" if wd == 5 else "#E91E63" if wd == 6 else "#1E3A5F"

s = get_shift(d)
colors = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
sel_c = colors.get(selected, "#8BC34A")

# 5. CSS 스타일
st.markdown(f"""
<style>
    [data-testid="stAppViewBlockContainer"] {{ max-width: 400px !important; margin: 0 auto !important; padding: 1rem 10px !important; }}
    header {{ visibility: hidden; }}
    .date-box {{ text-align: center; background: #F4F7FF; padding: 15px; border-radius: 15px; font-weight: 800; border: 1px solid #D6DCEC; font-size: 18px; }}
    .status-msg {{ text-align: center; font-size: 13px; font-weight: 700; color: #666; margin: 10px 0; }}
    .nav-row {{ display: flex; justify-content: space-between; margin-bottom: 10px; gap: 5px; }}
    .nav-btn {{ flex: 1; text-align: center; padding: 10px; background: white; border: 1px solid #EEE; border-radius: 8px; text-decoration: none; color: #1E3A5F; font-size: 13px; font-weight: 700; }}
    .tab-container {{ display: flex; width: 100%; margin-top: 15px; gap: 2px; }}
    .tab-item {{ flex: 1; text-align: center; padding: 12px 0; font-size: 12px; font-weight: 800; color: #333 !important; text-decoration: none; border-radius: 10px 10px 0 0; opacity: 0.7; transition: 0.2s; }}
    .tab-item.active {{ opacity: 1; color: white !important; transform: translateY(-2px); }}
    
    /* 카드 높이 고정 및 레이아웃 */
    .menu-card {{
        border: 2px solid {sel_c}; border-top: 5px solid {sel_c}; border-radius: 0 0 20px 20px;
        height: 240px; display: flex; flex-direction: column; justify-content: center; align-items: center;
        padding: 20px; background: white; margin-top: -1px; box-shadow: 0 8px 20px rgba(0,0,0,0.05); text-align: center;
    }}
    .main-menu {{ font-size: 21px; font-weight: 900; color: #111; line-height: 1.4; margin-bottom: 15px; word-break: keep-all; }}
    .side-menu {{ color: #666; font-size: 15px; line-height: 1.6; word-break: keep-all; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
</style>
""", unsafe_allow_html=True)

# 6. UI 렌더링
st.markdown(f"""
<div class="date-box">
    {d.strftime("%Y.%m.%d")} (<span style="color:{wd_color}">{wd_name}</span>)
    <span style="background:{s['bg']}; color:white; padding:2px 8px; border-radius:10px; font-size:12px; margin-left:5px; vertical-align:middle;">{s['n']}</span>
</div>
<div class="status-msg">{get_status_msg()}</div>
<div class="nav-row">
    <a href="?d={(d-timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">◀ 이전</a>
    <a href="?d={today}&meal={selected}" class="nav-btn" target="_self">오늘</a>
    <a href="?d={(d+timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">다음 ▶</a>
</div>
""", unsafe_allow_html=True)

# 7. 탭 메뉴
tabs_html = '<div class="tab-container">'
for m, c in colors.items():
    is_active = "active" if m == selected else ""
    tabs_html += f'<a href="?d={d}&meal={m}" class="tab-item {is_active}" style="background:{c}" target="_self">{m}</a>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# 8. 식단 출력 및 예외 처리
meal_info = data.get(d.strftime("%Y-%m-%d"), {}).get(selected)

if meal_info and str(meal_info['menu']).strip() not in ["", "nan", "None"]:
    main_m = meal_info['menu']
    side_m = meal_info['side']
else:
    if selected == "간편식":
        main_m = "오늘은 간편식을<br>제공하지 않습니다."
        side_m = ""
    else:
        main_m = "식단 정보 없음"
        side_m = "해당 일자의 식단이 등록되지 않았습니다."

st.markdown(f"""
<div class="menu-card">
    <div class="main-menu">{main_m}</div>
    <div style="width:30%; height:1.5px; background:#F0F0F0; margin:15px auto;"></div>
    <div class="side-menu">{side_m}</div>
</div>
""", unsafe_allow_html=True)
