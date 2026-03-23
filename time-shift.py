import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 ---
START_DATE = datetime(2026, 3, 24).date()
RANK = ["김태언", "이태원", "이정석"]  # 선임 -> 후임 서열
HALL_ROTATION = ["김태언", "이정석", "이태원"]
WORKER_COLORS = {
    "황재업": "#E1F5FE", 
    "이태원": "#F3E5F5", 
    "이정석": "#FFFDE7", 
    "김태언": "#E8F5E9",
    "안 함": "#FFFFFF"
}

# --- 2. 로직 함수 ---
def get_daily_layout(target_date):
    diff = (target_date - START_DATE).days
    if diff % 3 != 0: return None
    
    seq = (diff // 3) + 5 
    hall_worker = HALL_ROTATION[(seq // 2) % 3]
    others = [p for p in RANK if p != hall_worker]
    
    # 회관 1회차: 선임A-후임B / 2회차: 후임A-선임B
    if seq % 2 == 0:
        return hall_worker, others[0], others[1]
    else:
        return hall_worker, others[1], others[0]

# --- 3. UI 및 CSS ---
st.set_page_config(page_title="성의교정 C조", layout="centered")

# 강조 스타일 함수 (행 전체에 적용)
def highlight_row(row, target_name):
    if target_name != "안 함" and target_name in row.values:
        color = WORKER_COLORS.get(target_name, "#F0F0F0")
        return [f'background-color: {color}; font-weight: bold; color: black;'] * len(row)
    return [''] * len(row)

with st.sidebar:
    st.header("👤 개인 설정")
    menu = st.radio("메뉴", ["📅 근무 편성표", "📍 오늘 상황판"])
    selected_user = st.selectbox("강조할 이름 선택", ["안 함", "황재업"] + RANK)

# --- 4. 메인 화면 ---
if menu == "📅 근무 편성표":
    st.subheader("📅 성의교정 C조 근무 편성표")
    
    data = []
    # 3/24부터 60일치 생성
    for i in range(60):
        d = START_DATE + timedelta(days=i)
        res = get_daily_layout(d)
        if res:
            h, a, b = res
            data.append({
                "날짜": f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][d.weekday()]})",
                "조장": "황재업", 
                "회관": h, 
                "의산A": a, 
                "의산B": b
            })
    
    df = pd.DataFrame(data)
    
    # [핵심] 스타일 적용 후 출력
    styled_df = df.style.apply(highlight_row, target_name=selected_user, axis=1)
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        hide_index=True  # 인덱스(숫자) 숨기기
    )

elif menu == "📍 오늘 상황판":
    st.subheader("📍 C조 실시간 상황판")
    sel_date = st.date_input("조회 날짜", datetime.now().date())
    res = get_daily_layout(sel_date)
    
    if res:
        h, a, b = res
        st.info(f"💡 {sel_date} 근무: **조장(황재업), 회관({h}), 의산A({a}), 의산B({b})**")
        
        # 실제 시간표 데이터 예시 (상단에서 정의한 BASE_PATTERN 사용 권장)
        # 여기서는 구조 확인용으로 약식 생성
        sample_board = pd.DataFrame({
            "시간": ["07:00", "08:00", "09:00", "10:00"],
            "황재업(조)": ["안내실", "안내실", "안내실", "휴게"],
            f"{h}(회)": ["로비", "휴게", "순찰", "안내실"],
            f"{a}(A)": ["휴게", "로비", "로비", "순찰/휴"],
            f"{b}(B)": ["로비", "휴게", "휴게", "로비"]
        })
        
        styled_board = sample_board.style.apply(highlight_row, target_name=selected_user, axis=1)
        
        st.dataframe(
            styled_board,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("비번(휴무)입니다.")
