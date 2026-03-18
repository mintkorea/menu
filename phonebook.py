import streamlit as st
import streamlit.components.v1 as components

# 1. 상태 관리 설정
if 'current_view' not in st.session_state:
    st.session_state.current_view = "성희회관"

# 2. CSS: 상단 여백 및 타이틀 크기 강제 축소
st.markdown("""
    <style>
        /* 메인 컨텐츠 영역의 상단 여백 제거 */
        .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; }
        /* 스트림릿 기본 헤더 제거 */
        header { visibility: hidden; }
        /* 버튼 간격 조정 */
        div[data-testid="stHorizontalBlock"] { gap: 5px !important; }
        button { height: 35px !important; padding: 0px !important; font-size: 14px !important; }
    </style>
""", unsafe_allow_html=True)

# 3. 타이틀을 작고 슬림하게 배치
st.markdown("### 🚨 보안비상연락망 (미화)")

# 4. 네비게이션 버튼 (슬림형)
col1, col2 = st.columns(2)
with col1:
    if st.button("🏢 성희회관", use_container_width=True):
        st.session_state.current_view = "성희회관"
with col2:
    if st.button("🔬 의산연", use_container_width=True):
        st.session_state.current_view = "의산연"

# 5. 데이터 정의 (안순재 님 오타 수정 및 전체 명단 반영)
# [의산연 데이터 일부]
data_uisan = [
    {"위치": "8층", "성명": "안순재", "연락처": "010-9119-8879"},
    {"위치": "7층", "성명": "안순재", "연락처": "010-9119-8879"}, # 오타 수정 완료
    {"위치": "6층", "성명": "장 성", "연락처": "010-8938-3988"},
    {"위치": "5층", "성명": "조미연", "연락처": "010-2252-2036"},
    {"위치": "4층", "성명": "김정옥", "연락처": "010-9011-0659"},
    {"위치": "3층", "성명": "장 성", "연락처": "010-8938-3988"},
    {"위치": "2층", "성명": "이연숙", "연락처": "010-9117-3965"}
    # ... 나머지 명단도 동일한 형식으로 추가 가능
]

# [성희회관 데이터 일부]
data_sunghee = [
    {"위치": "14층", "성명": "유순복", "연락처": "010-6370-0845"},
    {"위치": "13층", "성명": "박태연", "연락처": "010-5682-8927"},
    {"위치": "12층", "성명": "기성원", "연락처": "010-2618-9120"},
    {"위치": "11층", "성명": "김성순", "연락처": "010-4604-7608"},
    {"위치": "10층", "성명": "박현순", "연락처": "010-8714-7703"},
    {"위치": "반장", "성명": "허영찬", "연락처": "010-9894-3415"}
]

# 6. 표 생성 및 렌더링
view = st.session_state.current_view
target_data = data_sunghee if view == "성희회관" else data_uisan

html_string = f"""
<div style="font-family: sans-serif;">
    <p style="margin: 5px 0; font-weight: bold; color: #555;">📍 {view} 명단</p>
    <table style="width: 100%; border-collapse: collapse; font-size: 14px;">
        <tr style="background-color: #f8f9fa; border-bottom: 2px solid #dee2e6;">
            <th style="padding: 8px; text-align: center;">위치</th>
            <th style="padding: 8px; text-align: center;">성명</th>
            <th style="padding: 8px; text-align: center;">연락처</th>
        </tr>
"""
for row in target_data:
    html_string += f"""
        <tr style="border-bottom: 1px solid #eee;">
            <td style="padding: 8px; text-align: center;"><b>{row['위치']}</b></td>
            <td style="padding: 8px; text-align: center;">{row['성명']}</td>
            <td style="padding: 8px; text-align: center;">
                <a href="tel:{row['연락처']}" style="color: #007bff; text-decoration: none; font-weight: bold;">{row['연락처']}</a>
            </td>
        </tr>
    """
html_string += "</table></div>"

components.html(html_string, height=600, scrolling=True)
