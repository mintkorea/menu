import streamlit as st

# 1. 페이지 설정 (최상단 고정)
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

# 3. 안전한 CSS (충돌 요소 제거)
st.markdown("""
    <style>
    /* 헤더 숨김 및 여백 최소화 */
    [data-testid="stHeader"] { display: none; }
    .block-container { 
        padding-top: 1rem !important; 
        padding-bottom: 5rem !important; 
        max-width: 500px; 
        margin: auto; 
    }
    
    .hub-title { 
        font-size: 22px; font-weight: 800; text-align: center; 
        color: #1E3A5F; margin-bottom: 20px; 
    }
    .app-card {
        display: block; padding: 18px; border-radius: 12px; border: 1px solid #E0E0E0;
        text-decoration: none !important; margin-bottom: 12px; 
        background: white; border-left: 10px solid #1E3A5F;
    }
    .app-title { font-size: 17px; font-weight: bold; color: #1E3A5F; }
    .app-desc { font-size: 13px; color: #666; margin-top: 4px; }
    
    /* 관리자 영역 - 단순화 */
    .admin-section {
        margin-top: 60px;
        padding: 15px;
        background-color: #f8f9fa;
        border-radius: 10px;
        border: 1px solid #ddd;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 메인 콘텐츠
st.markdown('<div class="hub-title">🏫 성의교정 업무 통합 포털</div>', unsafe_allow_html=True)

for app in st.session_state.apps:
    st.markdown(f'''
        <a href="{app['url']}" target="_blank" class="app-card" style="border-left-color: {app['color']};">
            <div class="app-title">{app['title']}</div>
            <div class="app-desc">{app['desc']}</div>
        </a>
    ''', unsafe_allow_html=True)

# 5. 관리자 인증 (단순 구조로 변경)
st.markdown('<div class="admin-section">', unsafe_allow_html=True)
st.write("⚙️ **관리자 설정**")
pw = st.text_input("비밀번호를 입력하세요", type="password", key="secure_pw")
st.markdown('</div>', unsafe_allow_html=True)

if pw == "1234":
    st.divider()
    menu = st.radio("작업 선택", ["추가하기", "삭제하기"], horizontal=True)
    
    if menu == "추가하기":
        with st.form("add_form", clear_on_submit=True):
            n = st.text_input("이름")
            u = st.text_input("URL")
            d = st.text_input("설명")
            c = st.color_picker("색상", "#1E3A5F")
            if st.form_submit_button("목록에 추가"):
                if n and u:
                    st.session_state.apps.append({"title": n, "url": u, "desc": d, "color": c})
                    st.rerun()
                else:
                    st.error("이름과 URL은 필수입니다.")

    elif menu == "삭제하기":
        target = st.selectbox("삭제할 앱 선택", [a['title'] for a in st.session_state.apps])
        if st.button("선택 삭제", type="primary"):
            st.session_state.apps = [a for a in st.session_state.apps if a['title'] != target]
            st.rerun()
