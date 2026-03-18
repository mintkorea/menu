import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="보안 통합 연락망", layout="wide")

# 명찰 이미지(1773785171515.jpg) 기반 28인 전수 실데이터 적용
security_data = [
    # 1행: 지휘부
    {"g": "top", "p": "보안반장", "n": "유정수", "t": "010-5316-8065", "b": "1970.09.25", "e": "2020.09.01"},
    {"g": "top", "p": "보안소장", "n": "이규용", "t": "010-8883-6580", "b": "1972.03.01", "e": "-"},
    {"g": "top", "p": "보안부소장", "n": "박상현", "t": "010-3193-4603", "b": "1988.07.31", "e": "-"},
    {"g": "top", "p": "보안반장", "n": "오제준", "t": "010-3352-8933", "b": "1970.03.29", "e": "2022.05.18"},
    
    # 2~3행: A조
    {"g": "a", "p": "보안조장", "n": "배준용", "t": "010-4717-7065", "b": "1969.12.24", "e": "2022.07.26"},
    {"g": "a", "p": "보안조원", "n": "이명구", "t": "010-8638-5819", "b": "1964.09.15", "e": "2025.03.21"},
    {"g": "a", "p": "보안조장", "n": "손병휘", "t": "010-9966-2090", "b": "1972.05.23", "e": "2016.05.05"},
    {"g": "a", "p": "보안조원", "n": "권순호", "t": "010-2539-1799", "b": "1980.12.14", "e": "2026.02.11"},
    {"g": "a", "p": "보안조원", "n": "김영중", "t": "010-7726-5963", "b": "1959.02.26", "e": "2024.08.21"},
    {"g": "a", "p": "보안조원", "n": "김삼동", "t": "010-2345-8081", "b": "1967.02.01", "e": "2025.05.02"},
    {"g": "a", "p": "보안조원", "n": "김전식", "t": "010-3277-0808", "b": "1966.07.23", "e": "2025.02.10"},
    {"g": "a", "p": "보안요원", "n": "공석", "t": "", "b": "-", "e": "-"},

    # 4~5행: B조
    {"g": "b", "p": "보안조장", "n": "심규천", "t": "010-8287-9895", "b": "1967.04.10", "e": "2024.11.11"},
    {"g": "b", "p": "보안조원", "n": "임종현", "t": "010-7741-6732", "b": "1968.01.18", "e": "2021.08.10"},
    {"g": "b", "p": "보안조장", "n": "황일범", "t": "010-8929-4294", "b": "1969.05.30", "e": "2022.04.01"},
    {"g": "b", "p": "보안조원", "n": "이상길", "t": "010-9904-0247", "b": "1978.07.13", "e": "2024.09.11"},
    {"g": "b", "p": "보안조원", "n": "권영국", "t": "010-4085-9982", "b": "1969.07.20", "e": "2025.01.21"},
    {"g": "b", "p": "보안조원", "n": "전준수", "t": "010-5687-7107", "b": "1971.07.17", "e": "2025.04.03"},
    {"g": "b", "p": "보안조원", "n": "허용", "t": "010-8845-0163", "b": "1968.08.01", "e": "2026.01.16"},
    {"g": "b", "p": "보안요원", "n": "공석", "t": "", "b": "-", "e": "-"},

    # 6~7행: C조
    {"g": "c", "p": "보안조장", "n": "황재업", "t": "010-9278-6622", "b": "1980.03.12", "e": "2023.05.26"},
    {"g": "c", "p": "보안조원", "n": "이태원", "t": "010-9265-7881", "b": "1963.11.23", "e": "2025.04.01"},
    {"g": "c", "p": "보안조장", "n": "피재영", "t": "010-9359-2569", "b": "1972.08.07", "e": "2022.04.19"},
    {"g": "c", "p": "보안조원", "n": "남형민", "t": "010-8767-7073", "b": "1977.11.24", "e": "2018.02.27"},
    {"g": "c", "p": "보안조원", "n": "김태언", "t": "010-5386-5386", "b": "1971.03.04", "e": "2024.10.12"},
    {"g": "c", "p": "보안조원", "n": "이정석", "t": "010-2417-1173", "b": "1972.09.01", "e": "2025.07.21"},
    {"g": "c", "p": "보안조원", "n": "강경훈", "t": "010-3436-6107", "b": "1981.05.04", "e": "2024.11.29"},
    {"g": "c", "p": "보안요원", "n": "공석", "t": "", "b": "-", "e": "-"},

    # 8행: 기숙사
    {"g": "dorm", "p": "보안반장", "n": "이강택", "t": "010-9048-6708", "b": "1965.08.13", "e": "2023.08.03"},
    {"g": "dorm", "p": "보안조원", "n": "유시균", "t": "010-8737-5770", "b": "1962.02.21", "e": "2008.10.15"},
    {"g": "dorm", "p": "보안조원", "n": "이상헌", "t": "010-4285-4231", "b": "1965.10.09", "e": "2022.04.01"},
    {"g": "dorm", "p": "보안요원", "n": "공석", "t": "", "b": "-", "e": "-"},
]

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    body {{ font-family: 'Malgun Gothic', sans-serif; margin: 0; padding: 5px; background: #f8f9fa; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 3px; }}
    .card {{
        height: 48px; border-radius: 5px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; background: white; border: 1px solid #dee2e6;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05); cursor: pointer;
    }}
    .card:nth-child(4n-2) {{ border-right: 3px solid #343a40; }}
    
    .top {{ background: #f1f3f5; }}
    .a {{ background: #e7f5ff; }}
    .b {{ background: #fff5f5; }}
    .c {{ background: #fff9db; }}
    .dorm {{ background: #f3fcf3; }}
    
    .p {{ font-size: 8px; font-weight: bold; color: #868e96; margin-bottom: 1px; }}
    .n {{ font-size: 13px; font-weight: bold; color: #212529; }}

    /* 초슬림 모달 디자인 - 전화버튼 노출 보장 */
    #modalOverlay {{
        display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.7); z-index: 9999; justify-content: center; align-items: center;
    }}
    .modal-content {{
        background: white; width: 80%; max-width: 260px; padding: 15px; border-radius: 12px;
        text-align: center; position: relative; box-shadow: 0 10px 20px rgba(0,0,0,0.2);
    }}
    .close-x {{
        position: absolute; top: 8px; right: 12px; font-size: 20px; color: #adb5bd; cursor: pointer;
    }}
    .m-title {{ font-size: 22px; font-weight: bold; margin-bottom: 2px; }}
    .m-sub {{ font-size: 14px; color: #1971c2; font-weight: bold; margin-bottom: 10px; }}
    .m-info {{ font-size: 13px; color: #495057; line-height: 1.4; margin-bottom: 15px; }}
    .call-btn {{
        display: block; background: #2f9e44; color: white; padding: 12px;
        border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 17px;
    }}
</style>
</head>
<body>
<div class="grid">
"""

for m in security_data:
    # 직위 앞에 조 이름 추가 (A조 보안조장 등)
    prefix = ""
    if m['g'] == 'a': prefix = "A조 "
    elif m['g'] == 'b': prefix = "B조 "
    elif m['g'] == 'c': prefix = "C조 "
    
    display_p = prefix + m['p']
    
    html_code += f"""
    <div class="card {m['g']}" onclick="openModal('{m['n']}', '{display_p}', '{m['t']}', '{m['b']}', '{m['e']}')">
        <span class="p">{display_p}</span>
        <span class="n">{m['n']}</span>
    </div>
    """

html_code += """
</div>

<div id="modalOverlay" onclick="closeModal()">
    <div class="modal-content" onclick="event.stopPropagation()">
        <span class="close-x" onclick="closeModal()">&times;</span>
        <div id="mName" class="m-title"></div>
        <div id="mPos" class="m-sub"></div>
        <div class="m-info">
            🎂 생일: <span id="mBirth"></span><br>
            📅 입사: <span id="mEntry"></span>
        </div>
        <a id="mCall" href="" class="call-btn">📞 전화 연결</a>
    </div>
</div>

<script>
    function openModal(n, p, t, b, e) {
        if(n === '공석') return;
        document.getElementById('mName').innerText = n;
        document.getElementById('mPos').innerText = p;
        document.getElementById('mBirth').innerText = b;
        document.getElementById('mEntry').innerText = e;
        document.getElementById('mCall').href = "tel:" + t;
        document.getElementById('modalOverlay').style.display = 'flex';
    }
    function closeModal() {
        document.getElementById('modalOverlay').style.display = 'none';
    }
</script>
</body></html>
"""

components.html(html_code, height=650, scrolling=False)
