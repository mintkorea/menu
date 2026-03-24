
import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의 워크플레이스 허브", page_icon="🏫", layout="wide")

# 2. 초기 데이터 설정 (session_state 활용)
if 'apps' not in st.session_state:
    st.session_state.apps = [
        {"title": "📱 대관 조회 (모바일)", "url": "https://klzsyte9n8ftnuwcuid9tw.streamlit.app/", "desc": "현장용 대관 및 당직 내역 확인", "color": "#1E3A5F"},
        {"title": "💻 대관 관리 (PC)", "url": "https://rental-2q7nwue9hmapek9nuir6vh.streamlit.app/", "desc": "엑셀 다운로드 및 상세 조회", "color": "#1E3A5F"},
        {"title": "🍱 주간 식단표", "url": "https://3y2krzjwosv86ccxobc38i.streamlit.app/", "desc": "교내 식당 메뉴 및 식사 정보", "color": "#4CAF50"},
        {"title": "🚨 보안 비상연락망", "url": "https://t78ulrec88a9tku62zekge.streamlit.app/", "desc": "보안파트 긴급 연락처", "color": "#F44336"},
        {"title": "미화 비상연락망", "url": "https://mintkorea-evsteam.streamlit.app/", "desc": "미화 파트 비상연락처", "color": "#F44336"}
    ]

# 3. 디자인 스타일 (여백 최적화)
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem !important; max-width: 800px; margin: auto; }
    .hub-title { font-size: 26px; font-weight: 800; text-align: center; color: #1E3A5F; margin-bottom: 20px; }
    .app-card {
        display: block; padding: 18px; border-radius: 12px; border: 1px solid #E0E0E0;
        text-decoration: none !important; margin-bottom: 12px; transition: 0.2s;
        background: white; border-left: 8px solid #1E3A5F;
    }
    .app-card:hover { background: #F0F4F8; transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.05); }
    .app-title { font-size: 18px; font-weight: bold; color: #1E3A5F; }
    .app-desc { font-size: 13px; color: #666; margin-top: 4px; }
    
    /* 관리 섹션 구분선 */
    .admin-divider { margin-top: 50px; border-top: 1px dashed #ccc; padding-top: 20px; }
</style>
""", unsafe_allow_html=True)

# 4. 메인 화면: 앱 런처 출력
st.markdown('<div class="hub-title">🏫 성의교정 업무 통합 포털</div>', unsafe_allow_html=True)

cols = st.columns(2)
for idx, app in enumerate(st.session_state.apps):
    with cols[idx % 2]:
        st.markdown(f'''
            <a href="{app['url']}" target="_blank" class="app-card" style="border-left-color: {app['color']};">
                <div class="app-title">{app['title']}</div>
                <div class="app-desc">{app['desc']}</div>
            </a>
        ''', unsafe_allow_html=True)

# 5. 하단 관리 모드 (섹션 분리)
st.markdown('<div class="admin-divider"></div>', unsafe_allow_html=True)

with st.expander("⚙️ 런처 목록 수정하기 (관리자용)"):
    tab_add, tab_del = st.tabs(["➕ 앱 추가", "🗑️ 앱 삭제"])
    
    with tab_add:
        c1, c2 = st.columns(2)
        with c1:
            add_name = st.text_input("앱 이름 (예: 셔틀버스)")
            add_url = st.text_input("연결 URL (https://...)")
        with c2:
            add_desc = st.text_input("설명 (예: 시간표 확인)")
            add_color = st.color_picker("카드 포인트 색상", "#1E3A5F")
        
        if st.button("목록에 즉시 추가", use_container_width=True):
            if add_name and add_url:
                st.session_state.apps.append({"title": add_name, "url": add_url, "desc": add_desc, "color": add_color})
                st.rerun()
            else:
                st.warning("이름과 URL을 입력해주세요.")

    with tab_del:
        if st.session_state.apps:
            app_list = [app['title'] for app in st.session_state.apps]
            del_target = st.selectbox("삭제할 앱을 선택하세요", app_list)
            if st.button(f"'{del_target}' 삭제하기", type="primary", use_container_width=True):
                st.session_state.apps = [a for a in st.session_state.apps if a['title'] != del_target]
                st.rerun()
        else:
            st.write("삭제할 앱이 없습니다.")
