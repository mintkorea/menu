import streamlit as st

# 1. 페이지 설정 및 모바일 최적화 디지인
st.set_page_config(page_title="성의교정 연락망", layout="wide")

st.markdown("""
<style>
    /* 전체 여백 최소화 */
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    
    /* 카드 스타일: 슬림하고 직관적으로 변경 */
    .contact-card {
        background: #ffffff;
        padding: 10px 14px;
        border-radius: 12px;
        margin-bottom: 10px;
        border: 1px solid #eee;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* ⭐ 핵심: 별표, 이름, 아이콘을 모두 강제로 한 줄에 가로로 배치 (Flexbox) */
    .main-row {
        display: flex;
        align-items: center;
        justify-content: space-between; /* 요소 간 간격 자동 조절 */
        width: 100%;
    }

    /* 왼쪽 구역 (별표 + 이름) */
    .left-section {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .name-text { font-weight: 700; font-size: 1.15rem; color: #111; margin: 0; }
    .pos-text { font-size: 0.9rem; color: #666; font-weight: normal; margin-left: 5px; }
    .work-text { font-size: 0.85rem; color: #888; margin-top: 4px; padding-left: 2px; }

    /* 오른쪽 구역 (흑백 아이콘) */
    .icon-section {
        display: flex;
        align-items: center;
        gap: 16px; /* 아이콘 간 간격 */
    }

    .icon-btn {
        text-decoration: none !important;
        color: #333 !important; /* 흑백 아이콘 색상 */
        font-size: 24px; /* 아이콘 크기 */
    }

    /* 스트림릿 기본 버튼 투명화 (별표 전용) */
    div[data-testid="stColumn"] button {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        color: #ffc107 !important;
        font-size: 24px !important;
        line-height: 1;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 2. 통합 데이터 (PDF 원본 내용을 모두 포함)
def get_contacts():
    return [
        {"dept": "총무팀", "name": "박현욱", "pos": "팀장", "ext": "8190", "mobile": "010-6245-0589", "work": "부서업무 총괄"},
        {"dept": "총무팀", "name": "김종래", "pos": "차장", "ext": "8191", "mobile": "010-9056-3701", "work": "시설 및 자산관리 (대학본관, 의산연 등)"},
        {"dept": "총무팀", "name": "장영섭", "pos": "차장", "ext": "8193", "mobile": "010-5072-0919", "work": "예비군대대장, 민방위, 병무행정, 행사"},
        {"dept": "총무팀", "name": "주종호", "pos": "과장", "ext": "8202", "mobile": "010-3324-1187", "work": "보안, 미화, 대관, 게스트하우스"},
        {"dept": "총무팀", "name": "강은희", "pos": "대리", "ext": "8206", "mobile": "010-9127-1021", "work": "의료원 직인/문서배부, 월례조회, 행사"},
        {"dept": "총무팀", "name": "김보라", "pos": "선임", "ext": "8192", "mobile": "010-8073-0527", "work": "명예교수실 관리, 차량등록"},
        {"dept": "안전관리", "name": "윤호열", "pos": "UM", "ext": "8199", "mobile": "010-2623-7963", "work": "소방/방재 인증평가, 시설관리 (옴니버스파크 등)"},
        {"dept": "안전관리", "name": "주상건", "pos": "차장", "ext": "7135", "mobile": "010-9496-6483", "work": "시신기증 업무"},
        {"dept": "안전관리", "name": "곽정승", "pos": "과장", "ext": "8194", "mobile": "010-5218-6504", "work": "사업계획, 예산, 주차관리"},
        {"dept": "안전관리", "name": "박일용", "pos": "과장", "ext": "8201", "mobile": "010-6205-7751", "work": "계약(임대차), 사인물, 교원기숙사"},
        {"dept": "안전관리", "name": "김준석", "pos": "과장", "ext": "8205", "mobile": "010-9256-6904", "work": "연구실 안전관리, 출입증, 식대"},
        {"dept": "의산연별관", "name": "주용덕", "pos": "보안", "ext": "별관", "mobile": "010-2021-9541", "work": "의산연 별관 보안 지원"},
        {"dept": "의산연별관", "name": "안정진", "pos": "보안", "ext": "별관", "mobile": "010-4925-2926", "work": "의산연 별관 보안 지원"},
        {"dept": "협력업체", "name": "신성휴", "pos": "소장", "ext": "-", "mobile": "010-7161-2201", "work": "미화 협력업체 총괄 (세안)"},
        {"dept": "협력업체", "name": "이규용", "pos": "소장", "ext": "8300", "mobile": "010-8883-6580", "work": "보안 협력업체 총괄 (에스텍)"},
    ]

# 3. 로직 및 상태 관리
if "fav" not in st.session_state:
    st.session_state.fav = set()

data = get_contacts()

# 검색 및 필터 UI
col_search, col_fav = st.columns([2.5, 1])
with col_search:
    q = st.text_input("🔍 이름/부서/업무 검색", placeholder="예: 보안, 예비군, 시신")
with col_fav:
    show_fav = st.checkbox("⭐ 즐겨찾기")

# 4. 리스트 출력 로직
st.caption(f"검색 결과: {len(data)}명")

for i, c in enumerate(data):
    # 검색 필터링
    if q and not any(q.lower() in str(v).lower() for v in c.values()):
        continue
    if show_fav and i not in st.session_state.fav:
        continue

    is_f = i in st.session_state.fav
    star = "★" if is_f else "☆"
    # 전화번호 하이픈 제거
    tel_link = f"tel:023147{c['ext']}" if c['ext'].isdigit() else f"tel:{c['ext']}"
    mob_link = f"tel:{c['mobile'].replace('-', '')}"

    # 카드 레이아웃
    with st.container():
        st.markdown('<div class="contact-card">', unsafe_allow_html=True)
        
        # 이름, 부서, 아이콘을 담은 한 줄 레이아웃 (가로 고정)
        col_name, col_icons = st.columns([0.7, 0.3])
        
        with col_name:
            # 별표 버튼과 이름을 세로로 쌓지 않고 가로로 밀착 배치
            c_star, c_title = st.columns([0.1, 0.9])
            with c_star:
                if st.button(star, key=f"fav_{i}"):
                    if is_f: st.session_state.fav.remove(i)
                    else: st.session_state.fav.add(i)
                    st.rerun()
            with c_title:
                st.markdown(f'<p class="name-text">{c["name"]} <span class="pos-text">{c["pos"]} · {c["dept"]}</span></p>', unsafe_allow_html=True)
            
            # 하단 업무 내용
            st.markdown(f'<div class="work-text">{c["work"]}</div>', unsafe_allow_html=True)

        with col_icons:
            # 내선(☎️) 및 휴대폰(📱) 아이콘 배치
            st.markdown(f"""
                <div class="icon-section">
                    {"<a href='"+tel_link+"' class='icon-btn'>☎️</a>" if c['ext'] != "-" else ""}
                    <a href="{mob_link}" class="icon-btn">📱</a>
                </div>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
