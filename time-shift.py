import streamlit as st
from datetime import datetime

# --- [v1.07] 실시간 근무지 상황판 전용 버전 ---
# 기준일: 3월 9일 (이날부터 3일 주기로 근무 판정)
PATTERN_START = datetime(2026, 3, 9).date()
st.set_page_config(page_title="C조 실시간 근무 현황", layout="wide")

# --- [1] CSS: 사용자 원본 박스 디자인 완벽 복구 ---
st.markdown("""
    <style>
    /* 헤더 간격 유지 */
    .block-container { padding-top: 3.5rem !important; }
    
    /* 타이틀 스타일 */
    .fixed-title { 
        font-size: 28px !important; 
        font-weight: 800 !important; 
        margin-bottom: 20px !important; 
        text-align: center;
    }
    
    /* 실시간 근무지 4칸 박스 */
    .status-container { 
        display: flex; 
        flex-direction: column; 
        gap: 12px; 
    }
    .status-card {
        border: 2px solid #2E4077; 
        border-radius: 12px;
        padding: 20px; 
        text-align: center; 
        background-color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .name-label { 
        font-size: 22px; 
        font-weight: 800; 
        color: #333; 
        margin-bottom: 10px; 
        border-bottom: 1px dotted #ccc; 
        padding-bottom: 5px;
    }
    .loc-label { 
        font-size: 26px; 
        font-weight: 800; 
        color: #C04B41; /* 이미지의 강조된 붉은색 */
    }
    </style>
    """, unsafe_allow_html=True)

# [타이틀 표시]
st.markdown('<div class="fixed-title">📅 C조 실시간 근무 현황</div>', unsafe_allow_html=True)

# --- [2] 실시간 근무 및 장소 판정 로직 ---
# 현재 날짜 및 시간 기준 (2026-03-24)
today = datetime.now().date()
days_diff = (today - PATTERN_START).days
is_workday = (days_diff % 3 == 0)

if is_workday:
    # 근무자 순번 계산
    sc = days_diff // 3
    ci, i2 = (sc // 2) % 3, sc % 2 == 1
    
    # 성희, 의산A, 의산B 배정 로직
    if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
    elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
    else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    
    # 실시간 근무지 매핑 (원본 이미지 기준)
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="name-label">황재업</div><div class="loc-label">안내실</div></div>
            <div class="status-card"><div class="name-label">{h}</div><div class="loc-label">로비</div></div>
            <div class="status-card"><div class="name-label">{a}</div><div class="loc-label">로비</div></div>
            <div class="status-card"><div class="name-label">{b}</div><div class="loc-label">휴게</div></div>
        </div>
    """, unsafe_allow_html=True)
else:
    st.warning("✅ 오늘은 C조 비번입니다.")

# 하단 업데이트 시간 표시
st.caption(f"최종 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
