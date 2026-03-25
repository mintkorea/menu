import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS: 상단 밀착 및 검색창 주변 여백 미세 조정
st.markdown("""
<style>
    /* 상단 헤더 숨기기 */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 최상단 여백 제거 */
    [data-testid="stMainBlockContainer"] {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        gap: 0rem !important;
    }

    /* 타이틀 설정 */
    .main-title {
        font-size: 1.8rem; 
        font-weight: 800;
        color: #000;
        text-align: center;
        margin-bottom: 0px !important;
        padding: 0px !important;
    }

    /* 검색창 상하 여백 조정 (축구장 폐쇄, 적정 간격 확보) */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stTextInput"]) {
        padding-top: 15px !important;    /* 타이틀 ~ 검색창 사이 */
        padding-bottom: 20px !important; /* 검색창 ~ 첫 결과(박현욱) 사이 */
    }

    .stTextInput { 
        margin: 0px !important;
    }

    .stTextInput input {
        border-radius: 4px !important;
        border: 1px solid #cccccc !important;
        height: 42px !important;
    }

    /* 연락처 카드 스타일 */
    .contact-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0px; 
        border-bottom: 1px solid #eeeeee;
    }

    .info-section { flex: 0.8; padding-right: 10px; }
    .name-row { display: flex; align-items: baseline; gap: 8px; }
    .name-text { font-weight: 700; font-size: 1.1rem; color: #000; }
    .pos-dept { font-size: 0.95rem; color: #555; }
    .work-text { font-size: 0.85rem; color: #888; margin-top: 4px; line-height: 1.4; }

    .icon-section {
        min-width: 85px; 
        display: flex;
        justify-content: flex-end;
        gap: 20px; 
    }
    
    .icon-link {
        text-decoration: none !important;
        font-size: 1.4rem; 
        font-weight: 700;
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# 타이틀
st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터셋
data = [
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

# 5. 결과 리스트 출력
for p in data:
    if query and not any(query.lower() in str(val).lower() for val in p.values()):
        continue
        
    ext_val = p.get('ext', '')
    ext_tel = f"023147{ext_val}" if ext_val.isdigit() else ""
    if p['name'] == "주상건": ext_tel = "0222587135"
    
    mob_tel = p['mobile'].replace('-', '')
    
    contact_html = f"""
    <div class="contact-card">
        <div class="info-section">
            <div class="name-row">
                <span class="name-text">{p['name']}</span>
                <span class="pos-dept">{p['pos']} · {p['dept']}</span>
            </div>
            <div class="work-text">{"- " + p['work'] if p['work'] else ""}</div>
        </div>
        <div class="icon-section">
            {"<a href='tel:"+ext_tel+"' class='icon-link'>☎</a>" if ext_tel else ""}
            <a href="tel:{mob_tel}" class="icon-link">M</a>
        </div>
    </div>
    """
    st.markdown(contact_html, unsafe_allow_html=True)
