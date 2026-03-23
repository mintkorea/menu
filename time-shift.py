import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 시간 변환 및 계산 로직 ---
def format_time(excel_val):
    if pd.isna(excel_val): return ""
    total_seconds = int(round(excel_val * 24 * 3600))
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}"

# --- 2. C조 상세 시간표 데이터 (120분 합산 구간 반영) ---
RAW_DATA = [
    {"No": "1", "시작": 0.2916, "종료": 0.3125, "할당": "60분", "조장": "안내실", "대원": "로비", "당직A": "로비", "당직B": "휴게"},
    {"No": "2", "시작": 0.3333, "종료": 0.3750, "할당": "120분", "조장": "안내실", "대원": "휴게", "당직A": "휴게", "당직B": "로비"},
    {"No": "3", "시작": 0.3750, "종료": 0.4166, "할당": "60분", "조장": "안내실", "대원": "순찰", "당직A": "휴게", "당직B": "로비"},
    # [중요] No.4+5 통합 구간: 순찰부터 식사까지 총 120분
    {"No": "4-5", "시작": 0.4166, "종료": 0.5000, "할당": "120분", "조장": "휴게/로비", "대원": "안내실", "당직A": "로비/순찰", "당직B": "순찰(30)→휴게(30)→식사(60)"},
    {"No": "6", "시작": 0.5000, "종료": 0.5416, "할당": "60분", "조장": "순찰", "대원": "휴게", "당직A": "안내실", "당직B": "로비"},
    {"No": "7", "시작": 0.5416, "종료": 0.5833, "할당": "60분", "조장": "안내실", "대원": "휴게", "당직A": "로비", "당직B": "휴게"},
    {"No": "8", "시작": 0.5833, "종료": 0.6250, "할당": "60분", "조장": "로비", "대원": "순찰", "당직A": "휴게", "당직B": "안내실"},
    {"No": "9", "시작": 0.6250, "종료": 0.6666, "할당": "60분", "조장": "안내실", "대원": "휴게", "당직B": "로비", "당직B": "휴게"},
    {"No": "10", "시작": 0.6666, "종료": 0.7083, "할당": "60분", "조장": "휴게", "대원": "안내실", "당직A": "휴게", "당직B": "로비"},
    {"No": "야1", "시작": 0.7083, "종료": 0.7500, "할당": "60분", "조장": "안내실", "대원": "휴게", "당직A": "휴게", "당직B": "로비"},
    {"No": "야2", "시작": 0.7500, "종료": 0.7916, "할당": "60분", "조장": "안내실", "대원": "석식", "당직A": "로비", "당직B": "석식"},
]

# --- 3. UI 및 출력 ---
st.subheader("🗓️ C조 근무 상황판 (시간 합산 로직)")

# (날짜 선택 및 인원 계산 로직은 이전과 동일)
selected_date = st.sidebar.date_input("날짜", datetime.now().date())
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    # 당일 인원 확정
    a_rotation = ["이태원", "김태언", "이정석"]
    idx = (days_diff // 3)
    a_worker = a_rotation[(idx // 2) % 3]
    others = [n for n in ["김태언", "이태원", "이정석"] if n != a_worker]
    # 선임순 정렬 (김 > 이태 > 이정) - 편의상 간략화
    others.sort(key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x])
    b_worker, c_worker = (others[1], others[0]) if idx % 2 == 1 else (others[0], others[1])

    st.info(f"✅ **{selected_date}** | A: {a_worker} | B: {b_worker} | C: {c_worker}")

    # 데이터 프레임 생성
    table_data = []
    for r in RAW_DATA:
        table_data.append({
            "시작": format_time(r["시작"]),
            "종료": format_time(r["종료"]),
            "시간": r["할당"],
            "황재업(조)": r["조장"],
            f"{a_worker}(A)": r["대원"],
            f"{b_worker}(B)": r["당직A"],
            f"{c_worker}(C)": r["당직B"]
        })

    # 스타일 적용 (120분 구간 강조)
    df = pd.DataFrame(table_data)
    st.dataframe(
        df.style.apply(lambda x: ['background-color: #4a1a1a' if x['시간'] == '120분' else '' for _ in x], axis=1),
        use_container_width=True, hide_index=True
    )

    st.markdown("""
    > **💡 당직 B(C) 필독:** > 10:00~12:00 구간은 **[순찰 30분 → 휴게 30분 → 식사 60분]**으로 이어지는 통합 120분 근무입니다.
    """)
