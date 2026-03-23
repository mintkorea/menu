import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 24시간 타임라인 생성 (07:00 ~ 익일 07:00) ---
def generate_24h_schedule(a_name, b_name, c_name):
    # 의산연 A(B근무자) 패턴: 1=근무(로비/순찰), 2=휴게/식사, 3=취침/대기 등
    # 사용자가 주신 패턴: 1, 2, 2, 1, 1, 2, 2, 1, 1, 2, 2, 1 (연속성 반영)
    pattern_a = ["근무", "휴게", "휴게", "근무", "근무", "휴게", "휴게", "근무", "근무", "휴게", "휴게", "근무", "취침", "취침", "취침", "근무"]
    # 당직 B(C근무자)는 A와 정반대
    pattern_b = ["휴게" if p == "근무" else "근무" for p in pattern_a]
    
    # 성의회관(A) 위치 로테이션 (1시간 단위)
    loc_a = ["로비", "휴게", "순찰", "안내실", "로비", "휴게", "순찰", "안내실"] * 3
    
    rows = []
    start_time = datetime.strptime("07:00", "%H:%M")
    
    for i in range(24):
        curr_time = (start_time + timedelta(hours=i)).strftime("%H:%M")
        next_time = (start_time + timedelta(hours=i+1)).strftime("%H:%M")
        
        # 의산연 패턴 적용 (순환)
        p_idx = i % len(pattern_a)
        
        rows.append({
            "시간": f"{curr_time} - {next_time}",
            f"{a_name}(회관A)": loc_a[i],
            f"{b_worker}(의산B)": "로비/순찰" if pattern_a[p_idx] == "근무" else "휴게/식사",
            f"{c_worker}(의산C)": "로비/순찰" if pattern_b[p_idx] == "근무" else "휴게/식사"
        })
    return rows

# --- 2. 앱 UI ---
st.set_page_config(layout="wide")
st.title("🛡️ C조 24시간 근무 상황판 (07시~07시)")

# 날짜 및 인원 로직 (3/24 기준)
selected_date = st.sidebar.date_input("조회 날짜", datetime(2026, 3, 24).date())
base_date = datetime(2026, 3, 3).date()
days_diff = (selected_date - base_date).days

if days_diff >= 0 and days_diff % 3 == 0:
    idx = days_diff // 3
    a_rotation = ["이태원", "김태언", "이정석"]
    a_worker = a_rotation[(idx // 2) % 3]
    others = sorted([m for m in ["김태언", "이태원", "이정석"] if m != a_worker], 
                   key=lambda x: {"김태언":1, "이태원":2, "이정석":3}[x])
    b_worker, c_worker = (others[1], others[0]) if idx % 2 == 1 else (others[0], others[1])

    st.success(f"📅 **{selected_date} C조 명단** | 회관: {a_worker} | 의산B: {b_worker} | 의산C: {c_worker}")

    # 상황판 생성
    data = generate_24h_schedule(a_worker, b_worker, c_worker)
    df = pd.DataFrame(data)

    # 시각적 가독성 스타일링
    def highlight_shift(s):
        if "로비" in s or "순찰" in s:
            return 'background-color: #1e3a8a; color: white;' # 근무 중 (남색)
        if "휴게" in s or "식사" in s:
            return 'background-color: #14532d; color: white;' # 휴게 중 (초록)
        return ''

    st.table(df) # 모바일 최적화 표

    st.info("""
    **💡 근무 원칙 요약**
    1. **매시 정각 교대**: 모든 근무지는 정각에 인원이 바뀝니다.
    2. **의산연 대칭 구조**: B근무자가 근무할 때 C근무자는 반드시 휴게합니다 (반대도 동일).
    3. **회관 독자 로테이션**: 회관 A는 의산연과 별개로 1시간마다 지정된 동선으로 이동합니다.
    """)

else:
    st.warning("C조 근무일이 아닙니다.")
