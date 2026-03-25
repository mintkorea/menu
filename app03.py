import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 여백 및 간격 정밀 조정 CSS
st.markdown("""
<style>
    /* 1. 상단 바(헤더) 공간을 완전히 제거하고 위로 밀착 */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    
    /* 2. 메인 컨테이너의 상단 패딩을 0으로 고정 (최상단 여백 제거) */
    [data-testid="stMainBlockContainer"], 
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 0.5rem !important; /* 약간의 숨통만 틔우고 거의 밀착 */
        padding-bottom: 0rem !important;
        gap: 0rem !important;
    }

    /* 3. 타이틀 설정: 잘림 방지 및 아래 여백 조정 */
    .main-title {
        font-size: 1.8rem; 
        font-weight: 800;
        color: #000;
        text-align: center;
        line-height: 1.4;      /* 잘림 방지를 위해 행간 확보 */
        margin-top: 0px !important;
        margin-bottom: 5px !important; /* 타이틀과 검색창 사이 간격 */
        padding: 0px !important;
    }

    /* 4. 검색창 위아래 여백을 항목 간격(약 12px) 수준으로 조정 */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stTextInput"]) {
        padding-top: 5px !important;  /* 타이틀 바로 아래 여백 */
        padding-bottom: 12px !important; /* 검색창과 첫 항목(박현욱) 사이 여백 */
    }

    .stTextInput { 
        margin: 0px !important;
    }

    .stTextInput input {
        border-radius: 4px !important;
        border: 1px solid #cccccc !important;
        height: 42px !important;
    }

    /* 연락처 카드 (항목 간 간격) */
    .contact-card {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 12px 0px; /* 항목 위아래 여백 */
        border-bottom: 1px solid #eeeeee;
    }

    .info-section { flex: 0.8; padding-right: 10px; }
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

# 타이틀 출력
st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 데이터 (검색 확인용)
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"8191","mobile":"010-9056-3701","work":"시설 및 자산관리"},
]

# 검색창 (라벨 공간 제거)
query = st.text_input("search", placeholder="성함, 부서 또는 업무 검색...", label_visibility="collapsed")

# 리스트 출력
for p in data:
    if query and not any(query.lower() in str(val).lower() for val in p.values()):
        continue
        
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
