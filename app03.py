import streamlit as st

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 연락망", layout="wide")

# 2. 여백 최적화 CSS
st.markdown("""
<style>
    /* 1. 상단 투명 헤더 제거 */
    header[data-testid="stHeader"] {
        display: none !important;
    }

    /* 2. 전체 컨테이너 여백 조정 (타이틀이 안 잘리도록 상단 1rem 확보) */
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        gap: 0rem !important; /* 위젯 간 간격 제거 */
    }

    /* 3. 타이틀 스타일: 잘림 방지를 위해 마진 대신 패딩 사용 */
    .main-title {
        font-size: 1.8rem; 
        font-weight: 800;
        color: #000000;
        text-align: center;
        line-height: 1.2;      /* 줄 간격 확보로 잘림 방지 */
        margin: 0px !important;
        padding-top: 5px !important;
        padding-bottom: 5px !important;
    }

    /* 4. 검색창(stTextInput) 여백 제거 */
    /* 위젯 자체의 패딩과 상단 라벨 공간 삭제 */
    div[data-testid="stVerticalBlock"] > div:has(div[data-testid="stTextInput"]) {
        padding-top: 0px !important;
    }
    
    .stTextInput { 
        margin-top: -5px !important; /* 타이틀과 더 밀착 */
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

# 타이틀 표시
st.markdown('<div class="main-title">비상연락망</div>', unsafe_allow_html=True)

# 데이터 (예시 일부)
data = [
    {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
    {"dept":"총무팀","name":"김종래","pos":"차장","ext":"8191","mobile":"010-9056-3701","work":"시설 및 자산관리"},
]

# 검색창: label_visibility="collapsed"로 라벨 공간까지 완전히 제거
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
