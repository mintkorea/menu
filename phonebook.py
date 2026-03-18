import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="보안 통합 연락망", layout="wide")

# 1. 고밀도 그리드 및 팝업 제어 HTML/JS
html_code = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    body { font-family: sans-serif; margin: 0; padding: 5px; background-color: #f4f7f9; }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 5px;
    }
    .node {
        background: white; border: 1px solid #ddd; border-radius: 4px;
        height: 55px; display: flex; flex-direction: column;
        align-items: center; justify-content: center; cursor: pointer;
        box-shadow: 0 1px 2px rgba(0,0,0,0.05);
    }
    .node .pos { font-size: 9px; color: #777; }
    .node .name { font-size: 13px; font-weight: bold; color: #333; }
    
    /* 섹션 헤더 (공간 최소화) */
    .header {
        grid-column: span 4; background: #e9ecef; font-size: 11px;
        font-weight: bold; padding: 4px; border-radius: 3px;
        margin-top: 8px; text-align: center; color: #495057;
    }

    /* 팝업 스타일 */
    #overlay {
        display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        background: rgba(0,0,0,0.6); z-index: 100;
    }
    #details {
        display: none; position: fixed; top: 50%; left: 50%; 
        transform: translate(-50%, -50%); width: 85%;
        background: white; border-radius: 12px; padding: 20px;
        z-index: 101; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    }
    .call-btn {
        display: block; background: #28a745; color: white;
        text-decoration: none; padding: 12px; border-radius: 8px;
        font-weight: bold; margin-top: 15px; font-size: 16px;
    }
    .close-btn { margin-top: 10px; color: #666; font-size: 14px; cursor: pointer; }
</style>
</head>
<body>

<div class="grid-container">
    <div class="header">🛡️ 소장 / 부소장 / 반장</div>
    <div class="node" onclick="show('유정수', '반장', '010-5316-8065', '1970.09.25')"><span class="pos">반장</span><span class="name">유정수</span></div>
    <div class="node" onclick="show('이규용', '소장', '010-8883-6580', '-')"><span class="pos">소장</span><span class="name">이규용</span></div>
    <div class="node" onclick="show('박상현', '부소장', '010-3193-4603', '-')"><span class="pos">부소장</span><span class="name">박상현</span></div>
    <div class="node" onclick="show('오제준', '반장', '010-3352-8933', '-')"><span class="pos">반장</span><span class="name">오제준</span></div>

    <div class="header">🏢 성의회관A / 🏫 옴니버스A</div>
    <div class="node" onclick="show('배준용', 'A조장', '010-4717-7065', '1969.12.24')"><span class="pos">A조장</span><span class="name">배준용</span></div>
    <div class="node" onclick="show('이명구', 'A조원', '010-8638-5819', '1964.09.15')"><span class="pos">A조원</span><span class="name">이명구</span></div>
    <div class="node" onclick="show('손병휘', 'A조장', '010-9966-2090', '-')"><span class="pos">A조장</span><span class="name">손병휘</span></div>
    <div class="node" onclick="show('권순호', 'A조원', '010-2539-1799', '-')"><span class="pos">A조원</span><span class="name">권순호</span></div>
    
    </div>

<div id="overlay" onclick="hide()"></div>
<div id="details">
    <h2 id="p-name" style="margin:0;">이름</h2>
    <p id="p-info" style="color:#666; margin:10px 0;">직위 | 생일</p>
    <a href="#" id="p-tel" class="call-btn">📞 전화 걸기</a>
    <div class="close-btn" onclick="hide()">창 닫기</div>
</div>

<script>
    function show(name, pos, tel, birth) {
        document.getElementById('p-name').innerText = name;
        document.getElementById('p-info').innerText = pos + " | 생신: " + birth;
        document.getElementById('p-tel').href = "tel:" + tel.replace(/-/g, "");
        document.getElementById('p-tel').innerText = "📞 " + tel + " 연결";
        document.getElementById('overlay').style.display = 'block';
        document.getElementById('details').style.display = 'block';
    }
    function hide() {
        document.getElementById('overlay').style.display = 'none';
        document.getElementById('details').style.display = 'none';
    }
</script>

</body>
</html>
"""

# 컴포넌트 실행 (높이를 28명 기준에 맞춰 조절)
components.html(html_code, height=700, scrolling=True)
