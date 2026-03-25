import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 흑백 테마 및 초슬림 레이아웃 (CSS)
st.markdown("""
<style>
    .block-container { padding-top: 1rem; background-color: #ffffff; }
    
    /* 타이틀: 흑백 심플 */
    h1 {
        font-size: 1.1rem !important;
        font-weight: 700;
        color: #000000;
        margin-bottom: 0.8rem !important;
        border-bottom: 1px solid #eeeeee;
        padding-bottom: 0.5rem;
    }

    /* 카드 스타일 (70:30 배분) */
    .contact-card {
        background: #ffffff;
        padding: 10px 5px;
        margin-bottom: 0px;
        border-bottom: 1px solid #f2f2f2; /* 카드 구분선 */
        display: flex;
        justify-content: space-between;
        align-items: center;
    }

    /* 정보 구역 (70%) */
    .info-section {
        flex: 0.7;
    }

    .name-text { 
        font-weight: 700; 
        font-size: 1.05rem; 
        color: #000000; 
    }
    
    .pos-dept { 
        font-size: 0.95rem; 
        color: #666666;
        margin-left: 4px;
    }

    .work-text {
        font-size: 0.8rem;
        color: #999999;
        margin-top: 2px;
    }

    /* 흑백 아이콘 구역 (30%) */
    .icon-section {
        flex: 0.3;
        display: flex;
        justify-content: flex-end;
        gap: 22px; /* 아이콘 사이 충분한 간격 */
        padding-right: 5px;
    }
    
    .icon-link {
        text-decoration: none !important;
        font-size: 1.4rem; 
        color: #000000 !important; /* 완전 흑백 */
        filter: grayscale(100%);
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* 검색창 흑백 스타일 */
    .stTextInput input {
        border-radius: 5px !important;
        border: 1px solid #dddddd !important;
        background-color: #fafafa !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("비상연락망")

# 3. 데이터 (핵심 인원 반영)
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군, 민방위, 행사"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 미화, 대관"},
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방방재, 시설관리"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증 업무"},
    {"dept":"협력업체","name":"이규용","pos":"소장","ext":"02-3147-8300","mobile":"010-8883-6580","work":"보안 협력업체"},
]

# 4. 검색창
query = st.text_input("", placeholder="검색어 입력...")

# 5. 출력
filtered_data = [
    item for item in data 
    if any(query.lower() in str(val).lower() for val in item.values())
] if query else data

for p in filtered_data:
    ext_tel = p['ext'].replace('-', '')
    mob_tel = p['mobile'].replace('-', '')
    
    st.markdown(f"""
    <div class="contact-card">
        <div class="info-section">
            <div>
                <span class="name-text">{p['name']}</span>
                <span class="pos-dept">{p['pos']} · {p['dept']}</span>
            </div>
            <div class="work-text">- {p['work']}</div>
        </div>
        <div class="icon-section">
            {"<a href='tel:"+ext_tel+"' class='icon-link'>☎</a>" if p['ext'] != '-' else ""}
            <a href="tel:{mob_tel}" class="icon-link">📱</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
