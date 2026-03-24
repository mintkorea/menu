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

# 3. 디자인 스타일 (상단 여백 제거 및 카드 디자인)
st.markdown("""
<style>
    /* 상단 여백 완전 제거 */
    .block-container { 
        padding-top: 0rem !important; 
        padding-bottom: 2rem !important; 
        max-width: 600px; 
        margin: auto; 
    }
    header {visibility: hidden;} /* Streamlit 기본 상단 헤더 숨김 */
    
    .hub-title { 
        font-size: 24px; font-weight: 800; text-align: center; 
        color: #1E3A5F; margin-top: 10px; margin-bottom: 20px; 
    }
    .app-card {
        display: block; padding: 18px; border-radius: 12px; border: 1px solid #E0E0E0;
        text-decoration: none !important; margin-bottom: 12px; transition: 0.2s;
        background: white; border-left: 8px solid #1E3A5F;
    }
    .app-card:active { background: #F0F4F8; transform: scale(0.98); }
    .app-title { font-size: 18px; font-weight: bold; color: #1E3A5F; }
    .app-desc { font-size: 13px; color: #666; margin-top: 4px; }
</style>
""", unsafe_allow_html=True)

# 4. 메인 화면: 앱 런처
st.markdown('<div class="hub-title">🏫 성의교정 업무 통합 포털</div>', unsafe_allow_html=True)

for app in st.session_state.apps:
    st.markdown(f'''
        <a href="{app['url']}" target="_blank" class="app-card" style="border-left-color: {app['color']};">
            <div class="app-title">{app['title']}</div>
            <div class="app-desc">{app['desc']}</div>
        </a>
    ''', unsafe_allow_html=True)

# 5. 숨겨진 관리 기능 (화면 맨 아래에서 비밀번호 입력 시만 노출)
st.markdown("<br><br><br>", unsafe_allow_html=True) # 본문과 간격 유지
pw = st.text_input("관리자 인증", type="password", placeholder="비밀번호 입력 시 설정 메뉴 노출")

if pw == "1234": # 비밀번호는 원하시는 대로 수정하세요
    st.divider()
    st.subheader("⚙️ 런처 관리 모드")
    tab_add, tab_del = st.tabs(["➕ 추가", "🗑️ 삭제"])
    
    with tab_add:
        c1, c2 = st.columns(2)
        with c1:
            n = st.text_input("이름")
            u = st.text_input("URL")
        with c2:
            d = st.text_input("설명")
            c = st.color_picker("색상", "#1E3A5F")
        if st.button("추가 완료"):
            st.session_state.apps.append({"title": n, "url": u, "desc": d, "color": c})
            st.rerun()

    with tab_del:
        app_list = [a['title'] for a in st.session_state.apps]
        target = st.selectbox("삭제 대상", app_list)
        if st.button("삭제 실행", type="primary"):
            st.session_state.apps = [a for a in st.session_state.apps if a['title'] != target]
            st.rerun()
