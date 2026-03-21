import streamlit as st

# 페이지 설정
st.set_page_config(page_title="성의교정 비상연락망", layout="wide")

# [span_0](start_span)[span_1](start_span)[span_2](start_span)[span_3](start_span)[span_4](start_span)[span_5](start_span)[span_6](start_span)PDF의 모든 데이터를 슬림하게 통합[span_0](end_span)[span_1](end_span)[span_2](end_span)[span_3](end_span)[span_4](end_span)[span_5](end_span)[span_6](end_span)
contacts = [
    {"g": "총무", "n": "박현욱", "p": "팀장", "t": "010-6245-0589", "ext": "8190", "w": "부서업무 총괄"},
    {"g": "총무", "n": "김종래", "p": "차장", "t": "010-9056-3701", "ext": "8191", "w": "시설/자산관리(본관,의산연,성의회관)"},
    {"g": "총무", "n": "장영섭", "p": "차장", "t": "010-5072-0919", "ext": "8193", "w": "예비군, 민방위, 행사"},
    {"g": "총무", "n": "주종호", "p": "과장", "t": "010-3324-1187", "ext": "8202", "w": "보안, 미화, 대관, 게스트하우스"},
    {"g": "총무", "n": "강은희", "p": "대리", "t": "010-9127-1021", "ext": "8206", "w": "직인/문서배부, 행사, 회의"},
    {"g": "총무", "n": "김보라", "p": "선임", "t": "010-8073-0527", "ext": "8192", "w": "명예교수실, 차량등록"},
    {"g": "총무", "n": "노종현", "p": "책임", "t": "010-9425-3109", "ext": "8195", "w": "행사, 회의자료, 예비군사무"},
    {"g": "총무", "n": "고규호", "p": "책임", "t": "010-3381-8870", "ext": "8196", "w": "다이어리, 인증평가, 안전점검"},
    {"g": "안전", "n": "윤호열", "p": "UM", "t": "010-2623-7963", "ext": "8199", "w": "소방/방재, 시설관리(옴니버스 등)"},
    {"g": "안전", "n": "주상건", "p": "차장", "t": "010-9496-6483", "ext": "7135", "w": "시신기증 업무"},
    {"g": "안전", "n": "곽정승", "p": "과장", "t": "010-5218-6504", "ext": "8194", "w": "사업계획, 예산, 주차관리"},
    {"g": "안전", "n": "박일용", "p": "과장", "t": "010-6205-7751", "ext": "8201", "w": "임대차, 사인물, 교원기숙사"},
    {"g": "안전", "n": "이경종", "p": "부장", "t": "010-2623-7963", "ext": "8203", "w": "교수업적평가, 문서분배"},
    {"g": "안전", "n": "김준석", "p": "과장", "t": "010-9256-6904", "ext": "8205", "w": "연구실 안전관리, 출입증"},
    {"g": "비서", "n": "이경자", "p": "부장", "t": "010-6306-3652", "ext": "8071", "w": "의무부총장 비서"},
    {"g": "비서", "n": "이상희", "p": "과장", "t": "010-3445-0623", "ext": "8068", "w": "사무처장 비서"},
    {"g": "시설", "n": "성의상황실", "p": "본관", "t": "02-3147-8000", "ext": "8000", "w": "메인 상황실"},
    {"g": "시설", "n": "통합관제", "p": "지원", "t": "02-2258-5555", "ext": "5555", "w": "통합 관제 센터"},
    {"g": "시설", "n": "전기팀", "p": "지원", "t": "02-2258-5672", "ext": "*1-5672", "w": "전기 시설 관리"},
    {"g": "시설", "n": "설비팀", "p": "지원", "t": "02-2258-5624", "ext": "*1-5624", "w": "설비 시설 관리"},
    {"g": "시설", "n": "영선팀", "p": "지원", "t": "02-2258-5605", "ext": "*1-5605", "w": "영선 시설 관리"}
]

st.title("📞 성의교정 연락망")
search = st.text_input("검색어를 입력하세요", placeholder="이름, 부서, 업무 등")

# 필터링 및 출력
st.markdown("---")
for c in contacts:
    if not search or any(search.lower() in str(v).lower() for v in c.values()):
        tel = c['t'].replace("-", "")
        # 슬림한 한 줄 레이아웃
        st.markdown(f"""
            <div style="border-bottom: 1px solid #eee; padding: 8px 0;">
                <a href="tel:{tel}" style="text-decoration: none; color: black; display: flex; justify-content: space-between;">
                    <div style="flex: 1;">
                        <b>{c['n']}</b> <small style="color: #666;">{c['p']} ({c['g']})</small><br>
                        <span style="font-size: 0.85em; color: #888;">{c['w']}</span>
                    </div>
                    <div style="text-align: right;">
                        <span style="color: #007bff; font-weight: bold;">{c['ext']}</span><br>
                        <small style="color: #999;">{c['t']}</small>
                    </div>
                </a>
            </div>
        """, unsafe_allow_html=True)
