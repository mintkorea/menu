import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 (서열 및 로테이션) ---
START_DATE = datetime(2026, 3, 24).date()
RANK = ["김태언", "이태원", "이정석"]  # 선임 -> 후임 서열
HALL_ROTATION = ["김태언", "이정석", "이태원"] # 회관 2회 연속 로직용
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "이정석": "#FFFDE7", "김태언": "#E8F5E9"}

# --- 2. 로직 함수 (입사순 및 회관 2회 연속 반영) ---
def get_daily_layout(target_date):
    diff = (target_date - START_DATE).days
    if diff % 3 != 0: return None
    
    # 3/24(이태원 회관 마지막)을 고려한 seq 설정
    seq = (diff // 3) + 5 
    hall_worker = HALL_ROTATION[(seq // 2) % 3]
    others = [p for p in RANK if p != hall_worker]
    
    # 회관 1회차: 선임A-후임B / 2회차: 후임A-선임B
    if seq % 2 == 0:
        return hall_worker, others[0], others[1]
    else:
        return hall_worker, others[1], others[0]

# --- 3. UI 및 스타일 설정 ---
st.set_page_config(page_title="성의교정 C조", layout="centered")

with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴", ["📅 근무 편성표", "📍 오늘 상황판"])
    user_name = st.selectbox("👤 이름 강조", ["안 함", "황재업"] + RANK)

# [수정] 행 전체 배경색 강조 함수
def apply_row_style(row):
    # 선택된 이름이 행의 어떤 값에라도 포함되어 있다면 강조
    if user_name != "안 함" and user_name in row.values:
        color = WORKER_COLORS.get(user_name, "#F0F0F0")
        return [f'background-color: {color}; font-weight: bold'] * len(row)
    return [''] * len(row)

# --- 4. 메인 화면 ---
if menu == "📅 근무 편성표":
    st.markdown("### 📅 성의교정 C조 근무 편성표")
    rows = []
    for i in range(60):
        d = START_DATE + timedelta(days=i)
        res = get_daily_layout(d)
        if res:
            h, a, b = res
            rows.append({
                "날짜": f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][d.weekday()]})",
                "조장": "황재업", "회관": h, "의산A": a, "의산B": b
            })
    
    df = pd.DataFrame(rows)
    # 스타일 적용 및 인덱스 숨기기
    st.dataframe(
        df.style.apply(apply_row_style, axis=1), 
        use_container_width=True, 
        hide_index=True
    )

elif menu == "📍 오늘 상황판":
    st.markdown("### 📍 C조 실시간 상황판")
    sel_date = st.date_input("날짜 선택", datetime.now().date())
    res = get_daily_layout(sel_date)
    
    if res:
        h, a, b = res
        st.success(f"**{sel_date} 근무자:** 조장(황재업), 회관({h}), 의산A({a}), 의산B({b})")
        
        # 시간표 구성 (간략화 예시)
        # 실제 BASE_PATTERN 데이터를 여기에 리스트로 넣으시면 됩니다.
        board_data = pd.DataFrame([
            {"시간": "07:00", "조장": "안내실", "회관": "로비", "의산A": "휴게", "의산B": "로비"},
            # ... 나머지 시간대 생략 ...
        ])
        
        # 컬럼명 변경 (근무자 이름 포함)
        board_data.columns = ["시간", "황재업(조)", f"{h}(회)", f"{a}(A)", f"{b}(B)"]
        
        # 스타일 적용
        st.dataframe(
            board_data.style.apply(apply_row_style, axis=1), 
            use_container_width=True, 
            hide_index=True
        )
    else:
        st.warning("비번입니다.")
