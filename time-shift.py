import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import streamlit.components.v1 as components

# --- [1] 설정 및 CSS (셀 너비 및 정렬 고정) ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { padding-top: 3.2rem !important; max-width: 500px; margin: auto; }
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 16px !important; text-align: center; margin-bottom: 15px; color: #555; }
    
    /* 현황판 카드 스타일 */
    .status-container { display: grid; grid-template-columns: repeat(2, 1fr); gap: 8px; margin-bottom: 15px; }
    .status-card { border: 2px solid #2E4077; border-radius: 10px; padding: 8px 0; text-align: center; background: #F8F9FA; }
    .worker-name { font-size: 14px !important; font-weight: 700; color: #444; }
    .status-val { font-size: 17px; font-weight: 900; color: #C04B41; }
    
    /* 표 너비 비율 고정 */
    .b-header { display: flex; border: 1px solid #dee2e6; border-bottom: none; font-weight: bold; text-align: center; font-size: 13px; }
    .bh-time { width: 30%; background: #f8f9fa; border-right: 1px solid #dee2e6; padding: 7px 0; }
    .bh-sh { width: 35%; background: #FFF2CC; border-right: 1px solid #dee2e6; padding: 7px 0; }
    .bh-us { width: 35%; background: #D9EAD3; padding: 7px 0; }

    [data-testid="stTable"] table { width: 100% !important; table-layout: fixed !important; }
    [data-testid="stTable"] th, [data-testid="stTable"] td { padding: 6px 2px !important; text-align: center !important; font-size: 11px !important; }
    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 공통 데이터 및 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
PATTERN_START = datetime(2026, 3, 9).date()

# 연락망 데이터
security_contacts = [
    {"g": "top", "p": "보안반장", "n": "유정수", "t": "010-5316-8065"},
    {"g": "top", "p": "보안소장", "n": "이규용", "t": "010-8883-6580"},
    {"g": "top", "p": "부소장", "n": "박상현", "t": "010-3193-4603"},
    {"g": "top", "p": "보안반장", "n": "오제준", "t": "010-3352-8933"},
    {"g": "a", "p": "조장", "n": "배준용", "t": "010-4717-7065"},
    {"g": "b", "p": "조장", "n": "심규천", "t": "010-8287-9895"},
    {"g": "c", "p": "조장", "n": "황재업", "t": "010-9278-6622"},
    {"g": "c", "p": "조원", "n": "이태원", "t": "010-9265-7881"},
    {"g": "c", "p": "조원", "n": "김태언", "t": "010-5386-5386"},
    {"g": "c", "p": "조원", "n": "이정석", "t": "010-2417-1173"}
]

def get_workers_by_date(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

# --- [3] 화면 구성 (탭별 독립 블록) ---
tab1, tab2, tab3 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표", "📞 비상 연락망"])

# 1. 실시간 현황 탭
with tab1:
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="title-sub">{now.strftime("%Y-%m-%d %H:%M:%S")}</div>', unsafe_allow_html=True)
    
    j, s, a, b = get_workers_by_date(now.date())
    if j is None: j, s, a, b = "황재업", "김태언", "이태원", "이정석"

    time_data = [
        ["07:00", "08:00", "안내실", "로비", "로비", "휴게"], ["08:00", "09:00", "안내실", "휴게", "휴게", "로비"],
        ["13:00", "14:00", "안내실", "휴게", "순찰", "로비"], ["14:00", "15:00", "순찰", "안내실", "로비", "휴게"],
        ["15:00", "16:00", "안내실", "휴게", "로비", "휴게"] # 예시 데이터 단축
    ]
    df_rt = pd.DataFrame(time_data, columns=["From", "To", j, s, a, b])
    
    # 상단 요약 카드
    st.markdown(f"""<div class="status-container">
        <div class="status-card"><div class="worker-name">{j}</div><div class="status-val">안내실</div></div>
        <div class="status-card"><div class="worker-name">{s}</div><div class="status-val">휴게</div></div>
    </div>""", unsafe_allow_html=True)
    
    st.markdown('<div class="b-header"><div class="bh-time">시간</div><div class="bh-sh">성의회관</div><div class="bh-us">의산연</div></div>', unsafe_allow_html=True)
    st.table(df_rt)

# 2. 근무 편성표 탭 (오류 수정 핵심)
with tab2:
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    
    # 탭 내부 위젯
    c1, c2 = st.columns(2)
    with c1: start_d = st.date_input("📅 시작일", now.date(), key="date_sel")
    with c2: dur = st.slider("📆 일수", 7, 60, 31, key="slider_sel")

    cal_list = []
    for i in range(dur):
        d = start_d + timedelta(days=i)
        w_j, w_s, w_a, w_b = get_workers_by_date(d)
        if w_j: cal_list.append({"날짜": d.strftime("%m/%d(%a)"), "조장": w_j, "성희": w_s, "의산A": w_a, "의산B": w_b})
    
    if cal_list:
        st.dataframe(pd.DataFrame(cal_list), use_container_width=True, hide_index=True)
    else:
        st.info("해당 기간에 C조 근무가 없습니다.")

# 3. 비상 연락망 탭
with tab3:
    st.markdown('<div class="unified-title">보안팀 비상 연락망</div>', unsafe_allow_html=True)
    
    contact_html = """
    <style>
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; }
        .card { height: 42px; border-radius: 4px; border: 1px solid #eee; text-align: center; cursor: pointer; background: #fff9db; }
        .n { font-size: 13px; font-weight: bold; display: block; margin-top: 10px; }
    </style>
    <div class="grid">
    """
    for m in security_contacts:
        contact_html += f'<div class="card" onclick="alert(\'{m["t"]}\')"><span class="n">{m["n"]}</span></div>'
    contact_html += "</div>"
    
    components.html(contact_html, height=400)
