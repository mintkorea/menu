import streamlit as st
import streamlit.components.v1 as components

# --- [1] 페이지 설정 및 공통 스타일 ---
st.set_page_config(page_title="보안/미화 통합 연락망", layout="wide")

st.markdown("""
    <style>
        /* 상단 여백 확보 (탭 잘림 방지) */
        .block-container { 
            padding-top: 3.2rem !important; 
            max-width: 500px;
            margin: auto;
        }
        
        /* 공통 타이틀 스타일 */
        .unified-title { 
            font-size: 24px !important; 
            font-weight: 800; 
            text-align: center; 
            margin-bottom: 20px; 
        }

        /* 미화팀 버튼 스타일 슬림화 */
        div[data-testid="stHorizontalBlock"] { gap: 8px !important; }
        button { height: 38px !important; font-size: 15px !important; font-weight: bold !important; }
    </style>
""", unsafe_allow_html=True)

# --- [2] 데이터 설정 ---
# 1. 보안팀 데이터
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

# 2. 미화팀 데이터
data_uisan = [{"위치": "8층", "성명": "안순재", "연락처": "010-9119-8879"},{"위치": "7층", "성명": "안순재", "연락처": "010-9119-8879"},{"위치": "6층", "성명": "장 성", "연락처": "010-8938-3988"},{"위치": "5층", "성명": "조미연", "연락처": "010-2252-2036"},{"위치": "4층", "성명": "김정옥", "연락처": "010-9011-0659"},{"위치": "3층", "성명": "장 성", "연락처": "010-8938-3988"},{"위치": "세포실", "성명": "이연숙", "연락처": "010-9117-3965"},{"위치": "3층(세포)", "성명": "강민례", "연락처": "010-3385-9952"},{"위치": "1층(남)", "성명": "이정숙", "연락처": "010-3722-0765"},{"위치": "1층(북)", "성명": "이명자", "연락처": "010-6274-2355"},{"위치": "B1층", "성명": "이서빈", "연락처": "010-7755-8613"},{"위치": "B2층", "성명": "선양순", "연락처": "010-9967-7301"},{"위치": "본관지원", "성명": "정순식", "연락처": "010-9564-0029"},{"위치": "본관지원", "성명": "조성일", "연락처": "010-3952-2441"},{"위치": "별관 5층", "성명": "이선자", "연락처": "010-8210-7106"},{"위치": "별관 3,4", "성명": "김인숙", "연락처": "010-4120-6055"},{"위치": "별관 1,2", "성명": "정혜숙", "연락처": "010-9130-0652"},{"위치": "별관지원", "성명": "이창남", "연락처": "010-3133-0638"}]
data_sunghee = [{"위치": "14층", "성명": "유순복", "연락처": "010-6370-0845"},{"위치": "13층", "성명": "박태연", "연락처": "010-5682-8927"},{"위치": "12층", "성명": "기성원", "연락처": "010-2618-9120"},{"위치": "11층", "성명": "김성순", "연락처": "010-4604-7608"},{"위치": "10층", "성명": "박현순", "연락처": "010-8714-7703"},{"위치": "9층", "성명": "이재숙", "연락처": "010-8762-1178"},{"위치": "9층", "성명": "채예홍", "연락처": "010-5202-4638"},{"위치": "8층", "성명": "이애란", "연락처": "010-3046-8520"},{"위치": "7층", "성명": "박인순", "연락처": "010-5745-1427"},{"위치": "6층", "성명": "김순이", "연락처": "010-6370-6807"},{"위치": "5층", "성명": "최정숙", "연락처": "010-3850-2011"},{"위치": "4,5층", "성명": "신춘옥", "연락처": "010-2305-8914"},{"위치": "4층", "성명": "조계순", "연락처": "010-2211-7864"},{"위치": "3층", "성명": "김옥화", "연락처": "010-8000-9643"},{"위치": "2층", "성명": "임윤숙", "연락처": "010-3283-2799"},{"위치": "1층", "성명": "허봉혜", "연락처": "010-9014-7470"},{"위치": "1층", "성명": "양명선", "연락처": "010-6671-1442"},{"위치": "지원(외곽)", "성명": "김철규", "연락처": "010-6299-0079"},{"위치": "지원(승강)", "성명": "천제수", "연락처": "010-7537-6059"},{"위치": "지원(주차)", "성명": "박문희", "연락처": "010-8859-9333"},{"위치": "지원(전층)", "성명": "최연주", "연락처": "010-5744-1772"},{"위치": "지원(여)", "성명": "양경순", "연락처": "010-5728-9427"},{"위치": "반장", "성명": "허영찬", "연락처": "010-9894-3415"}]

# --- [3] 화면 구성 (탭) ---
tab_sec, tab_clean = st.tabs(["🛡️ 보안팀", "🧹 미화팀"])

# [보안팀 탭]
with tab_sec:
    st.markdown('<div class="unified-title">성의교정 보안팀 비상연락망</div>', unsafe_allow_html=True)
    
    sec_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <style>
        body { font-family: 'Malgun Gothic', sans-serif; margin: 0; padding: 5px; background: #ffffff; }
        .grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; }
        .card { height: 42px; border-radius: 4px; display: flex; flex-direction: column; align-items: center; justify-content: center; background: white; border: 1px solid #eeeeee; box-shadow: 0 1px 1px rgba(0,0,0,0.05); cursor: pointer; }
        .empty { visibility: hidden; pointer-events: none; }
        .card:nth-child(4n-2) { border-right: 2px solid #444444; }
        .top { background: #f8f9fa; } .a { background: #ebfbee; } .b { background: #fff5f5; } .c { background: #fff9db; } .dorm { background: #f3fcf3; }
        .p { font-size: 7px; font-weight: bold; color: #888888; margin-bottom: 1px; }
        .n { font-size: 13px; font-weight: bold; color: #333333; }
        #modal { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255, 255, 255, 0.4); backdrop-filter: blur(2px); z-index: 9999; justify-content: center; align-items: center; }
        .modal-c { background: white; width: 85%; max-width: 260px; padding: 20px; border-radius: 15px; text-align: center; border: 1px solid #ddd; box-shadow: 0 10px 30px rgba(0,0,0,0.15); position: relative; }
        .close { position: absolute; top: 8px; right: 12px; font-size: 22px; color: #bbb; cursor: pointer; }
        .m-t { font-size: 24px; font-weight: bold; margin-bottom: 4px; }
        .m-s { font-size: 15px; color: #1c7ed6; font-weight: bold; margin-bottom: 12px; }
        .m-i { font-size: 14px; color: #666; border-top: 1px solid #f1f3f5; padding-top: 12px; margin-bottom: 15px; line-height: 1.6; }
        .m-tel { font-size: 18px; font-weight: bold; color: #e8590c; margin-bottom: 15px; display: block; }
        .btn { display: block; background: #40c057; color: white; padding: 12px; border-radius: 10px; text-decoration: none; font-weight: bold; font-size: 19px; }
    </style>
    </head>
    <body>
    <div class="grid">
    """
    for m in security_data:
        is_empty = "empty" if m['n'] == "공석" else ""
        p_text = f"{m['g'].upper()}조 {m['p']}" if m['g'] in ['a','b','c'] else m['p']
        if m['g'] == 'dorm': p_text = "기숙사 " + m['p']
        sec_html += f'<div class="card {m["g"]} {is_empty}" onclick="openM(\'{m["n"]}\',\'{p_text}\',\'{m["t"]}\',\'{m["b"]}\',\'{m["e"]}\')"><span class="p">{p_text}</span><span class="n">{m["n"]}</span></div>'

    sec_html += """
    </div>
    <div id="modal" onclick="closeM()"><div class="modal-c" onclick="event.stopPropagation()"><span class="close" onclick="closeM()">&times;</span><div id="mName" class="m-t"></div><div id="mPos" class="m-s"></div><div class="m-i">🎂 생년: <span id="mB"></span><br>📅 입사: <span id="mE"></span></div><div id="mTD" class="m-tel"></div><a id="mC" href="" class="btn">📞 전화 걸기</a></div></div>
    <script>
        function openM(n,p,t,b,e){ if(n==='공석')return; document.getElementById('mName').innerText=n; document.getElementById('mPos').innerText=p; document.getElementById('mB').innerText=b; document.getElementById('mE').innerText=e; document.getElementById('mTD').innerText=t; document.getElementById('mC').href="tel:"+t; document.getElementById('modal').style.display='flex'; }
        function closeM(){ document.getElementById('modal').style.display='none'; }
    </script>
    </body></html>
    """
    components.html(sec_html, height=550, scrolling=False)

# [미화팀 탭]
with tab_clean:
    st.markdown('<div class="unified-title">성의교정 미화팀 비상연락망</div>', unsafe_allow_html=True)
    
    # 미화팀 빌딩 선택 상태 관리
    if 'bld' not in st.session_state: st.session_state.bld = "성희회관"
    
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🏢 성희회관", use_container_width=True): st.session_state.bld = "성희회관"
    with c2:
        if st.button("🔬 의산연", use_container_width=True): st.session_state.bld = "의산연"

    view_bld = st.session_state.bld
    target_data = data_sunghee if view_bld == "성희회관" else data_uisan

    clean_html = f"""
    <div style="font-family: sans-serif; color: #333;">
        <p style="margin: 10px 0 5px 0; font-size: 14px; font-weight: bold; color: #666;">📍 {view_bld} 명단</p>
        <table style="width: 100%; border-collapse: collapse; font-size: 14px; border-top: 2px solid #444;">
            <tr style="background-color: #f8f9fa;">
                <th style="padding: 8px 2px; border-bottom: 1px solid #ccc; width: 25%;">위치</th>
                <th style="padding: 8px 2px; border-bottom: 1px solid #ccc; width: 25%;">성명</th>
                <th style="padding: 8px 2px; border-bottom: 1px solid #ccc; width: 50%;">연락처</th>
            </tr>
    """
    for row in target_data:
        clean_html += f"""
            <tr style="border-bottom: 1px solid #eee;">
                <td style="padding: 8px 2px; text-align: center;"><b>{row['위치']}</b></td>
                <td style="padding: 8px 2px; text-align: center;">{row['성명']}</td>
                <td style="padding: 8px 2px; text-align: center;">
                    <a href="tel:{row['연락처']}" style="color: #007bff; text-decoration: none; font-weight: bold;">{row['연락처']}</a>
                </td>
            </tr>
        """
    clean_html += "</table></div>"
    components.html(clean_html, height=700, scrolling=True)
