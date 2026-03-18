import streamlit as st

st.set_page_config(page_title="보안 통합 연락망", layout="wide")

# 1. 데이터 베이스 (지휘 체계 및 구역별 정렬)
# 이미지 스케치 순서: 반장/소장/부소장/반장 -> 회관A/옴니A -> 회관B/옴니B ...
CONTACTS = [
    {"pos": "반장", "name": "유정수", "tel": "010-5316-8065"},
    {"pos": "소장", "name": "이규용", "tel": "010-8883-6580"},
    {"pos": "부소", "name": "박상현", "tel": "010-3193-4603"},
    {"pos": "반장", "name": "오제준", "tel": "010-3352-8933"},
    {"pos": "조장", "name": "배준용", "tel": "010-4717-7065"},
    {"pos": "조원", "name": "이명구", "tel": "010-8638-5819"},
    {"pos": "조장", "name": "손병휘", "tel": "010-9966-2090"},
    {"pos": "조원", "name": "권순호", "tel": "010-2539-1799"},
    # ... 나머지 28명 인원 순차 입력 가능
]

# 2. 강제 4열 그리드 스타일 (모바일 깨짐 방지 핵심)
st.markdown("""
    <style>
    .main-title { font-size: 22px; font-weight: bold; text-align: center; margin-bottom: 15px; }
    .grid-container {
        display: grid;
        grid-template-columns: repeat(4, 1fr); /* 무조건 가로 4칸 */
        gap: 6px;
        padding: 5px;
    }
    .grid-item {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 6px;
        padding: 8px 2px;
        text-align: center;
        text-decoration: none;
        color: #333;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 60px;
    }
    .grid-item:active { background: #f8f9fa; border-color: #007bff; }
    .p-pos { font-size: 10px; color: #007bff; margin-bottom: 2px; }
    .p-name { font-size: 13px; font-weight: bold; }
    .area-label { background: #f1f3f5; padding: 5px; font-size: 12px; font-weight: bold; text-align: center; border-radius: 5px; margin: 10px 0; }
    </style>
""", unsafe_allow_html=True)

# 3. 화면 렌더링
st.markdown('<div class="main-title">📱 보안팀 비상연락망</div>', unsafe_allow_html=True)

# 구역 표시 라벨
col1, col2 = st.columns(2)
with col1: st.markdown('<div class="area-label">🏢 성의회관 / 의산연</div>', unsafe_allow_html=True)
with col2: st.markdown('<div class="area-label">🏫 옴니버스</div>', unsafe_allow_html=True)

# 전체 4x7 그리드 생성 (HTML 방식)
grid_content = '<div class="grid-container">'
for person in CONTACTS:
    link = f"tel:{person['tel'].replace('-', '')}"
    grid_content += f'''
        <a href="{link}" class="grid-item">
            <span class="p-pos">{person['pos']}</span>
            <span class="p-name">{person['name']}</span>
        </a>
    '''
grid_content += '</div>'

# 최종 출력 (코드가 노출되지 않게 한 번에 렌더링)
st.markdown(grid_content, unsafe_allow_html=True)

st.write("---")
st.caption("💡 각 이름을 누르면 해당 인원에게 즉시 전화를 겁니다.")
