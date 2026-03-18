import streamlit as st

st.set_page_config(page_title="보안/미화 비상연락망", layout="wide")

# 1. 통합 데이터 정리 (보안/미화 전체)
all_data = {
    "배준용(장)": {"role": "보안 A조장", "phone": "010-4717-7065", "birth": "1969.12.24", "join": "2022.07.26"},
    "이명구": {"role": "보안 A조원", "phone": "010-8638-5819", "birth": "1964.09.15", "join": "2025.03.21"},
    "손병휘(장)": {"role": "보안 A조장(옴니)", "phone": "010-9966-2090", "birth": "1972.05.23", "join": "2016.05.05"},
    "유순복": {"role": "미화 14층", "phone": "010-6370-0845", "birth": "-", "join": "2026.06~"},
    "박태연": {"role": "미화 13층", "phone": "010-5682-8927", "birth": "-", "join": "2026.06~"}
}

# 2. 스타일: 상단 정보창 고정 및 가독성 향상
st.markdown("""
    <style>
    .info-card {
        background-color: #f8fbff; padding: 15px; border-radius: 12px;
        border: 2px solid #3b82f6; margin-bottom: 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .call-btn {
        display: block; width: 100%; background: #2563eb; color: white !important;
        text-align: center; padding: 12px; border-radius: 8px;
        text-decoration: none; font-weight: bold; margin-top: 10px; font-size: 16px;
    }
    div[data-testid="stRadio"] > div { flex-direction: row !important; flex-wrap: wrap; gap: 10px; }
    </style>
""", unsafe_allow_html=True)

# 3. 상태 관리 및 정보 노출 (화면 흐림 없이 즉시 반영)
# 세션 스테이트를 사용하여 선택된 값을 상단에 즉시 표시
if 'choice' not in st.session_state:
    st.session_state.choice = "미선택"

# --- 상단 고정 정보창 ---
if st.session_state.choice in all_data:
    m = all_data[st.session_state.choice]
    st.markdown(f"""
        <div class="info-card">
            <h3 style='margin:0; color:#1e40af;'>👤 {st.session_state.choice} <small>({m['role']})</small></h3>
            <p style='margin:8px 0;'>🎂 생일: {m['birth']} | 📅 입사: {m['join']}</p>
            <a href="tel:{m['phone'].replace('-','')}" class="call-btn">📞 {m['phone']} 전화걸기</a>
        </div>
    """, unsafe_allow_html=True)
else:
    st.info("💡 아래 명단에서 이름을 선택하면 즉시 정보가 나타납니다.")

st.write("---")

# 4. 명단 배치 (라디오 버튼 - 가로 배치 고정)
st.subheader("🏥 성의회관/의산연 보안 (A조)")
# index=0을 '미선택'으로 두어 초기화 상태 유지
res_a = st.radio("보안_A", ["미선택", "배준용(장)", "이명구", "김영중", "김삼동"], horizontal=True, key="sec_a", label_visibility="collapsed")
if res_a != "미선택":
    st.session_state.choice = res_a

st.subheader("🏫 옴니버스 보안 (A조)")
res_o = st.radio("보안_O", ["미선택", "손병휘(장)", "권순호", "김전식"], horizontal=True, key="sec_o", label_visibility="collapsed")
if res_o != "미선택":
    st.session_state.choice = res_o

st.subheader("🧹 성의회관 미화팀")
res_m = st.radio("미화", ["미선택", "유순복", "박태연", "기성원", "김성순"], horizontal=True, key="mihwa", label_visibility="collapsed")
if res_m != "미선택":
    st.session_state.choice = res_m

# 5. 화면 갱신 트리거 (선택 시 흐림 현상 최소화)
if st.button("🔄 정보 초기화"):
    st.session_state.choice = "미선택"
    st.rerun()
