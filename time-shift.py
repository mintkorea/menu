import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz

# --- [1] 설정 및 CSS (셀 너비 균등 및 디자인 최적화) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 2.5rem !important; }
    
    /* 타이틀 및 시간 (17.5px 확대) */
    .unified-title { font-size: 26px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 17.5px !important; text-align: center; margin-bottom: 20px; color: #555; font-weight: 500; }
    
    /* 카드 디자인 (높이 축소 및 성함 강조) */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 15px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 10px; padding: 6px 0; 
        text-align: center; background: #F8F9FA; min-height: 65px;
    }
    .worker-name { font-size: 17px !important; font-weight: 700; color: #444; margin-bottom: 2px; }
    .status-val { font-size: 19px; font-weight: 900; color: #C04B41; }
    
    /* 건물 헤더 스타일 */
    .b-header { display: flex; border: 1px solid #dee2e6; border-bottom: none; font-weight: bold; text-align: center; font-size: 13px; }
    .b-section { width: 33.33%; padding: 6px 0; border-right: 1px solid #dee2e6; }
    .b-section:last-child { border-right: none; }

    /* 표 스타일 (셀 너비 균등 16.6% & 폰트 12px) */
    [data-testid="stTable"] { width: 100% !important; table-layout: fixed !important; }
    [data-testid="stTable"] td { 
        width: 16.66% !important; 
        padding: 2px 0 !important; font-size: 12px !important; 
        line-height: 1.0 !important; height: 30px !important; text-align: center !important; 
    }
    
    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 날짜/시간 및 근무자 패턴 로직 (사용자님 원본 로직) ---
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

# --- [3] 화면 구성 (Tab 시스템) ---
tab1, tab2 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    if not is_work_day:
        st.warning("📅 오늘은 C조 휴무일입니다.")
        jojang, seonghui, uisanA, uisanB = "황재업", "김태언", "이태원", "이정석"

    # 표 데이터 (근무자 이름 변수 적용)
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
    # 헤더에 이름 넣기
    df_rt = pd.DataFrame(time_data, columns=["From", "To", jojang, seonghui, uisanA, uisanB])

    def get_rt_idx(h, m):
        if h == 1 and m < 40: return 16
        if h == 1 and m >= 40: return 17
        for i, row in df_rt.iterrows():
            sh, eh = int(row['From'].split(':')[0]), int(row['To'].split(':')[0])
            if eh == 0: eh = 24
            if sh <= h < eh: return i
        return 20

    curr_idx = get_rt_idx(now.hour, now.minute)
    curr_row = df_rt.iloc[curr_idx]

    # 상단 요약 카드
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{jojang}</div><div class="status-val">{curr_row[jojang]}</div></div>
            <div class="status-card"><div class="worker-name">{seonghui}</div><div class="status-val">{curr_row[seonghui]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanA}</div><div class="status-val">{curr_row[uisanA]}</div></div>
            <div class="status-card"><div class="worker-name">{uisanB}</div><div class="status-val">{curr_row[uisanB]}</div></div>
        </div>
    """, unsafe_allow_html=True)

    # ⭐️ 건물명 헤더 추가
    st.markdown(f"""
        <div class="b-header">
            <div class="b-section" style="background:#fff;">구분 (시간)</div>
            <div class="b-section" style="background:#FFF2CC;">성의회관</div>
            <div class="b-section" style="background:#D9EAD3;">의산연</div>
        </div>
    """, unsafe_allow_html=True)

    # ⭐️ 하이라이트 행을 맨 위로 (iloc[curr_idx:] 사용)
    st.table(df_rt.iloc[curr_idx:].style.apply(lambda r: ['background-color: #FFE5E5; font-weight: bold']*len(r) if r.name == curr_idx else ['']*len(r), axis=1))

with tab2:
    # 편성표 로직 (기존 유지)
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    # ... (생략된 Tab2 원본 코드 동일하게 사용)
