import streamlit as st

# 1. 페이지 설정 및 디자인 최적화 (모바일 최적화)
st.set_page_config(page_title="성의교정 연락망", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1rem; padding-bottom: 0rem; }
    .contact-card { padding: 8px 0; border-bottom: 1px solid #f1f1f1; }
    .main-row {
        display: flex; justify-content: space-between; align-items: center;
        text-decoration: none; color: inherit !important;
    }
    .name-text { font-size: 1.05rem; font-weight: bold; color: #111; }
    .pos-text { font-size: 0.85rem; color: #666; margin-left: 5px; }
    .work-text { font-size: 0.8rem; color: #888; display: block; margin-top: 2px; line-height: 1.3; }
    .right-info { text-align: right; min-width: 105px; }
    .ext-text { font-size: 0.9rem; font-weight: bold; color: #007bff; }
    .mobile-text { font-size: 0.75rem; color: #aaa; }
    .stButton > button {
        border: none !important; background: transparent !important;
        padding: 0 !important; color: #ffc107 !important; font-size: 20px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 2. 이미지 기반 전체 데이터 (업무 내용 상세 포함)
def get_contacts():
    return [
        # 총무팀
        {"dept": "총무팀", "name": "박현욱", "pos": "팀장", "ext": "02-3147-8190", "mobile": "010-6245-0589", "work": "부서업무 총괄"},
        {"dept": "총무팀", "name": "김종래", "pos": "차장", "ext": "02-3147-8191", "mobile": "010-9056-3701", "work": "시설 및 자산관리 (대학본관, 의산연, 성의회관 등)"},
        {"dept": "총무팀", "name": "장영섭", "pos": "차장", "ext": "02-3147-8193", "mobile": "010-5072-0919", "work": "예비군대대장, 민방위, 병무행정, 행사, ITC, 의무위원회"},
        {"dept": "총무팀", "name": "주종호", "pos": "과장", "ext": "02-3147-8202", "mobile": "010-3324-1187", "work": "보안, 미화, 대관, 게스트하우스, 인체유래물은행"},
        {"dept": "총무팀", "name": "강은희", "pos": "대리", "ext": "02-3147-8206", "mobile": "010-9127-1021", "work": "의료원 직인/문서배부, 월례조회, 행사, 회의"},
        {"dept": "총무팀", "name": "김보라", "pos": "선임", "ext": "02-3147-8192", "mobile": "010-8073-0527", "work": "명예교수실 점검 및 관리, 명예교수 차량등록, 부서운영비"},
        {"dept": "총무팀", "name": "노종현", "pos": "책임", "ext": "02-3147-8195", "mobile": "010-9425-3109", "work": "행사, 회의자료취합, 단위기관장회의, 예비군대대"},
        {"dept": "총무팀", "name": "고규호", "pos": "책임", "ext": "02-3147-8196", "mobile": "010-3381-8870", "work": "캘린더/다이어리, 인증평가, 대학정보공시, 시설안전점검"},
        {"dept": "총무팀", "name": "김두리", "pos": "사원", "ext": "02-3147-8204", "mobile": "010-9661-1257", "work": "성의기숙사 사감"},
        {"dept": "총무팀", "name": "임세리", "pos": "사원", "ext": "02-3147-8197", "mobile": "010-3281-1229", "work": "우편, 물품/비품청구, 정수기관리, 정보보호"},
        {"dept": "총무팀", "name": "김종식", "pos": "사원", "ext": "-", "mobile": "010-9256-6904", "work": "업무지원"},
        # 안전관리
        {"dept": "안전관리", "name": "윤호열", "pos": "UM", "ext": "02-3147-8199", "mobile": "010-2623-7963", "work": "소방/방재 인증평가, 시설관리 (옴니버스파크, 기숙사 등)"},
        {"dept": "안전관리", "name": "주상건", "pos": "차장", "ext": "02-2258-7135", "mobile": "010-9496-6483", "work": "시신기증 업무"},
        {"dept": "안전관리", "name": "곽정승", "pos": "과장", "ext": "02-3147-8194", "mobile": "010-5218-6504", "work": "사업계획, 예산, 주차/차량관리"},
        {"dept": "안전관리", "name": "박일용", "pos": "과장", "ext": "02-3147-8201", "mobile": "010-6205-7751", "work": "계약 (임대차, 용역 등), 사인물관리, 교원기숙사"},
        {"dept": "안전관리", "name": "이경종", "pos": "부장", "ext": "02-3147-8203", "mobile": "010-2623-7963", "work": "교수업적평가 (위원회관리), 문서분배, 그룹웨어 ITC"},
        {"dept": "안전관리", "name": "김준석", "pos": "과장", "ext": "02-3147-8205", "mobile": "010-9256-6904", "work": "연구실 안전관리, 출입증등록, 연구원식대, 기타서무"},
        # 비서실
        {"dept": "비서실", "name": "이경자", "pos": "부장", "ext": "02-3147-8071", "mobile": "010-6306-3652", "work": "의무부총장, 기획조정실장 비서"},
        {"dept": "비서실", "name": "이상희", "pos": "과장", "ext": "02-3147-8068", "mobile": "010-3445-0623", "work": "영성구현실장, 사무처장 비서"},
        {"dept": "비서실", "name": "박은영", "pos": "과장", "ext": "02-3147-8069", "mobile": "010-5348-6849", "work": "의과대학장 비서"},
        # 의산연 별관 및 협력업체
        {"dept": "의산연별관", "name": "주용덕", "pos": "보안", "ext": "별관", "mobile": "010-2021-9541", "work": "의산연 별관 보안 지원"},
        {"dept": "의산연별관", "name": "김승배", "pos": "보안", "ext": "별관", "mobile": "010-8704-2591", "work": "의산연 별관 보안 지원"},
        {"dept": "의산연별관", "name": "안정진", "pos": "보안", "ext": "별관", "mobile": "010-4925-2926", "work": "의산연 별관 보안 지원"},
        {"dept": "협력업체", "name": "신성휴", "pos": "소장", "ext": "-", "mobile": "010-7161-2201", "work": "미화 협력업체 총괄 (세안)"},
        {"dept": "협력업체", "name": "이규용", "pos": "소장", "ext": "02-3147-8300", "mobile": "010-8883-6580", "work": "보안 협력업체 총괄 (에스텍)"},
    ]

# 3. 상태 관리 및 검색 UI
if "fav" not in st.session_state: st.session_state.fav = set()
contacts = get_contacts()

col_search, col_fav = st.columns([2.5, 1])
with col_search:
