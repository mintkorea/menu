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

# 3. CSS (강력한 여백 제거 및 디자인)
st.markdown("""
    <style>
    /* 상단 메뉴바와 여백을 완전히 숨김 */
    header[data-testid="stHeader"] { visibility: hidden; height: 0% !important; }
    .block-container { 
        padding-top: 0rem !important; 
        padding-bottom: 5rem !important; 
        max-width: 500px; 
        margin: auto; 
    }
    
    .hub-title { 
        font-size: 24px; font-weight: 800; text-align: center; 
        color: #1E3A5F; margin-top: -20px; margin-bottom: 20px; 
    }
    .app-card {
        display: block; padding: 18px; border-radius: 12px; border: 1px solid #E0E0E0;
        text-decoration: none !important; margin-bottom: 12px; 
        background: white; border-left: 8px solid #1E3A5F;
    }
    .app-title { font-size: 18px; font-weight: bold; color: #1E3A5F; }
    .app-desc { font-size: 13px; color: #666; margin-top: 4px; }
    
    /* 관리자 인증 구역 - 노란색으로 강조 */
    .admin-highlight {
        background-color: #FFF9C4;
        padding: 15px;
        border-radius: 10px;
        border: 2px dashed #FBC02D;
        margin-top: 40px;
    }
    </style>
    """, unsafe_allow_html=True)

# 4. 메인 화면 출력
st.markdown('<div class="hub-title">🏫 성의교정 업무 통합 포털</div>', unsafe_allow_html=True)

for app in st.session_state.apps:
    st.markdown(f'''
        <a href="{app['url']}" target="_blank" class="app-card" style="border-left-color: {app['color']};">
            <div class="app-title">{app['title']}</div>
            <div class="app-desc">{app['desc']}</div>
        </a>
    ''', unsafe_allow_html=True)

# 5. 관리자 인증 (눈에 띄게 변경)
st.markdown('<div class="admin-highlight">', unsafe_allow_html=True)
st.info("🛠️ **목록을 수정하려면 아래에 비밀번호를 입력하세요.**")
admin_pw = st.text_input("관리자 인증 (PW: 1234)", type="password")
st.markdown('</div>', unsafe_allow_html=True)

if admin_pw == "1234":
    st.success("✅ 인증 완료! 수정 메뉴가 열렸습니다.")
    t_add, t_del = st.tabs(["➕ 앱 추가", "🗑️ 앱 삭제"])
    
    with t_add:
        name = st.text_input("앱 이름")
        url = st.text_input("연결 URL")
        desc = st.text_input("설명")
        col = st.color_picker("색상", "#1E3A5F")
        if st.button("목록에 추가하기"):
            st.session_state.apps.append({"title": name, "url": url, "desc": desc, "color": col})
            st.rerun()

    with t_del:
        if st.session_state.apps:
            target = st.selectbox("삭제할 앱 선택", [a['title'] for a in st.session_state.apps])
            if st.button("선택한 항목 삭제", type="primary"):
                st.session_state.apps = [a for a in st.session_state.apps if a['title'] != target]
                st.rerun()
