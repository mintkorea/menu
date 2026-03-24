import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import streamlit.components.v1 as components

# --- [1] 페이지 설정 및 스타일 ---
st.set_page_config(page_title="보안팀 통합 시스템", layout="wide")

st.markdown("""
    <style>
        .block-container { padding-top: 3.2rem !important; max-width: 500px; margin: auto; }
        .unified-title { font-size: 22px !important; font-weight: 800; text-align: center; margin-bottom: 20px; color: #222; }
        
        /* 테이블 폰트 및 간격 최적화 */
        [data-testid="stTable"] table { width: 100% !important; }
        [data-testid="stTable"] thead tr th { font-size: 12px !important; padding: 6px !important; text-align: center !important; background-color: #f8f9fa; }
        [data-testid="stTable"] td { font-size: 12px !important; padding: 6px !important; text-align: center !important; }
    </style>
""", unsafe_allow_html=True)

# --- [2] 데이터 및 C조 패턴 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
PATTERN_START = datetime(2026, 3, 9).date() # 패턴 기준일

# 보안팀 연락망 데이터
security_data = [
    {"g": "top", "p": "보안반장", "n": "유정수", "t": "010-5316-8065", "b": "1970.09.25", "e": "2020.09.01"},
    {"g": "top", "p": "보안소장", "n": "이규용", "t": "010-8883-6580", "b": "1972.03.01", "e": "-"},
    {"g": "top", "p": "보안부소장", "n": "박상현", "t": "010-3193-4603", "b": "1988.07.31", "e": "-"},
    {"g": "top", "p": "보안반장", "n": "오제준", "t": "010-3352-8933", "b": "1970.03.29", "e": "2022.05.18"},
    {"g": "a", "p": "보안조장", "n": "배준용", "t": "010-4717-7065", "b": "1969.12.24", "e": "2022.07.26"},
    {"g": "a", "p": "보안조원", "n": "이명구", "t": "010-8638-5819", "b": "1964.09.15", "e": "2025.03.21"},
    {"g": "a", "p": "보안조장", "n": "손병휘", "t": "010-9966-2090", "b": "1972.05.23", "e": "2016.05.05"},
    {"g": "a", "p": "보안조원", "n": "권순호", "t": "010-2539-1799", "b": "1980.12.14", "e": "2026.02.11"},
    {"g": "a", "p": "보안조원", "n": "김영중", "t": "010-7726-5963", "b": "1959.02.26", "e": "2024.08.21"},
    {"g": "a", "p": "보안조원", "n": "김삼동", "t": "010-2345-8081", "b": "1967.02.01", "e": "2025.05.02"},
    {"g": "a", "p": "보안조원", "n": "김전식", "t": "010-3277-0808", "b": "1966.07.23", "e": "2025.02.10"},
    {"g": "a", "p": "보안요원", "n": "공석", "t": "", "b": "-", "e": "-"},
    {"g": "b", "p": "보안조장", "n": "심규천", "t": "010-8287-9895", "b": "1967.04.10", "e": "2024.11.11"},
    {"g": "b", "p": "보안조원", "n": "임종현", "t": "010-7741-6732", "b": "1968.01.18", "e": "2021.08.10"},
    {"g": "b", "p": "보안조장", "n": "황일범", "t": "010-8929-4294", "b": "1969.05.30", "e": "2022.04.01"},
    {"g": "b", "p": "보안조원", "n": "이상길", "t": "010-9904-0247", "b": "1978.07.13", "e": "2024.09.11"},
    {"g": "b", "p": "보안조원", "n": "권영국", "t": "010-4085-9982", "b": "1969.07.20", "e": "2025.01.21"},
    {"g": "b", "p": "보안조원", "n": "전준수", "t": "010-5687-7107", "b": "1971.07.17", "e": "2025.04.03"},
    {"g": "b", "p": "보안조원", "n": "허용", "t": "010-8845-0163", "b": "1968.08.01", "e": "2026.01.16"},
    {"g": "b", "p": "보안요원", "n": "공석", "t": "", "b": "-", "e": "-"},
    {"g": "c", "p": "보안조장", "n": "황재업", "t": "010-9278-6622", "b": "1980.03.12", "e": "2023.05.26"},
    {"g": "c", "p": "보안조원", "n": "이태원", "t": "010-9265-7881", "b": "1963.11.23", "e": "2025.04.01"},
    {"g": "c", "p": "보안조장", "n": "피재영", "t": "010-9359-2569", "b": "1972.08.07", "e": "2022.04.19"},
    {"g": "c", "p": "보안조원", "n": "남형민", "t": "010-8767-7073", "b": "1977.11.24", "e": "2018.02.27"},
    {"g": "c", "p": "보안조원", "n": "김태언", "t": "010-5386-5386", "b": "1971.03.04", "e": "2024.10.12"},
    {"g": "c", "p": "보안조원", "n": "이정석", "t": "010-2417-1173", "b": "1972.09.01", "e": "2025.07.21"},
    {"g": "c", "p": "보안조원", "n": "강경훈", "t": "010-3436-6107", "b": "1981.05.04", "e": "2024.11.29"},
    {"g": "c", "p": "보안요원", "n": "공석", "t": "", "b": "-", "e": "-"},
    {"g": "dorm", "p": "보안반장", "n": "이강택", "t": "010-9048-6708", "b": "1965.08.13", "e": "2023.08.03"},
    {"g": "dorm", "p": "보안조원", "n": "유시균", "t": "010-8737-5770", "b": "1962.02.21", "e": "2008.10.15"},
    {"g": "dorm", "p": "보안조원", "n": "이상헌", "t": "010-4285-4231", "b": "1965.10.09", "e": "2022.04.01"},
    {"g": "dorm", "p": "보안요원", "n": "공석", "t": "", "b": "-", "e": "-"},
]

# C조 패턴 함수 (수정된 로직)
def get_workers_by_date(target_date):
    diff = (target_date - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: return "황재업", "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: return "황재업", "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: return "황재업", "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
    return None, None, None, None

# --- [3] 화면 구성 (3개 탭) ---
tab_now, tab_list, tab_tel = st.tabs(["🕒 실시간 현황", "📅 근무 편성표", "📞 보안 연락망"])

# 탭 1: 실시간 현황
with tab_now:
    st.markdown('<div class="unified-title">C조 오늘 근무 현황</div>', unsafe_allow_html=True)
    wj, ws, wa, wb = get_workers_by_date(now.date())
    if wj:
        st.success(f"✅ 오늘은 **C조** 근무일입니다.")
        st.info(f"📍 조장: {wj} / 성의: {ws} / 의산A: {wa} / 의산B: {wb}")
    else:
        st.warning("비번(또는 타 조 근무일)입니다.")

# 탭 2: 근무 편성표 (문제 해결된 부분)
with tab_list:
    st.markdown('<div class="unified-title">C조 월간 근무 편성표</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        s_date = st.date_input("📅 시작일 선택", now.date())
    with col2:
        period = st.slider("📆 표시 기간(일)", 7, 60, 31)

    sched_data = []
    for i in range(period):
        target_d = s_date + timedelta(days=i)
        wj, ws, wa, wb = get_workers_by_date(target_d)
        if wj:
            sched_data.append({
                "날짜": target_d.strftime("%m/%d"),
                "요일": ["월","화","수","목","금","토","일"][target_d.weekday()],
                "조장": wj, "성의교정": ws, "의산연A": wa, "의산연B": wb
            })
    
    if sched_data:
        df = pd.DataFrame(sched_data)
        st.table(df) # 표 출력 부분 정상화
    else:
        st.info("선택한 기간 내에 C조 근무일이 없습니다.")

# 탭 3: 보안 연락망 (모달 기능 포함)
with tab_tel:
    st.markdown('<div class="unified-title">보안팀 비상연락망</div>', unsafe_allow_html=True)
    # (HTML 모달 코드 부분 - 가독성을 위해 이전 버전의 HTML을 그대로 연결)
    html_code = """
    <style>
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; font-family: sans-serif; }
        .card { height: 45px; border-radius: 4px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: #fff; border: 1px solid #eee; cursor: pointer; }
        .n { font-size: 13px; font-weight: bold; }
        .p { font-size: 8px; color: #888; }
        .top { background: #f8f9fa; } .a { background: #ebfbee; } .b { background: #fff5f5; } .c { background: #fff9db; }
    </style>
    <div class="grid">
    """
    for m in security_data:
        p_text = f"{m['g'].upper()}조" if m['g'] in ['a','b','c'] else "관리"
        html_code += f"<div class='card {m['g']}' onclick=\"alert('{m['n']}: {m['t']}')\"><span class='p'>{p_text}</span><span class='n'>{m['n']}</span></div>"
    html_code += "</div>"
    components.html(html_code, height=500)
