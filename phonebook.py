import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="보안팀 연락망", layout="wide")

# [좌1(회관), 좌2(회관), 우1(옴니), 우2(옴니)] 순서의 28인 데이터
security_data = [
    # 1행: 지휘부 (반장-소장-부소장-반장)
    {"g": "top", "p": "반장(회관)", "n": "유정수", "t": "010-5316-8065", "b": "1970.09.25", "e": "2020.09.01"},
    {"g": "top", "p": "소장", "n": "이규용", "t": "010-8883-6580", "b": "1972.03.01", "e": "-"},
    {"g": "top", "p": "부소장", "n": "박상현", "t": "010-3193-4603", "b": "1988.07.31", "e": "-"},
    {"g": "top", "p": "반장(옴니)", "n": "오제준", "t": "010-3352-8933", "b": "-", "e": "-"},
    
    # 2~3행: A조 (회관 4명 / 옴니 4명)
    {"g": "a", "p": "A장(회관)", "n": "배준용", "t": "010-4717-7065", "b": "1969.12.24", "e": "2022.07.26"},
    {"g": "a", "p": "A원(회관)", "n": "이명구", "t": "010-8638-5819", "b": "1964.09.15", "e": "2025.03.21"},
    {"g": "a", "p": "A장(옴니)", "n": "손병휘", "t": "010-9966-2090", "b": "-", "e": "-"},
    {"g": "a", "p": "A원(옴니)", "n": "권순호", "t": "010-2539-1799", "b": "-", "e": "-"},
    {"g": "a", "p": "A원(회관)", "n": "김영중", "t": "010-7726-5963", "b": "1959.02.26", "e": "2024.08.21"},
    {"g": "a", "p": "A원(회관)", "n": "김삼동", "t": "010-8081-XXXX", "b": "-", "e": "-"},
    {"g": "a", "p": "A원(옴니)", "n": "김전식", "t": "-", "b": "-", "e": "-"},
    {"g": "a", "p": "A원(옴니)", "n": "보안요원", "t": "-", "b": "-", "e": "-"},

    # 4~5행: B조 (회관 4명 / 옴니 4명)
    {"g": "b", "p": "B장(회관)", "n": "심규천", "t": "010-8287-9895", "b": "-", "e": "-"},
    {"g": "b", "p": "B원(회관)", "n": "임종현", "t": "010-7741-6732", "b": "-", "e": "-"},
    {"g": "b", "p": "B장(옴니)", "n": "황일범", "t": "010-8929-4294", "b": "-", "e": "-"},
    {"g": "b", "p": "B원(옴니)", "n": "이상길", "t": "010-9904-0247", "b": "-", "e": "-"},
    {"g": "b", "p": "B원(회관)", "n": "요원B1", "t": "-", "b": "-", "e": "-"},
    {"g": "b", "p": "B원(회관)", "n": "요원B2", "t": "-", "b": "-", "e": "-"},
    {"g": "b", "p": "B원(옴니)", "n": "요원B3", "t": "-", "b": "-", "e": "-"},
    {"g": "b", "p": "B원(옴니)", "n": "보안요원", "t": "-", "b": "-", "e": "-"},

    # 6~7행: C조 (회관 4명 / 옴니 4명)
    {"g": "c", "p": "C장(회관)", "n": "김태언", "t": "-", "b": "-", "e": "1순위"},
    {"g": "c", "p": "C원(회관)", "n": "이태원", "t": "-", "b": "-", "e": "2순위"},
    {"g": "c", "p": "C원(옴니)", "n": "이정석", "t": "-", "b": "-", "e": "3순위"},
    {"g": "c", "p": "C원(옴니)", "n": "요원C1", "t": "-", "b": "-", "e": "-"},
    {"g": "c", "p": "C원(회관)", "n": "요원C2", "t": "-", "b": "-", "e": "-"},
    {"g": "c", "p": "C원(회관)", "n": "요원C3", "t": "-", "b": "-", "e": "-"},
    {"g": "c", "p": "C원(옴니)", "n": "요원C4", "t": "-", "b": "-", "e": "-"},
    {"g": "c", "p": "C원(옴니)", "n": "보안요원", "t": "-", "b": "-", "e": "-"},

    # 8행: 기숙사
    {"g": "dorm", "p": "기숙사", "n": "요원D1", "t": "-", "b": "-", "e": "-"},
    {"g": "dorm", "p": "기숙사", "n": "요원D2", "t": "-", "b": "-", "e": "-"},
    {"g": "dorm", "p": "기숙사", "n": "요원D3", "t": "-", "b": "-", "e": "-"},
    {"g": "dorm", "p": "기숙사", "n": "요원D4", "t": "-", "b": "-", "e": "-"},
]

html_code = f"""
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    body {{ font-family: 'Malgun Gothic', sans-serif; margin: 0; padding: 5px; background: #f8f9fa; }}
    .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; padding-bottom: 20px; }}
    .card {{
        height: 46px; border-radius: 6px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; background: white; border: 1px solid #ddd;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1); cursor: pointer;
    }}
    /* 센터 구분선 강화 */
    .card:nth-child(4n-2) {{ border-right: 3px solid #666; }}
    
    .top {{ background: #eee; color: #333; }}
    .a {{ background: #e7f5ff; color: #1971c2; border-color: #a5d8ff; }}
    .b {{ background: #f3f0ff; color: #6f2dbd; border-color: #d0bfff; }}
    .c {{ background: #fff4e6; color: #d9480f; border-color: #ffd8a8; }}
    .dorm {{ background: #ebfbee; color: #2b8a3e; border-color: #b2f2bb; }}
    
    .p {{ font-size: 8px; font-weight: bold; margin-bottom: 1px; }}
    .n {{ font-size: 14px; font-weight: bold; }}

    /* 모달 레이어 */
    #modalOverlay {{
        display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.6); z-index: 9999; justify-content: center; align-items: center;
    }}
    .modal-content {{
        background: white; width: 80%; max-width: 320px; padding: 25px; border-radius: 15px;
        position: relative; text-align: center; box-shadow: 0 10px 25px rgba(0,0,0,0.2);
    }}
    .close-btn {{
        position: absolute; top: 10px; right: 15px; font-size: 24px; color: #aaa;
        cursor: pointer; font-weight: bold;
    }}
    .call-btn {{
        display: block; background: #28a745; color: white; padding: 12px;
        margin-top: 20px; border-radius: 8px; text-decoration: none; font-weight: bold; font-size: 18px;
    }}
</style>
</head>
<body>
<div class="grid">
"""

for m in security_data:
    html_code += f"""
    <div class="card {m['g']}" onclick="openModal('{m['n']}', '{m['p']}', '{m['t']}', '{m['b']}', '{m['e']}')">
        <span class="p">{m['p']}</span>
        <span class="n">{m['n']}</span>
    </div>
    """

html_code += """
</div>

<div id="modalOverlay" onclick="closeModal()">
    <div class="modal-content" onclick="event.stopPropagation()">
        <span class="close-btn" onclick="closeModal()">&times;</span>
        <div id="mName" style="font-size:24px; font-weight:bold; margin-bottom:5px;"></div>
        <div id="mPos" style="color:#1971c2; font-weight:bold; margin-bottom:15px; border-bottom:1px solid #eee; padding-bottom:10px;"></div>
        <div style="font-size:15px; color:#444; line-height:1.6;">
            🎂 생일: <span id="mBirth" style="font-weight:bold;"></span><br>
            📅 입사: <span id="mEntry" style="font-weight:bold;"></span>
        </div>
        <a id="mCall" href="" class="call-btn">📞 전화 연결</a>
    </div>
</div>

<script>
    function openModal(n, p, t, b, e) {
        if(n === '보안요원') return;
        document.getElementById('mName').innerText = n;
        document.getElementById('mPos').innerText = p;
        document.getElementById('mBirth').innerText = b;
        document.getElementById('mEntry').innerText = e;
        document.getElementById('mCall').href = "tel:" + t.replace(/-/g,'');
        document.getElementById('modalOverlay').style.display = 'flex';
    }
    function closeModal() {
        document.getElementById('modalOverlay').style.display = 'none';
    }
</script>
</body></html>
"""

components.html(html_code, height=900, scrolling=True)
