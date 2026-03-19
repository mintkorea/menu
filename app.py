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
            result.setdefault(d, {})[m] = {
                "menu": str(r['menu']),
                "side": str(r['side'])
            }
        return result
    except: return {}

URL = "https://docs.google.com/spreadsheets/d/1l07s4rubmeB5ld8oJayYrstL34UPKtxQwYptIocgKV0/export?format=csv"
data = load_data(URL)

# 3. 상태 관리 (URL 파라미터 기반)
params = st.query_params
today = get_now().date()

try:
    d = datetime.strptime(params.get("d", str(today)), "%Y-%m-%d").date()
except:
    d = today

# 기본 식사 자동 선택 로직 (시간대별)
def get_default_meal():
    t = get_now().time()
    if t < time(9, 0): return "조식"
    if t < time(14, 0): return "중식"
    if t < time(19, 20): return "석식"
    return "중식"

selected = params.get("meal", get_default_meal())

# 4. 근무조 계산
def get_shift(d):
    anchor = datetime(2026, 3, 13).date()
    arr = [
        {"n": "A조", "bg": "#FF9800"},
        {"n": "B조", "bg": "#E91E63"},
        {"n": "C조", "bg": "#2196F3"}
    ]
    return arr[(d - anchor).days % 3]

s = get_shift(d)
colors = {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
sel_c = colors.get(selected, "#8BC34A")

# 5. 스타일 정의 (디자인 업그레이드)
st.markdown(f"""
<style>
    .block-container {{ max-width: 480px; padding: 1rem 0.5rem; }}
    header {{ visibility: hidden; }}

    /* 날짜 박스 */
    .date-box {{
        text-align: center; background: #F4F7FF; padding: 18px; 
        border-radius: 15px; font-weight: 800; font-size: 19px; 
        border: 1px solid #D6DCEC; color: #1E3A5F;
    }}
    
    /* 네비게이션 */
    .nav {{ display: flex; margin: 12px 0; background: white; border-radius: 10px; border: 1px solid #EEE; }}
    .nav a {{ 
        flex: 1; text-align: center; padding: 10px; text-decoration: none; 
        font-weight: 700; color: #555; font-size: 14px;
    }}
    .nav a:hover {{ background: #F8F9FA; }}

    /* 인덱스 탭 스타일 */
    .tab-wrap {{ 
        display: flex; justify-content: space-between; 
        margin-top: 20px; gap: 2px;
    }}
    .tab {{ 
        flex: 1; text-align: center; padding: 12px 0; font-size: 13px; 
        font-weight: 800; color: white; text-decoration: none; 
        opacity: 0.3; border-radius: 10px 10px 0 0; 
        transition: all 0.2s ease;
    }}
    .tab.active {{ 
        opacity: 1; transform: translateY(-2px); /* 활성화 시 위로 살짝 올라옴 */
        box-shadow: 0 -4px 10px rgba(0,0,0,0.05);
    }}

    /* 메뉴 카드 (탭과 결합) */
    .card {{ 
        border-radius: 0 0 20px 20px; padding: 40px 20px; 
        margin-top: -1px; text-align: center; background: white; 
        border: 2px solid {sel_c}; border-top: 5px solid {sel_c};
        box-shadow: 0 12px 25px rgba(0,0,0,0.08);
        word-break: keep-all;
    }}
    .menu-title {{ font-size: 24px; font-weight: 900; color: #111; line-height: 1.4; }}
    .menu-sub {{ margin-top: 18px; color: #555; line-height: 1.7; font-size: 15px; }}

    /* 상태 메시지 */
    .status-box {{
        text-align: center; margin-top: 20px; padding: 12px;
        background: #F8F9FA; border-radius: 12px; font-size: 13px;
        font-weight: 700; color: #666; border: 1px solid #EEE;
    }}
</style>
""", unsafe_allow_html=True)

# 6. UI 렌더링
st.markdown(f"""
<div class="date-box">
    {d.strftime("%Y.%m.%d")}
    <span style="background:{s['bg']}; color:white; padding:3px 10px; border-radius:12px; font-size:12px; margin-left:5px;">
        {s['n']}
    </span>
</div>
<div class="nav">
    <a href="?d={(d-timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}">◀ 이전</a>
    <a href="?d={today}&meal={selected}">오늘</a>
    <a href="?d={(d+timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}">다음 ▶</a>
</div>
""", unsafe_allow_html=True)

# 7. 탭 메뉴 생성
tabs_html = '<div class="tab-wrap">'
for m, c in colors.items():
    active_class = "active" if m == selected else ""
    tabs_html += f'<a href="?d={d}&meal={m}" class="tab {active_class}" style="background:{c}">{m}</a>'
tabs_html += '</div>'
st.markdown(tabs_html, unsafe_allow_html=True)

# 8. 메뉴 카드 출력
meal_info = data.get(d.strftime("%Y-%m-%d"), {}).get(selected, {
    "menu": "정보 없음",
    "side": "식단 정보가 등록되지 않았습니다."
})

st.markdown(f"""
<div class="card">
    <div style="font-size: 13px; font-weight: bold; color: {sel_c}; margin-bottom: 10px;">{selected}</div>
    <div class="menu-title">{meal_info['menu']}</div>
    <div style="width:40%; height:1.5px; background:#F0F0F0; margin:15px auto;"></div>
    <div class="menu-sub">{meal_info['side']}</div>
</div>
""", unsafe_allow_html=True)

# 9. 실시간 상태 메시지 (추가)
st.markdown(f'<div class="status-box">💡 즐거운 식사 시간 되세요!</div>', unsafe_allow_html=True)
