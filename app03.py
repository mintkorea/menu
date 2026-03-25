import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 스타일 시트 (직함 크기 상향 및 버튼 균형)
st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    
    /* 타이틀 크기 */
    h1 {
        font-size: 1.2rem !important;
        font-weight: 700;
        margin-bottom: 1rem !important;
    }

    /* 카드 스타일 */
    .contact-card {
        background: #ffffff;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 10px;
        border: 1px solid #eee;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }

    /* 이름 및 직함/부서 (폰트 크기 조정) */
    .card-header {
        display: flex;
        align-items: center;
        gap: 8px;
    }

    .name-text { 
        font-weight: 700; 
        font-size: 1.1rem; /* 이름 기준 크기 */
        color: #1a1a1a; 
    }
    
    .pos-dept { 
        font-size: 1.0rem; /* 기존 0.8rem에서 2포인트(약 0.2rem) 키움 */
        color: #555;
        font-weight: 500;
    }

    /* 업무 부분 (심플 대시) */
    .work-text {
        font-size: 0.85rem;
        color: #666;
        margin: 6px 0;
        padding-left: 2px;
    }

    /* 버튼 최소화 및 동일 크기 배분 */
    .button-row {
        display: flex;
        gap: 8px;
        margin-top: 10px;
    }
    
    .btn {
        flex: 1; /* 내선/휴대폰 버튼 크기를 동일하게 맞춤 */
        text-align: center;
        padding: 6px 0;
        border-radius: 6px;
        text-decoration: none !important;
        font-size: 0.8rem;
        color: #555 !important;
        background-color: #f5f5f5;
        border: 1px solid #ddd;
    }
    
    .stTextInput { margin-bottom: 1rem; }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 3. 데이터 구성 (이미지 정보 기반)
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리 (대학본관, 의산연, 성의회관 등)"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군대대장, 민방위, 병무행정, 행사, ITC"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 미화, 대관, 게스트하우스"},
    {"dept":"총무팀","name":"강은희","pos":"대리","ext":"02-3147-8206","mobile":"010-9127-1021","work":"의료원 직인/문서배부, 월례조회, 행사"},
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방/방재 인증평가, 시설관리 (옴니버스파크)"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증 업무"},
    {"dept":"안전관리","name":"박일용","pos":"과장","ext":"02-3147-8201","mobile":"010-6205-7751","work":"계약(임대차, 용역 등), 사인물관리, 교원기숙사"},
    {"dept":"비서실","name":"이경자","pos":"부장","ext":"02-3147-8071","mobile":"010-6306-3652","work":"의무부총장, 기획조정실장 비서"},
    {"dept":"협력업체","name":"이규용","pos":"소장","ext":"02-3147-8300","mobile":"010-8883-6580","work":"보안 및 경비 업무 총괄"},
]

# 4. 검색창
query = st.text_input("", placeholder="성함 또는 업무를 검색하세요")

# 5. 출력부
filtered_data = [
    item for item in data 
    if any(query.lower() in str(val).lower() for val in item.values())
] if query else data

for p in filtered_data:
    st.markdown(f"""
    <div class="contact-card">
        <div class="card-header">
            <span class="name-text">{p['name']}</span>
            <span class="pos-dept">{p['pos']} · {p['dept']}</span>
        </div>
        <div class="work-text">
            - {p['work']}
        </div>
        <div class="button-row">
            {"<a href='tel:"+p['ext'].replace('-', '')+"' class='btn'>내선 연결</a>" if p.get('ext') and p['ext'] != '-' else ""}
            <a href="tel:{p['mobile'].replace('-', '')}" class="btn">휴대폰 연결</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
