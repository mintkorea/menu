import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (디자인 정밀 조정) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    /* 1. 상단 여백 (기존보다 약간 줄임) */
    .block-container { padding-top: 2.2rem !important; }
    
    /* 2. 타이틀 및 시간 (시간 폰트 +2pt 확대) */
    .unified-title { 
        font-size: 26px !important; 
        font-weight: 800 !important;
        text-align: center; 
        margin-bottom: 5px; 
        color: #1E1E1E; 
    }
    .title-sub { 
        font-size: 17px !important; /* 기존 15px -> 17px 확대 */
        text-align: center; 
        margin-bottom: 15px; 
        color: #555; 
        font-weight: 500;
    }
    
    /* 3. 카드 섹션 (높이 더 낮추고 콤팩트하게) */
    .status-container { 
        display: grid; 
        grid-template-columns: repeat(2, 1fr); 
        gap: 8px; 
        margin-bottom: 15px; 
    }
    .status-card { 
        border: 2px solid #2E4077; 
        border-radius: 10px; 
        padding: 5px 0px; /* 패딩 최소화 */
        text-align: center; 
        background: #F8F9FA; 
        min-height: 60px; /* 높이 더 낮춤 */
    }
    .worker-name { 
        font-size: 16.5px !important; /* 표 내부 폰트보다 확실히 크게 */
        font-weight: 700; 
        color: #444; 
        margin-bottom: 0px; 
    }
    .status-val { 
        font-size: 19px; 
        font-weight: 900; 
        color: #C04B41; 
    }
    
    /* 4. 테이블 스타일 (줄간격 및 폰트 축소) */
    [data-testid="stTable"] td { 
        padding: 2px 0 !important; 
        font-size: 13px !important; /* 표 내부 이름 폰트 축소 */
        line-height: 1.1 !important;
        height: 28px !important;
        text-align: center !important; 
    }
    
    /* 탭 메뉴 스타일 강조 */
    .stTabs [data-baseweb="tab-list"] { gap: 20px; justify-content: center; }
    .stTabs [data-baseweb="tab"] { font-weight: bold; font-size: 16px; }

    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜/시간 및 근무자 패턴 로직 (기존 유지) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers_by_date(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

jojang, seonghui, uisanA, uisanB = get_workers_by_date(now.date())
is_work_day = jojang is not None

# --- [3] 화면 구성 ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y년 %m월 %d일 %H:%M:%S")}</div>', unsafe_allow_html=True)

    if not is_work_day:
        st.warning("📅 오늘은 C조 휴무일입니다.")
        jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

    time_data = [
        ["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
        ["09:00", "10:00", "순찰", "안내실", "휴게", "로비"], ["10:00", "11:00", "휴게", "안내실", "로비", "순찰"],
        ["11:00", "12:00", "안내실", "중식", "로비", "중식"], ["12:00", "13:00", "중식", "안내실", "중식", "로비"],
        ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
        ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"], ["16:00", "17:00", "휴게", "안내실", "휴게", "로비"],
        ["17:00", "18:00", "안내실", "휴게", "휴게", "로비"], ["18:00", "19:00", "안내실", "석식", "로비", "석식"],
        ["19:00", "20:00", "안내실", "안내실", "석식", "로비"], ["20:00", "21:00", "석식", "안내실", "로비", "휴게"],
        ["21:00", "22:00", "안내실", "순찰", "로비", "휴게"], ["22:00", "23:00", "순찰", "안내실", "순찰", "로비"],
        ["23:00", "01:40", "안내실", "휴게", "휴게", "로비"], ["01:40", "02:00", "안내실", "안내실", "로비", "로비"],
        ["02:00", "05:00", "휴게", "안내실", "로비", "휴게"], ["05:00", "06:00", "안내실", "순찰", "로비", "순찰"],
        ["06:00", "07:00", "안내실", "안내실", "휴게", "로비"],
    ]
    df_rt = pd.DataFrame(time_data, columns=["From", "To", "조장", "성의", "의생A", "의생B"])

    def get_rt_row(h, m):
        if h == 1 and m < 40: return df_rt[df_rt['From'] == "23:00"].iloc[0]
        if h == 1 and m >= 40: return df_rt[df_rt['From'] == "01:40"].iloc[0]
        for _, row in df_rt.iterrows():
            try:
                sh, eh = int(row['From'].split(':')[0]), int(row['To'].split(':')[0])
                if eh == 0: eh = 24
                if sh <= h < eh: return row
            except: continue
        return df_rt.iloc[-1]

    curr = get_rt_row(now.hour, now.minute)

    # 현황 카드 (높이 축소 및 폰트 강조)
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr['조장']}</div></div>
            <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{curr['성의']}</div></div>
            <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{curr['의생A']}</div></div>
            <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{curr['의생B']}</div></div>
        </div>
    """, unsafe_allow_html=True)

    # 표 출력 (초슬림 스타일 적용)
    st.table(df_rt.style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.equals(curr) and is_work_day else ['']*len(r), axis=1))

with tab2:
    # (탭 2 로직은 기존 소스와 동일하게 유지)
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    # ... (생략된 탭 2 코드 그대로 사용) ...
