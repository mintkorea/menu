import streamlit as st

st.set_page_config(page_title="보안 비상연락망", layout="wide")

# 1. 통합 데이터 (스케치 및 사진 기반 28인 명단)
# 데이터를 기반으로 배치
CONTACT_DATA = [
    # 지휘부 (첫 줄)
    {"성명": "유정수", "직위": "반장", "tel": "010-5316-8065"},
    {"성명": "이규용", "직위": "소장", "tel": "010-8883-6580"},
    {"성명": "박상현", "직위": "부소장", "tel": "010-3193-4603"},
    {"성명": "오제준", "직위": "반장", "tel": "010-3352-8933"},
    # A조 (회관 vs 옴니)
    {"성명": "배준용", "직위": "조장", "tel": "010-4717-7065"},
    {"성명": "이명구", "직위": "조원", "tel": "010-8638-5819"},
    {"성명": "손병휘", "직위": "조장", "tel": "010-9966-2090"},
    {"성명": "권순호", "직위": "조원", "tel": "010-2539-1799"},
    # (이하 28명 인원 동일 패턴으로 추가 가능...)
]

# 2. 강제 4열 그리드 CSS 정의
st.markdown("""
    <style>
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr); /* 무조건 4열 고정 */
        gap: 8px;
        padding: 10px;
    }
    .grid-item {
        background-color: #ffffff;
        border: 1px solid #dee2e6;
        border-radius: 8px;
        padding: 10px 5px;
        text-align: center;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        cursor: pointer;
        text-decoration: none;
        color: inherit;
    }
    .grid-item:active { background-color: #e9ecef; }
    .name { font-weight: bold; font-size: 14px; color: #333; display: block; }
    .pos { font-size: 11px; color: #666; margin-bottom: 5px; display: block; }
    .call-icon { font-size: 16px; color: #28a745; }
    </style>
""", unsafe_allow_html=True)

# 3. 화면 구현
st.subheader("📱 보안팀 비상연락망 (4x7 배치)")

# 상단 탭/구역 표시 (스케치 반영)
col1, col2 = st.columns(2)
with col1: st.info("🏢 회관 / 의산연")
with col2: st.info("🏫 옴니버스")

# 4x7 그리드 생성
grid_html = '<div class="grid-container">'
for person in CONTACT_DATA:
    tel_link = f"tel:{person['tel'].replace('-', '')}"
    grid_html += f'''
        <a href="{tel_link}" class="grid-item">
            <span class="pos">{person['직위']}</span>
            <span class="name">{person['성명']}</span>
            <span class="call-icon">📞</span>
        </a>
    '''
grid_html += '</div>'

# HTML 출력
st.markdown(grid_html, unsafe_allow_html=True)

st.write("---")
st.caption("💡 각 카드를 누르면 즉시 전화로 연결됩니다.")
