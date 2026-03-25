import streamlit as st

# 1. 페이지 설정 및 디자인 최적화
st.set_page_config(page_title="성의교정 연락망", layout="wide")

st.markdown("""
<style>
    /* 전체 배경 및 폰트 설정 */
    .block-container { padding-top: 1rem; }
    
    /* 카드 스타일: 모바일에서도 깔끔하게 보이도록 설정 */
    .contact-card {
        background: #ffffff;
        padding: 15px;
        border-radius: 12px;
        margin-bottom: 15px;
        border: 1px solid #eee;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* ⭐ 별표와 이름을 강제로 한 줄에 배치 (Flexbox) */
    .header-row {
        display: flex;
        align-items: center;
        gap: 12px;
        margin-bottom: 8px;
    }

    .name-text { font-weight: 700; font-size: 1.15rem; color: #111; margin: 0; }
    .pos-text { font-size: 0.9rem; color: #666; font-weight: normal; }
    .work-text { font-size: 0.85rem; color: #888; margin-top: 4px; padding-left: 2px; }

    /* 하단 버튼 그룹: 내선/휴대폰 가로 배치 */
    .btn-group { display: flex; gap: 10px; margin-top: 12px; }
    .tel-link {
        flex: 1;
        text-align: center;
        padding: 10px 0;
        border-radius: 8px;
        font-size: 0.9rem;
        text-decoration: none !important;
        font-weight: 600;
        border: 1px solid #ddd;
    }
    .btn-ext { background: #fdfdfd; color: #333 !important; }
    .btn-mob { background: #007bff; color: white !important; border-color: #007bff; }

    /* 스트림릿 기본 버튼 투명화 (별표용) */
    div[data-testid="stColumn"] button {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        color: #ffc107 !important;
        font-size: 24px !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# 2. 데이터 (업무 내용 상세 반영)
def get_data():
    return [
        {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
        {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리 (대학본관, 의산연, 성의회관 등)"},
        {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군대대장, 민방위, 병무행정, ITC 등"},
        {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 미화, 대관, 게스트하우스, 인체유래물은행"},
        {"dept":"총무팀","name":"강은희","pos":"대리","ext":"02-3147-8206","mobile":"010-9127-1021","work":"의료원 직인/문서배부, 행사, 회의 지원"},
        {"dept":"총무팀","name":"김보라","pos":"선임","ext":"02-3147-8192","mobile":"010-8073-0527","work":"명예교수실 점검 및 관리, 차량등록, 부서운영비"},
        {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방/방재 인증평가, 시설관리 (옴니버스파크 등)"},
        {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증 업무 총괄"},
        {"dept":"비서실","name":"이경자","pos":"부장","ext":"02-3147-8071","mobile":"010-6306-3652","work":"의무부총장, 기획조정실장 비서"},
    ]

# 3. 로직 및 상태 관리
if "fav" not in st.session_state:
    st.session_state.fav = set()

data = get_data()

# 검색 인터페이스
c1, c2 = st.columns([4, 1])
with c1:
    q = st.text_input("🔍 이름/부서/업무 검색", placeholder="예: 보안, 예비군, 시신")
with c2:
    only_fav = st.checkbox("⭐")

# 필터링
filtered = data
if q:
    s = q.lower()
    filtered = [x for x in filtered if any(s in str(v).lower() for v in x.values())]
if only_fav:
    filtered = [x for x in filtered if x["name"] in st.session_state.fav]

st.caption(f"검색 결과: {len(filtered)}명")

# 4. 리스트 출력 (모바일 최적화 레이아웃)
for i, c in enumerate(filtered):
    is_f = c["name"] in st.session_state.fav
    star = "★" if is_f else "☆"
    
    st.markdown('<div class="contact-card">', unsafe_allow_html=True)
    
    # 별표와 이름을 강제로 가로 정렬하기 위한 컬럼 (간격 최소화)
    col_star, col_name = st.columns([0.15, 0.85])
    with col_star:
        if st.button(star, key=f"f_{i}"):
            if is_f: st.session_state.fav.remove(c["name"])
            else: st.session_state.fav.add(c["name"])
            st.rerun()
            
    with col_name:
        st.markdown(f'<p class="name-text">{c["name"]} <span class="pos-text">{c["pos"]} · {c["dept"]}</span></p>', unsafe_allow_html=True)
    
    # 업무 내용 표시
    st.markdown(f'<div class="work-text">{c["work"]}</div>', unsafe_allow_html=True)
    
    # 하단 버튼 (전화 연결)
    ext_link = f"tel:{c['ext'].replace('-', '')}"
    mob_link = f"tel:{c['mobile'].replace('-', '')}"
    
    st.markdown(f"""
        <div class="btn-group">
            {"<a href='"+ext_link+"' class='tel-link btn-ext'>내선 연결</a>" if c['ext'] != "-" else ""}
            <a href="{mob_link}" class="tel-link btn-mob">휴대폰 연결</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
