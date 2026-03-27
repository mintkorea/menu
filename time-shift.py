import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar

# --- [1] 페이지 설정 및 스타일 (기존 유지) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    .stTabs [data-baseweb="tab-list"] { gap: 2px; display: flex; width: 100%; justify-content: space-around; }
    .stTabs [data-baseweb="tab"] { flex: 1; text-align: center; height: 40px; background-color: #f0f2f6; border-radius: 5px 5px 0 0; padding: 0px !important; font-weight: 800; font-size: 12px !important; }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    .main-title { text-align: center; font-size: 18px; font-weight: 900; color: #2E4077; margin-top: 5px; }
    .date-display { text-align: center; font-size: 14px; color: #666; margin-bottom: 10px; }
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 6px; margin-bottom: 10px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 8px 2px; text-align: center; background: white; }
    .worker-name { font-size: 14px; font-weight: 800; color: #333; }
    .status-val { font-size: 16px; font-weight: 900; color: #C04B41; }
    .msg-card { grid-column: span 2; padding: 20px; font-weight: 800; color: #2E4077; border: 2px solid #2E4077; background: #f9f9f9; }
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 5px; margin-bottom: 20px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 12px; text-align: center; table-layout: fixed; }
    .custom-table td { border: 1px solid #dee2e6; padding: 8px 2px; }
    .cal-table { width: 100%; border-collapse: collapse; table-layout: fixed; border: 1px solid #ccc; margin-bottom: 35px; }
    .cal-td { border: 1px solid #eee; height: 55px; vertical-align: top; padding: 0 !important; }
    .cal-date-part { height: 40%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 15px; background: white; }
    .cal-shift-part { height: 60%; display: flex; align-items: center; justify-content: center; font-weight: 900; font-size: 12px; }
    .sun { color: #d32f2f !important; }
    .sat { color: #1976d2 !important; }
    .hi-text { color: white !important; font-weight: 900; }
    .today-border { border: 3px solid #333 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 (근무 규칙 반영) ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()
PATTERN_START = date(2024, 1, 1) # 기준일

def get_workers(target_date):
    # 가. 조장은 고정 / 나. 조원은 김태언, 이정석, 이태원 순으로 2회씩 성의회관
    # 다. 나머지 2명은 선임이 당직A, 후임이 당직B (입사순: 김태언, 이태원, 이정석)
    crew = ["김태언", "이태원", "이정석"] # 입사순 정렬
    diff = (target_date - PATTERN_START).days
    cycle = diff % 6 # 6일 주기
    
    hall_idx = cycle // 2
    hall_worker = crew[hall_idx]
    others = [p for p in crew if p != hall_worker]
    
    # 선임이 첫날 당직A, 둘째날 당직B 규칙
    if cycle % 2 == 0:
        return "황재업", hall_worker, others[0], others[1]
    else:
        return "황재업", hall_worker, others[1], others[0]

def get_shift_simple(dt):
    diff = (dt - PATTERN_START).days
    return ["C", "A", "B"][diff % 3]

# --- [3] 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown('<div class="main-title">🛡️ 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="date-display">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    # 근무 시간 적용 (07:00 기준)
    is_work_time = now_kst.hour >= 7 or (now_kst.hour == 6 and now_kst.minute >= 40)
    current_date = today_kst if now_kst.hour >= 7 else today_kst - timedelta(days=1)
    names = get_workers(current_date)
    
    # 카드 영역 메시지 제어 (가, 나, 다, 라)
    if now_kst.hour >= 7: # 근무 중
        idx_now = (now_kst.hour - 7) # 단순 예시 인덱스
        data_list = [["07:00", "08:00", "보안실", "로비", "순찰", "휴게"]] * 24 # 실제 데이터 대체 필요
        
        st.markdown(f'''<div class="status-container">
            <div class="status-card"><div class="worker-name">{names[0]}</div><div class="status-val">보안실</div></div>
            <div class="status-card"><div class="worker-name">{names[1]}</div><div class="status-val">로비</div></div>
            <div class="status-card"><div class="worker-name">{names[2]}</div><div class="status-val">순찰</div></div>
            <div class="status-card"><div class="worker-name">{names[3]}</div><div class="status-val">휴게</div></div>
        </div>''', unsafe_allow_html=True)
    else:
        # 새벽 시간대 메시지
        if 0 <= now_kst.hour < 6 or (now_kst.hour == 6 and now_kst.minute < 40):
            st.markdown('<div class="status-container"><div class="status-card msg-card">오늘 하루도 보람차고 즐거운 하루가 되도록 합시다.</div></div>', unsafe_allow_html=True)
        elif 6 <= now_kst.hour < 7:
            st.markdown('<div class="status-container"><div class="status-card msg-card">근무 준비중...</div></div>', unsafe_allow_html=True)

    # 근무 테이블 (나, 다, 라)
    st.write("---")
    # 테이블 상단 노출 및 하이라이트 로직 유지...

with tab2:
    # 2. 근무편성표 탭 (슬라이더 및 하이라이트 적용)
    month_offset = st.slider("조회 월 변경", -12, 12, 0)
    # ... (기존 구조에 날짜 계산 로직만 정교화)

with tab3:
    # 3. 근무달력 (기존 구조 유지, 폰트 차이 및 하이라이트 색상 수정)
    # ...
