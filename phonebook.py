import streamlit as st

st.set_page_config(page_title="보안 비상연락망", layout="centered")

# 스타일 설정: 버튼 간격 최소화 및 카드 디자인
st.markdown("""
    <style>
    .stButton>button {
        width: 100%; text-align: left; border-radius: 0; 
        margin-bottom: -10px; border: none; border-bottom: 1px solid #eee;
        background-color: white; padding: 10px;
    }
    .info-card {
        background-color: #f0f7ff; padding: 15px; 
        border-radius: 8px; margin: 10px 0; border-left: 5px solid #007bff;
    }
    .call-btn {
        display: block; width: 100%; background-color: #007bff; color: white; 
        text-align: center; padding: 12px; border-radius: 5px; 
        text-decoration: none; font-weight: bold; margin-top: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# 클릭 상태 저장용 사전
if 'opened' not in st.session_state:
    st.session_state.opened = {}

def draw_member(name, role, phone, birth, join):
    # 이름 버튼 출력
    if st.button(f"👤 {name} ({role})"):
        st.session_state.opened[name] = True
    
    # 클릭된 상태라면 상세 카드 표출 (닫기 기능 없음)
    if st.session_state.opened.get(name):
        st.markdown(f"""
            <div class="info-card">
                <p>🎂 <b>생년월일:</b> {birth}</p>
                <p>📅 <b>입사일자:</b> {join}</p>
                <p>📞 <b>연락처:</b> {phone}</p>
                <a href="tel:{phone.replace('-','')}" class="call-btn">즉시 전화걸기</a>
            </div>
        """, unsafe_allow_html=True)

# --- 실제 명단 배치 ---

st.caption("🚩 지휘부")
draw_member("이규용", "소장", "010-8883-6580", "1972.03.01", "-")
draw_member("박상현", "부소장", "010-3193-4603", "1988.07.31", "-")

st.divider()
st.caption("🏥 성의회관 / 의산연")
draw_member("유정수", "반장", "010-5316-8065", "1970.09.25", "2020.09.01")

st.write("🅰️ **A조**")
draw_member("배준용", "조장", "010-4717-7065", "1969.12.24", "2022.07.26")
draw_member("이명구", "조원", "010-8638-5819", "1964.09.15", "2025.03.21")
draw_member("김영중", "조원", "010-7726-5963", "1959.02.26", "2024.08.21")
draw_member("김삼동", "조원", "010-2345-8081", "1967.02.01", "2025.05.02")

# B조, C조 및 옴니버스도 동일한 draw_member 함수로 쭉 나열하면 됩니다.
