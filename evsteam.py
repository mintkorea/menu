
import streamlit as st
import streamlit.components.v1 as components

# 1. 페이지 설정 및 여백 극소화
st.set_page_config(page_title="미화 연락망", layout="centered")

st.markdown("""
    <style>
        /* 전체 여백 제거 */
        .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
        header { visibility: hidden; }
        #MainMenu { visibility: hidden; }
        
        /* 버튼 슬림화 */
        div[data-testid="stHorizontalBlock"] { gap: 5px !important; }
        button { height: 32px !important; font-size: 14px !important; padding: 0px !important; }
        
        /* 타이틀 슬림화 */
        .main-title { font-size: 18px; font-weight: bold; margin-bottom: 8px; color: #222; }
    </style>
""", unsafe_allow_html=True)

# 2. 상태 관리
if 'building' not in st.session_state:
    st.session_state.building = "성희회관"

# 3. 데이터 복원 (수정 사항 반영)
# 의산연 명단
data_uisan = [
    {"위치": "8층", "성명": "안순재", "연락처": "010-9119-8879"},
    {"위치": "7층", "성명": "안순재", "연락처": "010-9119-8879"},
    {"위치": "6층", "성명": "장 성", "연락처": "010-8938-3988"},
    {"위치": "5층", "성명": "조미연", "연락처": "010-2252-2036"},
    {"위치": "4층", "성명": "김정옥", "연락처": "010-9011-0659"},
    {"위치": "3층", "성명": "장 성", "연락처": "010-8938-3988"},
    {"위치": "세포실", "성명": "이연숙", "연락처": "010-9117-3965"}, # 2층 -> 세포실 수정
    {"위치": "3층(세포)", "성명": "강민례", "연락처": "010-3385-9952"},
    {"위치": "1층(남)", "성명": "이정숙", "연락처": "010-3722-0765"},
    {"위치": "1층(북)", "성명": "이명자", "연락처": "010-6274-2355"},
    {"위치": "B1층", "성명": "이서빈", "연락처": "010-7755-8613"},
    {"위치": "B2층", "성명": "선양순", "연락처": "010-9967-7301"},
    {"위치": "본관지원", "성명": "정순식", "연락처": "010-9564-0029"},
    {"위치": "본관지원", "성명": "조성일", "연락처": "010-3952-2441"},
    {"위치": "별관 5층", "성명": "이선자", "연락처": "010-8210-7106"},
    {"위치": "별관 3,4", "성명": "김인숙", "연락처": "010-4120-6055"},
    {"위치": "별관 1,2", "성명": "정혜숙", "연락처": "010-9130-0652"},
    {"위치": "별관지원", "성명": "이창남", "연락처": "010-3133-0638"}
]

# 성희회관 명단
data_sunghee = [
    {"위치": "14층", "성명": "유순복", "연락처": "010-6370-0845"},
    {"위치": "13층", "성명": "박태연", "연락처": "010-5682-8927"},
    {"위치": "12층", "성명": "기성원", "연락처": "010-2618-9120"},
    {"위치": "11층", "성명": "김성순", "연락처": "010-4604-7608"},
    {"위치": "10층", "성명": "박현순", "연락처": "010-8714-7703"},
    {"위치": "9층", "성명": "이재숙", "연락처": "010-8762-1178"},
    {"위치": "9층", "성명": "채예홍", "연락처": "010-5202-4638"},
    {"위치": "8층", "성명": "이애란", "연락처": "010-3046-8520"},
    {"위치": "7층", "성명": "박인순", "연락처": "010-5745-1427"},
    {"위치": "6층", "성명": "김순이", "연락처": "010-6370-6807"},
    {"위치": "5층", "성명": "최정숙", "연락처": "010-3850-2011"},
    {"위치": "4,5층", "성명": "신춘옥", "연락처": "010-2305-8914"},
    {"위치": "4층", "성명": "조계순", "연락처": "010-2211-7864"},
    {"위치": "3층", "성명": "김옥화", "연락처": "010-8000-9643"},
    {"위치": "2층", "성명": "임윤숙", "연락처": "010-3283-2799"},
    {"위치": "1층", "성명": "허봉혜", "연락처": "010-9014-7470"},
    {"위치": "1층", "성명": "양명선", "연락처": "010-6671-1442"},
    {"위치": "지원(외곽)", "성명": "김철규", "연락처": "010-6299-0079"},
    {"위치": "지원(승강)", "성명": "천제수", "연락처": "010-7537-6059"},
    {"위치": "지원(주차)", "성명": "박문희", "연락처": "010-8859-9333"},
    {"위치": "지원(전층)", "성명": "최연주", "연락처": "010-5744-1772"},
    {"위치": "지원(여)", "성명": "양경순", "연락처": "010-5728-9427"},
    {"위치": "반장", "성명": "허영찬", "연락처": "010-9894-3415"}
]

# 4. 화면 구성
st.markdown('<p class="main-title">📞 미화 비상연락망</p>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    if st.button("🏢 성희회관", use_container_width=True):
        st.session_state.building = "성희회관"
with col2:
    if st.button("🔬 의산연", use_container_width=True):
        st.session_state.building = "의산연"

# 5. HTML 표 렌더링 (줄 간격 최적화)
view = st.session_state.building
target = data_sunghee if view == "성희회관" else data_uisan

html_code = f"""
<div style="font-family: sans-serif; color: #333;">
    <p style="margin: 5px 0; font-size: 13px; font-weight: bold; color: #666;">📍 {view} 명단</p>
    <table style="width: 100%; border-collapse: collapse; font-size: 13.5px; border-top: 2px solid #444;">
        <tr style="background-color: #f8f9fa;">
            <th style="padding: 6px 2px; border-bottom: 1px solid #ccc; width: 25%;">위치</th>
            <th style="padding: 6px 2px; border-bottom: 1px solid #ccc; width: 25%;">성명</th>
            <th style="padding: 6px 2px; border-bottom: 1px solid #ccc; width: 50%;">연락처</th>
        </tr>
"""

for row in target:
    html_code += f"""
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 6px 2px; text-align: center; background-color: #fff;"><b>{row['위치']}</b></td>
            <td style="padding: 6px 2px; text-align: center;">{row['성명']}</td>
            <td style="padding: 6px 2px; text-align: center;">
                <a href="tel:{row['연락처']}" style="color: #007bff; text-decoration: none; font-weight: bold; font-size: 14.5px;">{row['연락처']}</a>
            </td>
        </tr>
    """

html_code += "</table></div>"

# 높이를 더 촘촘하게 설정하여 스크롤 최소화
components.html(html_code, height=750, scrolling=True)
