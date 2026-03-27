import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, date
import pytz
import calendar
import streamlit.components.v1 as components

# --- [1] 페이지 설정 및 스타일 (탭 및 표 헤더 최적화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    /* 상단 여백 5mm (약 20px) */
    .block-container { padding-top: 20px !important; max-width: 500px; margin: auto; }
    
    /* [해결] 탭 메뉴 가로 꽉 차게 설정 */
    .stTabs [data-baseweb="tab-list"] { 
        gap: 0px; 
        display: flex; 
        width: 100%;
    }
    .stTabs [data-baseweb="tab"] {
        flex: 1; 
        text-align: center;
        height: 40px; 
        background-color: #f0f2f6; 
        padding: 0px !important; 
        font-weight: 800; 
        font-size: 12px !important; 
    }
    .stTabs [aria-selected="true"] { background-color: #2E4077 !important; color: white !important; }
    
    /* [해결] 현황 부분 셀 헤더 최적화 (건물명/근무자 일치) */
    .table-container { width: 100%; border: 1px solid #dee2e6; border-radius: 5px; overflow-x: auto; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 11px; text-align: center; table-layout: fixed; }
    .custom-table td, .custom-table th { border: 1px solid #dee2e6; padding: 6px 1px; word-break: break-all; }
    .header-bg-sung { background-color: #FFF2CC; font-weight: 800; }
    .header-bg-ui { background-color: #D9EAD3; font-weight: 800; }

    /* 플로팅 버튼 스타일 */
    #scrollToTopBtn {
        position: fixed; bottom: 20px; right: 20px; z-index: 99;
        width: 45px; height: 45px; background-color: #2E4077; color: white;
        border: none; border-radius: 50%; cursor: pointer; font-weight: bold; font-size: 20px;
    }
    </style>
    
    <button onclick="window.scrollTo({top: 0, behavior: 'smooth'})" id="scrollToTopBtn" title="Go to top">▲</button>
    """, unsafe_allow_html=True)

# --- [2] 핵심 로직 ---
kst = pytz.timezone('Asia/Seoul')
now_kst = datetime.now(kst)
today_kst = now_kst.date()
PATTERN_START = date(2026, 3, 9)

def get_workers(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

def get_shift_simple(dt):
    diff = (dt - PATTERN_START).days
    return ["C", "A", "B"][diff % 3]

# --- [3] 탭 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 근무현황", "📅 편성표", "🏥 근무달력"])

with tab1:
    st.markdown(f'<div style="text-align:center; font-size:14px; color:666;">{now_kst.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    is_prep = (5 <= now_kst.hour < 7) or (now_kst.hour == 5 and now_kst.minute >= 30)
    work_date = today_kst if (now_kst.hour >= 7 or is_prep) else (today_kst - timedelta(days=1))
    names = get_workers(work_date) or ("황재업", "김태언", "이태원", "이정석")
    
    # 실시간 카드
    st.markdown(f'''<div style="display:grid; grid-template-columns: repeat(2, 1fr); gap:6px; margin-bottom:10px;">
        <div style="border:2px solid #2E4077; border-radius:10px; padding:6px; text-align:center;">
            <div style="font-size:12px;">{names[0]}</div><div style="font-size:15px; font-weight:900; color:#C04B41;">안내실</div>
        </div>
        <div style="border:2px solid #2E4077; border-radius:10px; padding:6px; text-align:center;">
            <div style="font-size:12px;">{names[1]}</div><div style="font-size:15px; font-weight:900; color:#C04B41;">로비</div>
        </div>
    </div>''', unsafe_allow_html=True)

    data_list = [["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"], ["09:00", "10:00", "안내실", "순찰", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "휴게"], ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"], ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"], ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"], ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"], ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"], ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"], ["23:00", "00:00", "안내실", "휴게", "휴게", "로비"], ["00:00", "01:00", "안내실", "휴게", "휴게", "로비"], ["01:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"], ["02:00", "03:00", "휴게", "안내실", "로비", "휴게"], ["03:00", "04:00", "휴게", "안내실", "로비", "휴게"], ["04:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"]]
    
    idx = find_idx(now_kst) # 이전 코드의 find_idx 함수 사용
    rows_html = "".join([f"<tr{' style=\"background:#FFE5E5;\"' if i==0 else ''}><td>{r[0]}</td><td>{r[1]}</td><td>{r[2]}</td><td>{r[3]}</td><td>{r[4]}</td><td>{r[5]}</td></tr>" for i, r in enumerate(data_list[idx:])])
    
    # [해결] 표 헤더 2단 구조 최적화
    st.markdown(f'''<div class="table-container"><table class="custom-table">
        <tr style="background:#f4f4f4; font-weight:bold;"><td colspan="2">시간</td><td colspan="2" class="header-bg-sung">성의회관</td><td colspan="2" class="header-bg-ui">의산연</td></tr>
        <tr style="background:#fff; font-weight:bold;"><td>From</td><td>To</td><td>{names[0]}</td><td>{names[1]}</td><td>{names[2]}</td><td>{names[3]}</td></tr>
        {rows_html}</table></div>''', unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="main-title">📅 근무 편성표</div>', unsafe_allow_html=True)
    # ... (편성표 로직 동일)

with tab3:
    st.markdown('<div class="main-title">🏥 근무달력 (12개월)</div>', unsafe_allow_html=True)
    # ... (12개월 달력 로직 동일)
    # [중요] 12개월 반복 루프 적용 (range(12))
