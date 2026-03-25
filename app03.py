import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 슬림 디자인 스타일 (CSS)
st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    
    /* 타이틀 크기 절반 축소 */
    h1 {
        font-size: 1.2rem !important;
        font-weight: 700;
        margin-bottom: 1rem !important;
    }

    /* 개별 카드 스타일 (더 얇게) */
    .contact-card {
        background: #ffffff;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border: 1px solid #eee;
    }

    /* 이름 및 직함 */
    .card-header {
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .name-text { 
        font-weight: 700; 
        font-size: 1rem; 
        color: #1a1a1a; 
    }
    
    .pos-dept { 
        font-size: 0.8rem; 
        color: #777;
    }

    /* 업무 부분 (장식 제거, 대시 처리) */
    .work-text {
        font-size: 0.8rem;
        color: #666;
        margin: 4px 0;
        padding-left: 4px;
    }

    /* 버튼 최소화 및 컬러 제거 */
    .button-row {
        display: flex;
        gap: 5px;
        margin-top: 8px;
    }
    
    .btn {
        padding: 4px 8px;
        border-radius: 4px;
        text-decoration: none !important;
        font-size: 0.75rem;
        color: #555 !important;
        background-color: #f0f0f0;
        border: 1px solid #ddd;
    }
    
    /* 검색창 슬림화 */
    .stTextInput { margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 3. 데이터 구성 (전체 리스트 반영)
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리 (대학본관, 의산연, 성의회관 등)"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군대대장, 민방위, 병무행정, 행사, ITC"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 미화, 대관, 게스트하우스"},
    {"dept":"총무팀","name":"강은희","pos":"대리","ext":"02-3147-8206","mobile":"010-9127-1021","work":"의료원 직인/문서배부, 월례조회, 행사"},
    {"dept":"총무팀","name":"김보라","pos":"선임","ext":"02-3147-8192","mobile":"010-8073-0527","work":"명예교수실 관리, 차량등록, 부서운영비"},
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방/방재 인증평가, 시설관리 (옴니버스파크)"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증 업무"},
    {"dept":"안전관리","name":"곽정승","pos":"과장","ext":"02-3147-8194","mobile":"010-5218-6504","work":"사업계획, 예산, 주차/차량관리"},
    {"dept":"협력업체","name":"이규용","pos":"소장","ext":"02-3147-8300","mobile":"010-8883-6580","work":"보안 및 경비 업무 총괄"},
]

# 4. 검색창
query = st.text_input("", placeholder="이름 또는 업무 검색")

# 5. 리스트 출력
filtered_data = [
    item for item in data 
    if any(query.lower() in str(val).lower() for val in item.values())
] if query else data

for person in filtered_data:
    st.markdown(f"""
    <div class="contact-card">
        <div class="card-header">
            <span class="name-text">{person['name']}</span>
            <span class="pos-dept">{person['pos']} · {person['dept']}</span>
        </div>
        <div class="work-text">
            - {person['work']}
        </div>
        <div class="button-row">
            {"<a href='tel:"+person['ext'].replace('-', '')+"' class='btn'>내선</a>" if person.get('ext') and person['ext'] != '-' else ""}
            <a href="tel:{person['mobile'].replace('-', '')}" class="btn">휴대폰</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
