import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS 스타일 (아이콘 영역 최적화)
st.markdown("""
<style>
    header[data-testid="stHeader"] { display: none !important; }
    [data-testid="stMainBlockContainer"] { padding-top: 1rem !important; }
    .main-title { font-size: 1.6rem; font-weight: 800; text-align: center; margin-bottom: 15px; }
    
    .contact-card { 
        display: flex; justify-content: space-between; align-items: center; 
        padding: 10px 0px; border-bottom: 1px solid #eeeeee; width: 100%; 
    }
    
    /* 정보 영역: 더 넓게 확보 */
    .info-section { flex: 1; min-width: 0; padding-right: 10px; }
    .name-row { display: flex; align-items: baseline; gap: 6px; flex-wrap: nowrap; }
    .name-text { font-weight: 700; font-size: 1.05rem; color: #000; white-space: nowrap; }
    .pos-dept { font-size: 0.85rem; color: #555; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
    .work-text { font-size: 0.8rem; color: #777; margin-top: 3px; line-height: 1.3; word-break: keep-all; }
    
    /* 아이콘 영역: 너비 축소 및 간격 조정 */
    .icon-section { 
        min-width: 55px; /* 70px -> 55px로 축소 */
        display: flex; justify-content: flex-end; 
        gap: 8px; /* 15px -> 8px로 축소 */
        flex-shrink: 0; 
    }
    .icon-link { 
        text-decoration: none !important; font-size: 1.15rem; 
        font-weight: 800; color: #007bff !important; 
        width: 24px; text-align: center; 
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터셋
contact_data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"8191","mobile":"010-9056-3701","work":"시설 및 자산관리(대학본부, 의생명산업연구원, 성의회관 등)"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"8193","mobile":"010-5072-0919","work":"예비군대대장, 민방위, 업무행정, 행사, 그룹웨어 ITC, 의무위원회, 기타서무"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"8202","mobile":"010-3324-1187","work":"보안, 미화, 대관, 게스트하우스, 인체유래물은행"},
    {"dept":"총무팀","name":"강은희","pos":"대리","ext":"8206","mobile":"010-9127-1021","work":"의료원 직인/문서배부, 월례조회, 행사, 회의"},
    {"dept":"총무팀","name":"김보라","pos":"선임","ext":"8192","mobile":"010-8073-0527","work":"명예교수실 점검 및 관리, 명예교수 차량등록, 부서운영비"},
    {"dept":"총무팀","name":"노종현","pos":"책임","ext":"8195","mobile":"010-9425-3109","work":"행사, 회의자료취합, 단위기관장회의, 예비군대대"},
    {"dept":"총무팀","name":"고규호","pos":"책임","ext":"8196","mobile":"010-3381-8870","work":"캘린더/다이어리, 인증평가, 대학정보공시, 시설안전점검"},
    {"dept":"총무팀","name":"김두리","pos":"사원","ext":"8204","mobile":"010-9661-1257","work":"성의기숙사 사감"},
    {"dept":"총무팀","name":"임세리","pos":"사원","ext":"8197","mobile":"010-3281-1229","work":"우편, 물품/비품청구, 정수기관리, 정보보호"},
    {"dept":"총무팀","name":"김종식","pos":"사원","ext":"","mobile":"010-9256-6904","work":"업무지원"},
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"8199","mobile":"010-2623-7963","work":"소방/방재 인증평가, 시설/자산관리(옴니버스파크, 성의기숙사, 병원별관 등)"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"7135","mobile":"010-9496-6483","work":"시신기증 업무"},
    {"dept":"안전관리","name":"곽정승","pos":"과장","ext":"8194","mobile":"010-5218-6504","work":"사업계획, 예산, 주차/차량관리"},
    {"dept":"안전관리","name":"박일용","pos":"과장","ext":"8201","mobile":"010-6205-7751","work":"계약(임대차, 용역 등), 사인물관리, 교원기숙사"},
    {"dept":"안전관리","name":"이경종","pos":"부장","ext":"8203","mobile":"010-2623-7963","work":"교수업적평가(위원회관리), 문서분배, 그룹웨어 ITC"},
    {"dept":"안전관리","name":"김준석","pos":"과장","ext":"8205","mobile":"010-9256-6904","work":"연구실 안전관리, 출입증등록, 연구원식당, 기타서무업무"},
    {"dept":"비서실","name":"이경자","pos":"부장","ext":"8071","mobile":"010-6306-3652","work":"의무부총장, 기획조정실장 비서"},
    {"dept":"비서실","name":"이상희","pos":"과장","ext":"8068","mobile":"010-3445-0623","work":"영성구현실장, 사무처장 비서"},
    {"dept":"비서실","name":"박은영","pos":"과장","ext":"8069","mobile":"010-5348-6849","work":"의과대학장 비서"},
    {"dept":"의산연 별관","name":"주용덕","pos":"","ext":"","mobile":"010-2021-9541","work":""},
    {"dept":"의산연 별관","name":"김승배","pos":"","ext":"","mobile":"010-8704-2591","work":""},
    {"dept":"의산연 별관","name":"안정진","pos":"","ext":"","mobile":"010-4925-2926","work":""},
    {"dept":"협력업체","name":"신성휴","pos":"소장","ext":"","mobile":"010-7161-2201","work":"미화 소장"},
    {"dept":"협력업체","name":"이규용","pos":"소장","ext":"8300","mobile":"010-8883-6580","work":"보안 소장"},
]

# 4. 검색창
query = st.text_input("search", placeholder="성함, 부서 또는 업무 검색...", label_visibility="collapsed")

# 5. 출력 로직
for p in contact_data:
    # 검색 필터
    name, dept, work, pos = p.get('name',''), p.get('dept',''), p.get('work',''), p.get('pos','')
    if query and query.lower() not in f"{name}{dept}{work}{pos}".lower():
        continue

    # T(내선), M(휴대폰) 아이콘 생성
    t_html = ""
    ext_val = str(p.get('ext', '')).strip()
    if ext_val:
        prefix = "022258" if name == "주상건" else "023147"
        t_html = f'<a href="tel:{prefix}{ext_val}" class="icon-link">T</a>'

    m_html = ""
    mobile_val = str(p.get('mobile', '')).replace('-', '').strip()
    if mobile_val:
        m_html = f'<a href="tel:{mobile_val}" class="icon-link">M</a>'

    # 텍스트 구성
    sep = " · " if pos and dept else ""
    work_html = f'<div class="work-text">- {work}</div>' if work else ""

    # 한 줄 HTML 카드 렌더링
    card_html = (
        f'<div class="contact-card">'
        f'<div class="info-section">'
        f'<div class="name-row"><span class="name-text">{name}</span><span class="pos-dept">{pos}{sep}{dept}</span></div>'
        f'{work_html}'
        f'</div>'
        f'<div class="icon-section">{t_html}{m_html}</div>'
        f'</div>'
    )
    
    st.markdown(card_html, unsafe_allow_html=True)
