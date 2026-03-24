import streamlit as st

# 1. 페이지 설정
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

# 3. 디자인 스타일 (여백 및 가시성 개선)
st.markdown("""
<style>
    .block-container { padding-top: 0rem !important; max-width: 600px; margin: auto; }
    header {visibility: hidden;}
    .hub-title { font-size: 24px; font-weight: 800; text-align: center; color: #1E3A5F; margin-top: 15px; margin-bottom: 20px; }
    .app-card {
        display: block; padding: 18px; border-radius: 12px; border: 1px solid #E0E0E0;
        text-decoration: none !important; margin-bottom: 12px; background: white; border-left: 8px solid #1E3A5F;
    }
    .app-title { font-size: 18px; font-weight: bold; color: #1E3A5F; }
    .app-desc { font-size: 13px; color: #666; margin-top: 4px; }
    
    /* 인증 구역 강조 */
    .admin-zone {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-top: 50px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# 4. 메인 런처 화면
st.markdown('<div class="hub-title">🏫 성의교정 업무 통합 포털</div>', unsafe_allow_html=True)

for app in st.session_state.apps:
    st.markdown(f'''
        <a href="{app['url']}" target="_blank" class="app-card" style="border-left-color: {app['color']};">
            <div class="app-title">{app['title']}</div>
            <div class="app-desc">{app['desc']}</div>
        </a>
    ''', unsafe_allow_html=True)

# 5. 관리자 인증 섹션 (가시성 확보)
st.markdown('<div class="admin-zone">', unsafe_allow_html=True)
st.write("🔒 **시스템 설정 (관리자 전용)**")
# 이 칸에 비밀번호 '1234'를 입력하고 엔터를 치세요.
pw = st.text_input("인증 번호 입력", type="password", key="admin_pw", help="비밀번호 입력 시 편집 메뉴가 나타납니다.")
st.markdown('</div>', unsafe_allow_html=True)

if pw == "1234":
    st.success("인증 성공! 아래에서 앱 목록을 수정하세요.")
    tab_add, tab_del = st.tabs(["➕ 앱 추가", "🗑️ 앱 삭제"])
    
    with tab_add:
        n = st.text_input("이름")
        u = st.text_input("URL")
        d = st.text_input("설명")
        c = st.color_picker("색상", "#1E3A5F")
        if st.button("목록에 추가"):
            st.session_state.apps.append({"title": n, "url": u, "desc": d, "color": c})
            st.rerun()

    with tab_del:
        app_list = [a['title'] for a in st.session_state.apps]
        target = st.selectbox("삭제할 앱 선택", app_list)
        if st.button("선택 항목 삭제", type="primary"):
            st.session_state.apps = [a for a in st.session_state.apps if a['title'] != target]
            st.rerun()
