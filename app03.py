import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. CSS: 상단 여백 확보 및 아이콘 간격 최소화
st.markdown("""
<style>
    /* 상단 여백 확보 (타이틀 잘림 방지) */
    .block-container { 
        padding-top: 4.5rem !important; 
        background-color: #ffffff; 
    }
    
    /* 타이틀: 중앙 정렬 및 크기 확대 */
    .main-title {
        font-size: 1.6rem;
        font-weight: 800;
        color: #000000;
        text-align: center;
        margin-bottom: 0.6rem !important;
    }

    /* 검색창: 간격 밀착 */
    .stTextInput { margin-top: -10px !important; margin-bottom: -28px !important; }
    .stTextInput input {
        border-radius: 4px !important;
        border: 1px solid #cccccc !important;
        height: 42px !important;
    }

    /* 카드 스타일: 이름과 아이콘 간격 밀착 */
    .contact-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 14px 0px;
        border-bottom: 1px solid #f2f2f2;
    }

    /* 정보 구역 (85%) */
    .info-section { flex: 0.85; }
    .name-row { display: flex; align-items: baseline; gap: 6px; }
    .name-text { font-weight: 700; font-size: 1.15rem; color: #000; }
    .pos-dept { font-size: 1.0rem; color: #666; }
    .work-text { font-size: 0.85rem; color: #999; margin-top: 2px; }

    /* 아이콘 구역 (15%): 간격 극소화 및 새로운 흑백 아이콘 */
    .icon-section {
        flex: 0.15;
        display: flex;
        justify-content: flex-end;
        gap: 8px; /* 아이콘 사이 간격 극소화 */
        padding-right: 5px;
    }
    
    .icon-link {
        text-decoration: none !important;
        font-size: 1.5rem; 
        color: #1a1a1a !important;
        display: flex;
        align-items: center;
        filter: grayscale(100%);
    }
</style>
""", unsafe_allow_html=True)

# 타이틀
st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 데이터 로드
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"8191","mobile":"010-9056-3701","work":"시설 및 자산관리 (본관, 의산연 등)"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"8193","mobile":"010-5072-0919","work":"예비군, 민방위, 행사"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"8202","mobile":"010-3324-1187","work":"보안, 미화, 대관"},
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"8199","mobile":"010-2623-7963","work":"소방방재, 시설관리"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"7135","mobile":"010-9496-6483","work":"시신기증 업무"},
    {"dept":"협력업체","name":"이규용","pos":"소장","ext":"8300","mobile":"010-8883-6580","work":"보안 협력업체 총괄"},
]

# 4. 검색창
query = st.text_input("", placeholder="성함, 부서 또는 업무 검색")

# 5. 리스트 출력
filtered_data = [
    item for item in data 
    if any(query.lower() in str(val).lower() for val in item.values())
] if query else data

st.markdown('<div class="list-container">', unsafe_allow_html=True)
for p in filtered_data:
    ext_val = p['ext']
    ext_tel = f"023147{ext_val}" if ext_val.isdigit() else ext_val
    mob_tel = p['mobile'].replace('-', '')
    
    st.markdown(f"""
    <div class="contact-card">
        <div class="info-section">
            <div class="name-row">
                <span class="name-text">{p['name']}</span>
                <span class="pos-dept">{p['pos']} · {p['dept']}</span>
            </div>
            <div class="work-text">- {p['work']}</div>
        </div>
        <div class="icon-section">
            {"<a href='tel:"+ext_tel+"' class='icon-link'>⌗</a>" if ext_val != '-' else ""}
            <a href="tel:{mob_tel}" class="icon-link">▶</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
