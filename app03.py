import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 개별 카드 및 모바일 최적화 스타일 (CSS)
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; background-color: #f5f7f9; }
    
    /* 개별 카드 스타일 */
    .contact-card {
        background: #ffffff;
        padding: 18px;
        border-radius: 15px;
        margin-bottom: 16px;
        border: none;
        box-shadow: 0 4px 12px rgba(0,0,0,0.08); /* 그림자 강조로 카드 느낌 부여 */
    }

    /* 이름 및 직함 한 줄 고정 */
    .card-header {
        display: flex;
        align-items: baseline;
        gap: 8px;
        margin-bottom: 8px;
    }

    .name-text { 
        font-weight: 800; 
        font-size: 1.2rem; 
        color: #1a1a1a; 
        margin: 0; 
    }
    
    .pos-dept { 
        font-size: 0.9rem; 
        color: #666; 
        font-weight: 500;
    }

    /* 업무 내용 구역 */
    .work-box {
        background-color: #f9fbff;
        padding: 10px 12px;
        border-radius: 8px;
        font-size: 0.88rem;
        color: #555;
        line-height: 1.5;
        margin: 10px 0;
        border-left: 3px solid #007bff; /* 업무 내용 강조 선 */
    }

    /* 하단 전화 버튼 구역 */
    .button-row {
        display: flex;
        gap: 10px;
        margin-top: 15px;
    }
    
    .btn {
        flex: 1;
        text-align: center;
        padding: 12px 0;
        border-radius: 10px;
        text-decoration: none !important;
        font-size: 0.95rem;
        font-weight: 700;
        transition: 0.2s;
    }
    
    .btn-ext { 
        background-color: #ffffff; 
        color: #444 !important; 
        border: 1px solid #dee2e6; 
    }
    
    .btn-mob { 
        background-color: #007bff; 
        color: #ffffff !important; 
        border: none;
    }
    
    /* 검색창 스타일 개선 */
    .stTextInput input {
        border-radius: 10px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 3. 데이터 구성
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리 (대학본관, 의산연, 성의회관 등)"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군대대장, 민방위, 병무행정, 행사, ITC"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 미화, 대관, 게스트하우스, 인체유래물은행"},
    {"dept":"총무팀","name":"강은희","pos":"대리","ext":"02-3147-8206","mobile":"010-9127-1021","work":"의료원 직인/문서배부, 월례조회, 행사, 회의"},
    {"dept":"총무팀","name":"김보라","pos":"선임","ext":"02-3147-8192","mobile":"010-8073-0527","work":"명예교수실 점검 및 관리, 차량등록, 부서운영비"},
    {"dept":"총무팀","name":"노종현","pos":"책임","ext":"02-3147-8195","mobile":"010-9425-3109","work":"행사, 회의자료취합, 단위기관장회의, 예비군대대"},
    {"dept":"총무팀","name":"고규호","pos":"책임","ext":"02-3147-8196","mobile":"010-3381-8870","work":"캘린더/다이어리, 인증평가, 대학정보공시"},
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방/방재 인증평가, 시설관리 (옴니버스파크 등)"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증 업무"},
    {"dept":"비서실","name":"이경자","pos":"부장","ext":"02-3147-8071","mobile":"010-6306-3652","work":"의무부총장, 기획조정실장 비서"},
    {"협력업체":"보안","name":"이규용","pos":"소장","ext":"02-3147-8300","mobile":"010-8883-6580","work":"보안 및 경비 업무"},
]

# 4. 검색창
query = st.text_input("", placeholder="성함, 부서 또는 담당 업무를 입력하세요")

# 5. 리스트 출력
filtered_data = [
    item for item in data 
    if any(query.lower() in str(val).lower() for val in item.values())
] if query else data

st.caption(f"총 {len(filtered_data)}개의 연락처가 있습니다.")

for person in filtered_data:
    # 카드 시작
    st.markdown(f"""
    <div class="contact-card">
        <div class="card-header">
            <span class="name-text">{person['name']}</span>
            <span class="pos-dept">{person['pos']} · {person.get('dept', person.get('협력업체', ''))}</span>
        </div>
        <div class="work-box">
            {person['work']}
        </div>
        <div class="button-row">
            {"<a href='tel:"+person['ext'].replace('-', '')+"' class='btn btn-ext'>내선 연결</a>" if person.get('ext') and person['ext'] != '-' else ""}
            <a href="tel:{person['mobile'].replace('-', '')}" class="btn btn-mob">휴대폰 연결</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
