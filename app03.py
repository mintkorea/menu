import streamlit as st

# 1. 페이지 설정 및 디자인 최적화
st.set_page_config(page_title="성의교정 연락망", layout="wide")

st.markdown("""
<style>
    .block-container { padding-top: 1rem; }
    
    /* 카드 전체 레이아웃 */
    .contact-card {
        background: #ffffff;
        padding: 14px;
        border-radius: 12px;
        margin-bottom: 12px;
        border: 1px solid #eee;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }

    /* 별표와 이름을 한 줄로 고정 (모바일에서도 유지) */
    .name-row {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 6px;
    }

    .name-text { font-weight: 700; font-size: 1.1rem; color: #111; }
    .pos-text { font-size: 0.85rem; color: #777; }
    .work-text { font-size: 0.85rem; color: #888; padding-left: 2px; line-height: 1.4; }

    /* 버튼 그룹 레이아웃 */
    .btn-group { display: flex; gap: 8px; margin-top: 10px; }
    .tel-link {
        flex: 1;
        text-align: center;
        padding: 8px 0;
        background: #f8f9fa;
        border-radius: 8px;
        font-size: 0.85rem;
        text-decoration: none !important;
        color: #333 !important;
        font-weight: 600;
        border: 1px solid #eee;
    }

    /* ⭐ 버튼 투명화 및 정렬 */
    div[data-testid="stHorizontalBlock"] button {
        border: none !important;
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        color: #ffc107 !important;
        font-size: 22px !important;
        line-height: 1;
    }
</style>
""", unsafe_allow_html=True)

st.title("📞 성의교정 비상연락망")

# ---------------- 데이터 (이미지 텍스트 완벽 반영) ----------------
def get_data():
    return [
        {"dept":"총무팀","name":"박현욱","pos":"팀장","ext":"02-3147-8190","mobile":"010-6245-0589","work":"부서업무 총괄"},
        {"dept":"총무팀","name":"김종래","pos":"차장","ext":"02-3147-8191","mobile":"010-9056-3701","work":"시설 및 자산관리 (대학본관, 의산연, 성의회관 등)"},
        {"dept":"총무팀","name":"장영섭","pos":"차장","ext":"02-3147-8193","mobile":"010-5072-0919","work":"예비군대대장, 민방위, 병무행정, 행사, ITC, 기타서무"},
        {"dept":"총무팀","name":"주종호","pos":"과장","ext":"02-3147-8202","mobile":"010-3324-1187","work":"보안, 미화, 대관, 게스트하우스, 인체유래물은행"},
        {"dept":"총무팀","name":"강은희","pos":"대리","ext":"02-3147-8206","mobile":"010-9127-1021","work":"의료원 직인/문서배부, 월례조회, 행사, 회의"},
        {"dept":"총무팀","name":"김보라","pos":"선임","ext":"02-3147-8192","mobile":"010-8073-0527","work":"명예교수실 점검 및 관리, 차량등록, 부서운영비"},
        {"dept":"총무팀","name":"노종현","pos":"책임","ext":"02-3147-8195","mobile":"010-9425-3109","work":"행사, 회의자료취합, 단위기관장회의, 예비군대대"},
        {"dept":"총무팀","name":"고규호","pos":"책임","ext":"02-3147-8196","mobile":"010-3381-8870","work":"캘린더/다이어리, 인증평가, 대학정보공시, 안전점검"},
        {"dept":"총무팀","name":"김두리","pos":"사원","ext":"02-3147-8204","mobile":"010-9661-1257","work":"성의기숙사 사감"},
        {"dept":"총무팀","name":"임세리","pos":"사원","ext":"02-3147-8197","mobile":"010-3281-1229","work":"우편, 물품/비품청구, 정수기관리, 정보보호"},
        {"dept":"총무팀","name":"김종식","pos":"사원","ext":"-","mobile":"010-9256-6904","work":"업무지원"},
        {"dept":"안전관리","name":"윤호열","pos":"UM","ext":"02-3147-8199","mobile":"010-2623-7963","work":"소방/방재 인증평가, 시설관리 (옴니버스파크 등)"},
        {"dept":"안전관리","name":"주상건","pos":"차장","ext":"02-2258-7135","mobile":"010-9496-6483","work":"시신기증 업무"},
        {"dept":"안전관리","name":"곽정승","pos":"과장","ext":"02-3147-8194","mobile":"010-5218-6504","work":"사업계획, 예산, 주차/차량관리"},
        {"dept":"안전관리","name":"박일용","pos":"과장","ext":"02-3147-8201","mobile":"010-6205-7751","work":"계약(임대차, 용역 등), 사인물관리, 교원기숙사"},
        {"dept":"안전관리","name":"이경종","pos":"부장","ext":"02-3147-8203","mobile":"010-2623-7963","work":"교수업적평가, 문서분배, 그룹웨어 ITC"},
        {"dept":"안전관리","name":"김준석","pos":"과장","ext":"02-3147-8205","mobile":"010-9256-6904","work":"연구실 안전관리, 출입증등록, 기타서무"},
        {"dept":"비서실","name":"이경자","pos":"부장","ext":"02-3147-8071","mobile":"010-6306-3652","work":"의무부총장, 기획조정실장 비서"},
        {"dept":"비서실","name":"이상희","pos":"과장","ext":"02-3147-8068","mobile":"010-3445-0623","work":"영성구현실장, 사무처장 비서"},
        {"dept":"비서실","name":"박은영","pos":"과장","ext":"02-3147-8069","mobile":"010-5348-6849","work":"의과대학장 비서"},
    ]

# ---------------- 로직 및 상태 ----------------
if "fav" not in st.session_state:
    st.session_state.fav = set()

data = get_data()

c1, c2 = st.columns([3, 1])
with c1:
    q = st.text_input("🔍 이름/부서/업무 검색", placeholder="예: 보안, 예비군, 시신")
with c2:
    only_fav = st.checkbox("⭐")

filtered = data
if q:
    s = q.lower()
    filtered = [x for x in filtered if any(s in str(v).lower() for v in x.values())]
if only_fav:
    filtered = [x for x in filtered if x["name"] in st.session_state.fav]

st.caption(f"검색 결과: {len(filtered)}명")

# ---------------- 리스트 출력 ----------------
for i, c in enumerate(filtered):
    is_f = c["name"] in st.session_state.fav
    star = "★" if is_f else "☆"
    
    st.markdown('<div class="contact-card">', unsafe_allow_html=True)
    
    # 별표와 이름을 강제로 한 줄에 배치하기 위해 st.columns의 간격을 최소화
    col_fav, col_name = st.columns([0.1, 0.9])
    with col_fav:
        if st.button(star, key=f"f_{i}"):
            if is_f: st.session_state.fav.remove(c["name"])
            else: st.session_state.fav.add(c["name"])
            st.rerun()
    with col_name:
        st.markdown(f'<div class="name-text">{c["name"]} <span class="pos-text">{c["pos"]} · {c["dept"]}</span></div>', unsafe_allow_html=True)
    
    # 업무 내용
    st.markdown(f'<div class="work-text">{c["work"]}</div>', unsafe_allow_html=True)
    
    # 하단 버튼 (내선, 휴대폰)
    ext_link = f"tel:{c['ext'].replace('-', '')}"
    mob_link = f"tel:{c['mobile'].replace('-', '')}"
    
    st.markdown(f"""
        <div class="btn-group">
            {"<a href='"+ext_link+"' class='tel-link'>내선 연결</a>" if c['ext'] != "-" else ""}
            <a href="{mob_link}" class="tel-link" style="background:#007bff; color:white !important;">휴대폰 연결</a>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
