import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의 워크플레이스 허브", page_icon="🏫", layout="wide")

# 2. 데이터 초기화
if 'apps' not in st.session_state:
    st.session_state.apps = [
        {"title": "📱 대관 조회 (모바일)", "url": "https://klzsyte9n8ftnuwcuid9tw.streamlit.app/", "desc": "현장용 대관 및 당직 내역 확인", "color": "#1E3A5F"},
        {"title": "💻 대관 관리 (PC)", "url": "https://rental-2q7nwue9hmapek9nuir6vh.streamlit.app/", "desc": "엑셀 다운로드 및 상세 조회", "color": "#1E3A5F"},
        {"title": "🍱 주간 식단표", "url": "https://3y2krzjwosv86ccxobc38i.streamlit.app/", "desc": "교내 식당 메뉴 및 식사 정보", "color": "#4CAF50"},
        {"title": "🚨 보안 비상연락망", "url": "https://t78ulrec88a9tku62zekge.streamlit.app/", "desc": "보안파트 긴급 연락처", "color": "#F44336"},
        {"title": "미화 비상연락망", "url": "https://mintkorea-evsteam.streamlit.app/", "desc": "미화 파트 비상연락처", "color": "#F44336"}
    ]

# 3. CSS (상단 적정 여백 및 심플 관리자 영역)
st.markdown("""
    <style>
    /* 상단 헤더 숨김 및 적정 여백 설정 */
    [data-testid="stHeader"] { display: none; }
    .block-container { 
        padding-top: 2.5rem !important; /* 여백을 0에서 2.5로 늘려 답답함 해소 */
        padding-bottom: 5rem !important; 
        max-width: 500px; 
        margin: auto; 
    }
    
    .hub-title { 
        font-size: 22px; font-weight: 800; text-align: center; 
        color: #1E3A5F; margin-bottom: 25px; 
    }
    .app-card {
        display: block; padding: 18px; border-radius: 12px; border: 1px solid #E4E7EB;
        text-decoration: none !important; margin-bottom: 12px; 
        background: white; border-left: 8px solid #1E3A5F;
    }
    .app-title { font-size: 17px; font-weight: bold; color: #1E3A5F; }
    .app-desc { font-size: 13px; color: #666; margin-top: 4px; }
    
    /* 관리자 영역 - 화려한 색상 제거 후 차분하게 변경 */
    .admin-simple-zone {
        margin-top: 80px;
        padding-top: 20px;
        border-top: 1px solid #EEE;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 메인 화면
st.markdown('<div class="hub-title">🏫 성의교정 업무 통합 포털</div>', unsafe_allow_html=True)

for app in st.session_state.apps:
    st.markdown(f'''
        <a href="{app['url']}" target="_blank" class="app-card" style="border-left-color: {app['color']};">
            <div class="app-title">{app['title']}</div>
            <div class="app-desc">{app['desc']}</div>
        </a>
    ''', unsafe_allow_html=True)

# 5. 심플 관리자 인증
st.markdown('<div class="admin-simple-zone">', unsafe_allow_html=True)
# 별도의 안내 문구 없이 깔끔하게 입력창만 배치
admin_pw = st.text_input("Admin Access", type="password", placeholder="비밀번호 입력")
st.markdown('</div>', unsafe_allow_html=True)

if admin_pw == "1234":
    st.write("---")
    tab_a, tab_b = st.tabs(["추가", "삭제"])
    
    with tab_a:
        with st.form("add_app", clear_on_submit=True):
            n = st.text_input("앱 이름")
            u = st.text_input("URL")
            d = st.text_input("설명")
            c = st.color_picker("색상", "#1E3A5F")
            if st.form_submit_button("확인"):
                if n and u:
                    st.session_state.apps.append({"title": n, "url": u, "desc": d, "color": c})
                    st.rerun()

    with tab_b:
        target = st.selectbox("삭제할 앱", [a['title'] for a in st.session_state.apps])
        if st.button("삭제하기"):
            st.session_state.apps = [a for a in st.session_state.apps if a['title'] != target]
            st.rerun()
