import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 설정 및 데이터 관리 ---
st.set_page_config(page_title="보안 통합 관리 시스템", layout="wide")
LEAVE_FILE = 'leave_data.csv'

def load_leaves():
    if os.path.exists(LEAVE_FILE):
        return pd.read_csv(LEAVE_FILE)
    return pd.DataFrame(columns=['날짜', '성명', '대근자'])

def save_leaves(df):
    df.to_csv(LEAVE_FILE, index=False, encoding='utf-8-sig')

# 28명 전체 명단 데이터 (정렬된 리스트)
CONTACT_DATA = [
    {"id": 0, "조": "공통", "직위": "소장", "성명": "이규용", "연락처": "010-8883-6580"},
    {"id": 1, "조": "공통", "직위": "부소장", "성명": "박상현", "연락처": "010-3193-4603"},
    {"id": 2, "조": "공통", "직위": "반장", "성명": "유정수", "연락처": "010-5316-8065"},
    {"id": 3, "조": "공통", "직위": "반장", "성명": "오제준", "연락처": "010-3352-8933"},
    {"id": 4, "조": "공통", "직위": "반장", "성명": "이강택", "연락처": "010-9048-6708"},
    {"id": 5, "조": "A조", "직위": "조장", "성명": "배준용", "연락처": "010-4717-7065"},
    {"id": 6, "조": "A조", "직위": "조원", "성명": "이명구", "연락처": "010-8638-5819"},
    {"id": 7, "조": "A조", "직위": "조원", "성명": "김영중", "연락처": "010-7726-5963"},
    {"id": 8, "조": "A조", "직위": "조원", "성명": "김삼동", "연락처": "010-2345-8081"},
    {"id": 9, "조": "B조", "직위": "조장", "성명": "심규천", "연락처": "010-8287-9895"},
    {"id": 10, "조": "B조", "직위": "조원", "성명": "임종현", "연락처": "010-7741-6732"},
    {"id": 11, "조": "B조", "직위": "조원", "성명": "권영국", "연락처": "010-4085-9982"},
    {"id": 12, "조": "B조", "직위": "조원", "성명": "전준수", "연락처": "010-5687-7107"},
    {"id": 13, "조": "C조", "직위": "조장", "성명": "황재업", "연락처": "010-9278-6622"},
    {"id": 14, "조": "C조", "직위": "조원", "성명": "이태원", "연락처": "010-9265-7881"},
    {"id": 15, "조": "C조", "직위": "조원", "성명": "김태언", "연락처": "010-5386-5386"},
    {"id": 16, "조": "C조", "직위": "조원", "성명": "이정석", "연락처": "010-2417-1173"},
    {"id": 17, "조": "A조", "직위": "조장", "성명": "손병휘", "연락처": "010-9966-2090"},
    {"id": 18, "조": "A조", "직위": "조원", "성명": "권순호", "연락처": "010-2539-1799"},
    {"id": 19, "조": "A조", "직위": "조원", "성명": "김진식", "연락처": "010-3277-0808"},
    {"id": 20, "조": "B조", "직위": "조장", "성명": "황일범", "연락처": "010-8929-4294"},
    {"id": 21, "조": "B조", "직위": "조원", "성명": "이상길", "연락처": "010-9904-0247"},
    {"id": 22, "조": "B조", "직위": "조원", "성명": "허용", "연락처": "010-8845-0163"},
    {"id": 23, "조": "C조", "직위": "조장", "성명": "피재영", "연락처": "010-9359-2569"},
    {"id": 24, "조": "C조", "직위": "조원", "성명": "남형민", "연락처": "010-8767-7073"},
    {"id": 25, "조": "C조", "직위": "조원", "성명": "강경훈", "연락처": "010-3436-6107"},
    {"id": 26, "조": "기숙사", "직위": "조원", "성명": "유시균", "연락처": "010-8737-5770"},
    {"id": 27, "조": "기숙사", "직위": "조원", "성명": "이상헌", "연락처": "010-4285-4231"}
]

menu = st.sidebar.selectbox("메뉴 선택", ["📱 비상연락망", "📝 연차 관리", "🗓️ C조 근무표"])

# --- [메뉴 1: 비상연락망] ---
if menu == "📱 비상연락망":
    st.subheader("📱 비상연락망 (터치 시 인접 8인 확대)")
    
    # 세션 상태로 선택된 인원 관리
    if 'selected_id' not in st.session_state:
        st.session_state.selected_id = None

    # 전체 리스트 표시
    df = pd.DataFrame(CONTACT_DATA)
    
    # 1. 확대 영역 계산 (선택된 인원이 있을 경우)
    if st.session_state.selected_id is not None:
        sid = st.session_state.selected_id
        # 선택된 인원을 중심으로 앞뒤 8명 추출 (인덱스 범위 조절)
        start = max(0, sid - 3)
        end = min(len(CONTACT_DATA), start + 8)
        # 만약 끝부분이라 8개가 안되면 시작지점 재조정
        if end - start < 8:
            start = max(0, end - 8)
        
        target_group = CONTACT_DATA[start:end]
        st.write("🔍 **확대 모드 (전화 버튼 클릭)**")
        
        # 확대용 카드 레이아웃 (2열 4행으로 크게)
        cols = st.columns(2)
        for idx, person in enumerate(target_group):
            with cols[idx % 2]:
                tel = person['연락처'].replace('-', '')
                # 강조 스타일
                is_selected = "border: 2px solid #FF4B4B;" if person['id'] == sid else ""
                st.markdown(f"""
                    <div style="background:#f0f2f6; padding:10px; border-radius:10px; text-align:center; margin-bottom:10px; {is_selected}">
                        <b style="font-size:16px;">{person['성명']} ({person['직위']})</b><br>
                        <a href="tel:{tel}" style="text-decoration:none; color:white; background:#2e7d32; padding:5px 20px; border-radius:5px; display:inline-block; margin-top:5px; font-weight:bold;">📞 {person['연락처']}</a>
                    </div>
                """, unsafe_allow_html=True)
        
        if st.button("닫기 (전체보기)"):
            st.session_state.selected_id = None
            st.rerun()
            
    # 2. 전체 그리드 표시 (4열 초소형)
    st.write("---")
    st.write("💡 인원을 터치하면 크게 볼 수 있습니다.")
    
    cards_html = ""
    for r in CONTACT_DATA:
        cards_html += f'''
        <div class="card" onclick="window.parent.postMessage({{type: 'streamlit:set_widget_value', value: {r['id']}, widgetId: 'select_person'}}, '*')">
            <div class="name">{r['성명']}</div>
            <div class="rank">{r['직위']}</div>
            <div class="phone">{r['연락처'][-4:]}</div>
        </div>
        '''
    
    # Streamlit과 통신하기 위한 커스텀 컴포넌트 처리용 보이지 않는 셀렉트박스
    selected = st.sidebar.number_input("ID", key="select_person", value=-1, label_visibility="collapsed")
    if selected != -1 and selected != st.session_state.selected_id:
        st.session_state.selected_id = selected
        st.rerun()

    st.components.v1.html(f"""
    <style>
        .container {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 4px; font-family: sans-serif; }}
        .card {{ background: #fff; border: 1px solid #ddd; border-radius: 4px; padding: 5px 2px; text-align: center; cursor: pointer; }}
        .name {{ font-weight: bold; font-size: 11px; }}
        .rank {{ font-size: 8px; color: #666; }}
        .phone {{ font-size: 8px; color: #2e7d32; font-weight: bold; }}
        .card:active {{ background: #e0e0e0; }}
    </style>
    <div class="container">{cards_html}</div>
    """, height=500, scrolling=True)

# --- 이하 연차 관리 및 C조 근무표 코드는 이전과 동일하게 유지 ---
elif menu == "📝 연차 관리":
    # (기존 코드와 동일)
    st.subheader("📝 연차 관리")
    leaves_df = load_leaves()
    # ... [생략] ...
    
elif menu == "🗓️ C조 근무표":
    # (기존 코드와 동일)
    st.subheader("🗓️ C조 근무표")
    # ... [생략] ...
