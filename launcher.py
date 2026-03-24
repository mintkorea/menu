import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의 워크플레이스 허브", page_icon="🏫", layout="wide")

# 2. 초기 데이터 설정 (최초 실행 시에만 로드)
if 'apps' not in st.session_state:
    st.session_state.apps = [
        {"title": "📱 대관 조회 (모바일)", "url": "https://klzsyte9n8ftnuwcuid9tw.streamlit.app/", "desc": "현장용 대관 및 당직 내역 확인", "color": "#1E3A5F"},
        {"title": "💻 대관 관리 (PC)", "url": "https://rental-2q7nwue9hmapek9nuir6vh.streamlit.app/", "desc": "엑셀 다운로드 및 상세 조회", "color": "#1E3A5F"},
        {"title": "🍱 주간 식단표", "url": "https://3y2krzjwosv86ccxobc38i.streamlit.app/", "desc": "교내 식당 메뉴 및 식사 정보", "color": "#4CAF50"},
        {"title": "🚨 보안 비상연락망", "url": "https://t78ulrec88a9tku62zekge.streamlit.app/", "desc": "보안파트 긴급 연락처", "color": "#F44336"},
        {"title": "미화 비상연락망", "url": "https://mintkorea-evsteam.streamlit.app/", "desc": "미화 파트 비상연락처", "color": "#F44336"}
    ]

# 3. 디자인 스타일 (CSS)
st.markdown("""
<style>
    .hub-title { font-size: 28px; font-weight: 800; text-align: center; color: #1E3A5F; margin-bottom: 25px; }
    .app-card {
        display: block; padding: 20px; border-radius: 12px; border: 1px solid #E0E0E0;
        text-decoration: none !important; margin-bottom: 15px; transition: 0.2s;
        background: white; border-left: 8px solid #1E3A5F;
    }
    .app-card:hover { background: #F0F4F8; transform: translateY(-3px); box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .app-title { font-size: 19px; font-weight: bold; color: #1E3A5F; }
    .app-desc { font-size: 14px; color: #666; margin-top: 6px; }
</style>
""", unsafe_allow_html=True)

# 4. 사이드바: 앱 관리 기능 (추가/삭제)
with st.sidebar:
    st.header("🛠️ 런처 관리자")
    
    with st.expander("➕ 새 앱 추가"):
        new_title = st.text_input("앱 이름", placeholder="예: 셔틀버스 시간표")
        new_url = st.text_input("URL 주소", placeholder="https://...")
        new_desc = st.text_input("설명", placeholder="간략한 용도 설명")
        new_color = st.color_picker("테두리 색상", "#1E3A5F")
        
        if st.button("목록에 추가하기"):
            if new_title and new_url:
                st.session_state.apps.append({
                    "title": new_title, "url": new_url, "desc": new_desc, "color": new_color
                })
                st.rerun()
            else:
                st.error("이름과 URL은 필수입니다.")

    with st.expander("🗑️ 앱 삭제"):
        app_names = [app['title'] for app in st.session_state.apps]
        delete_target = st.selectbox("삭제할 앱 선택", app_names)
        if st.button("선택한 앱 삭제"):
            st.session_state.apps = [app for app in st.session_state.apps if app['title'] != delete_target]
            st.rerun()

    st.info("💡 팁: 설정한 내용은 브라우저를 닫기 전까지 유지됩니다. 영구 저장을 원하시면 코드를 직접 수정해야 합니다.")

# 5. 메인 화면 구성
st.markdown('<div class="hub-title">🏫 성의교정 업무 통합 포털</div>', unsafe_allow_html=True)

# 카드 출력 (2열 배치)
cols = st.columns(2)
for idx, app in enumerate(st.session_state.apps):
    with cols[idx % 2]:
        st.markdown(f'''
            <a href="{app['url']}" target="_blank" class="app-card" style="border-left-color: {app['color']};">
                <div class="app-title">{app['title']}</div>
                <div class="app-desc">{app['desc']}</div>
            </a>
        ''', unsafe_allow_html=True)

st.markdown("---")
