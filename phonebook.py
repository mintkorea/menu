import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 설정 및 데이터 관리 ---
st.set_page_config(page_title="보안 통합 관리 시스템", layout="wide")

# (데이터 유실 방지를 위한 CSV 로드 함수는 이전과 동일)
def load_leaves():
    if os.path.exists('leave_data.csv'):
        return pd.read_csv('leave_data.csv')
    return pd.DataFrame(columns=['날짜', '성명', '대근자'])

# 상세 정보가 포함된 확장 데이터 (사번, 생일 예시 추가)
# 실제 데이터에 맞게 이 부분을 수정하시면 됩니다.
CONTACT_DATA = [
    {"id": 0, "조": "C조", "직위": "조원", "성명": "김태언", "연락처": "010-5386-5386", "사번": "2023001", "생일": "01월 01일"},
    {"id": 1, "조": "C조", "직위": "조원", "성명": "이태원", "연락처": "010-9265-7881", "사번": "2023002", "생일": "02월 02일"},
    {"id": 2, "조": "C조", "직위": "조원", "성명": "이정석", "연락처": "010-2417-1173", "사번": "2023003", "생일": "03월 03일"},
    {"id": 3, "조": "C조", "직위": "조장", "성명": "황재업", "연락처": "010-9278-6622", "사번": "2023004", "생일": "04월 04일"},
    # ... 나머지 인원들도 동일한 형식으로 추가 가능
]

# (나머지 28명 명단 생략 - 구조 동일)

menu = st.sidebar.selectbox("메뉴 선택", ["📱 비상연락망", "📝 연차 관리", "🗓️ C조 근무표"])

# --- [메뉴 1: 비상연락망] ---
if menu == "📱 비상연락망":
    st.subheader("📱 비상연락망 (이름 터치 시 상세정보)")
    
    # 세션 상태로 선택된 인원 관리
    if 'selected_person' not in st.session_state:
        st.session_state.selected_person = None

    # 1. 상세 정보 카드 표시 (누군가 클릭했을 때만 상단에 노출)
    if st.session_state.selected_person:
        p = st.session_state.selected_person
        tel_link = p['연락처'].replace('-', '')
        
        st.markdown(f"""
            <div style="background-color: #ffffff; border: 2px solid #2e7d32; border-radius: 15px; padding: 20px; text-align: center; margin-bottom: 20px; box-shadow: 0px 4px 10px rgba(0,0,0,0.1);">
                <h2 style="margin: 0; color: #333;">{p['성명']} <span style="font-size: 16px; color: #666;">({p['직위']})</span></h2>
                <hr style="border: 0.5px solid #eee;">
                <p style="font-size: 18px; margin: 10px 0;"><b>📞 전화번호:</b> {p['연락처']}</p>
                <p style="font-size: 16px; margin: 5px 0; color: #555;"><b>🆔 사번:</b> {p['사번']} | <b>🎂 생일:</b> {p['생일']}</p>
                <div style="margin-top: 15px;">
                    <a href="tel:{tel_link}" style="text-decoration: none; background-color: #2e7d32; color: white; padding: 12px 40px; border-radius: 30px; font-size: 18px; font-weight: bold; display: inline-block;">전화 걸기</a>
                </div>
            </div>
        """, unsafe_allow_html=True)
        
        if st.button("닫기 ✖", use_container_width=True):
            st.session_state.selected_person = None
            st.rerun()

    # 2. 전체 인원 그리드 (버튼 방식)
    st.write("---")
    cols = st.columns(4) # 4열 배치
    
    for idx, person in enumerate(CONTACT_DATA):
        with cols[idx % 4]:
            # 각 인원 이름으로 버튼 생성 (터치 대응)
            if st.button(f"{person['성명']}\n{person['연락처'][-4:]}", key=f"btn_{person['id']}", use_container_width=True):
                st.session_state.selected_person = person
                st.rerun()

# --- [메뉴 2: 연차 관리 & 메뉴 3: C조 근무표] ---
# (이전의 로직과 동일하게 유지 - 오늘 기준 1개월 노출 및 날짜 선택 기능 포함)
elif menu == "📝 연차 관리":
    # (연차 관리 코드 생략)
    pass

elif menu == "🗓️ C조 근무표":
    # (오늘 기준 1개월 근무표 코드 생략)
    pass
