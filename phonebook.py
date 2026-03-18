import streamlit as st
import pandas as pd

# --- 데이터 (제공해주신 데이터 활용) ---
CONTACT_DATA = [
    {"id": 0, "조": "공통", "직위": "소장", "성명": "이규용", "연락처": "010-8883-6580"},
    # ... (중략) ...
    {"id": 27, "조": "기숙사", "직위": "조원", "성명": "이상헌", "연락처": "010-4285-4231"}
]

# --- 스타일 설정 ---
st.markdown("""
    <style>
    /* 전체보기 4열 그리드 유지 */
    .main-grid {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 5px;
    }
    /* 버튼 디자인 최적화 (4열에서도 안 깨지게) */
    .stButton > button {
        width: 100%;
        padding: 5px 0px;
        font-size: 11px !important;
        height: 50px;
        line-height: 1.2;
    }
    /* 확대창 디자인 */
    .zoom-box {
        background-color: #e8f4ff;
        padding: 15px;
        border-radius: 10px;
        border: 2px solid #007bff;
        text-align: center;
        margin-bottom: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# --- 로직 부분 ---
if 'sel_id' not in st.session_state:
    st.session_state.sel_id = None

# 1. 상단 확대 영역 (선택 시에만 노출)
if st.session_state.sel_id is not None:
    target = next(p for p in CONTACT_DATA if p['id'] == st.session_state.sel_id)
    st.markdown(f"""
        <div class="zoom-box">
            <h3 style='margin:0;'>👤 {target['성명']} ({target['직위']})</h3>
            <p style='margin:5px 0; color:#555;'>소속: {target['조']}</p>
            <a href="tel:{target['연락처'].replace('-','')}" 
               style="display:block; background:#28a745; color:white; text-decoration:none; 
                      padding:12px; border-radius:8px; font-weight:bold; font-size:18px;">
               📞 {target['연락처']} 전화걸기
            </a>
        </div>
    """, unsafe_allow_html=True)
    if st.button("❌ 닫기", use_container_width=True):
        st.session_state.sel_id = None
        st.rerun()

# 2. 하단 전체 4열 명단 (안 밀리는 구조)
st.write("### 📱 비상연락망 (이름 클릭)")

# 4열 구성을 위해 4개씩 묶어서 처리
for i in range(0, len(CONTACT_DATA), 4):
    cols = st.columns(4)
    for j in range(4):
        idx = i + j
        if idx < len(CONTACT_DATA):
            p = CONTACT_DATA[idx]
            # 버튼 라벨에 이름과 뒷번호 표시
            label = f"{p['성명']}\n({p['연락처'][-4:]})"
            if cols[j].button(label, key=f"btn_{p['id']}"):
                st.session_state.sel_id = p['id']
                st.rerun()
