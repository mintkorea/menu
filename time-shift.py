import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- [1] CSS: 표 헤더 및 레이아웃 설정 ---
st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; }
    /* 건물명 섹션 스타일 */
    .building-header {
        display: grid; grid-template-columns: 140px 1fr 1fr; /* From/To 너비 제외 분할 */
        text-align: center; font-weight: bold; background-color: #F0F2F6;
        border: 1px solid #dee2e6; border-bottom: none;
    }
    .b-section { padding: 5px 0; border-right: 1px solid #dee2e6; }
    
    /* 카드 디자인 */
    .status-container { 
        display: grid; grid-template-columns: repeat(2, 1fr); 
        gap: 8px; margin-bottom: 15px; 
    }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 10px; 
        padding: 8px 0; text-align: center; background: #F8F9FA;
        min-height: 60px; display: flex; flex-direction: column; justify-content: center;
    }
    .status-val { font-size: 19px; font-weight: 800; color: #C04B41; }
    
    /* 테이블 인덱스 숨기기 */
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 데이터 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
# 근무자 명단 추출 (사용자 스크린샷 기준)
j, s, a, b = "황재업", "이태원", "이정석", "김태언" 

# 시간 및 위치 데이터
time_raw = [["07:00", "08:00"], ["08:00", "09:00"], ["09:00", "10:00"], ["10:00", "11:00"], ["11:00", "12:00"], ["12:00", "13:00"]] # ... 생략
loc_raw = [["안내실", "로비", "로비", "휴게"], ["안내실", "휴게", "휴게", "로비"], ["순찰", "안내실", "휴게", "로비"], ["휴게", "안내실", "로비", "순찰"], ["안내실", "중식", "로비", "중식"], ["중식", "안내실", "중식", "로비"]]

# ⭐️ 수정사항: 표 헤더에 실근무자 성함 배치
df_full = pd.DataFrame([t + l for t, l in zip(time_raw, loc_raw)], 
                       columns=["From", "To", j, s, a, b])

idx = get_curr_idx(now.hour, now.minute) # 현재 시간 인덱스 계산 로직
df_display = df_full.iloc[idx:].copy()

# --- [3] 화면 출력 ---
st.subheader("🕒 C조 실시간 근무 현황")

# 상단 요약 카드
st.markdown(f"""
    <div class="status-container">
        <div class="status-card"><div style="font-size:14px; color:#666;">{j}</div><div class="status-val">{df_full.iloc[idx][j]}</div></div>
        <div class="status-card"><div style="font-size:14px; color:#666;">{s}</div><div class="status-val">{df_full.iloc[idx][s]}</div></div>
        <div class="status-card"><div style="font-size:14px; color:#666;">{a}</div><div class="status-val">{df_full.iloc[idx][a]}</div></div>
        <div class="status-card"><div style="font-size:14px; color:#666;">{b}</div><div class="status-val">{df_full.iloc[idx][b]}</div></div>
    </div>
""", unsafe_allow_html=True)

# ⭐️ 수정사항: 표 바로 위에 건물명 헤더 배치
st.markdown(f"""
    <div class="building-header">
        <div class="b-section" style="background:#fff; border-left:1px solid #dee2e6;">시간</div>
        <div class="b-section" style="background:#FFF2CC;">성의회관</div>
        <div class="b-section" style="background:#D9EAD3; border-right:1px solid #dee2e6;">의산연</div>
    </div>
""", unsafe_allow_html=True)

# 표 출력
st.table(df_display.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == idx else ['']*len(r), axis=1))
