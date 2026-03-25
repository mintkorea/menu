import streamlit as st

# 1. 페이지 설정 및 디자인 최적화
st.set_page_config(page_title="성의교정 연락망", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .contact-card { padding: 12px 0; border-bottom: 1px dotted #ddd; }
    
    /* 별표와 이름을 한 줄에 배치 */
    .name-row { display: flex; align-items: center; gap: 8px; margin-bottom: 2px; }
    .fav-btn-style { font-size: 20px; cursor: pointer; line-height: 1; }
    
    .link-wrapper { text-decoration: none; color: inherit !important; display: flex; justify-content: space-between; align-items: flex-start; }
    .name-text { font-size: 1.1rem; font-weight: bold; color: #111; }
    .pos-text { font-size: 0.85rem; color: #666; }
    .work-text { font-size: 0.85rem; color: #888; display: block; padding-left: 28px; line-height: 1.4; }
    
    .right-info { text-align: right; min-width: 105px; }
    .ext-text { font-size: 1rem; font-weight: bold; color: #007bff; display: block; }
    .mobile-text { font-size: 0.8rem; color: #aaa; }
    
    /* 스트림릿 버튼 투명화 (별표 전용) */
    div[data-testid="column"] button {
        border: none !important; background: transparent !important; padding: 0 !important;
        box-shadow: none !important; color: #ffc107 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 2. 데이터셋 (이미지의 모든 정보 반영)
def get_data():
    return [
        {"dept": "총무팀", "name": "박현욱", "pos": "팀장", "ext": "02-3147-8190", "mobile": "010-6245-0589", "work": "부서업무 총괄"},
        {"dept": "총무팀", "name": "김종래", "pos": "차장", "ext": "02-3147-8191", "mobile": "010-9056-3701", "work": "시설 및 자산관리(대학본관, 의산연, 성의회관 등)"},
        {"dept": "총무팀", "name": "장영섭", "pos": "차장", "ext": "02-3147-8193", "mobile": "010-5072-0919", "work": "예비군대대장, 민방위, 병무행정, 행사, ITC, 기타서무"},
        {"dept": "총무팀", "name": "주종호", "pos": "과장", "ext": "02-3147-8202", "mobile": "010-3324-1187", "work": "보안, 미화, 대관, 게스트하우스, 인체유래물은행"},
        {"dept": "총무팀", "name": "강은희", "pos": "대리", "ext": "02-3147-8206", "mobile": "010-9127-1021", "work": "의료원 직인/문서배부, 월례조회, 행사, 회의"},
        {"dept": "총무팀", "name": "김보라", "pos": "선임", "ext": "02-3147-8192", "mobile": "010-8073-0527", "work": "명예교수실 점검 및 관리, 차량등록, 부서운영비"},
        {"dept": "총무팀", "name": "노종현", "pos": "책임", "ext": "02-3147-8195", "mobile": "010-9425-3109", "work": "행사, 회의자료취합, 단위기관장회의, 예비군대대"},
        {"dept": "총무팀", "name": "고규호", "pos": "책임", "ext": "02-3147-8196", "mobile": "010-3381-8870", "work": "캘린더/다이어리, 인증평가, 대학정보공시, 안전점검"},
        {"dept": "총무팀", "name": "김두리", "pos": "사원", "ext": "02-3147-8204", "mobile": "010-9661-1257", "work": "성의기숙사 사감"},
        {"dept": "총무팀", "name": "임세리", "pos": "사원", "ext": "02-3147-8197", "mobile": "010-3281-1229", "work": "우편, 물품/비품청구, 정수기관리, 정보보호"},
        {"dept": "총무팀", "name": "김종식", "pos": "사원", "ext": "-", "mobile": "010-9256-6904", "work": "업무지원"},
        {"dept": "안전관리", "name": "윤호열", "pos": "UM", "ext": "02-3147-8199", "mobile": "010-2623-7963", "work": "소방/방재 인증평가, 시설관리(옴니버스파크 등)"},
        {"dept": "안전관리", "name": "주상건", "pos": "차장", "ext": "02-2258-7135", "mobile": "010-9496-6483", "work": "시신기증 업무"},
        {"dept": "안전관리", "name": "곽정승", "pos": "과장", "ext": "02-3147-8194", "mobile": "010-5218-6504", "work": "사업계획, 예산, 주차/차량관리"},
        {"dept": "안전관리", "name": "박일용", "pos": "과장", "ext": "02-3147-8201", "mobile": "010-6205-7751", "work": "계약(임대차, 용역 등), 사인물관리, 교원기숙사"},
        {"dept": "안전관리", "name": "이경종", "pos": "부장", "ext": "02-3147-8203", "mobile": "010-2623-7963", "work": "교수업적평가, 문서분배, 그룹웨어 ITC"},
        {"dept": "안전관리", "name": "김준석", "pos": "과장", "ext": "02-3147-8205", "mobile": "010-9256-6904", "work": "연구실 안전관리, 출입증등록, 기타서무"},
        {"dept": "비서실", "name": "이경자", "pos": "부장", "ext": "02-3147-8071", "mobile": "010-6306-3652", "work": "의무부총장, 기획조정실장 비서"},
        {"dept": "비서실", "name": "이상희", "pos": "과장", "ext": "02-3147-8068", "mobile": "010-3445-0623", "work": "영성구현실장, 사무처장 비서"},
        {"dept": "비서실", "name": "박은영", "pos": "과장", "ext": "02-3147-8069", "mobile": "010-5348-6849", "work": "의과대학장 비서"},
        {"dept": "의산연별관", "name": "주용덕", "pos": "보안", "ext": "별관", "mobile": "010-2021-9541", "work": "의산연 별관 보안"},
        {"dept": "의산연별관", "name": "김승배", "pos": "보안", "ext": "별관", "mobile": "010-8704-2591", "work": "의산연 별관 보안"},
        {"dept": "의산연별관", "name": "안정진", "pos": "보안", "ext": "별관", "mobile": "010-4925-2926", "work": "의산연 별관 보안"},
        {"dept": "협력업체", "name": "신성휴", "pos": "소장", "ext": "-", "mobile": "010-7161-2201", "work": "미화 협력업체 총괄"},
        {"dept": "협력업체", "name": "이규용", "pos": "소장", "ext": "8300", "mobile": "010-8883-6580", "work": "보안 협력업체 총괄"},
    ]

# 3. 로직 처리
if "favorites" not in st.session_state:
    st.session_state.favorites = set()

data = get_data()

# 검색 및 필터 UI
c1, c2 = st.columns([3, 1])
with c1:
    search = st.text_input("🔍 이름/부서/업무 검색", placeholder="예: 예비군, 시신, 보안")
with c2:
    only_fav = st.checkbox("⭐ 즐겨찾기")

# 필터링
display_list = data
if search:
    display_list = [c for c in display_list if any(search.lower() in str(v).lower() for v in c.values())]
if only_fav:
    display_list = [c for c in display_list if c['name'] in st.session_state.favorites]

st.caption(f"총 {len(display_list)}명 검색됨")

# 4. 리스트 출력 (이름+별표 일체형)
for i, c in enumerate(display_list):
    is_f = c['name'] in st.session_state.favorites
    star = "★" if is_f else "☆"
    tel_url = f"tel:{c['mobile'].replace('-', '')}"
    
    with st.container():
        # 카드 전체 레이아웃
        st.markdown(f'<div class="contact-card">', unsafe_allow_html=True)
        
        # 상단 이름 및 전화번호 행
        col_main, col_tel = st.columns([0.7, 0.3])
        
        with col_main:
            # 별표 버튼과 이름을 가로로 배치하기 위해 서브 컬럼 사용
            b_col, n_col = st.columns([0.1, 0.9])
            with b_col:
                if st.button(star, key=f"btn_{c['name']}_{i}"):
                    if is_f: st.session_state.favorites.remove(c['name'])
                    else: st.session_state.favorites.add(c['name'])
                    st.rerun()
            with n_col:
                st.markdown(f'<div class="name-text">{c["name"]} <span class="pos-text">{c["pos"]} ({c["dept"]})</span></div>', unsafe_allow_html=True)
            
            # 업무 내용은 이름 아래에 들여쓰기해서 표시
            st.markdown(f'<span class="work-text">{c["work"]}</span>', unsafe_allow_html=True)
            
        with col_tel:
            # 내선번호와 휴대폰 번호를 클릭 가능한 링크로 표시
            st.markdown(f"""
                <a href="{tel_url}" style="text-decoration:none;">
                    <div class="right-info">
                        <span class="ext-text">{c['ext'][-4:] if '-' in c['ext'] else c['ext']}</span>
                        <span class="mobile-text">{c['mobile']}</span>
                    </div>
                </a>
            """, unsafe_allow_html=True)
            
        st.markdown('</div>', unsafe_allow_html=True)
