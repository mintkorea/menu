import streamlit as st
from datetime import datetime, timedelta, time
from zoneinfo import ZoneInfo

# 1. 기초 설정
KST = ZoneInfo("Asia/Seoul")
def get_now(): return datetime.now(KST)

st.set_page_config(page_title="성의교정 주간식단", page_icon="🍽️", layout="centered")

# 2. 고정 식단 데이터 (이미지 기반 3월 4주차 데이터)
# CSV 로드 대신 관리하기 편하도록 직접 딕셔너리로 구성했습니다.
MEAL_DATA = {
    "2026-03-23": {
        "조식": {"menu": "포테이토소세지빵", "side": "당근스프, 바게트, 잡곡식빵, 딸기잼, 버터, 칠리빈즈, 샐러드, 우유, 커피, 누룽지"},
        "중식": {"menu": "시래기감자탕", "side": "매운두부조림, 흑향미밥, 아삭이쌈장박이, 석박지, 미숫가루"},
        "석식": {"menu": "제육볶음", "side": "청상추쌈/쌈장, 흰쌀밥, 유부된장국, 꼬시래기야채무침, 깍두기"},
        "야식": {"menu": "돈까스야채나베", "side": "흰쌀밥, 흑임자드레싱샐러드, 오복채무침, 열무김치, 요구르트"}
    },
    "2026-03-24": {
        "조식": {"menu": "고등어양념조림", "side": "흰쌀밥, 맑은콩나물국, 황태소걸절이, 열무김치, 누룽지, 커피"},
        "간편식": {"menu": "핫크리스피핫도그", "side": "하루견과 & 바나나"},
        "중식": {"menu": "쑥갓김치어묵우동", "side": "야채계란찜, 추가쌀밥, 망고요거트샐러드, 열무김치, 요구르트"},
        "석식": {"menu": "바베큐폭찹", "side": "흰쌀밥, 미역국, 고추장우엉조림, 오리엔탈샐러드, 깍두기"},
        "야식": {"menu": "너비아니구이", "side": "오곡찰밥, 도시락김, 근대된장국, 메추리알조림, 무생채, 열무김치, 매실"}
    },
    "2026-03-25": {
        "조식": {"menu": "중화풍새우볶음밥", "side": "비엔나야채볶음, 얼큰짬뽕국, 양념깻잎지, 열무김치, 누룽지, 커피"},
        "간편식": {"menu": "소불고기버거", "side": "딸기우유"},
        "중식": {"menu": "매콤불향돼지고기", "side": "양배추찜/쌈장, 혼합잡곡밥, 시금치된장국, 참나물유자무침, 포기김치, 식혜"},
        "석식": {"menu": "태국식팟타이", "side": "세모카레춘권, 추가쌀밥, 미소시루, 양파채절임, 포기김치"},
        "야식": {"menu": "누룽지영양닭죽", "side": "새송이장조림, 볶음김치, 두유"}
    },
    "2026-03-26": {
        "조식": {"menu": "부대찌개", "side": "계란말이, 흰쌀밥, 근대된장나물, 깍두기, 라면3종, 사과주스"},
        "간편식": {"menu": "풀드포크버거", "side": "오렌지주스"},
        "중식": {"menu": "블랙마파두부덮밥", "side": "야끼만두, 완두콩밥, 팽이장국, 오이지나물, 모짜샐러드, 포기김치, 매실"},
        "석식": {"menu": "미트볼라따뚜이", "side": "알감자버터구이, 흰쌀밥, 얼큰김칫국, 무피클, 열무김치"},
        "야식": {"menu": "그래놀라단호박샌드", "side": "초코우유"}
    },
    "2026-03-27": {
        "조식": {"menu": "바나나땅콩샌드", "side": "버섯야채죽, 바게트, 딸기잼, 버터, 샐러드, 우유, 커피, 누룽지, 김치"},
        "중식": {"menu": "닭갈비", "side": "깻잎와사비무침, 수수기장밥, 미역국, 후르츠코슬로우, 포기김치, 수정과"},
        "석식": {"menu": "참치야채볶음밥", "side": "데리야끼마요, 매콤떡볶이, 계란파국, 단무지무침, 열무김치"},
        "야식": {"menu": "강된장덮밥", "side": "흰쌀밥, 미역국, 떡갈비볶음, 연근조림, 깍두기, 요구르트"}
    }
}

# 3. 날짜 및 상태 관리
params = st.query_params
now_dt = get_now()
today_date = now_dt.date()
d = datetime.strptime(params["d"], "%Y-%m-%d").date() if "d" in params else today_date
selected = params.get("meal", "중식")
d_str = d.strftime("%Y-%m-%d")

# 식단 존재 여부 확인
meal_info = MEAL_DATA.get(d_str, {}).get(selected)
meal_exists = meal_info is not None

# 4. 배식 안내 문구 로직
def get_realtime_status(selected_meal, meal_exists):
    if not meal_exists: return ""
    if d != today_date: return f"📅 {d.strftime('%m월 %d일')} {selected_meal} 식단"
    
    now_t = get_now().time()
    is_weekend = d.weekday() >= 5
    lunch_start = time(11, 30) if is_weekend else time(11, 20)
    meal_schedule = {
        "조식": {"start": time(7, 0), "end": time(9, 0)},
        "간편식": {"start": time(7, 0), "end": time(11, 0)}, 
        "중식": {"start": lunch_start, "end": time(14, 0)},
        "석식": {"start": time(17, 20), "end": time(19, 20)},
        "야식": {"start": time(18, 0), "end": time(19, 20)}
    }
    sched = meal_schedule[selected_meal]
    if sched["start"] <= now_t <= sched["end"]:
        return f"✅ 지금은 <span style='color:#8BC34A;'>{selected_meal} 배식 중</span>입니다."
    if now_t < sched["start"]:
        target_dt = datetime.combine(today_date, sched["start"], tzinfo=KST)
        diff = target_dt - get_now()
        h, m = divmod(int(diff.total_seconds() // 60), 60)
        return f"⏳ {selected_meal} 제공까지 {h}시간 {m}분 남았습니다." if h > 0 else f"⏳ {selected_meal} 제공까지 {m}분 남았습니다."
    return f"🏁 {selected_meal} 배식이 종료되었습니다."

# 5. 근무조/요일 설정
def get_shift(target_d):
    anchor = datetime(2026, 3, 13).date()
    arr = [{"n":"A조","bg":"#FF9800"}, {"n":"B조","bg":"#E91E63"}, {"n":"C조","bg":"#2196F3"}]
    return arr[(target_d - anchor).days % 3]

weekday_names = ["월", "화", "수", "목", "금", "토", "일"]
wd = d.weekday()
wd_color = "#2196F3" if wd == 5 else "#E91E63" if wd == 6 else "#1E3A5F"
s, colors = get_shift(d), {"조식": "#E95444", "간편식": "#F1A33B", "중식": "#8BC34A", "석식": "#4A90E2", "야식": "#673AB7"}
sel_c = colors.get(selected, "#8BC34A")

# 6. 스타일 CSS (날짜 박스 슬림 및 타이틀 간격 유지)
st.markdown(f"""
<style>
    [data-testid="stAppViewBlockContainer"] {{ max-width: 420px !important; margin: 0 auto !important; padding-top: 1rem !important; }}
    header {{ visibility: hidden; }}
    div[data-testid="stVerticalBlock"] {{ gap: 0rem !important; }}
    .main-title {{ text-align: center; font-size: 22px; font-weight: 900; color: #1E3A5F; margin-bottom: 24px; line-height: 1.2; display: block; }}
    .date-box {{ text-align: center; background: #F4F7FF; padding: 4px; border-radius: 15px; font-weight: 800; border: 1px solid #D6DCEC; font-size: 16px; margin-bottom: 10px; }}
    .status-msg {{ text-align: center; font-size: 14px; font-weight: 700; color: #555; margin-bottom: 15px; min-height: 20px; }}
    .nav-row {{ display: flex; justify-content: space-between; gap: 8px; margin-bottom: 20px; }}
    .nav-btn {{ flex: 1; text-align: center; padding: 6px 0; background: white; border: 1px solid #EEE; border-radius: 8px; text-decoration: none; color: #1E3A5F; font-size: 13px; font-weight: 800; }}
    .tab-container {{ display: flex; width: 100%; gap: 1px; }}
    .tab-item {{ flex: 1; text-align: center; padding: 6px 0 20px 0; font-size: 12px; font-weight: 800; color: white !important; text-decoration: none; border-radius: 10px 10px 0 0; opacity: 0.6; }}
    .tab-item.active {{ opacity: 1; }}
    .menu-card {{ border: 1.5px solid #673AB7; border-top: 5px solid {sel_c}; border-radius: 0 0 20px 20px; min-height: 210px; display: flex; flex-direction: column; justify-content: center; align-items: center; padding: 20px; background: white; text-align: center; margin-top: -1px; }}
    .main-menu {{ font-size: 20px; font-weight: 900; color: #111; margin-bottom: 15px; line-height: 1.4; }}
    .side-menu {{ color: #777; font-size: 15px; line-height: 1.6; }}
    button[title="Manage app"], #MainMenu, footer, .stDeployButton {{ display: none !important; }}
</style>
""", unsafe_allow_html=True)

# 7. UI 구성
st.markdown('<div class="main-title">🍽️ 성의교정 주간식단</div>', unsafe_allow_html=True)
st.markdown(f"""
<div class="date-box">
    {d.strftime("%Y.%m.%d")} (<span style="color:{wd_color}">{weekday_names[wd]}</span>)
    <span style="background:{s['bg']}; color:white; padding:1px 8px; border-radius:10px; font-size:11px; margin-left:5px; vertical-align:middle;">{s['n']}</span>
</div>
<div class="status-msg">{get_realtime_status(selected, meal_exists)}</div>
<div class="nav-row">
    <a href="?d={(d-timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">PREV</a>
    <a href="?d={today_date.strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">TODAY</a>
    <a href="?d={(d+timedelta(1)).strftime('%Y-%m-%d')}&meal={selected}" class="nav-btn" target="_self">NEXT</a>
</div>
""", unsafe_allow_html=True)

# 탭 메뉴
tabs_html = '<div class="tab-container">'
for m, c in colors.items():
    active_class = "active" if m == selected else ""
    tabs_html += f'<a href="?d={d_str}&meal={m}" class="tab-item {active_class}" style="background:{c}" target="_self">{m}</a>'
st.markdown(tabs_html + '</div>', unsafe_allow_html=True)

# 8. 식단 출력 (문구 조건부 설정)
if meal_exists:
    main_m, side_m = meal_info['menu'], meal_info['side']
else:
    main_m = "오늘은 간편식을 제공하지 않습니다." if selected == "간편식" else "아직 식단 정보가 업데이트 되지 않았습니다"
    side_m = ""

st.markdown(f"""
<div class="menu-card">
    <div class="main-menu">{main_m}</div>
    <div style="width:40px; height:1px; background:#EEE; margin-bottom:15px;"></div>
    <div class="side-menu">{side_m}</div>
</div>
""", unsafe_allow_html=True)
