import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 설정 및 데이터 관리 ---
st.set_page_config(page_title="보안 통합 관리 시스템", layout="wide")

def load_leaves():
    if os.path.exists('leave_data.csv'):
        return pd.read_csv('leave_data.csv')
    return pd.DataFrame(columns=['날짜', '성명', '대근자'])

# 인원 데이터 (사번, 생일 포함)
CONTACT_DATA = [
    {"id": 0, "조": "C조", "직위": "조원", "성명": "김태언", "연락처": "010-5386-5386", "사번": "2023001", "생일": "01월 01일"},
    {"id": 1, "조": "C조", "직위": "조원", "성명": "이태원", "연락처": "010-9265-7881", "사번": "2023002", "생일": "02월 02일"},
    {"id": 2, "조": "C조", "직위": "조원", "성명": "이정석", "연락처": "010-2417-1173", "사번": "2023003", "생일": "03월 03일"},
    {"id": 3, "조": "C조", "직위": "조장", "성명": "황재업", "연락처": "010-9278-6622", "사번": "2023004", "생일": "04월 04일"},
    # ... 추가 인원 데이터
]

# --- 2. C조 상세 시간표 데이터 (첨부파일 기반) ---
# 모바일 가독성을 위해 핵심 동선 위주로 재구성
TIMETABLE_DATA = [
    {"구분": "주간1", "시간": "07:00-07:30", "조장": "안내실", "대원(A)": "로비", "당직A(B)": "로비", "당직B(C)": "휴게"},
    {"구분": "주간2", "시간": "08:00-08:30", "조장": "안내실", "대원(A)": "휴게", "당직A(B)": "휴게", "당직B(C)": "로비"},
    {"구분": "주간4", "시간": "10:00-10:30", "조장": "휴게", "대원(A)": "안내실", "당직A(B)": "로비", "당직B(C)": "순찰"},
    {"구분": "주간7", "시간": "13:00-13:30", "조장": "안내실", "대원(A)": "휴게", "당직A(B)": "로비", "당직B(C)": "휴게"},
    {"구분": "석식", "시간": "18:00-19:00", "조장": "안내실", "대원(A)": "석식", "당직A(B)": "로비", "당직B(C)": "석식"},
    {"구분": "야간1", "시간": "19:00-19:30", "조장": "안내실", "대원(A)": "휴게", "당직A(B)": "휴게", "당직B(C)": "로비"},
    {"구분": "야간2", "시간": "20:00-21:00", "조장": "안내실", "대원(A)": "순찰", "당직A(B)": "로비", "당직B(C)": "휴게"},
]

menu = st.sidebar.selectbox("메뉴 선택", ["📱 비상연락망", "🗓️ C조 근무표 & 시간표", "📝 연차 관리"])

# --- [메뉴: 근무표 & 시간표] ---
if menu == "🗓️ C조 근무표 & 시간표":
    st.subheader("🗓️ C조 근무 편성 및 상세 시간표")
    
    # 1. 날짜 선택 및 편성 계산 (이전 로직 동일)
    today = datetime.now().date()
    selected_date = st.sidebar.date_input("조회 날짜 선택", today)
    
    base_date = datetime(2026, 3, 3).date()
    days_diff = (selected_date - base_date).days
    
    if days_diff >= 0 and days_diff % 3 == 0:
        count_idx = days_diff // 3
        a_rotation = ["이태원", "김태언", "이정석"]
        staff_rank = {"김태언": 1, "이태원": 2, "이정석": 3}
        
        a_worker = a_rotation[(count_idx // 2) % 3]
        others = sorted([n for n in staff_rank.keys() if n != a_worker], key=lambda x: staff_rank[x])
        b_worker, c_worker = others[0], others[1]
        if count_idx % 2 == 1: b_worker, c_worker = c_worker, b_worker
        
        # 상단 현황판
        st.markdown(f"""
            <div style="background:#f8f9fa; padding:10px; border-radius:10px; border-left:5px solid #2e7d32; margin-bottom:15px;">
                <h4 style="margin:0;">📅 {selected_date} C조 근무자</h4>
                <p style="margin:5px 0; font-size:14px;">
                    <b>조장:</b> 황재업 | <b>회관(A):</b> {a_worker} | <b>의산연(B):</b> {b_worker} | <b>의산연(C):</b> {c_worker}
                </p>
            </div>
        """, unsafe_allow_html=True)
        
        # 2. 상세 시간표 열람 (성명 매칭)
        st.write("🕒 **시간대별 상세 위치**")
        
        display_timetable = []
        for row in TIMETABLE_DATA:
            display_timetable.append({
                "시간": row["시간"],
                "황재업": row["조장"],
                a_worker: row["대원(A)"],
                b_worker: row["당직A(B)"],
                c_worker: row["당직B(C)"]
            })
            
        st.dataframe(
            pd.DataFrame(display_timetable),
            use_container_width=True,
            hide_index=True
        )
        
        st.caption("※ 표를 옆으로 밀어서 전체 시간을 확인하세요. (모바일 최적화)")
        
    else:
        st.warning("선택하신 날짜는 C조 근무일이 아닙니다.")

# --- 나머지 메뉴 (비상연락망, 연차관리)는 이전과 동일하게 유지 ---
