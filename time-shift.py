import streamlit as st
import pandas as pd

# 페이지 설정 (모바일 최적화 및 넓은 화면)
st.set_page_config(layout="wide")

# CSS: 탭 디자인 및 상단 고정 (사용자님 스타일 반영)
st.markdown("""
    <style>
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        height: 45px;
        background-color: #f8f9fa;
        border-radius: 4px;
        font-weight: bold;
    }
    </style>
    """, unsafe_allow_html=True)

# 메인 탭 구성 (사용자님 요청 3대 핵심 탭)
tab1, tab2, tab3 = st.tabs(["📊 근무현황판", "📝 근무편성표", "📅 근무달력"])

# --- [탭 1: 근무현황판] ---
with tab1:
    st.subheader("오늘의 근무 현황")
    # 현재 근무자, 순찰 구역(Gamma Knife Center 등) 정보를 보여주는 로직
    st.info("현재 옴니버스 파크 시설 관리 및 근무 중입니다.")

# --- [탭 2: 근무편성표] ---
with tab2:
    st.subheader("주간 근무 편성표")
    # C-조(황재업, 김태언, 이태원, 이정석 등)의 교대 명단 로직
    # (이전에 작업하시던 데이터 테이블 형태를 여기에 배치)

# --- [탭 3: 근무달력] ---
with tab3:
    st.subheader("월간 근무 스케줄")
    # 달력 형태로 근무일을 시각화하는 부분
    # (Streamlit 달력 라이브러리 혹은 표 형식 활용)

# 플로팅 TOP 버튼 (작업 중 요청하셨던 기능)
st.markdown("""
    <div style="position: fixed; bottom: 20px; right: 20px; z-index: 100;">
        <button onclick="window.scrollTo(0, 0);" style="border-radius: 50%; width: 50px; height: 50px; background-color: #007bff; color: white; border: none; cursor: pointer;">TOP</button>
    </div>
    """, unsafe_allow_html=True)
