import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 및 서열 데이터 ---
START_DATE = datetime(2026, 3, 24).date()
RANK = ["김태언", "이태원", "이정석"]  # 선임 -> 후임 순
HALL_ROTATION = ["김태언", "이정석", "이태원"] # 회관 2회 연속 순번
WORKER_COLORS = {
    "황재업": "#E1F5FE", "이태원": "#F3E5F5", 
    "이정석": "#FFFDE7", "김태언": "#E8F5E9", "안 함": "#FFFFFF"
}

# --- 2. 근무 로직 (이미지 분석 및 사용자 설명 반영) ---
def get_daily_layout(target_date):
    diff = (target_date - START_DATE).days
    if diff % 3 != 0: return None
    
    # 3/27부터 김태언 2회 시작되도록 오프셋 조정
    seq = (diff // 3) + 5 
    hall_worker = HALL_ROTATION[(seq // 2) % 3]
    others = [p for p in RANK if p != hall_worker]
    
    # 회관 1회차: 선임A-후임B / 2회차: 후임A-선임B
    if seq % 2 == 0:
        return hall_worker, others[0], others[1]
    else:
        return hall_worker, others[1], others[0]

# --- 3. UI 및 스타일링 ---
st.set_page_config(page_title="성의교정 C조", layout="centered")

with st.sidebar:
    st.header("👤 설정")
    menu = st.radio("메뉴", ["📅 근무 편성표", "📍 오늘 상황판"])
    selected_user = st.selectbox("강조할 이름 선택", ["안 함", "황재업"] + RANK)

# [수정] 가장 안정적인 스타일 적용 함수 (데이터프레임 전체 스캔)
def style_dataframe(df, target_name):
    def _color_background(val):
        # 개별 셀의 값이 선택된 이름과 일치하는지 확인
        if target_name != "안 함" and val == target_name:
            color = WORKER_COLORS.get(target_name, "#F0F0F0")
            return f'background-color: {color}; font-weight: bold; border: 2px solid #555;'
        return ''
    
    # 줄 전체 강조를 위한 로직
    def _highlight_row(s):
        if target_name != "안 함" and target_name in s.values:
            color = WORKER_COLORS.get(target_name, "#F0F0F0")
            return [f'background-color: {color}; color: black; font-weight: bold;'] * len(s)
        return [''] * len(s)

    return df.style.apply(_highlight_row, axis=1)

# --- 4. 화면 출력 ---
if menu == "📅 근무 편성표":
    st.subheader("📅 성의교정 C조 근무 편성표")
    
    data = []
    for i in range(60):
        d = START_DATE + timedelta(days=i)
        res = get_daily_layout(d)
        if res:
            h, a, b = res
            data.append({
                "날짜": f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][d.weekday()]})",
                "조장": "황재업", "회관": h, "의산A": a, "의산B": b
            })
    
    df = pd.DataFrame(data)
    # 스타일 적용
    st.dataframe(
        style_dataframe(df, selected_user),
        use_container_width=True,
        hide_index=True
    )

elif menu == "📍 오늘 상황판":
    st.subheader("📍 C조 실시간 상황판")
    sel_date = st.date_input("날짜 선택", datetime.now().date())
    res = get_daily_layout(sel_date)
    
    if res:
        h, a, b = res
        st.info(f"💡 {sel_date} : **조장(황재업), 회관({h}), 의산A({a}), 의산B({b})**")
        
        # 시간표 데이터 (이미지 499070.png 기준)
        board_data = pd.DataFrame({
            "시간": ["07:00", "08:00", "09:00", "10:00", "11:00", "12:00"],
            "황재업(조)": ["안내실", "안내실", "안내실", "휴게", "안내실", "중식"],
            f"{h}(회)": ["로비", "휴게", "순찰", "안내실", "중식", "안내실"],
            f"{a}(A)": ["휴게", "로비", "로비", "순찰/휴", "중식", "로비"],
            f"{b}(B)": ["로비", "휴게", "휴게", "로비", "로비", "중식"]
        })
        
        st.dataframe(
            style_dataframe(board_data, selected_user),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("비번입니다.")
