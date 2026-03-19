import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기본 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단 가이드", page_icon="🍴", layout="centered")

# 데이터 로딩
@st.cache_data(ttl=600)
def load_meal_data(url):
    df = pd.read_csv(url)
    structured = {}
    for _, row in df.iterrows():
        d = str(row['date']).strip()
        m = str(row['meal_type']).strip()
        structured.setdefault(d, {})[m] = {
            "menu": row['menu'],
            "side": row['side']
        }
    return structured

def get_work_shift(target_date):
    anchor = datetime(2026, 3, 13).date()
    shifts = [{"n": "A조", "bg": "#FF9800"}, {"n": "B조", "bg": "#E91E63"}, {"n": "C조", "bg": "#2196F3"}]
    return shifts[(target_date - anchor).days % 3]

CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)

now = get_now()
curr_date = now.date()

# 상태
params = st.query_params
d = datetime.strptime(params.get("d", str(curr_date)), "%Y-%m-%d").date()
selected_meal = params.get("meal", "중식")

# 스타일
st.markdown("""
<style>
.block-container { max-width: 500px !important; padding: 1rem; }

/* 탭 */
.tab-bar {
    display: flex;
    flex-wrap: nowrap;
    overflow-x: auto;
    gap: 6px;
    padding: 8px 4px;
}
.tab-bar::-webkit-scrollbar { display: none; }

.tab-item {
    flex: 0 0 auto;
    white-space: nowrap;
    padding: 8px 14px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 700;
    text-decoration: none;
    color: white;
    opacity: 0.4;
}
.tab-item.active {
    opacity: 1;
    transform: scale(1.05);
}

/* 카드 */
.menu-card {
    border-radius: 20px;
    padding: 25px 15px;
    text-align: center;
    background: white;
    border: 3px solid var(--c);
    margin-top: 10px;
}

/* 네비 */
.nav-bar {
    display: flex;
    margin: 10px 0;
}
.nav-btn {
    flex: 1;
    text-align: center;
    padding: 8px;
    text-decoration: none;
    color: #1E3A5F;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# 색상
color_theme = {
    "조식": "#E95444",
    "간편식": "#F1A33B",
    "중식": "#8BC34A",
    "석식": "#4A90E2",
    "야식": "#673AB7"
}

# 날짜 표시
shift = get_work_shift(d)

st.markdown(f"""
<div style="text-align:center; font-size:20px; font-weight:800;">
{d} <span style="background:{shift['bg']}; color:white; padding:2px 8px; border-radius:10px;">
{shift['n']}
</span>
</div>
""", unsafe_allow_html=True)

# 날짜 이동
st.markdown(f"""
<div class="nav-bar">
<a href="?d={(d-timedelta(1)).strftime('%Y-%m-%d')}&meal={selected_meal}" class="nav-btn">◀</a>
<a href="?d={curr_date}&meal={selected_meal}" class="nav-btn">오늘</a>
<a href="?d={(d+timedelta(1)).strftime('%Y-%m-%d')}&meal={selected_meal}" class="nav-btn">▶</a>
</div>
""", unsafe_allow_html=True)

# ✅ 탭 (핵심)
tabs_html = '<div class="tab-bar">'
for m, c in color_theme.items():
    active = "active" if m == selected_meal else ""
    tabs_html += f"""
    <a href="?d={d}&meal={m}" class="tab-item {active}" style="background:{c}">
        {m}
    </a>
    """
tabs_html += "</div>"

st.markdown(tabs_html, unsafe_allow_html=True)

# 데이터 표시
date_key = d.strftime("%Y-%m-%d")
meal = meal_data.get(date_key, {}).get(selected_meal, {"menu": "없음", "side": ""})
c = color_theme[selected_meal]

st.markdown(f"""
<div class="menu-card" style="--c:{c}">
    <div style="font-size:24px; font-weight:800;">{meal['menu']}</div>
    <div style="margin-top:10px; color:#555;">{meal['side']}</div>
</div>
""", unsafe_allow_html=True)
