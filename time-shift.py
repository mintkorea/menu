import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import pytz
import streamlit.components.v1 as components

# --- [1] 설정 및 CSS ---
st.set_page_config(page_title="C조 통합 근무 시스템", layout="wide")

st.markdown("""
    <style>
    .block-container { 
        padding-top: 3.2rem !important; 
        max-width: 500px;
        margin: auto;
    }
    
    .unified-title { font-size: 24px !important; font-weight: 800; text-align: center; margin-bottom: 5px; }
    .title-sub { font-size: 16px !important; text-align: center; margin-bottom: 15px; color: #555; }
    
    /* 연락망 그리드 스타일 */
    .sec-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 5px; margin-top: 10px; }
    
    /* 표 및 데이터프레임 중앙 정렬 */
    [data-testid="stTable"] { display: flex; justify-content: center; }
    thead tr th:first-child, tbody th { display:none; }
    </style>
    """, unsafe_allow_html=True)

# --- [2] 데이터 로직 ---
kst = pytz.timezone('Asia/Seoul')
now = datetime.now(kst)
PATTERN_START = datetime(2026, 3, 9).date()

# 보안팀 전체 연락망 데이터
security_contacts = [
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
    {"g": "b", "p": "보안조장", "n": "심규천", "t": "010-8287-9895", "b": "1967.04.10", "e": "2024.11.11"},
    {"g": "b", "p": "보안조원", "n": "임종현", "t": "010-7741-6732", "b": "1968.01.18", "e": "2021.08.10"},
    {"g": "b", "p": "보안조장", "n": "황일범", "t": "010-8929-4294", "b": "1969.05.30", "e": "2022.04.01"},
    {"g": "b", "p": "보안조원", "n": "이상길", "t": "010-9904-0247", "b": "1978.07.13", "e": "2024.09.11"},
    {"g": "b", "p": "보안조원", "n": "권영국", "t": "010-4085-9982", "b": "1969.07.20", "e": "2025.01.21"},
    {"g": "b", "p": "보안조원", "n": "전준수", "t": "010-5687-7107", "b": "1971.07.17", "e": "2025.04.03"},
    {"g": "b", "p": "보안조원", "n": "허용", "t": "010-8845-0163", "b": "1968.08.01", "e": "2026.01.16"},
    {"g": "c", "p": "보안조장", "n": "황재업", "t": "010-9278-6622", "b": "1980.03.12", "e": "2023.05.26"},
    {"g": "c", "p": "보안조원", "n": "이태원", "t": "010-9265-7881", "b": "1963.11.23", "e": "2025.04.01"},
    {"g": "c", "p": "보안조장", "n": "피재영", "t": "010-9359-2569", "b": "1972.08.07", "e": "2022.04.19"},
    {"g": "c", "p": "보안조원", "n": "남형민", "t": "010-8767-7073", "b": "1977.11.24", "e": "2018.02.27"},
    {"g": "c", "p": "보안조원", "n": "김태언", "t": "010-5386-5386", "b": "1971.03.04", "e": "2024.10.12"},
    {"g": "c", "p": "보안조원", "n": "이정석", "t": "010-2417-1173", "b": "1972.09.01", "e": "2025.07.21"},
    {"g": "c", "p": "보안조원", "n": "강경훈", "t": "010-3436-6107", "b": "1981.05.04", "e": "2024.11.29"},
    {"g": "dorm", "p": "보안반장", "n": "이강택", "t": "010-9048-6708", "b": "1965.08.13", "e": "2023.08.03"},
    {"g": "dorm", "p": "보안조원", "n": "유시균", "t": "010-8737-5770", "b": "1962.02.21", "e": "2008.10.15"},
    {"g": "dorm", "p": "보안조원", "n": "이상헌", "t": "010-4285-4231", "b": "1965.10.09", "e": "2022.04.01"}
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

# --- [3] 화면 구성 ---
tab1, tab2, tab3 = st.tabs(["🕒 실시간 현황", "📅 근무 편성표", "📞 비상 연락망"])

with tab1:
    # (기존 tab1 실시간 현황 코드와 동일하므로 생략 - 사용 시 기존 코드 유지)
    st.markdown('<div class="unified-title">C조 실시간 근무 현황</div>', unsafe_allow_html=True)
    # ... (기존 실시간 현황 로직 적용) ...

with tab2:
    # (기존 tab2 근무 편성표 코드와 동일하므로 생략 - 사용 시 기존 코드 유지)
    st.markdown('<div class="unified-title">C조 근무 편성표</div>', unsafe_allow_html=True)
    # ... (기존 편성표 로직 적용) ...

with tab3:
    st.markdown('<div class="unified-title">보안팀 비상 연락망</div>', unsafe_allow_html=True)
    
    # 연락망 구현을 위한 HTML/JS (모달 팝업 포함)
    contact_html = """
    <style>
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; font-family: sans-serif; }
        .card { height: 42px; border-radius: 4px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: white; border: 1px solid #eee; box-shadow: 0 1px 2px rgba(0,0,0,0.05); cursor: pointer; }
        .p { font-size: 7px; font-weight: bold; color: #888; margin-bottom: 1px; }
        .n { font-size: 13px; font-weight: bold; color: #333; }
        .top { background: #f8f9fa; } .a { background: #ebfbee; } .b { background: #fff5f5; } .c { background: #fff9db; } .dorm { background: #f3fcf3; }
        
        /* 모달 스타일 */
        #modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 1000; justify-content: center; align-items: center; }
        .modal-content { background: white; width: 80%; max-width: 280px; padding: 20px; border-radius: 12px; text-align: center; position: relative; }
        .m-name { font-size: 22px; font-weight: bold; margin-bottom: 5px; }
        .m-pos { font-size: 14px; color: #007bff; font-weight: bold; margin-bottom: 15px; }
        .m-info { font-size: 13px; color: #666; margin-bottom: 20px; border-top: 1px solid #eee; padding-top: 10px; }
        .m-tel { font-size: 18px; font-weight: bold; color: #d9534f; margin-bottom: 20px; display: block; text-decoration: none; }
        .btn-call { background: #28a745; color: white; padding: 10px 0; border-radius: 8px; display: block; text-decoration: none; font-weight: bold; }
        .close-btn { position: absolute; top: 10px; right: 15px; font-size: 20px; cursor: pointer; color: #aaa; }
    </style>
    <div class="grid">
    """
    
    for m in security_contacts:
        p_text = f"{m['g'].upper()}조 {m['p']}" if m['g'] in ['a','b','c'] else m['p']
        if m['g'] == 'dorm': p_text = "기숙사"
        
        contact_html += f"""
        <div class="card {m['g']}" onclick="openModal('{m['n']}', '{p_text}', '{m['t']}', '{m['b']}', '{m['e']}')">
            <span class="p">{p_text}</span>
            <span class="n">{m['n']}</span>
        </div>
        """
        
    contact_html += """
    </div>
    <div id="modal" onclick="closeModal()">
        <div class="modal-content" onclick="event.stopPropagation()">
            <span class="close-btn" onclick="closeModal()">&times;</span>
            <div id="m-name" class="m-name"></div>
            <div id="m-pos" class="m-pos"></div>
            <div class="m-info">🎂 생일: <span id="m-birth"></span><br>📅 입사: <span id="m-entry"></span></div>
            <div id="m-tel-text" style="font-size:16px; font-weight:bold; margin-bottom:5px;"></div>
            <a id="m-call" href="" class="btn-call">📞 바로 전화걸기</a>
        </div>
    </div>
    <script>
        function openModal(n, p, t, b, e) {
            document.getElementById('m-name').innerText = n;
            document.getElementById('m-pos').innerText = p;
            document.getElementById('m-birth').innerText = b;
            document.getElementById('m-entry').innerText = e;
            document.getElementById('m-tel-text').innerText = t;
            document.getElementById('m-call').href = 'tel:' + t;
            document.getElementById('modal').style.display = 'flex';
        }
        function closeModal() {
            document.getElementById('modal').style.display = 'none';
        }
    </script>
    """
    components.html(contact_html, height=600, scrolling=False)
