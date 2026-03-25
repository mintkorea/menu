import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 흑백 아이콘 및 슬림 레이아웃 CSS
st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    
    /* 타이틀 크기 축소 */
    h1 {
        font-size: 1.1rem !important;
        font-weight: 700;
        margin-bottom: 0.8rem !important;
    }

    /* 카드 스타일 (Flexbox로 왼쪽 70%, 오른쪽 30% 배분) */
    .contact-card {
        background: #ffffff;
        padding: 12px;
        border-radius: 8px;
        margin-bottom: 8px;
        border: 1px solid #eee;
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
        font-size: 1.1rem; 
        color: #1a1a1a; 
    }
    
    .pos-dept { 
        font-size: 1.0rem; 
        color: #555;
        margin-left: 5px;
    }

    .work-text {
        font-size: 0.85rem;
        color: #777;
        margin-top: 4px;
    }

    /* 아이콘 버튼 구역 (30%) */
    .icon-section {
        flex: 0.3;
        display: flex;
        justify-content: flex-end;
        gap: 20px; /* 아이콘 사이 간격 */
    }
    
    .icon-link {
        text-decoration: none !important;
        font-size: 1.5rem; /* 아이콘 크기 */
        color: #333 !important; /* 흑백 설정 */
        display: flex;
        align-items: center;
        justify-content: center;
    }

    /* 검색창 슬림화 */
    .stTextInput { margin-bottom: 0.8rem; }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 3. 데이터 구성 (이미지 정보 반영)
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리 (본관, 의산연 등)"},
    {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군대대장, 민방위, 행사"},
    {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 미화, 대관, 게스트하우스"},
    {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방/방재 인증평가, 시설관리"},
    {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증 업무"},
    {"dept":"협력업체","name":"이규용","pos":"소장","ext":"02-3147-8300","mobile":"010-8883-6580","work":"보안 협력업체 총괄"},
]

# 4. 검색 기능
query = st.text_input("", placeholder="성함 또는 업무 검색")

# 5. 리스트 출력
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
            {"<a href='tel:"+ext_tel+"' class='icon-link' title='내선'>☎︎</a>" if p['ext'] != '-' else ""}
            <a href="tel:{mob_tel}" class="icon-link" title='휴대폰'>📱</a>
        </div>
    </div>
    """, unsafe_allow_html=True)
