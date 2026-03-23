import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 및 로직 ---
START_DATE = datetime(2026, 3, 24).date()
RANK = ["김태언", "이태원", "이정석"]  # 선임 순서
HALL_ROTATION = ["김태언", "이정석", "이태원"] # 회관 순번
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "이정석": "#FFFDE7", "김태언": "#E8F5E9"}

def get_daily_layout(target_date):
    diff = (target_date - START_DATE).days
    if diff % 3 != 0: return None
    # 3/27부터 김태언 2회 시작 유도 (이미지 패턴 반영)
    seq = (diff // 3) + 5 
    hall_worker = HALL_ROTATION[(seq // 2) % 3]
    others = [p for p in RANK if p != hall_worker]
    # 회관 1회차: 선임A-후임B / 2회차: 후임A-선임B
    if seq % 2 == 0: return hall_worker, others[0], others[1]
    else: return hall_worker, others[1], others[0]

# --- 2. UI 설정 ---
st.set_page_config(page_title="성의교정 C조", layout="centered")

with st.sidebar:
    st.header("👤 강조 설정")
    selected_user = st.selectbox("강조할 이름 선택", ["안 함", "황재업"] + RANK)

# --- 3. 스타일 함수 (행 전체 강조 및 요일 색상) ---
def apply_styles(df, target_name):
    # 기본 중앙 정렬 설정
    styled = df.style.set_properties(**{
        'text-align': 'center',
        'border': '1px solid #ddd'
    })
    
    # 1. 특정 이름이 포함된 행(Row)만 배경색 변경
    def highlight_row(row):
        if target_name != "안 함" and target_name in row.values:
            color = WORKER_COLORS.get(target_name, "#ffffff")
            return [f'background-color: {color}; font-weight: bold; color: black;'] * len(row)
        return [''] * len(row)

    # 2. 요일별 글자 색상 (날짜 열 기준)
    def color_day(val):
        if "토" in str(val): return 'color: blue; font-weight: bold;'
        if "일" in str(val): return 'color: red; font-weight: bold;'
        return ''

    return styled.apply(highlight_row, axis=1).map(color_day, subset=['날짜'])

# --- 4. 메인 화면 출력 ---
st.markdown("<h3 style='text-align:center;'>📅 성의교정 C조 근무편성표</h3>", unsafe_allow_html=True)

display_data = []
for i in range(45):
    d = START_DATE + timedelta(days=i)
    res = get_daily_layout(d)
    if res:
        h, a, b = res
        display_data.append({
            "날짜": f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][d.weekday()]})",
            "조장": "황재업", "회관": h, "의산A": a, "의산B": b
        })

if display_data:
    df = pd.DataFrame(display_data)
    # 스타일 적용 후 출력
    st.dataframe(
        apply_styles(df, selected_user),
        use_container_width=True,
        hide_index=True
    )

# --- 5. 실시간 상황판 (간략) ---
st.markdown("---")
st.markdown("<h3 style='text-align:center;'>📍 오늘 근무 상황</h3>", unsafe_allow_html=True)
today_res = get_daily_layout(datetime.now().date())
if today_res:
    h, a, b = today_res
    st.success(f"**오늘의 근무자:** 조장(황재업), 회관({h}), 의산A({a}), 의산B({b})")
else:
    st.info("오늘은 C조 비번(휴무)입니다.")
