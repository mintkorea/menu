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

# 3. 세션 상태 관리
now_dt = get_now()
if 'd' not in st.session_state: st.session_state.d = now_dt.date()
if 'meal' not in st.session_state:
    t = now_dt.time()
    if t < time(9, 0): st.session_state.meal = "조식"
    elif t < time(14, 0): st.session_state.meal = "중식"
    elif t < time(19, 20): st.session_state.meal = "석식"
    else: st.session_state.meal = "중식"

# 4. 근무조 및 색상 설정
def get_shift(target_d):
    anchor = datetime(2026, 3, 13).date()
    arr = [{"n":"A조","bg":"#FF9800"}, {"n":"B조","bg":"#E91E63"}, {"n":"C조","bg":"#2196F3"}]
    return arr[(target_d - anchor).days % 3]

colors = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
sel_c = colors.get(st.session_state.meal, "#8BC34A")

# 5. CSS: 강제 너비 고정 및 버튼 밀착
tab_styles = ""
for i, (m, c) in enumerate(colors.items()):
    is_active = (st.session_state.meal == m)
    tab_styles += f"""
        div[data-testid="column"]:nth-of-type({i+1}) button {{
            background-color: {c if is_active else "#f0f2f6"} !important;
            color: {"white" if is_active else "#666"} !important;
            border: 1px solid {c if is_active else "#D1D9E6"} !important;
            border-radius: 10px 10px 0 0 !important;
            height: 40px !important;
            font-size: 11px !important;
            font-weight: 800 !important;
            opacity: {1 if is_active else 0.4} !important;
            margin: 0 !important;
        }}
    """

st.markdown(f"""
<style>
    /* [핵심] 전체 앱의 너비를 스마트폰 사이즈로 강제 고정 */
    [data-testid="stAppViewBlockContainer"] {{
        max-width: 400px !important;
        padding: 1rem 0.5rem !important;
        margin: 0 auto !important;
    }}
    header {{ visibility: hidden; }}
    
    /* 버튼들 사이의 간격을 없애고 일렬로 배치 */
    div[data-testid="stHorizontalBlock"] {{
        gap: 2px !important;
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
    }}
    div[data-testid="column"] {{
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }}

    {tab_styles}

    .date-box {{ text-align: center; background: #F4F7FF; padding: 12px; border-radius: 15px; font-weight: 800; border: 1px solid #D6DCEC; margin-bottom: 8px; }}
    .card {{ 
        border-radius: 0 0 20px 20px; padding: 30px 15px; margin-top: -1px; 
        text-align: center; background: white; border: 2px solid {sel_c}; border-top: 4px solid {sel_c};
        box-shadow: 0 5px 15px rgba(0,0,0,0.05);
    }}
</style>
""", unsafe_allow_html=True)

# 6. UI: 날짜 및 네비게이션
curr_d = st.session_state.d
s = get_shift(curr_d)
st.markdown(f'<div class="date-box">{curr_d.strftime("%Y.%m.%d")} ({s["n"]})</div>', unsafe_allow_html=True)

c1, c2, c3 = st.columns(3)
if c1.button("◀", use_container_width=True): st.session_state.d -= timedelta(1); st.rerun()
if c2.button("오늘", use_container_width=True): st.session_state.d = now_dt.date(); st.rerun()
if c3.button("다음 ▶", use_container_width=True): st.session_state.d += timedelta(1); st.rerun()

# 7. 식단 탭 (버튼)
st.write("") 
t_cols = st.columns(len(colors))
for i, m in enumerate(colors.keys()):
    if t_cols[i].button(m, use_container_width=True, key=f"t_{m}"):
        st.session_state.meal = m
        st.rerun()

# 8. 메뉴 카드
meal_info = data.get(curr_d.strftime("%Y-%m-%d"), {}).get(st.session_state.meal, {"menu":"정보 없음", "side":"식단이 없습니다."})

st.markdown(f"""
<div class="card">
    <div style="font-size: 20px; font-weight: 900; color: #111; line-height: 1.3;">{meal_info['menu']}</div>
    <div style="width:30%; height:1px; background:#EEE; margin:12px auto;"></div>
    <div style="color: #444; font-size: 14px; line-height: 1.5; word-break: keep-all;">{meal_info['side']}</div>
</div>
""", unsafe_allow_html=True)
