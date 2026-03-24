import streamlit as st
import json
import os

# 1. 페이지 설정 및 데이터 저장 파일 경로
st.set_page_config(page_title="성의교정 업무  포털", page_icon="🏫", layout="wide")
DB_FILE = "app_data.json"

# 2. 데이터 로드/저장 함수 (영구 보존용)
def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return [
        {"title": "📱 대관 조회 (모바일)", "url": "https://klzsyte9n8ftnuwcuid9tw.streamlit.app/", "desc": "현장용 대관 및 당직 내역 확인", "color": "#1E3A5F"},
        {"title": "💻 대관 관리 (PC)", "url": "https://rental-2q7nwue9hmapek9nuir6vh.streamlit.app/", "desc": "엑셀 다운로드 및 상세 조회", "color": "#1E3A5F"},
        {"title": "🍱 주간 식단표", "url": "https://3y2krzjwosv86ccxobc38i.streamlit.app/", "desc": "교내 식당 메뉴 및 식사 정보", "color": "#4CAF50"}
    ]

def save_data(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

if 'apps' not in st.session_state:
    st.session_state.apps = load_data()

# 3. CSS (적정 여백 및 심플 디자인)
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none; }
    .block-container { padding-top: 2.5rem !important; max-width: 500px; margin: auto; }
    .hub-title { font-size: 22px; font-weight: 800; text-align: center; color: #1E3A5F; margin-bottom: 25px; }
    .app-card {
        display: block; padding: 18px; border-radius: 12px; border: 1px solid #E4E7EB;
        text-decoration: none !important; margin-bottom: 12px; 
        background: white; border-left: 8px solid #1E3A5F;
    }
    .app-title { font-size: 17px; font-weight: bold; color: #1E3A5F; }
    .app-desc { font-size: 13px; color: #666; margin-top: 4px; }
    .admin-simple-zone { margin-top: 80px; padding-top: 20px; border-top: 1px solid #EEE; }
    </style>
    """, unsafe_allow_html=True)

# 4. 메인 화면 출력
st.markdown('<div class="hub-title">🏫 성의교정 업무 포털</div>', unsafe_allow_html=True)

for app in st.session_state.apps:
    st.markdown(f'''
        <a href="{app['url']}" target="_blank" class="app-card" style="border-left-color: {app['color']};">
            <div class="app-title">{app['title']}</div>
            <div class="app-desc">{app['desc']}</div>
        </a>
    ''', unsafe_allow_html=True)

# 5. 관리자 인증 및 편집 (수정/추가/삭제)
st.markdown('<div class="admin-simple-zone">', unsafe_allow_html=True)
admin_pw = st.text_input("Admin Access", type="password", placeholder="비밀번호 입력")
st.markdown('</div>', unsafe_allow_html=True)

if admin_pw == "1234":
    st.write("---")
    mode = st.radio("작업 선택", ["추가", "수정", "삭제"], horizontal=True)
    
    # 공통 이모지 리스트
    emoji_list = ["📱", "💻", "🍱", "🚨", "📋", "🏥", "📞", "📅", "🏢", "💡", "✅", "🔍"]

    if mode == "추가":
        with st.form("add_form"):
            col1, col2 = st.columns([1, 3])
            icon = col1.selectbox("아이콘", emoji_list)
            name = col2.text_input("앱 이름 (아이콘 제외)")
            url = st.text_input("URL")
            desc = st.text_input("설명")
            color = st.color_picker("포인트 색상", "#1E3A5F")
            if st.form_submit_button("저장하기"):
                full_title = f"{icon} {name}"
                st.session_state.apps.append({"title": full_title, "url": url, "desc": desc, "color": color})
                save_data(st.session_state.apps)
                st.rerun()

    elif mode == "수정":
        target_idx = st.selectbox("수정할 앱 선택", range(len(st.session_state.apps)), 
                                  format_func=lambda x: st.session_state.apps[x]['title'])
        target_app = st.session_state.apps[target_idx]
        
        with st.form("edit_form"):
            new_icon = st.selectbox("아이콘 변경", emoji_list)
            # 기존 타이틀에서 이모지 분리 시도 (단순화)
            current_name = target_app['title'].split(" ", 1)[-1] if " " in target_app['title'] else target_app['title']
            new_name = st.text_input("이름 수정", value=current_name)
            new_url = st.text_input("URL 수정", value=target_app['url'])
            new_desc = st.text_input("설명 수정", value=target_app['desc'])
            new_color = st.color_picker("색상 수정", value=target_app['color'])
            
            if st.form_submit_button("수정 완료"):
                st.session_state.apps[target_idx] = {
                    "title": f"{new_icon} {new_name}",
                    "url": new_url,
                    "desc": new_desc,
                    "color": new_color
                }
                save_data(st.session_state.apps)
                st.rerun()

    elif mode == "삭제":
        del_target = st.selectbox("삭제할 앱 선택", range(len(st.session_state.apps)), 
                                  format_func=lambda x: st.session_state.apps[x]['title'])
        if st.button("즉시 삭제", type="primary"):
            st.session_state.apps.pop(del_target)
            save_data(st.session_state.apps)
            st.rerun()
