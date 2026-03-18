import streamlit as st

st.set_page_config(page_title="보안 비상연락망", layout="wide")

# 데이터를 관리하기 편하도록 사전(Dict) 형태로 정리
security_data = {
    "배준용(장)": {"role": "A조장", "phone": "010-4717-7065", "birth": "1969.12.24", "join": "2022.07.26"},
    "이명구": {"role": "A조원", "phone": "010-8638-5819", "birth": "1964.09.15", "join": "2025.03.21"},
    "손병휘(장)": {"role": "A조장", "phone": "010-9966-2090", "birth": "1972.05.23", "join": "2016.05.05"},
    "권순호": {"role": "A조원", "phone": "010-2539-1799", "birth": "1980.12.14", "join": "2026.02.11"},
    # 필요한 인원을 여기에 계속 추가
}

# 상단 고정 스타일 설정
st.markdown("""
    <style>
    .info-box {
        background-color: #f0f7ff; padding: 15px; border-radius: 10px;
        border: 2px solid #007bff; margin-bottom: 20px;
    }
    .call-btn {
        display: block; width: 100%; background: #007bff; color: white !important;
        text-align: center; padding: 10px; border-radius: 5px;
        text-decoration: none; font-weight: bold; margin-top: 10px;
    }
    /* 라디오 버튼 텍스트 크기 조절 */
    div[data-testid="stMarkdownContainer"] > p { font-size: 14px; }
    </style>
""", unsafe_allow_html=True)

# 1. 상세 정보 표시 영역 (라디오 버튼 선택에 따라 변경)
selected_name = st.session_state.get('selected_name', "이름을 선택하세요")

if selected_name in security_data:
    m = security_data[selected_name]
    st.markdown(f"""
        <div class="info-box">
            <b style="font-size:18px;">{selected_name} ({m['role']})</b><br>
            🎂 생일: {m['birth']} | 📅 입사: {m['join']}<br>
            <a href="tel:{m['phone'].replace('-','')}" class="call-btn">📞 {m['phone']} 전화걸기</a>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("아래 명단에서 이름을 선택하면 상세 정보가 나타납니다.")

st.write("---")

# 2. 강제 좌우 배치를 위한 라디오 버튼 (horizontal=True)
st.write("🏢 **회관/의산연 vs 🏫 옴니버스**")

# 좌우 선택을 먼저 유도하거나, 아예 조별로 라디오 버튼을 가로로 배치
col1, col2 = st.columns(2) # 여기서는 레이아웃 목적이 아닌 그룹핑용

with col1:
    st.caption("🏥 회관/의산연 A조")
    choice_l = st.radio("선택", ["미선택", "배준용(장)", "이명구", "김영중", "김삼동"], 
                        horizontal=True, label_visibility="collapsed", key="radio_l")
    if choice_l != "미선택":
        st.session_state.selected_name = choice_l
        st.rerun()

with col2:
    st.caption("🏫 옴니버스 A조")
    choice_r = st.radio("선택", ["미선택", "손병휘(장)", "권순호", "김전식"], 
                        horizontal=True, label_visibility="collapsed", key="radio_r")
    if choice_r != "미선택":
        st.session_state.selected_name = choice_r
        st.rerun()
