import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="보안 통합 연락망", layout="wide")

html_code = """
<!DOCTYPE html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<style>
    body { font-family: sans-serif; margin: 0; padding: 5px; background-color: #f4f7f9; overflow-x: hidden; }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 4px; /* 간격 최소화 */
    }
    .node {
        background: white; border: 1px solid #ddd; border-radius: 4px;
        height: 42px; /* 높이 대폭 축소 */
        display: flex; flex-direction: column;
        align-items: center; justify-content: center; cursor: pointer;
    }
    .node .pos { font-size: 8px; color: #007bff; line-height: 1; }
    .node .name { font-size: 12px; font-weight: bold; color: #333; margin-top: 2px; }
    
    .header {
        grid-column: span 4; background: #e9ecef; font-size: 10px;
        font-weight: bold; padding: 3px; border-radius: 3px;
        margin-top: 6px; text-align: center; color: #495057;
    }

    /* 근접 팝업 스타일 (화면 중앙이 아닌 클릭 위치 대응 느낌) */
    #details-layer {
        display: none; position: fixed; bottom: 20px; left: 5%; width: 90%;
        background: white; border-radius: 12px; padding: 15px;
        z-index: 1000; box-shadow: 0 -4px 20px rgba(0,0,0,0.2);
        border-top: 4px solid #28a745;
    }
    .call-btn {
        display: block; background: #28a745; color: white;
        text-decoration: none; padding: 12px; border-radius: 8px;
        font-weight: bold; text-align: center; font-size: 16px; margin-top: 10px;
    }
    .info-text { font-size: 13px; color: #666; margin-bottom: 5px; text-align: center; }
    #overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; z-index: 999; }
</style>
</head>
<body>

<div class="grid-container">
    <div class="header">🛡️ 지휘부 / 공통</div>
    <div class="node" onclick="show('유정수', '반장', '010-5316-8065')"><span class="pos">반장</span><span class="name">유정수</span></div>
    <div class="node" onclick="show('이규용', '소장', '010-8883-6580')"><span class="pos">소장</span><span class="name">이규용</span></div>
    <div class="node" onclick="show('박상현', '부소장', '010-3193-4603')"><span class="pos">부소</span><span class="name">박상현</span></div>
    <div class="node" onclick="show('오제준', '반장', '010-3352-8933')"><span class="pos">반장</span><span class="name">오제준</span></div>

    <div class="header">🏢 회관A / 🏫 옴니A</div>
    <div class="node" onclick="show('배준용', 'A조장', '010-4717-7065')"><span class="pos">A장</span><span class="name">배준용</span></div>
    <div class="node" onclick="show('이명구', 'A조원', '010-8638-5819')"><span class="pos">A원</span><span class="name">이명구</span></div>
    <div class="node" onclick="show('손병휘', 'A조장', '010-9966-2090')"><span class="pos">A장</span><span class="name">손병휘</span></div>
    <div class="node" onclick="show('권순호', 'A조원', '010-2539-1799')"><span class="pos">A원</span><span class="name">권순호</span></div>

    <div class="header">🏢 회관B / 🏫 옴니B</div>
    <div class="node" onclick="show('심규천', 'B조장', '010-8287-9895')"><span class="pos">B장</span><span class="name">심규천</span></div>
    <div class="node" onclick="show('임종현', 'B조원', '010-7741-6732')"><span class="pos">B원</span><span class="name">임종현</span></div>
    <div class="node" onclick="show('황일범', 'B조장', '010-8929-4294')"><span class="pos">B장</span><span class="name">황일범</span></div>
    <div class="node" onclick="show('이상길', 'B조원', '010-9904-0247')"><span class="pos">B원</span><span class="name">이상길</span></div>
</div>

<div id="overlay" onclick="hide()"></div>
<div id="details-layer">
    <div style="text-align:right; color:#ccc; font-size:12px;" onclick="hide()">닫기 ✖</div>
    <div id="p-name" style="font-size:18px; font-weight:bold; text-align:center;">이름</div>
    <div id="p-info" class="info-text">직위 정보</div>
    <a href="#" id="p-tel" class="call-btn">전화 연결</a>
</div>

<script>
    function show(name, pos, tel) {
        document.getElementById('p-name').innerText = name;
        document.getElementById('p-info').innerText = pos + " | " + tel;
        document.getElementById('p-tel').href = "tel:" + tel.replace(/-/g, "");
        document.getElementById('details-layer').style.display = 'block';
        document.getElementById('overlay').style.display = 'block';
    }
    function hide() {
        document.getElementById('details-layer').style.display = 'none';
        document.getElementById('overlay').style.display = 'none';
    }
</script>

</body>
</html>
"""

components.html(html_code, height=600, scrolling=True)
