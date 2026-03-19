import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

# -----------------------------
# 기본 설정
# -----------------------------
KST = ZoneInfo("Asia/Seoul")
def now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 식단", page_icon="🍽️", layout="centered")

# -----------------------------
# 데이터
# -----------------------------
@st.cache_data(ttl=600)
def load_data(url):
    df = pd.read_csv(url)
    result = {}
    for _, r in df.iterrows():
        d = str(r['date']).strip()
        m = str(r['meal_type']).strip()
        result.setdefault(d, {})[m] = {
            "menu": r['menu'],
            "side": r['side']
        }
    return result

URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
data = load_data(URL)

# -----------------------------
# 상태
# -----------------------------
params = st.query_params
today = now().date()

try:
    d = datetime.strptime(params.get("d", str(today)), "%Y-%m-%d").date()
except:
    d = today

selected = params.get("meal", "중식")

# -----------------------------
# 근무조
# -----------------------------
def shift(d):
    anchor = datetime(2026,3,13).date()
    arr = [
        {"n":"A조","bg":"#FF9800"},
        {"n":"B조","bg":"#E91E63"},
        {"n":"C조","bg":"#2196F3"}
    ]
    return arr[(d-anchor).days % 3]

s = shift(d)

# -----------------------------
# 색상
# -----------------------------
colors = {
    "조식":"#E95444",
    "간편식":"#F1A33B",
    "중식":"#8BC34A",
    "석식":"#4A90E2",
    "야식":"#673AB7"
}

# -----------------------------
# 스타일
# -----------------------------
st.markdown("""
<style>

.block-container {
    max-width: 480px;
    padding: 1rem;
}

/* 날짜 카드 */
.date-box {
    text-align:center;
    background:#F4F7FF;
    padding:15px;
    border-radius:14px;
    font-weight:800;
    font-size:18px;
    border:1px solid #D6DCEC;
}

/* 네비 */
.nav {
    display:flex;
    margin:10px 0;
}
.nav a {
    flex:1;
    text-align:center;
    padding:8px;
    text-decoration:none;
    font-weight:700;
    color:#1E3A5F;
}

/* 탭 (붙어있는 스타일) */
.tab-wrap {
    display:flex;
    overflow-x:auto;
    flex-wrap:nowrap;
    margin-top:12px;
}
.tab-wrap::-webkit-scrollbar {
    display:none;
}

.tab {
    flex:0 0 auto;
    padding:10px 14px;
    font-size:13px;
    font-weight:800;
    color:white;
    text-decoration:none;
    opacity:0.35;
}

.tab.active {
    opacity:1;
    transform:scale(1.05);
}

/* 카드 */
.card {
    border-radius:20px;
    padding:25px 15px;
    margin-top:10px;
    text-align:center;
    background:white;
}

/* 메뉴 */
.menu-title {
    font-size:24px;
    font-weight:900;
}

.menu-sub {
    margin-top:12px;
    color:#444;
    line-height:1.5;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# 날짜 UI
# -----------------------------
st.markdown(f"""
<div class="date-box">
{d.strftime("%Y.%m.%d")}
<span style="background:{s['bg']}; color:white; padding:3px 8px; border-radius:10px; font-size:12px;">
{s['n']}
</span>
</div>
""", unsafe_allow_html=True)

# 네비
st.markdown(f"""
<div class="nav">
<a href="?d={(d-timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}">◀</a>
<a href="?d={today}&meal={selected}">오늘</a>
<a href="?d={(d+timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}">▶</a>
</div>
""", unsafe_allow_html=True)

# -----------------------------
# ⭐ 탭 (디자인 개선)
# -----------------------------
tabs = '<div class="tab-wrap">'
for m,c in colors.items():
    active = "active" if m==selected else ""
    tabs += f'<a href="?d={d}&meal={m}" class="tab {active}" style="background:{c}">{m}</a>'
tabs += '</div>'

st.markdown(tabs, unsafe_allow_html=True)

# -----------------------------
# 메뉴 카드
# -----------------------------
meal = data.get(d.strftime("%Y-%m-%d"), {}).get(selected, {
    "menu":"정보 없음",
    "side":"식단이 없습니다"
})

c = colors[selected]

st.markdown(f"""
<div class="card" style="border:3px solid {c}">
    <div class="menu-title">{meal['menu']}</div>
    <div style="width:30%; height:1px; background:#eee; margin:10px auto;"></div>
    <div class="menu-sub">{meal['side']}</div>
</div>
""", unsafe_allow_html=True)
