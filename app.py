import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정
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
            d_str = str(r['date']).strip()
            m_type = str(r['meal_type']).strip()
            result.setdefault(d_str, {})[m_type] = {"menu": str(r['menu']), "side": str(r['side'])}
        return result
    except: return {}

URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_data(URL)

# 3. 파라미터 및 상태 관리
params = st.query_params
today = get_now().date()

# 날짜 결정
try:
    d = datetime.strptime(params.get("d", str(today)), "%Y-%m-%d").date()
except:
    d = today

# 식사 결정 (파라미터 우선, 없으면 시간대별 자동)
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

# 5. 핵심 CSS: 전체 폭 강제 고정 및 탭 디자인
st.markdown(f"""
<style>
    /* 1. 전체 앱 컨테이너 폭을 400px로 제한 (좌우 늘어짐 원천 차단) */
    [data-testid="stAppViewBlockContainer"] {{
        max-width: 400px !important;
        margin: 0 auto !important;
        padding: 1rem 10px !important;
    }}
    header {{ visibility: hidden; }}

    /* 2. 날짜 및 네비게이션 스타일 */
    .date-box {{ text-align: center; background: #F4F7FF; padding: 15px; border-radius: 15px; font-weight: 800; border: 1px solid #D6DCEC; }}
    .nav-row {{ display: flex; justify-content: space-between; margin: 10px 0; gap: 5px; }}
    .nav-btn {{ 
        flex: 1; text-align: center; padding: 8px; background: white; border: 1px solid #EEE; 
        border-radius: 8px; text-decoration: none; color: #555; font-size: 14px; font-weight: 700;
    }}

    /* 3. 인덱스 탭 스타일 (모바일 한 줄 고정) */
    .tab-container {{
        display: flex;
        width: 100%;
        margin-top: 15px;
        gap: 2px;
    }}
    .tab-item {{
        flex: 1;
        text-align: center;
        padding: 12px 0;
        font-size: 12px;
        font-weight: 800;
        color: white;
        text-decoration: none;
        border-radius: 10px 10px 0 0;
        opacity: 0.35;
        transition: 0.2s;
    }}
    .tab-item.active {{
        opacity: 1;
        transform: translateY(-2px);
    }}

    /* 4. 카드 디자인 */
    .menu-card {{
        border: 2px solid {sel_c};
        border-top: 5px solid {sel_c};
        border-radius: 0 0 20px 20px;
        padding: 35px 15px;
        text-align: center;
        background: white;
        margin-top: -1px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    }}
</style>
""", unsafe_allow_html=True)

# 6. UI 렌더링
# 날짜 헤더
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

# 7. 인덱스 탭 (HTML로 직접 구현하여 늘어짐 방지)
tabs_html = '<div class="tab-container">'
for m, c in colors.items():
    is_active = "active" if m == selected else ""
    # target="_self"를 명시하여 새 창이 뜨지 않도록 강제
    tabs_html += f'<a href="?d={d}&meal={m}" class="tab-item {is_active}" style="background:{c}" target="_self">{m}</a>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# 8. 메뉴 카드 본문
meal = meal_data.get(d.strftime("%Y-%m-%d"), {}).get(selected, {"menu": "정보 없음", "side": "식단 정보가 없습니다."})

st.markdown(f"""
<div class="menu-card">
    <div style="font-size: 22px; font-weight: 900; color: #111; line-height: 1.4;">{meal['menu']}</div>
    <div style="width:30%; height:1.5px; background:#F0F0F0; margin:15px auto;"></div>
    <div style="color: #666; font-size: 15px; line-height: 1.6; word-break: keep-all;">{meal['side']}</div>
</div>
""", unsafe_allow_html=True)
