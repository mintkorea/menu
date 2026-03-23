import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 (서열 및 로테이션) ---
START_DATE = datetime(2026, 3, 24).date()
RANK = ["김태언", "이태원", "이정석"]  # 선임 -> 후임 순
HALL_ROTATION = ["김태언", "이정석", "이태원"]
WORKER_COLORS = {
    "황재업": "#E1F5FE", "이태원": "#F3E5F5", 
    "이정석": "#FFFDE7", "김태언": "#E8F5E9", "안 함": "#FFFFFF"
}

# --- 2. 근무 로직 ---
def get_daily_layout(target_date):
    diff = (target_date - START_DATE).days
    if diff % 3 != 0: return None
    seq = (diff // 3) + 5 
    hall_worker = HALL_ROTATION[(seq // 2) % 3]
    others = [p for p in RANK if p != hall_worker]
    if seq % 2 == 0:
        return hall_worker, others[0], others[1]
    else:
        return hall_worker, others[1], others[0]

# --- 3. UI 및 CSS 설정 (중앙 정렬 강제) ---
st.set_page_config(page_title="성의교정 C조", layout="centered")

st.markdown("""
    <style>
    /* 전체 표 내용 중앙 정렬 */
    [data-testid="stDataFrame"] td, [data-testid="stDataFrame"] th {
        text-align: center !important;
    }
    /* 테이블을 화면 중앙으로 배치 */
    .stDataFrame {
        margin-left: auto;
        margin-right: auto;
    }
    .main-title {
        text-align: center;
        color: #1E3A8A;
        font-weight: bold;
        font-size: 24px;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 사이드바 ---
with st.sidebar:
    st.header("👤 설정")
    menu = st.radio("메뉴", ["📅 근무 편성표", "📍 오늘 상황판"])
    selected_user = st.selectbox("강조할 이름 선택", ["안 함", "황재업"] + RANK)

# 강조 스타일 함수
def highlight_row(row):
    if selected_user != "안 함" and selected_user in row.values:
        color = WORKER_COLORS.get(selected_user, "#F0F0F0")
        return [f'background-color: {color}; font-weight: bold; color: black;'] * len(row)
    return [''] * len(row)

# --- 5. 화면 출력 ---
if menu == "📅 근무 편성표":
    st.markdown("<div class='main-title'>📅 성의교정 C조 근무 편성표</div>", unsafe_allow_html=True)
    
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
    # 스타일 적용 (중앙 정렬 CSS와 함께 작동)
    st.dataframe(
        df.style.apply(highlight_row, axis=1),
        use_container_width=True,
        hide_index=True
    )

elif menu == "📍 오늘 상황판":
    st.markdown("<div class='main-title'>📍 C조 실시간 상황판</div>", unsafe_allow_html=True)
    sel_date = st.date_input("날짜 선택", datetime.now().date())
    res = get_daily_layout(sel_date)
    
    if res:
        h, a, b = res
        st.info(f"💡 {sel_date} : **조장(황재업), 회관({h}), 의산A({a}), 의산B({b})**")
        
        # 시간표 데이터 (이미지 499070.png 기반)
        board_data = pd.DataFrame([
            {"시간": "07:00", "조": "안내실", "회": "로비", "A": "휴게", "B": "로비"},
            {"시간": "08:00", "조": "안내실", "회": "휴게", "A": "로비", "B": "휴게"},
            {"시간": "09:00", "조": "안내실", "회": "순찰", "A": "로비", "B": "휴게"},
            {"시간": "10:00", "조": "휴게", "회": "안내실", "A": "순찰/휴", "B": "로비"},
            # ... 필요한 만큼 추가 가능
        ])
        # 컬럼명에 근무자 이름 반영
        board_data.columns = ["시간", "황재업(조)", f"{h}(회)", f"{a}(A)", f"{b}(B)"]
        
        st.dataframe(
            board_data.style.apply(highlight_row, axis=1),
            use_container_width=True,
            hide_index=True
        )
    else:
        st.warning("비번입니다.")
