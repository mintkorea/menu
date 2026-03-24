import streamlit as st
import json
import os

# 1. 페이지 설정
st.set_page_config(page_title="성의 워크플레이스 허브", page_icon="🏫", layout="wide")
DB_FILE = "app_data.json"

# 2. 데이터 관리 함수
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

# 3. CSS (카드 높이 축소 및 슬림 디자인)
st.markdown("""
    <style>
    [data-testid="stHeader"] { display: none; }
    .block-container { 
        padding-top: 2.5rem !important; 
        max-width: 500px; 
        margin: auto; 
    }
    .hub-title { font-size: 20px; font-weight: 800; text-align: center; color: #1E3A5F; margin-bottom: 20px; }
    
    /* 카드 높이 줄이기: 패딩과 마진 최적화 */
    .app-card {
        display: block; 
        padding: 12px 16px; /* 위아래 패딩을 18px -> 12px로 축소 */
        border-radius: 10px; 
        border: 1px solid #E4E7EB;
        text-decoration: none !important; 
        margin-bottom: 8px; /* 카드 사이 간격 축소 */
        background: white; 
        border-left: 6px solid #1E3A5F; /* 선 두께도 약간 슬림하게 */
    }
    .app-title { font-size: 16px; font-weight: bold; color: #333; line-height: 1.2; }
    .app-desc { font-size: 12px; color: #777; margin-top: 2px; }
    
    .admin-simple-zone { margin-top: 50px; padding-top: 20px; border-top: 1px solid #EEE; }
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

# 5. 관리자 기능 (수정/이모지 포함)
st.markdown('<div class="admin-simple-zone">', unsafe_allow_html=True)
admin_pw = st.text_input("Admin Access", type="password", placeholder="비밀번호")
st.markdown('</div>', unsafe_allow_html=True)

if admin_pw == "1234":
    st.write("---")
    mode = st.radio("작업 선택", ["추가", "수정", "삭제"], horizontal=True)
    emoji_list = ["📱", "💻", "🍱", "🚨", "📋", "🏥", "📞", "📅", "🏢", "💡", "✅", "🔍", "🚗", "🍴"]

    if mode == "추가":
        with st.form("add_form", clear_on_submit=True):
            col1, col2 = st.columns([1, 3])
            icon = col1.selectbox("아이콘", emoji_list)
            name = col2.text_input("이름")
            url = st.text_input("URL")
            desc = st.text_input("설명")
            color = st.color_picker("색상", "#1E3A5F")
            if st.form_submit_button("저장"):
                st.session_state.apps.append({"title": f"{icon} {name}", "url": url, "desc": desc, "color": color})
                save_data(st.session_state.apps)
                st.rerun()

    elif mode == "수정":
        idx = st.selectbox("수정 대상", range(len(st.session_state.apps)), format_func=lambda x: st.session_state.apps[x]['title'])
        target = st.session_state.apps[idx]
        with st.form("edit_form"):
            new_icon = st.selectbox("아이콘 변경", emoji_list)
            curr_name = target['title'].split(" ", 1)[-1] if " " in target['title'] else target['title']
            new_name = st.text_input("이름 수정", value=curr_name)
            new_url = st.text_input("URL 수정", value=target['url'])
            new_desc = st.text_input("설명 수정", value=target['desc'])
            new_color = st.color_picker("색상 수정", value=target['color'])
            if st.form_submit_button("수정 완료"):
                st.session_state.apps[idx] = {"title": f"{new_icon} {new_name}", "url": new_url, "desc": new_desc, "color": new_color}
                save_data(st.session_state.apps)
                st.rerun()

    elif mode == "삭제":
        del_idx = st.selectbox("삭제 대상", range(len(st.session_state.apps)), format_func=lambda x: st.session_state.apps[x]['title'])
        if st.button("즉시 삭제", type="primary"):
            st.session_state.apps.pop(del_idx)
            save_data(st.session_state.apps)
            st.rerun()
