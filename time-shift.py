import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 (3/9 패턴 고정) ---
PATTERN_START_DATE = datetime(2026, 3, 9).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}

st.set_page_config(page_title="성의교정 C조 관리", layout="centered")

# --- 2. CSS 스타일 (표 중앙 정렬 및 가독성) ---
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 15px; }
    .period-text { font-size: 15px; color: #666; text-align: center; margin-bottom: 20px; }
    /* DataFrame 컨테이너 중앙 정렬 */
    [data-testid="stDataFrame"] { justify-content: center; display: flex; }
    section[data-testid="stSidebar"] { width: 300px !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 조회 설정")
    # 시작 날짜를 사용자가 직접 선택 (과거 날짜 선택 가능)
    default_start = datetime.now().date() - timedelta(days=7) # 기본값은 일주일 전
    start_date = st.date_input("📅 조회 시작일", default_start)
    duration_days = st.slider("📆 조회 기간(일)", min_value=7, max_value=90, value=30)
    
    st.divider()
    user_name = st.selectbox("👤 내 이름 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- 4. 근무 로직 및 데이터 생성 ---
st.markdown("<div class='main-title'>성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
st.markdown(f"<div class='period-text'>{start_date} 부터 {duration_days}일간의 일정입니다.</div>", unsafe_allow_html=True)

cal_list = []
end_date = start_date + timedelta(days=duration_days)

# 조회 시작일부터 종료일까지 하루씩 체크
check_date = start_date
while check_date <= end_date:
    diff_days = (check_date - PATTERN_START_DATE).days
    
    # 3일 간격 근무일 계산 (3/9 기준 나머지가 0인 날)
    if diff_days % 3 == 0:
        shift_count = diff_days // 3
        cycle_idx = (shift_count // 2) % 3 
        is_second_day = shift_count % 2 == 1
        
        # 패턴 배정
        if cycle_idx == 0: # 김태언 회관
            h, a, b = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
        elif cycle_idx == 1: # 이정석 회관
            h, a, b = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
        else: # 이태원 회관
            h, a, b = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
            
        wd = check_date.weekday()
        day_str = f"{check_date.strftime('%m/%d')}({['월','화','수','목','금','토','일'][wd]})"
        
        cal_list.append({
            "날짜": day_str,
            "조장": "황재업",
            "회관": h,
            "의산(A)": a,
            "의산(B)": b
        })
    check_date += timedelta(days=1)

# 데이터프레임 생성
df_cal = pd.DataFrame(cal_list)

# --- 5. 스타일링 및 출력 ---
def style_cells(val):
    # 요일별 색상
    if "(토)" in str(val): return 'color: #1E88E5; font-weight: bold;'
    if "(일)" in str(val): return 'color: #E53935; font-weight: bold;'
    # 강조 이름 색상
    if user_name != "안 함" and str(val) == user_name:
        return f'background-color: {WORKER_COLORS.get(user_name, "white")}; color: black; font-weight: bold;'
    return 'color: black;'

if not df_cal.empty:
    st.dataframe(
        df_cal.style.applymap(style_cells),
        use_container_width=True,
        hide_index=True,
        height=min(len(df_cal) * 36 + 40, 600) # 데이터 양에 따라 높이 조절
    )
else:
    st.warning("선택한 기간에 근무일이 없습니다.")

st.caption("💡 사이드바에서 '조회 시작일'을 변경하면 지난 일정도 확인할 수 있습니다.")
