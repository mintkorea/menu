import streamlit as st

# 1. 페이지 설정 (layout="wide" 유지)
st.set_page_config(page_title="성의 워크플레이스 허브", page_icon="🏫", layout="wide")

# 2. 초기 데이터 설정
if 'apps' not in st.session_state:
    st.session_state.apps = [
        {"title": "📱 대관 조회 (모바일)", "url": "https://klzsyte9n8ftnuwcuid9tw.streamlit.app/", "desc": "현장용 대관 및 당직 내역 확인", "color": "#1E3A5F"},
        {"title": "💻 대관 관리 (PC)", "url": "https://rental-2q7nwue9hmapek9nuir6vh.streamlit.app/", "desc": "엑셀 다운로드 및 상세 조회", "color": "#1E3A5F"},
        {"title": "🍱 주간 식단표", "url": "https://3y2krzjwosv86ccxobc38i.streamlit.app/", "desc": "교내 식당 메뉴 및 식사 정보", "color": "#4CAF50"},
        {"title": "🚨 보안 비상연락망", "url": "https://t78ulrec88a9tku62zekge.streamlit.app/", "desc": "보안파트 긴급 연락처", "color": "#F44336"},
        {"title": "미화 비상연락망", "url": "https://mintkorea-evsteam.streamlit.app/", "desc": "미화 파트 비상연락처", "color": "#F44336"}
    ]

# 3. 디자인 스타일 (상단 여백 제거 CSS 포함)
st.markdown("""
<style>
    /* 상단 여백 및 패딩 제거 */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 800px;
        margin: auto;
    }
    /* 사이드바 너비 조정 */
    section[data-testid="stSidebar"] {
        width: 300px !important;
    }
    .hub-title { 
        font-size: 26px; 
        font-weight: 800; 
        text-align: center; 
        color: #1E3A5F; 
        margin-top: 0px; 
        margin-bottom: 20px; 
    }
    .app-card {
        display: block; padding: 16px; border-radius: 12px; border: 1px solid #E0E0E0;
        text-decoration: none !important; margin-bottom: 12px; transition: 0.2s;
        background: white; border-left: 8px solid #1E3A5F;
    }
    .app-card:hover { background: #F0F4F8; transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.05); }
    .app-title { font-size: 18px; font-weight: bold; color: #1E3A5F; }
    .app-desc { font-size: 13px; color: #666; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# 4. 사이드바 구성 (사이드바가 항상 보이도록 설정)
# 모바일에서는 왼쪽 상단 '>' 화살표를 눌러야 열릴 수 있습니다.
with st.sidebar:
    st.title("🛠️ 런처 관리")
    st.write("앱 목록을 수정할 수 있습니다.")
    
    # 추가 기능
    with st.expander("➕ 앱 추가", expanded=False):
        new_title = st.text_input("이름")
        new_url = st.text_input("URL")
        new_desc = st.text_input("설명")
        new_color = st.color_picker("색상", "#1E3A5F")
        if st.button("추가"):
            if new_title and new_url:
                st.session_state.apps.append({"title": new_title, "url": new_url, "desc": new_desc, "color": new_color})
                st.rerun()

    # 삭제 기능
    if st.session_state.apps:
        with st.expander("🗑️ 앱 삭제"):
            app_names = [app['title'] for app in st.session_state.apps]
            target = st.selectbox("삭제 대상", app_names)
            if st.button("삭제"):
                st.session_state.apps = [a for a in st.session_state.apps if a['title'] != target]
                st.rerun()

# 5. 메인 화면 출력
st.markdown('<div class="hub-title">🏫 성의교정 업무 통합 포털</div>', unsafe_allow_html=True)

# 2열 배치로 깔끔하게 출력
cols = st.columns(2)
for idx, app in enumerate(st.session_state.apps):
    with cols[idx % 2]:
        st.markdown(f'''
            <a href="{app['url']}" target="_blank" class="app-card" style="border-left-color: {app['color']};">
                <div class="app-title">{app['title']}</div>
                <div class="app-desc">{app['desc']}</div>
            </a>
        ''', unsafe_allow_html=True)
