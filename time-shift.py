import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 기본 설정 및 연차 데이터 로드 ---
START_DATE = datetime(2026, 3, 24).date()
RANK = ["김태언", "이태원", "이정석"]
HALL_ROTATION = ["김태언", "이정석", "이태원"]
VACATION_FILE = 'vacation.csv'

def get_vacation_list(target_date):
    """특정 날짜에 연차인 사람 리스트 반환"""
    if os.path.exists(VACATION_FILE):
        df_vac = pd.read_csv(VACATION_FILE)
        # 날짜 형식 통일 후 필터링
        df_vac['날짜'] = pd.to_datetime(df_vac['날짜']).dt.date
        return df_vac[df_vac['날짜'] == target_date]['이름'].tolist()
    return []

# --- 2. 근무 배정 로직 (연차 반영 버전) ---
def get_daily_layout_with_vac(target_date):
    diff = (target_date - START_DATE).days
    if diff % 3 != 0: return None
    
    seq = (diff // 3) + 5 
    hall_worker = HALL_ROTATION[(seq // 2) % 3]
    others = [p for p in RANK if p != hall_worker]
    
    # 기본 배정 (회관, 의산A, 의산B)
    if seq % 2 == 0:
        res = [hall_worker, others[0], others[1]]
    else:
        res = [hall_worker, others[1], others[0]]
    
    # [핵심] 연차 체크 및 치환
    vac_people = get_vacation_list(target_date)
    final_res = []
    for person in res:
        if person in vac_people:
            final_res.append(f"🔴연차({person})") # 이름 옆에 표시하거나 '연차'로 치환
        else:
            final_res.append(person)
            
    return final_res # [회관, A, B] 순서

# --- 3. 화면 출력 (HTML 방식 적용) ---
def render_work_table(data_list):
    html = """
    <style>
        .work-table { width: 100%; border-collapse: collapse; text-align: center; }
        .work-table th, .work-table td { border: 1px solid #ddd; padding: 10px; }
        .vacation-row { background-color: #FFEBEE; font-weight: bold; } /* 연차 발생 시 줄 강조 */
    </style>
    <table class="work-table">
        <thead>
            <tr><th>날짜</th><th>조장</th><th>회관</th><th>의산A</th><th>의산B</th></tr>
        </thead>
        <tbody>
    """
    for row in data_list:
        # 줄에 '연차'라는 글자가 있으면 배경색 변경
        is_vac = any("연차" in str(v) for v in row.values())
        row_style = "class='vacation-row'" if is_vac else ""
        
        html += f"<tr {row_style}>"
        for key in row:
            html += f"<td>{row[key]}</td>"
        html += "</tr>"
    html += "</tbody></table>"
    st.markdown(html, unsafe_allow_html=True)

# --- 4. 메인 실행부 ---
st.subheader("🗓️ 연차 연동 C조 근무표")

display_data = []
for i in range(30): # 30일치
    d = START_DATE + timedelta(days=i)
    res = get_daily_layout_with_vac(d)
    if res:
        display_data.append({
            "날짜": d.strftime('%m/%d(%a)'),
            "조장": "황재업",
            "회관": res[0],
            "의산A": res[1],
            "의산B": res[2]
        })

render_work_table(display_data)
