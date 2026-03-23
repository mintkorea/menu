import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 시간 변환 함수 ---
def format_time(excel_val):
    if pd.isna(excel_val) or isinstance(excel_val, str): return ""
    total_seconds = int(round(excel_val * 24 * 3600))
    return f"{total_seconds // 3600:02d}:{(total_seconds % 3600) // 60:02d}"

# --- 2. 정밀 데이터 구성 (KeyError 방지를 위해 명칭 통일) ---
# 당직B의 10:00~12:00(No.4+5) 120분 구간을 정확히 병합
RAW_DATA = [
    {"No": "1", "시작": 0.2916, "종료": 0.3125, "할당": "60분", "조장": "안내실", "대원": "로비", "A_loc": "로비", "B_loc": "휴게"},
    {"No": "2", "시작": 0.3333, "종료": 0.3750, "할당": "120분", "조장": "안내실", "대원": "휴게", "A_loc": "휴게", "B_loc": "로비"},
    {"No": "3", "시작": 0.3750, "종료": 0.4166, "할당": "60분", "조장": "안내실", "대원": "순찰", "A_loc": "휴게", "B_loc": "로비"},
    # [핵심] No.4와 5를 합친 120분 구간 (당직B: 순찰30+휴게30+식사60)
    {"No": "4-5", "시작": 0.4166, "종료": 0.5000, "할당": "120분", "조장": "휴게/로비", "대원": "안내실", "A_loc": "로비/순찰", "B_loc": "순찰(30)→휴게(30)→식사(60)"},
    {"No": "6", "시작": 0.5000, "종료": 0.5416, "할당": "60분", "조장": "순찰", "대원": "휴게", "A_loc": "안내실", "B_loc": "로비"},
    {"No": "7", "시작": 0.5416, "종료": 0.5833, "할당": "60분", "조장": "안내실", "대원": "휴게", "A_loc": "로비", "B_loc": "휴게"},
    {"No": "8", "시작": 0.5833, "종료": 0.6250, "할당": "60분", "조장": "로비", "대원": "순찰", "A_loc": "휴게", "B_loc": "안내실"},
    {"No": "9", "시작": 0.6250, "종료": 0.6666, "할당": "60분", "조장": "안내실", "대원": "휴게", "A_loc": "로비", "B_loc": "휴게"},
    {"No": "10", "시작": 0.6666, "종료": 0.7083, "할당": "60분", "조장": "휴게", "대원": "안내실", "A_loc": "휴게", "B_loc": "로비"},
    {"No": "야1", "시작": 0.7083, "종료": 0.7500, "할당": "60분", "조장": "안내실", "대원": "휴게", "A_loc": "휴게", "B_loc": "로비"},
    {"No": "야2", "시작": 0.7500, "종료": 0.7916, "할당": "60분", "조장": "안내실", "대원": "석식", "A_loc": "로비", "B_loc": "석식"},
]

st.title("🗓️ C조 근무 상황판")

# --- 3. 근무자 로직 ---
selected_date = st.sidebar.date_input("날짜 선택", datetime(2026, 3, 24).date())
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    idx = days_diff // 3
    a_rotation = ["이태원", "김태언", "이정석"]
    # 2일 주기 회관(A) 로직
    a_worker = a_rotation[(idx // 2) % 3]
    
    # 나머지 B, C 인원 (선임순: 김태언 > 이태원 > 이정석)
    all_members = ["김태언", "이태원", "이정석"]
    others = [m for m in all_members if m != a_worker]
    others.sort(key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x])
    
    # B/C 교대 로직 (2일차에 교대)
    if idx % 2 == 1:
        b_worker, c_worker = others[1], others[0]
    else:
        b_worker, c_worker = others[0], others[1]

    st.success(f"✅ **{selected_date}** | A(회관): {a_worker} | B(의산연): {b_worker} | C(의산연): {c_worker}")

    # --- 4. 테이블 생성 ---
    table_rows = []
    for r in RAW_DATA:
        table_rows.append({
            "시작": format_time(r["시작"]),
            "종료": format_time(r["종료"]),
            "시간": r["할당"],
            "황재업(조)": r["조장"],
            f"{a_worker}(A)": r["대원"],
            f"{b_worker}(B)": r["A_loc"], # 당직A 자리
            f"{c_worker}(C)": r["B_loc"]  # 당직B 자리
        })

    df = pd.DataFrame(table_rows)

    # 120분 구간 및 당직B의 특수 구간 강조
    def style_row(row):
        if row['시간'] == '120분':
            return ['background-color: #353535; color: #ffeb3b'] * len(row)
        return [''] * len(row)

    st.dataframe(df.style.apply(style_row, axis=1), use_container_width=True, hide_index=True)
    
    st.info("💡 **당직 B(C) 안내**: 10:00~12:00(No.4-5)은 순찰(30분) → 휴게(30분) → 식사(60분)로 이어지는 총 120분 과정입니다.")

else:
    st.warning("C조 근무일이 아닙니다.")
