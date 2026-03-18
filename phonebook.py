import streamlit as st

st.set_page_config(page_title="비상연락망", layout="wide")

# 1. 사진 데이터를 바탕으로 한 통합 명단 (보안/미화)
# 보내주신 사진의 데이터를 모두 포함했습니다.
contact_data = {
    # 보안팀
    "이규용": {"role": "보안소장", "phone": "010-8883-6580", "info": "지휘부"},
    "박상현": {"role": "보안부소장", "phone": "010-3193-4603", "info": "지휘부"},
    "배준용": {"role": "보안 A조장", "phone": "010-4717-7065", "info": "성의회관"},
    "손병휘": {"role": "보안 A조장", "phone": "010-9966-2090", "info": "옴니버스"},
    # 성의회관 미화팀
    "유순복": {"role": "미화 14층", "phone": "010-6370-0845", "info": "성의회관"},
    "박태연": {"role": "미화 13층", "phone": "010-5682-8927", "info": "성의회관"},
    # 의산연 미화팀
    "안순재": {"role": "미화 8층", "phone": "010-9119-8879", "info": "의산연"},
    "장성": {"role": "미화 6층", "phone": "010-8938-3988", "info": "의산연"}
}

# 2. 모바일 강제 2열 및 고정창 디자인
st.markdown("""
    <style>
    /* 상단 정보 고정창 */
    .fixed-header {
        position: sticky; top: 0; z-index: 1000;
        background-color: #f0f7ff; padding: 15px;
        border-bottom: 3px solid #007bff; border-radius: 0 0 15px 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 20px;
    }
    /* 강제 2열 그리드 */
    .grid-container {
        display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
    }
    /* 버튼 스타일 */
    .stButton>button {
        width: 100%; height: 45px; border-radius: 8px;
        background-color: white; border: 1px solid #ddd; font-size: 14px;
    }
    .call-link {
        display: block; background: #007bff; color: white !important;
        text-align: center; padding: 12px; border-radius: 8px;
        text-decoration: none; font-weight: bold; margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 상태 관리 (선택된 인원)
if 'target' not in st.session_state:
    st.session_state.target = None

def update_target(name):
    st.session_state.target = name

# --- 상단 고정 정보창 ---
with st.container():
    st.markdown('<div class="fixed-header">', unsafe_allow_html=True)
    if st.session_state.target:
        name = st.session_state.target
        person = contact_data[name]
        st.markdown(f"""
            <h3 style='margin:0; color:#007bff;'>👤 {name} <small style='color:#666;'>({person['role']})</small></h3>
            <p style='margin:5px 0; font-size:14px;'>📍 소속: {person['info']}</p>
            <a href="tel:{person['phone'].replace('-','')}" class="call-link">📞 {person['phone']} 전화걸기</a>
        """, unsafe_allow_html=True)
    else:
        st.markdown("<p style='margin:0; color:#666;'>💡 명단에서 이름을 클릭하세요.</p>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 하단 명단 리스트 (강제 2열) ---
st.write("### 🏢 시설 비상연락망")

# 그룹별로 버튼 배치
groups = {
    "🏥 보안 (회관/의산연)": ["배준용", "이명구", "김영중", "김삼동"],
    "🏫 보안 (옴니버스)": ["손병휘", "권순호", "김전식"],
    "🧹 미화 (회관)": ["유순복", "박태연", "기성원", "김성순"]
}

for group_name, members in groups.items():
    st.caption(group_name)
    # HTML 그리드 안에서 Streamlit 버튼 실행
    st.markdown('<div class="grid-container">', unsafe_allow_html=True)
    cols = st.columns(2)
    for i, name in enumerate(members):
        with cols[i % 2]:
            if st.button(name, key=f"btn_{name}"):
                update_target(name)
                st.rerun()
