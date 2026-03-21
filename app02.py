import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 비상연락망 (2026)", layout="wide")

# 2. 데이터 구성 (PDF 원본 데이터 기반)
def get_contacts():
    return [
        # --- 총무팀 ---
        {"g": "총무", "n": "박현욱", "p": "팀장", "t": "010-6245-0589", "ext": "8190", "w": "부서업무 총괄"},
        {"g": "총무", "n": "김종래", "p": "차장", "t": "010-9056-3701", "ext": "8191", "w": "시설/자산관리(본관, 의산연, 성의회관)"},
        {"g": "총무", "n": "장영섭", "p": "차장", "t": "010-5072-0919", "ext": "8193", "w": "예비군대대장, 민방위, 병무, 행사"},
        {"g": "총무", "n": "주종호", "p": "과장", "t": "010-3324-1187", "ext": "8202", "w": "보안, 미화, 대관, 게스트하우스"},
        {"g": "총무", "n": "강은희", "p": "대리", "t": "010-9127-1021", "ext": "8206", "w": "의료원 직인/문서 배부, 행사, 회의"},
        {"g": "총무", "n": "김보라", "p": "선임", "t": "010-8073-0527", "ext": "8192", "w": "명예교수실 관리, 차량등록, 운영비"},
        {"g": "총무", "n": "노종현", "p": "책임", "t": "010-9425-3109", "ext": "8195", "w": "행사, 회의자료취합, 예비군사무"},
        {"g": "총무", "n": "고규호", "p": "책임", "t": "010-3381-8870", "ext": "8196", "w": "다이어리, 인증평가, 시설안전점검"},
        {"g": "총무", "n": "김두리", "p": "사원", "t": "010-9661-1257", "ext": "8204", "w": "성의기숙사 사감 (581-7523)"},
        {"g": "총무", "n": "임세리", "p": "사원", "t": "010-3281-1229", "ext": "8197", "w": "우편, 물품청구, 정수기, 정보보호"},
        {"g": "총무", "n": "김종식", "p": "사원", "t": "010-9256-6904", "ext": "지원", "w": "업무 지원"},
        
        # --- 안전관리 U ---
        {"g": "안전", "n": "윤호열", "p": "UM", "t": "010-2623-7963", "ext": "8199", "w": "소방/방재, 시설관리(옴니버스 등)"},
        {"g": "안전", "n": "주상건", "p": "차장", "t": "010-9496-6483", "ext": "7135", "w": "시신기증 업무"},
        {"g": "안전", "n": "곽정승", "p": "과장", "t": "010-5218-6504", "ext": "8194", "w": "사업계획, 예산, 주차/차량관리"},
        {"g": "안전", "n": "박일용", "p": "과장", "t": "010-6205-7751", "ext": "8201", "w": "계약(임대차, 용역), 교원기숙사"},
        {"g": "안전", "n": "이경종", "p": "부장", "t": "010-2623-7963", "ext": "8203", "w": "교수업적평가, 문서분배"},
        {"g": "안전", "n": "김준석", "p": "과장", "t": "010-9256-6904", "ext": "8205", "w": "연구실 안전관리, 출입증, 식대"},
        
        # --- 의산연 별관 ---
        {"g": "별관", "n": "주용덕", "p": "보안", "t": "010-2021-9541", "ext": "별관", "w": "의산연 별관 보안"},
        {"g": "별관", "n": "김승배", "p": "보안", "t": "010-8704-2591", "ext": "별관", "w": "의산연 별관 보안"},
        {"g": "별관", "n": "안정진", "p": "보안", "t": "010-4925-2926", "ext": "별관", "w": "의산연 별관 보안"},
        
        # --- 비서실 ---
        {"g": "비서", "n": "이경자", "p": "부장", "t": "010-6306-3652", "ext": "8071", "w": "의무부총장, 기획조정실장 비서"},
        {"g": "비서", "n": "이상희", "p": "과장", "t": "010-3445-0623", "ext": "8068", "w": "영성구현실장, 사무처장 비서"},
        {"g": "비서", "n": "박은영", "p": "과장", "t": "010-5348-6849", "ext": "8069", "w": "의과대학장 비서"},
        
        # --- 협력업체 ---
        {"g": "협력", "n": "신성휴", "p": "소장", "t": "010-7161-2201", "ext": "9102", "w": "미화 총괄 소장"},
        {"g": "협력", "n": "이규용", "p": "소장", "t": "010-8883-6580", "ext": "8300", "w": "보안 총괄 소장"},
    ]

# 3. CSS 스타일 (모바일 최적화 및 카드 디자인)
st.markdown("""
    <style>
    .block-container { padding: 1rem; background-color: #f8f9fa; }
    .contact-card {
        padding: 15px; border-radius: 12px;
        margin-bottom: 12px; background-color: white; 
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        display: block; text-decoration: none; color: inherit !important;
        border-left: 5px solid #007bff;
    }
    .name-row { display: flex; justify-content: space-between; align-items: center; }
    .name-text { font-size: 1.15rem; font-weight: bold; color: #333; }
    .ext-badge { background-color: #e7f1ff; color: #007bff; padding: 2px 8px; border-radius: 5px; font-weight: bold; }
    .info-text { font-size: 0.9rem; color: #666; margin-top: 6px; line-height: 1.4; }
    .call-hint { font-size: 0.8rem; color: #007bff; margin-top: 8px; text-align: right; font-weight: 500; }
    </style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")
st.caption("최종 업데이트: 2026. 03. 20.")

# 4. 검색창
search = st.text_input("🔍 이름, 부서, 업무 검색", placeholder="예: 보안, 박현욱, 시신")

# 5. 출력 로직
contacts = get_contacts()
for c in contacts:
    if not search or any(search.lower() in str(val).lower() for val in c.values()):
        # 전화번호 처리 (010 우선, 없으면 내선)
        clean_tel = c['t'].replace("-", "")
        
        # 내선 번호 다이얼 처리 규칙 적용
        ext_display = c['ext']
        if ext_display.startswith("*1"):
             dial_ext = "022258" + ext_display.replace("*1", "").strip()
        elif ext_display.isdigit():
             dial_ext = "023147" + ext_display
        else:
             dial_ext = clean_tel # 별관 등 텍스트인 경우 폰번호로 연결
             
        st.markdown(f"""
            <a href="tel:{clean_tel}" class="contact-card">
                <div class="name-row">
                    <span class="name-text">{c['n']} <small style="color:#777; font-weight:normal;">{c['p']}</small></span>
                    <span class="ext-badge">내선: {ext_display}</span>
                </div>
                <div class="info-text">
                    <b>{c['g']}</b> | {c['w']}
                </div>
                <div class="call-hint">터치하여 전화걸기 ({c['t']})</div>
            </a>
        """, unsafe_allow_html=True)
