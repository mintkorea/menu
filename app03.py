import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 강제 가로 정렬 및 디자인 (CSS)
st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    
    /* 카드 전체 설정 */
    .contact-card {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid #eee;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* ⭐ 핵심: 별표와 이름을 무조건 한 줄에 가로로 배치 */
    .flex-header {
        display: flex;
        align-items: center; /* 세로 중앙 정렬 */
        justify-content: flex-start;
        gap: 10px; /* 별표와 이름 사이 간격 */
        width: 100%;
    }

    .name-text { 
        font-weight: 700; 
        font-size: 1.15rem; 
        color: #111; 
        margin: 0; 
        white-space: nowrap; /* 이름 줄바꿈 방지 */
    }
    
    .pos-dept { 
        font-size: 0.85rem; 
        color: #777; 
        margin-left: 5px;
    }

    .work-text { 
        font-size: 0.85rem; 
        color: #888; 
        margin: 8px 0 0 35px; /* 별표 너비만큼 들여쓰기 */
        line-height: 1.4;
    }

    /* 하단 버튼 정렬 */
    .btn-container {
        display: flex;
        gap: 8px;
        margin-top: 12px;
    }
    .call-btn {
        flex: 1;
        text-align: center;
        padding: 10px 0;
        border-radius: 8px;
        text-decoration: none !important;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .ext { background: #f8f9fa; color: #333 !important; border: 1px solid #ddd; }
    .mob { background: #007bff; color: white !important; }

    /* 스트림릿 버튼 스타일 제거 (별표 전용) */
    .stButton > button {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        color: #ffc107 !important;
        font-size: 24px !important;
        line-height: 1 !important;
        width: 25px !important;
        height: 25px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 3. 데이터 (누락된 담당업무 모두 포함)
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리 (대학본관, 의산연, 성의회관 등)"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군대대장, 민방위, 병무행정, 행사, ITC"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 미화, 대관, 게스트하우스, 인체유래물은행"},
    {"dept":"총무팀","name":"강은희","pos":"대리","ext":"02-3147-8206","mobile":"010-9127-1021","work":"의료원 직인/문서배부, 월례조회, 행사, 회의"},
    {"dept":"총무팀","name":"김보라","pos":"선임","ext":"02-3147-8192","mobile":"010-8073-0527","work":"명예교수실 관리, 차량등록, 부서운영비"},
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방/방재 인증평가, 시설관리 (옴니버스파크)"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증 업무"},
    {"dept":"비서실","name":"이경자","pos":"부장","ext":"02-3147-8071","mobile":"010-6306-3652","work":"의무부총장, 기획조정실장 비서"},
]

# 4. 즐겨찾기 상태 유지
if "fav" not in st.session_state:
    st.session_state.fav = set()

# 검색창
search = st.text_input("🔍 이름/부서/업무 검색", placeholder="예: 보안, 예비군")

# 필터링
filtered = [x for x in data if any(search.lower() in str(v).lower() for v in x.values())] if search else data

# 5. 리스트 출력
for i, c in enumerate(filtered):
    is_f = c["name"] in st.session_state.fav
    star = "★" if is_f else "☆"
    
    # 카드 시작
    st.markdown('<div class="contact-card">', unsafe_allow_html=True)
    
    # [헤더 구역] 별표 버튼과 이름 정보를 Flexbox로 묶음
    # Streamlit 버튼을 HTML 구조 안에 넣기 위해 미세한 컬럼 사용 (버그 방지)
    head_col1, head_col2 = st.columns([0.1, 0.9])
    with head_col1:
        if st.button(star, key=f"f_{i}"):
            if is_f: st.session_state.fav.remove(c["name"])
            else: st.session_state.fav.add(c["name"])
            st.rerun()
    with head_col2:
        st.markdown(f'<p class="name-text">{c["name"]}<span class="pos-dept">{c["pos"]} · {c["dept"]}</span></p>', unsafe_allow_html=True)
    
    # [본문 구역] 업무 내용
    st.markdown(f'<div class="work-text">{c["work"]}</div>', unsafe_allow_html=True)
    
    # [하단 구역] 전화 버튼
    ext_link = f"tel:{c['ext'].replace('-', '')}"
    mob_link = f"tel:{c['mobile'].replace('-', '')}"
    st.markdown(f"""
        <div class="btn-container">
            {"<a href='"+ext_link+"' class='call-btn ext'>내선 연결</a>" if c['ext'] != "-" else ""}
            <a href="{mob_link}" class="call-btn mob">휴대폰 연결</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
