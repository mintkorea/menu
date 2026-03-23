import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

# --- 1. 기본 설정 ---
PATTERN_START_DATE = datetime(2026, 3, 9).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7"}
WEEKDAYS = ['월', '화', '수', '목', '금', '토', '일']

st.set_page_config(page_title="성의교정 C조 관리", layout="wide") # 달력은 넓게 보는게 좋습니다.

# --- 2. CSS 스타일 (중앙 정렬 및 표 디자인) ---
st.markdown("""
    <style>
    .main-title { font-size: 28px; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .sub-title { font-size: 16px; color: #666; text-align: center; margin-bottom: 20px; }
    /* DataFrame 중앙 정렬 */
    .stDataFrame { margin: 0 auto; }
    div[data-testid="stExpander"] div[role="button"] p { font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴", ["📅 월간 근무 달력", "📍 실시간 상황판"])
    user_name = st.selectbox("👤 이름 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])
    
    # 달력 이동을 위한 연/월 선택
    now = datetime.now()
    sel_year = st.selectbox("연도 선택", range(now.year - 1, now.year + 2), index=1)
    sel_month = st.selectbox("월 선택", range(1, 13), index=now.month - 1)

# --- 4. 근무 로직 함수 ---
def get_shift_info(target_date):
    """특정 날짜의 근무자 정보를 반환 (3/9 패턴 기준)"""
    diff_days = (target_date - PATTERN_START_DATE).days
    # 3일 간격 근무일인지 확인 (나머지가 0일 때가 근무일)
    if diff_days % 3 == 0:
        shift_count = diff_days // 3
        cycle_idx = (shift_count // 2) % 3 
        is_second_day = shift_count % 2 == 1
        
        if cycle_idx == 0: # 김태언 회관
            h, a, b = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
        elif cycle_idx == 1: # 이정석 회관
            h, a, b = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
        else: # 이태원 회관
            h, a, b = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
        return f"🏢{h}\n🅰️{a}\n🅱️{b}"
    return "" # 근무 없는 날

# --- 5. 화면 구현 ---
if menu == "📅 월간 근무 달력":
    st.markdown(f"<div class='main-title'>{sel_year}년 {sel_month}월 근무표</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-title'>🏢회관 / 🅰️의산A / 🅱️의산B</div>", unsafe_allow_html=True)

    # 달력 데이터 생성
    cal = calendar.monthcalendar(sel_year, sel_month)
    cal_data = []
    
    for week in cal:
        week_row = {}
        for idx, day in enumerate(week):
            day_name = ["월", "화", "수", "목", "금", "토", "일"][idx]
            if day == 0:
                week_row[day_name] = ""
            else:
                d = datetime(sel_year, sel_month, day).date()
                shift = get_shift_info(d)
                # 날짜 표시와 근무 정보 조합
                cell_content = f"[{day}]\n{shift}" if shift else f"[{day}]"
                week_row[day_name] = cell_content
        cal_data.append(week_row)

    df_cal = pd.DataFrame(cal_data)
    
    # --- 스타일링 함수 ---
    def style_calendar(val):
        style = 'white-space: pre-wrap; text-align: center; vertical-align: top; height: 100px; '
        if not val: return style
        
        # 강조 색상 적용
        if user_name != "안 함" and user_name in val:
            bg_color = WORKER_COLORS.get(user_name, "#FFFFFF")
            style += f'background-color: {bg_color}; font-weight: bold;'
        
        return style

    # 테이블 표시
    st.table(df_cal.style.applymap(style_calendar))
    
    st.caption("※ 3월 9일 패턴 시작일을 기준으로 과거 및 미래 날짜가 자동으로 계산됩니다.")

elif menu == "📍 실시간 상황판":
    st.info("실시간 상황판 메뉴입니다. 준비 중입니다.")
