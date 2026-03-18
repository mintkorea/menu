import streamlit as st

# 1. 페이지 설정 및 데이터 정의
if 'menu_tab' not in st.session_state:
    st.session_state.menu_tab = "성희회관"

# 성희회관 데이터 (사진 기반)
data_sunghee = [
    {"위치": "14층", "성명": "유순복", "연락처": "010-6370-0845", "비고": "B조(1직)"},
    {"위치": "13층", "성명": "박태연", "연락처": "010-5682-8927", "비고": "B조(1직)"},
    {"위치": "12층", "성명": "기성원", "연락처": "010-2618-9120", "비고": "A조(2직)"},
    {"위치": "11층", "성명": "김성순", "연락처": "010-4604-7608", "비고": "A조(3직)"},
    {"위치": "10층", "성명": "박현순", "연락처": "010-8714-7703", "비고": "B조(1직)"},
    {"위치": "9층", "성명": "이재숙", "연락처": "010-8762-1178", "비고": "A조(3직)"},
    {"위치": "반장", "성명": "허영찬", "연락처": "010-9894-3415", "비고": "A조(B조 지원)"},
]

# 의산연 데이터 (사진 기반)
data_uisan = [
    {"위치": "8층", "성명": "안순재", "연락처": "010-9119-8879", "비고": "A조"},
    {"위치": "7층", "성명": "안순재", "연락처": "010-9119-8880", "비고": "A조"},
    {"위치": "6층", "성명": "장 성", "연락처": "010-8938-3988", "비고": "B조"},
    {"위치": "5층", "성명": "조미연", "연락처": "010-2252-2036", "비고": "A조"},
    {"위치": "별관 5층", "성명": "이선자", "연락처": "010-8210-7106", "비고": "A조"},
]

# 2. 모바일 최적화 CSS (가로 버튼 고정)
st.markdown("""
<style>
    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
    }
    div[data-testid="column"] { min-width: 0px !important; flex: 1 !important; }
    button { width: 100% !important; font-weight: 800 !important; }
    .contact-table { width: 100%; border-collapse: collapse; font-size: 13px; }
    .contact-table th { background-color: #f8f9fa; padding: 10px; border-bottom: 2px solid #dee2e6; }
    .contact-table td { padding: 10px; border-bottom: 1px solid #eee; text-align: center; }
    .tel-link { color: #007bff; text-decoration: none; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

st.title("🚨 보안비상연락망")

# 3. 네비게이션 버튼 (회관 / 의산연)
col1, col2 = st.columns(2)
with col1:
    if st.button("🏢 성희회관", use_container_width=True):
        st.session_state.menu_tab = "성희회관"
with col2:
    if st.button("🔬 의산연", use_container_width=True):
        st.session_state.menu_tab = "의산연"

st.divider()

# 4. 선택된 건물의 표 출력
current_tab = st.session_state.menu_tab
target_data = data_sunghee if current_tab == "성희회관" else data_uisan

st.subheader(f"📍 {current_tab} 담당자 명단")

# HTML 표 생성 (전화걸기 링크 포함)
table_html = '<table class="contact-table"><tr><th>위치</th><th>성명</th><th>연락처</th></tr>'
for row in target_data:
    table_html += f'''
    <tr>
        <td>{row["위치"]}</td>
        <td>{row["성명"]}</td>
        <td><a class="tel-link" href="tel:{row["연락처"]}">{row["연락처"]}</a></td>
    </tr>
    '''
table_html += '</table>'

st.markdown(table_html, unsafe_allow_html=True)
