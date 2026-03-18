import streamlit as st

# 페이지 설정
st.set_page_config(page_title="보안 비상연락망", layout="wide")

# 1. 28명 전체 데이터 (이미지 순서에 맞춘 배치)
# 빈 칸(X)은 "공석"으로 처리하여 그리드 균형을 맞춥니다.
CONTACT_DATA = [
    {"pos": "반장", "name": "유정수", "tel": "010-5316-8065"},
    {"pos": "소장", "name": "이규용", "tel": "010-8883-6580"},
    {"pos": "부소", "name": "박상현", "tel": "010-3193-4603"},
    {"pos": "반장", "name": "오제준", "tel": "010-3352-8933"},
    # A조 영역
    {"pos": "A장", "name": "배준용", "tel": "010-4717-7065"},
    {"pos": "A원", "name": "이명구", "tel": "010-8638-5819"},
    {"pos": "A장", "name": "손병휘", "tel": "010-9966-2090"},
    {"pos": "A원", "name": "권순호", "tel": "010-2539-1799"},
    # B조 영역
    {"pos": "B장", "name": "심규천", "tel": "010-8287-9895"},
    {"pos": "B원", "name": "임종현", "tel": "010-7741-6732"},
    {"pos": "B장", "name": "황일범", "tel": "010-8929-4294"},
    {"pos": "B원", "name": "이상길", "tel": "010-9904-0247"},
    # C조 및 기타 (스케치에 따라 확장 가능)
]

# 2. 강제 그리드 주입 (이 부분이 있어야 모바일에서 안 깨집니다)
st.markdown("""
    <style>
    /* 무조건 4열 고정 CSS */
    .grid-wrapper {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 6px;
        width: 100%;
    }
    .grid-box {
        background-color: #f8f9fa;
        border: 1px solid #ddd;
        border-radius: 8px;
        padding: 10px 2px;
        text-align: center;
        text-decoration: none;
        color: black;
        font-family: sans-serif;
    }
    .grid-box:active { background-color: #e2e6ea; }
    .label-pos { font-size: 10px; color: #007bff; display: block; }
    .label-name { font-size: 13px; font-weight: bold; display: block; }
    
    /* 구역 구분 라벨 */
    .area-header {
        display: flex; justify-content: space-between;
        padding: 5px; margin-top: 10px; font-size: 12px; font-weight: bold;
        background: #eee; border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. 화면 구성
st.subheader("📱 보안팀 통합 연락망 (4x7)")

# 구역 가이드 (스케치 반영)
st.markdown("""
    <div class="area-header">
        <span>🏢 성의회관 / 의산연</span>
        <span>🏫 옴니버스</span>
    </div>
""", unsafe_allow_html=True)

# 4. 그리드 출력 (HTML 코드가 텍스트로 보이지 않게 함)
grid_html = '<div class="grid-wrapper">'
for person in CONTACT_DATA:
    tel_link = f"tel:{person['tel'].replace('-', '')}"
    grid_html += f'''
        <a href="{tel_link}" class="grid-box">
            <span class="label-pos">{person['pos']}</span>
            <span class="label-name">{person['name']}</span>
        </a>
    '''
grid_html += '</div>'

# 최종 렌더링
st.markdown(grid_html, unsafe_allow_html=True)

st.write("---")
st.caption("💡 각 칸을 터치하면 즉시 전화 앱으로 연결됩니다.")
