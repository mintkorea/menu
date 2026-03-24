import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (표 통합 및 개행 방지) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 3.2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 22px !important; font-weight: 800; text-align: center; margin-bottom: 20px; }
    
    /* 전체 시간표 보기 버튼 */
    .stButton > button {
        width: 100%; border-radius: 10px; height: 3.5em;
        background-color: #1E3A5F; color: white; font-weight: bold; margin-bottom: 20px;
    }

    /* 통합 테이블 스타일: 헤더와 본문을 하나처럼 연결 */
    .custom-table {
        width: 100%; border-collapse: collapse; text-align: center;
        font-family: sans-serif; table-layout: fixed; /* 칸 너비 고정 */
    }
    .custom-table th, .custom-table td {
        border: 1px solid #dee2e6; padding: 6px 2px;
        font-size: 11px; white-space: nowrap; overflow: hidden; /* 줄바꿈 절대 방지 */
    }
    .header-row { background-color: #f8f9fa; font-weight: bold; }
    .building-header { font-size: 12px; font-weight: bold; }
    .highlight-row { background-color: #FFE5E5; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# [로직 부분: target_date, jojang, seonghui, uisanA, uisanB 등 기존 코드 유지]
# ... (중략) ...

# --- [2] 통합 테이블 생성 함수 ---
def render_unified_table(df, highlight_idx=None):
    # 헤더 행 생성 (건물명 포함)
    html = f"""
    <table class="custom-table">
        <tr class="header-row">
            <th style="width: 20%;">시간</th>
            <th style="width: 20%; background:#FFF2CC;">성희</th>
            <th style="width: 20%; background:#FFF2CC;">{seonghui}</th>
            <th style="width: 20%; background:#D9EAD3;">의산A</th>
            <th style="width: 20%; background:#D9EAD3;">의산B</th>
        </tr>
    """
    # 데이터 행 생성
    for i, row in df.iterrows():
        row_class = "highlight-row" if i == highlight_idx else ""
        html += f"""
        <tr class="{row_class}">
            <td>{row['From']}~{row['To']}</td>
            <td>{row[jojang]}</td>
            <td>{row[seonghui]}</td>
            <td>{row[uisanA]}</td>
            <td>{row[uisanB]}</td>
        </tr>
        """
    html += "</table>"
    return html

# --- [3] 화면 구성 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    
    # 🟢 1. 새 창으로 전체 보기 (팝업 내에서도 통합 테이블 사용)
    @st.dialog("📅 당일 전체 시간표")
    def show_full():
        st.markdown(render_unified_table(df_rt, curr_idx), unsafe_allow_html=True)

    if st.button("📋 당일 전체 시간표 크게 보기"):
        show_full()

    # 🟢 2. 메인 화면: 현재 근무 (헤더와 본문이 합쳐진 형태)
    st.markdown("**▼ 현재 근무 상세**")
    # 현재 행(curr_idx)만 잘라서 통합 테이블로 렌더링
    st.markdown(render_unified_table(df_rt.iloc[curr_idx:curr_idx+1], curr_idx), unsafe_allow_html=True)

# [tab2 근무 편성표 로직 유지]
