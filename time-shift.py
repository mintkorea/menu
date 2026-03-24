import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (모바일 최적화 폰트 조절) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 3.2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 22px !important; font-weight: 800; text-align: center; }
    
    /* 버튼 스타일: 눈에 잘 띄는 파란색 버튼 */
    .stButton > button {
        width: 100%;
        border-radius: 10px;
        height: 3em;
        background-color: #1E3A5F;
        color: white;
        font-weight: bold;
    }

    /* 다이얼로그 내 표 폰트 강제 축소 (개행 방지) */
    .full-table-style td, .full-table-style th {
        font-size: 11px !important;
        white-space: nowrap !important;
        padding: 4px 2px !important;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 및 데이터 (기존 로직 유지) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
if now.hour < 7:
    target_date = (now - timedelta(days=1)).date()
else:
    target_date = now.date()

# [중략: get_workers_by_date 함수 및 time_data 정의 부분은 동일]
# (인원 배정 jojang, seonghui, uisanA, uisanB 로직 포함)

# ---------------------------------------------------------
# 팝업 창(새 창)으로 전체 시간표 띄우기 함수
@st.dialog("📅 당일 전체 시간표 (07:00 ~ 익일 07:00)")
def show_full_schedule(df):
    st.write(f"기준 날짜: {target_date.strftime('%Y-%m-%d')}")
    # 건물 헤더 다시 표시
    st.markdown(f"""<div style="display: flex; border: 1px solid #dee2e6; font-weight: bold; text-align: center; font-size: 12px;">
                <div style="width: 25%; padding: 5px 0;">시간</div>
                <div style="width: 37.5%; background:#FFF2CC;">성의회관</div>
                <div style="width: 37.5%; background:#D9EAD3;">의산연</div>
                </div>""", unsafe_allow_html=True)
    
    # 폰트가 깨지지 않게 HTML 클래스 적용하여 출력
    st.markdown('<div class="full-table-style">', unsafe_allow_html=True)
    st.table(df)
    st.markdown('</div>', unsafe_allow_html=True)
# ---------------------------------------------------------

# --- [3] 화면 구성 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    
    # 상단 요약 카드 (기존과 동일)
    # ... [생략] ...

    st.write("") # 간격 조절
    
    # 🟢 핵심 변경: 전체 시간표 버튼을 상단에 배치
    if st.button("📋 당일 전체 시간표 크게 보기"):
        show_full_schedule(df_rt)

    st.markdown("---")
    st.markdown("**▼ 현재 근무 상세**")
    
    # 메인 화면의 표는 아주 작게, 현재 근무 행만 강조해서 표시
    st.table(df_rt.iloc[curr_idx:curr_idx+1].style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r), axis=1))

# [tab2 근무 편성표 로직 유지]
