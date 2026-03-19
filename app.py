import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# -----------------------------
# 1. 기본 설정
# -----------------------------
KST = ZoneInfo("Asia/Seoul")
def get_now():
    return datetime.now(KST)

st.set_page_config(
    page_title="성의교정 식단 가이드",
    page_icon="🍴",
    layout="centered"
)

# -----------------------------
# 2. 데이터 로딩
# -----------------------------
@st.cache_data(ttl=600)
def load_meal_data(url):
    df = pd.read_csv(url)
    result = {}
    for _, row in df.iterrows():
        d = str(row['date']).strip()
        m = str(row['meal_type']).strip()
        result.setdefault(d, {})[m] = {
            "menu": row['menu'],
            "side": row['side']
        }
    return result

CSV_URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
meal_data = load_meal_data(CSV_URL)

# -----------------------------
# 3. 상태 처리
# -----------------------------
now = get_now()
curr_date = now.date()

params = st.query_params

# 날짜
try:
    d = datetime.strptime(params.get("d", str(curr_date)), "%Y-%m-%d").date()
except:
    d = curr_date

# 선택 식사
selected_meal = params.get("meal", "중식")

# -----------------------------
# 4. 근무조
# -----------------------------
def get_work_shift(target_date):
    anchor = datetime(2026, 3, 13).date()
    shifts = [
        {"n": "A조", "bg": "#FF9800"},
        {"n": "B조", "bg": "#E91E63"},
        {"n": "C조", "bg": "#2196F3"}
    ]
    return shifts[(target_date - anchor).days % 3]

shift = get_work_shift(d)

# -----------------------------
# 5. 스타일
# -----------------------------
st.markdown("""
<style>
.block-container {
    max-width: 500px !important;
    padding: 1rem;
}

/* 날짜 */
.date-box {
    text-align:center;
    font-size:20px;
    font-weight:800;
    margin-bottom:10px;
}

/* 네비 */
.nav-bar {
    display:flex;
    margin-bottom:10px;
}
.nav-btn {
    flex:1;
    text-align:center;
    padding:8px;
    text-decoration:none;
    font-weight:bold;
    color:#1E3A5F;
}

/* 탭 */
.tab-bar {
    display:flex;
    flex-wrap:nowrap;
    overflow-x:auto;
    gap:6px;
    padding:8px 4px;
}
.tab-bar::-webkit-scrollbar {
    display:none;
}

.tab-item {
    flex:0 0 auto;
    white-space:nowrap;
    padding:8px 14px;
    border-radius:12px;
    font-size:13px;
    font-weight:700;
    text-decoration:none;
    color:white;
    opacity:0.35;
    transition:0.2s;
}
.tab-item.active {
    opacity:1;
    transform:scale(1.05);
}

/* 카드 */
.menu-card {
    border-radius:20px;
    padding:25px 15px;
    text-align:center;
    background:white;
    margin-top:10px;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 6. 색상
# -----------------------------
color_theme = {
    "조식": "#E95444",
    "간편식": "#F1A33B",
    "중식": "#8BC34A",
    "석식": "#4A90E2",
    "야식": "#673AB7"
}

# -----------------------------
# 7. UI 출력
# -----------------------------

# 날짜
st.markdown(f"""
<div class="date-box">
{d.strftime("%Y.%m.%d")}
<span style="background:{shift['bg']}; color:white; padding:3px 8px; border-radius:10px; font-size:13px;">
{shift['n']}
</span>
</div>
""", unsafe_allow_html=True)

# 네비
st.markdown(f"""
<div class="nav-bar">
<a href="?d={(d-timedelta(1)).strftime('%Y-%m-%d')}&meal={selected_meal}" class="nav-btn">◀</a>
<a href="?d={curr_date}&meal={selected_meal}" class="nav-btn">오늘</a>
<a href="?d={(d+timedelta(1)).strftime('%Y-%m-%d')}&meal={selected_meal}" class="nav-btn">▶</a>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# ⭐ 핵심: 탭 UI (개행 완전 차단)
# -----------------------------
tabs_html = '<div class="tab-bar">'

for m, c in color_theme.items():
    active = "active" if m == selected_meal else ""
    tabs_html += f'<a href="?d={d}&meal={m}" class="tab-item {active}" style="background:{c}">{m}</a>'

tabs_html += '</div>'

st.markdown(tabs_html, unsafe_allow_html=True)

# -----------------------------
# 8. 식단 출력
# -----------------------------
date_key = d.strftime("%Y-%m-%d")
meal = meal_data.get(date_key, {}).get(selected_meal, {
    "menu": "정보 없음",
    "side": "등록된 식단이 없습니다."
})

c = color_theme[selected_meal]

st.markdown(f"""
<div class="menu-card" style="border:3px solid {c};">
    <div style="font-size:24px; font-weight:800;">{meal['menu']}</div>
    <div style="margin-top:12px; color:#555; line-height:1.5;">
        {meal['side']}
    </div>
</div>
""", unsafe_allow_html=True)
