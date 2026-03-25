import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 강력한 여백 제거 CSS (id와 특정 데이터 속성 타겟팅)
st.markdown("""
<style>
    /* 1. 최상단 헤더(회색선 등) 완전 제거 */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* 2. 전체 컨테이너 패딩 제거 및 요소 간 간격(gap) 0으로 설정 */
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 0rem !important;
        padding-bottom: 0rem !important;
        padding-left: 1rem !important;
        padding-right: 1rem !important;
        gap: 0rem !important; /* 요소 사이의 기본 마진 제거 */
    }

    /* 3. 타이틀 마진 및 패딩 제거 */
    .main-title {
        font-size: 1.8rem; 
        font-weight: 800;
        color: #000000;
        text-align: center;
        padding-top: 10px !important;
        padding-bottom: 0px !important;
        margin-bottom: -10px !important; /* 아래 요소와 강제 밀착 */
        letter-spacing: -1px;
    }

    /* 4. stTextInput(검색창) 주변의 모든 여백 제거 */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stTextInput"]) {
        padding-top: 0px !important;
        margin-top: -10px !important;
    }

    .stTextInput { 
        padding-top: 0px !important;
        padding-bottom: 10px !important;
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

    .info-section { 
        flex: 0.8; 
        padding-right: 10px; 
    }
    
    .name-row { display: flex; align-items: baseline; gap: 8px; }
    .name-text { font-weight: 700; font-size: 1.1rem; color: #000; }
    .pos-dept { font-size: 0.95rem; color: #555; }
    .work-text { font-size: 0.85rem; color: #888; margin-top: 2px; line-height: 1.3; }

    .icon-section {
        min-width: 75px; 
        display: flex;
        justify-content: flex-end;
        gap: 15px; 
    }
    
    .icon-link {
        text-decoration: none !important;
        font-size: 1.3rem; 
        font-weight: 700;
        color: #000000 !important;
    }
</style>
""", unsafe_allow_html=True)

# 타이틀
st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 데이터 (중략 - 기존과 동일)
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"8191","mobile":"010-9056-3701","work":"시설 및 자산관리(대학본부, 의생명산업연구원, 성의회관 등)"},
    # ... 나머지 데이터는 동일하므로 생략 ...
]

# 검색 기능 (레이블 제거를 위해 label_visibility="collapsed" 추가)
query = st.text_input("검색", placeholder="성함, 부서 또는 업무 검색...", label_visibility="collapsed")

# 리스트 출력
filtered_data = [
    item for item in data 
    if any(query.lower() in str(val).lower() for val in item.values())
] if query else data

for p in filtered_data:
    ext_val = p.get('ext', '')
    ext_tel = f"023147{ext_val}" if ext_val.isdigit() else ""
    mob_tel = p['mobile'].replace('-', '')
    
    st.markdown(f"""
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
    """, unsafe_allow_html=True)
