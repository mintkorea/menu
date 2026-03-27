import streamlit as st
import pandas as pd
from datetime import datetime

# 페이지 설정
st.set_page_config(page_title="Workplace Hub", layout="wide", initial_sidebar_state="collapsed")

# 모바일 최적화 및 스타일 설정
st.markdown("""
    <style>
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #f0f2f6;
        border-radius: 5px;
        padding: 5px 15px;
    }
    /* 플로팅 TOP 버튼 */
    .top-btn {
        position: fixed;
        bottom: 20px;
        right: 20px;
        background-color: #007bff;
        color: white;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 999;
        cursor: pointer;
    }
    </style>
    <a href="#top" class="top-btn">TOP</a>
    """, unsafe_allow_html=True)

# 메인 타이틀
st.title("🏢 Workplace Hub")

# 탭 생성 (현황, 근무달력, 연락처, 식단표)
tab1, tab2, tab3, tab4 = st.tabs(["📊 현황", "📅 근무달력", "📞 연락처", "🍴 식단표"])

with tab1:
    st.subheader("실시간 시설 현황")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("오늘의 업무", "시설 점검")
    with col2:
        st.metric("특이사항", "없음")
    st.write("---")
    st.info("의산연 및 옴니버스 파크 관리 모드입니다.")

with tab2:
    st.subheader("📅 C-조 근무달력 (3월)")
    # 근무자 명단 기반 스케줄 예시
    schedule = {
        "날짜": ["3/27", "3/28", "3/29", "3/30"],
        "주간": ["황재업", "김태언", "이태원", "이정석"],
        "야간": ["이정석", "안순재", "황재업", "김태언"]
    }
    st.table(pd.DataFrame(schedule))

with tab3:
    st.subheader("📞 비상 연락망")
    contacts = [
        {"성명": "황재업", "직책": "선임", "연락처": "010-XXXX-XXXX"},
        {"성명": "김태언", "직책": "대원", "연락처": "010-XXXX-XXXX"},
        {"성명": "이태원", "직책": "대원", "연락처": "010-XXXX-XXXX"},
        {"성명": "이정석", "직책": "대원", "연락처": "010-XXXX-XXXX"},
        {"성명": "안순재", "직책": "대원", "연락처": "010-XXXX-7979"} # 수정된 번호 반영
    ]
    st.dataframe(pd.DataFrame(contacts), use_container_width=True)

with tab4:
    st.subheader("🍴 주간 식단표")
    st.write("식단표 연동 기능을 준비 중입니다.")

