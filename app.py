import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단", page_icon="🍽️", layout="centered")

# 2. 데이터 로드 (캐싱)
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

def get_auto_meal():
    t = get_now().time()
    if t < time(9, 0): return "조식"
    if t < time(14, 0): return "중식"
    if t < time(19, 20): return "석식"
    return "중식"

selected = params.get("meal", get_auto_meal())

# 4. 근무조 계산
def get_shift(target_d):
    anchor = datetime(2026, 3, 13).date()
    arr = [{"n":"A조","bg":"#FF9800"}, {"n":"B조","bg":"#E91E63"}, {"n":"C조","bg":"#2196F3"}]
    return arr[(target_d - anchor).days % 3]

s = get_shift(d)
colors = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
sel_c = colors.get(selected, "#8BC34A")

# 5. CSS 스타일 (가독성 강화 및 에러 방지 처리)
st.markdown(f"""
<style>
    /* 전체 앱 컨테이너 폭 고정 */
    [data-testid="stAppViewBlockContainer"] {{
        max-width: 400px !important;
        margin: 0 auto !important;
        padding: 1rem 10px !important;
    }}
    header {{ visibility: hidden; }}

    /* 날짜 및 네비게이션 */
    .date-box {{ text-align: center; background: #F4F7FF; padding: 15px; border-radius: 15px; font-weight: 800; border: 1px solid #D6DCEC; }}
    .nav-row {{ display: flex; justify-content: space-between; margin: 10px 0; gap: 5px; }}
    .nav-btn {{ 
        flex: 1; text-align: center; padding: 8px; background: white; border: 1px solid #EEE; 
        border-radius: 8px; text-decoration: none; color: #1E3A5F; font-size: 14px; font-weight: 700;
    }}

    /* 탭 디자인: 가독성 대폭 개선 */
    .tab-container {{ display: flex; width: 100%; margin-top: 15px; gap: 2px; }}
    .tab-item {{
        flex: 1; text-align: center; padding: 12px 0; font-size: 13px; font-weight: 800;
        color: #333 !important; /* 비활성 상태 글자색: 진한 차콜색 */
        text-decoration: none; border-radius: 10px 10px 0 0;
        opacity: 0.75; /* 투명도를 높여서 잘 보이게 함 */
        transition: 0.2s;
    }}
    .tab-item.active {{
        opacity: 1;
        color: white !important; /* 활성 상태 글자색: 흰색 */
        font-weight: 900;
        transform: translateY(-2px);
    }}

    /* 메뉴 카드 */
    .menu-card {{
        border: 2px solid {sel_c};
        border-top: 5px solid {sel_c};
        border-radius: 0 0 20px 20px;
        padding: 40px 15px; text-align: center; background: white;
        margin-top: -1px; box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    }}
</style>
""", unsafe_allow_html=True)

# 6. UI 렌더링
st.markdown(f"""
<div class="date-box">
    {d.strftime("%Y.%m.%d")}
    <span style="background:{s['bg']}; color:white; padding:2px 8px; border-radius:10px; font-size:11px; margin-left:5px;">{s['n']}</span>
</div>
<div class="nav-row">
    <a href="?d={(d-timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">◀ 이전</a>
    <a href="?d={today}&meal={selected}" class="nav-btn" target="_self">오늘</a>
    <a href="?d={(d+timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">다음 ▶</a>
</div>
""", unsafe_allow_html=True)

# 7. 탭 메뉴 (가독성 반영)
tabs_html = '<div class="tab-container">'
for m, c in colors.items():
    is_active = "active" if m == selected else ""
    tabs_html += f'<a href="?d={d}&meal={m}" class="tab-item {is_active}" style="background:{c}" target="_self">{m}</a>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# 8. 식단 출력
meal = data.get(d.strftime("%Y-%m-%d"), {}).get(selected, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})

st.markdown(f"""
<div class="menu-card">
    <div style="font-size: 22px; font-weight: 900; color: #111; line-height: 1.4;">{meal['menu']}</div>
    <div style="width:30%; height:1.5px; background:#F0F0F0; margin:15px auto;"></div>
    <div style="color: #555; font-size: 15px; line-height: 1.6; word-break: keep-all;">{meal['side']}</div>
</div>
""", unsafe_allow_html=True)
