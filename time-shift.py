import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- [1] 설정 및 CSS (디테일 수정) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; }
    
    /* 1. 링크 메뉴 복구 */
    .tab-menu { display: flex; justify-content: center; gap: 20px; border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 20px; }
    .tab-item { font-size: 15px; font-weight: bold; color: #888; text-decoration: none; cursor: pointer; }
    .tab-active { color: #C04B41; border-bottom: 3px solid #C04B41; padding-bottom: 10px; }

    /* 2. 타이틀 및 시간 (시간 폰트 +2pt 키움) */
    .title-area { text-align: center; margin-bottom: 20px; }
    .main-title { font-size: 26px !important; font-weight: 800; margin-bottom: 8px; }
    .sub-date { font-size: 17px !important; color: #555; font-weight: 500; } /* 기존 15px -> 17px */

    /* 3. 카드 부분 (높이 낮추고 폰트 재조정) */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-bottom: 20px; }
    .status-card { 
        border: 2px solid #2E4077; 
        border-radius: 10px; 
        padding: 8px 0; /* 높이 낮춤 (기존 12px -> 8px) */
        text-align: center; 
        background: #fff; 
    }
    /* 카드 성명: 표(14px)보다 크게 설정 */
    .card-name { font-size: 16px !important; font-weight: 700; color: #555; margin-bottom: 2px; }
    /* 현황 표시 폰트: 소폭 줄임 */
    .card-status { font-size: 20px !important; font-weight: 900; color: #C04B41; }

    /* 4. 하단 표 스타일 */
    .b-header { display: flex; border: 1px solid #dee2e6; border-bottom: none; font-weight: bold; text-align: center; font-size: 14px; }
    .b-section { width: 33.33%; padding: 8px 0; border-right: 1px solid #dee2e6; }
    
    [data-testid="stTable"] td { 
        padding: 4px 0 !important; 
        font-size: 14px !important; /* 표 성명 14px */
        text-align: center !important; 
    }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 데이터 처리 (기존 로직 유지) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
date_str = now.strftime("%Y년 %m월 %d일 %H:%M:%S")

names = ["황재업", "이태원", "이정석", "김태언"]
# ... (데이터 테이블 생략 - 기존 코드와 동일) ...
# (이하 데이터 프레임 df_full 및 idx 계산 로직 동일하게 삽입)

# --- [3] 화면 출력 ---

# 1. 링크 메뉴 (복구)
st.markdown(f"""
    <div class="tab-menu">
        <div class="tab-item tab-active">🕒 실시간 근무 현황</div>
        <div class="tab-item">📅 월간 근무 편성표</div>
    </div>
""", unsafe_allow_html=True)

# 2. 타이틀 및 시간 (+2pt 적용)
st.markdown(f"""
    <div class="title-area">
        <div class="main-title">C조 실시간 근무 현황</div>
        <div class="sub-date">{date_str}</div>
    </div>
""", unsafe_allow_html=True)

# 3. 요약 카드 (높이 낮춤, 폰트 비율 조정)
st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div class="card-name">{names[0]}</div><div class="card-status">{curr_row[names[0]]}</div></div>
        <div class="status-card"><div class="card-name">{names[1]}</div><div class="card-status">{curr_row[names[1]]}</div></div>
        <div class="status-card"><div class="card-name">{names[2]}</div><div class="card-status">{curr_row[names[2]]}</div></div>
        <div class="status-card"><div class="card-name">{names[3]}</div><div class="card-status">{curr_row[names[3]]}</div></div>
    </div>
""", unsafe_allow_html=True)

# 4. 건물 구분 헤더 및 표
st.markdown(f"""
    <div class="b-header">
        <div class="b-section" style="background:#fff;">구분 (시간)</div>
        <div class="b-section" style="background:#FFF2CC;">성의회관</div>
        <div class="b-section" style="background:#D9EAD3;">의산연</div>
    </div>
""", unsafe_allow_html=True)

st.table(df_full.iloc[idx:].style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == idx else ['']*len(r), axis=1))
