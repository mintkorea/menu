import streamlit as st
import pandas as pd
from datetime import datetime
import pytz

# --- [1] 설정 및 CSS (스크린샷 스타일 반영) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2rem !important; }
    
    /* 표 헤더 위쪽 건물명 섹션 */
    .b-header-container {
        display: flex;
        margin-top: 20px;
        border: 1px solid #dee2e6;
        border-bottom: none;
        font-weight: bold;
        text-align: center;
    }
    .b-time { width: 150px; background: #fff; padding: 8px 0; border-right: 1px solid #dee2e6; }
    .b-seongui { flex: 1; background: #FFF2CC; padding: 8px 0; border-right: 1px solid #dee2e6; }
    .b-uysan { flex: 1; background: #D9EAD3; padding: 8px 0; }

    /* 테이블 스타일 */
    [data-testid="stTable"] { font-size: 15px !important; margin-top: 0px !important; }
    thead tr th { background-color: #f8f9fa !important; color: #333 !important; text-align: center !important; }
    thead tr th:first-child { display:none; }
    tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 데이터 로직 및 함수 정의 (NameError 방지) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)

# 현재 근무자 명단 (패턴에 따라 동적으로 변하게 하려면 이전 get_workers 함수 사용)
# 여기서는 예시로 스크린샷의 성함을 고정합니다.
j_name, s_name, a_name, b_name = "황재업", "이태원", "이정석", "김태언"

def get_curr_idx(h, m, df):
    if h == 1 and m < 40: return 16
    if h == 1 and m >= 40: return 17
    for i, row in df.iterrows():
        try:
            sh, eh = int(row['From'].split(':')[0]), int(row['To'].split(':')[0])
            if eh == 0 or eh < sh: eh = 24
            if sh <= h < eh: return i
        except: continue
    return len(df) - 1

# 전체 시간표 데이터
time_raw = [
    ["07:00", "08:00"], ["08:00", "09:00"], ["09:00", "10:00"], ["10:00", "11:00"],
    ["11:00", "12:00"], ["12:00", "13:00"], ["13:00", "14:00"], ["14:00", "15:00"],
    ["15:00", "16:00"], ["16:00", "17:00"], ["17:00", "18:00"], ["18:00", "19:00"],
    ["19:00", "20:00"], ["20:00", "21:00"], ["21:00", "22:00"], ["22:00", "23:00"],
    ["23:00", "01:40"], ["01:40", "02:00"], ["02:00", "05:00"], ["05:00", "06:00"], ["06:00", "07:00"]
]
loc_raw = [
    ["안내실", "로비", "로비", "휴게"], ["안내실", "휴게", "휴게", "로비"],
    ["순찰", "안내실", "휴게", "로비"], ["휴게", "안내실", "로비", "순찰"],
    ["안내실", "중식", "로비", "중식"], ["중식", "안내실", "중식", "로비"],
    ["안내실", "휴게", "순찰", "로비"], ["순찰", "안내실", "로비", "휴게"],
    ["안내실", "휴게", "로비", "휴게"], ["휴게", "안내실", "휴게", "로비"],
    ["안내실", "휴게", "휴게", "로비"], ["안내실", "석식", "로비", "석식"],
    ["안내실", "안내실", "석식", "로비"], ["석식", "안내실", "로비", "휴게"],
    ["안내실", "순찰", "로비", "휴게"], ["순찰", "안내실", "순찰", "로비"],
    ["안내실", "휴게", "휴게", "로비"], ["안내실", "안내실", "로비", "로비"],
    ["휴게", "안내실", "로비", "휴게"], ["안내실", "순찰", "로비", "순찰"], ["안내실", "안내실", "휴게", "로비"]
]

# ⭐️ 수정: 열 헤더에 실근무자 성함 배치
df_full = pd.DataFrame([t + l for t, l in zip(time_raw, loc_raw)], 
                       columns=["From", "To", j_name, s_name, a_name, b_name])

# 현재 인덱스 찾기 및 데이터 필터링 (상단 고정)
idx = get_curr_idx(now.hour, now.minute, df_full)
df_display = df_full.iloc[idx:].copy()

# --- [3] 화면 출력 ---
st.title("🕒 C조 실시간 근무 현황")

# ⭐️ 표 바로 위에 건물명 헤더 배치 (스크린샷 구조)
st.markdown(f"""
    <div class="b-header-container">
        <div class="b-time">구분 (시간)</div>
        <div class="b-seongui">성의회관</div>
        <div class="b-uysan">의산연</div>
    </div>
""", unsafe_allow_html=True)

# 표 출력 (현재 행 하이라이트)
st.table(df_display.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == idx else ['']*len(r), axis=1))
