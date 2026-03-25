import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 고정형 흑백 디자인 (상단 여백 및 간격 최적화)
st.markdown("""
<style>
    /* 상단 여백 확보 */
    .block-container { padding-top: 3rem !important; background-color: #ffffff; }
    
    /* 타이틀 및 상단 영역 */
    .main-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #000;
        margin-bottom: 0.5rem;
    }

    /* 검색창과 리스트 간격 최소화 */
    .stTextInput { margin-bottom: -15px !important; }
    .stTextInput input {
        border-radius: 4px !important;
        border: 1px solid #e0e0e0 !important;
        height: 38px !important;
    }

    /* 리스트 컨테이너 */
    .list-container { margin-top: 5px; }

    /* 개별 카드 (구분선 위주 슬림 디자인) */
    .contact-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 2px;
        border-bottom: 1px solid #f0f0f0;
    }

    /* 정보 구역 (70%) */
    .info-section { flex: 0.7; }
    .name-row { display: flex; align-items: baseline; gap: 5px; }
    .name-text { font-weight: 700; font-size: 1.05rem; color: #000; }
    .pos-dept { font-size: 0.95rem; color: #666; }
    .work-text { font-size: 0.85rem; color: #999; margin-top: 2px; }

    /* 아이콘 구역 (30%) */
    .icon-section {
        flex: 0.3;
        display: flex;
        justify-content: flex-end;
        gap: 25px;
        padding-right: 8px;
    }
    
    .icon-link {
        text-decoration: none !important;
        font-size: 1.3rem; 
        color: #000000 !important;
        display: flex;
        align-items: center;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 3. 전체 데이터 반영
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"8191","mobile":"010-9056-3701","work":"시설 및 자산관리"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"8193","mobile":"010-5072-0919","work":"예비군, 민방위, 행사"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"8202","mobile":"010-3324-1187","work":"보안, 미화, 대관"},
    {"dept":"총무팀","name":"강은희","pos":"대리","ext":"8206","mobile":"010-9127-1021","work":"직인, 문서배부, 행사"},
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"8199","mobile":"010-2623-7963","work":"소방방재, 시설관리"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"7135","mobile":"010-9496-6483","work":"시신기증 업무"},
    {"dept":"안전관리","name":"곽정승","pos":"과장","ext":"8194","mobile":"010-5218-6504","work":"사업계획, 예산, 주차"},
    {"dept":"비서실","name":"이경자","pos":"부장","ext":"8071","mobile":"010-6306-3652","work":"의무부총장 비서"},
    {"dept":"협력업체","name":"이규용","pos":"소장","ext":"8300","mobile":"010-8883-6580","work":"보안 협력업체"},
]

# 4. 검색창 (가능어 표시)
query = st.text_input("", placeholder="성함, 부서 또는 업무 검색 (예: 보안, 시설, 총무)")

# 5. 리스트 출력
filtered_data = [
    item for item in data 
    if any(query.lower() in str(val).lower() for val in item.values())
] if query else data

st.markdown('<div class="list-container">', unsafe_allow_html=True)
for p in filtered_data:
    # 내선번호 자동 완성 (02-3147-)
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
            {"<a href='tel:"+ext_tel+"' class='icon-link'>☎</a>" if ext_val != '-' else ""}
            <a href="tel:{mob_tel}" class="icon-link">📱</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
