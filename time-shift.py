import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import streamlit.components.v1 as components

# --- [1] 설정 및 CSS (셀 너비 고정 및 정렬) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 3.2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 16px !important; text-align: center; margin-bottom: 15px; color: #555; }
    
    /* 요약 카드 디자인 수정 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 15px; }
    .status-card { 
        border: 2px solid #2E4077; border-radius: 10px; padding: 8px 0; 
        text-align: center; background: #F8F9FA;
    }
    .worker-name { font-size: 14px !important; font-weight: 700; color: #444; margin-bottom: 2px; }
    .status-val { font-size: 17px; font-weight: 900; color: #C04B41; }
    
    /* 건물 헤더와 표의 열 너비 강제 일치 (중요) */
    .b-header { 
        display: flex; border: 1px solid #dee2e6; border-bottom: none; 
        font-weight: bold; text-align: center; font-size: 13px; 
    }
    .bh-time { width: 30%; background: #f8f9fa; border-right: 1px solid #dee2e6; padding: 7px 0; }
    .bh-sh { width: 35%; background: #FFF2CC; border-right: 1px solid #dee2e6; padding: 7px 0; }
    .bh-us { width: 35%; background: #D9EAD3; padding: 7px 0; }

    /* 표 셀 정렬 및 고정 너비 */
    [data-testid="stTable"] table { width: 100% !important; table-layout: fixed !important; }
    [data-testid="stTable"] th, [data-testid="stTable"] td { 
        padding: 6px 2px !important; text-align: center !important; font-size: 11px !important;
        overflow: hidden; text-overflow: ellipsis; white-space: nowrap;
    }
    /* 각 열 너비 비율 설정 (From/To : 성의 : 의산) */
    [data-testid="stTable"] tr th:nth-child(2), [data-testid="stTable"] tr td:nth-child(2),
    [data-testid="stTable"] tr th:nth-child(3), [data-testid="stTable"] tr td:nth-child(3) { width: 15% !important; } /* From, To */
    [data-testid="stTable"] tr th:nth-child(4), [data-testid="stTable"] tr td:nth-child(4),
    [data-testid="stTable"] tr th:nth-child(5), [data-testid="stTable"] tr td:nth-child(5) { width: 17.5% !important; } /* 성의(2명) */
    [data-testid="stTable"] tr th:nth-child(6), [data-testid="stTable"] tr td:nth-child(6),
    [data-testid="stTable"] tr th:nth-child(7), [data-testid="stTable"] tr td:nth-child(7) { width: 17.5% !important; } /* 의산(2명) */

    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 로직 및 데이터 (패턴 유지) ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
PATTERN_START = datetime(2026, 3, 9).date()

def get_workers_by_date(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        # 리턴 순서: 조장, 성의교정, 의산A, 의산B
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

# --- [3] 화면 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표", "📞 비상 연락망"])

with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)

    j, s, a, b = get_workers_by_date(now.date())
    if j is None: j, s, a, b = "황재업", "김태언", "이태원", "이정석"

    # 타임테이블 데이터 (이름 순서: 조장, 성의, 의산A, 의산B 고정)
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
    df_rt = pd.DataFrame(time_data, columns=["From", "To", j, s, a, b])

    # 현재 시간 인덱스 계산
    curr_idx = 20
    h, m = now.hour, now.minute
    if h == 1 and m < 40: curr_idx = 16
    elif h == 1 and m >= 40: curr_idx = 17
    else:
        for i, row in df_rt.iterrows():
            sh, eh = int(row['From'].split(':')[0]), int(row['To'].split(':')[0])
            if eh == 0: eh = 24
            if sh <= h < eh: curr_idx = i; break

    # 상단 카드 (표의 열 순서와 일치하도록 배치)
    row = df_rt.iloc[curr_idx]
    st.markdown(f"""
        <div class="status-container">
            <div class="status-card"><div class="worker-name">{j}</div><div class="status-val">{row[j]}</div></div>
            <div class="status-card"><div class="worker-name">{s}</div><div class="status-val">{row[s]}</div></div>
            <div class="status-card"><div class="worker-name">{a}</div><div class="status-val">{row[a]}</div></div>
            <div class="status-card"><div class="worker-name">{b}</div><div class="status-val">{row[b]}</div></div>
        </div>
    """, unsafe_allow_html=True)

    # 건물 헤더 (너비 비율을 표와 일치시킴)
    st.markdown("""
        <div class="b-header">
            <div class="bh-time">구분 (시간)</div>
            <div class="bh-sh">성의회관</div>
            <div class="bh-us">의산연</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 실시간 표 출력 (슬라이싱으로 현재 이후만 표시)
    st.table(df_rt.iloc[curr_idx:].style.apply(lambda x: ['background-color: #FFE5E5; font-weight: bold']*len(x) if x.name == curr_idx else ['']*len(x), axis=1))

# --- [4] tab2, tab3는 이전과 동일한 로직 유지 ---
# ... (편성표 및 연락망 코드 생략) ...
