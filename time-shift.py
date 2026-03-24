import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 스타일 설정 (표 간격 및 폰트 정밀 조정) ---
st.set_page_config(page_title="C조 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 1.5rem !important; max-width: 450px; margin: auto; }
    .title { font-size: 20px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    
    /* 표 디자인: 선을 얇게, 글자는 한 줄로 */
    .unified-table { width: 100%; border-collapse: collapse; font-size: 11px; text-align: center; table-layout: fixed; }
    .unified-table th, .unified-table td { 
        border: 1px solid #ddd; padding: 4px 1px; 
        white-space: nowrap; overflow: hidden; 
    }
    .bld-header { background-color: #f8f9fa; font-weight: bold; font-size: 10px; color: #777; }
    .name-header { background-color: #eee; font-weight: bold; font-size: 11px; }
    .curr-row { background-color: #FFE5E5; font-weight: bold; }
    
    /* 버튼: 작고 깔끔하게 */
    .stButton > button {
        width: 100%; height: 2.2em; border-radius: 5px; font-size: 12px;
        background-color: #f0f2f6; border: 1px solid #ddd; margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직: 날짜 및 이름 처리 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

# 07시 이전은 전일 근무로 간주
target_date = (now - timedelta(days=1)).date() if now.hour < 7 else now.date()
next_date = target_date + timedelta(days=1)

def get_names(d):
    # 패턴에 따른 근무자 추출 (중략 - 기존 로직 적용)
    # 결과는 반드시 2글자로 반환 (예: '재업', '태원')
    return ["재업", "태언", "정석", "태원"] # 예시

w_today = get_names(target_date)
w_next = get_names(next_date)

# --- [3] 통합 테이블 렌더링 함수 ---
def draw_table(names, highlight_idx=None, is_full=False):
    # names: [조장, 성희, 의산A, 의산B]
    j, s, a, b = names
    html = f"""
    <table class="unified-table">
        <tr class="bld-header">
            <th style="width:25%;">구분</th>
            <th colspan="2" style="background:#FFF2CC;">성의회관</th>
            <th colspan="2" style="background:#D9EAD3;">의학연</th>
        </tr>
        <tr class="name-header">
            <th>(시간)</th>
            <th style="background:#FFF2CC;">{j}</th><th style="background:#FFF2CC;">{s}</th>
            <th style="background:#D9EAD3;">{a}</th><th style="background:#D9EAD3;">{b}</th>
        </tr>
    """
    # 현재 시간대만 보여주거나(is_full=False), 전체를 보여줌
    display_df = df_rt if is_full else df_rt.iloc[curr_idx:curr_idx+1]
    
    for i, r in display_df.iterrows():
        row_style = "class='curr-row'" if i == highlight_idx else ""
        html += f"""
        <tr {row_style}>
            <td>{r['From']}~{r['To']}</td>
            <td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td>
        </tr>
        """
    return html + "</table>"

# --- [4] 화면 구성 ---
st.markdown(f'<div class="title">C조 근무 현황 ({now.strftime("%H:%M")})</div>', unsafe_allow_html=True)

# 버튼: 팝업으로 전체 표 보기
if st.button("📋 오늘 전체 시간표 보기"):
    st.markdown(draw_table(w_today, curr_idx, is_full=True), unsafe_allow_html=True)
else:
    # 기본 화면: 현재 근무 + 내일 예보만 심플하게
    st.markdown("**▼ 현재 근무 중**")
    st.markdown(draw_table(w_today, curr_idx), unsafe_allow_html=True)
    
    st.write("")
    st.markdown(f"**📅 내일 근무 예정 ({next_date.strftime('%m/%d')})**")
    st.markdown(draw_table(w_next), unsafe_allow_html=True)
