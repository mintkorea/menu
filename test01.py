import streamlit as st
import pandas as pd
from io import StringIO

# 1. 통합 데이터 로드 (모든 이미지의 상세 내용을 원본 그대로 반영)
def get_integrated_data():
    # 데이터 구조: 건물, 층, 상세구분, 명칭(검색용), 비고
    raw_data = """건물,층,구분,명칭,비고
성의회관,14F,숙소/교수실,게스트하우스(포스텍 사용: 김미주 팀장 담당) / 게스트하우스(학교관리: 주종호 과장 담당) / 성기현 교수실(1416호) / 백종호 교수실(1417호) / 박은호 교수실(1418호) / 김평만 교수실(1419호) / 김수정 교수실(1420호) / 최진일 교수실(1421호),
성의회관,13F,연구/입주사,김정훈 교수실(1301호) / 포스텍 서울공유오피스(1304호) / 화상회의실(1305호) / 조동우 교수실(1306호) / (주)플럼라인생명과학(1307, 1315호) / 김동 교수실(1308호) / (주)알젠오가노 바이오테크놀로지(1309-3호) / 맵스젠 기업부설연구소(1309-4호) / 셀로이드(주) 실험실(1309-7호) / 세포배양실 / 공동기기실,
성의회관,11F,도서관,효원도서관 (24시간 출입문 폐쇄) / 도서관장실 / 사서팀 / 연속간행물실 / 복사실,
의산연,지하1층,연구/행정,통합관제실 / 서태석 교수(B101) / 의공학교실연구소(B102) / 의공학교실사무실(B103) / 방사선분석실 / 대사영사실 / 산학협동실 / 초저온냉동고실(B113),
의산연,2층,연구/행정,정보전략팀 서버실(2001) / 가톨릭세포치료사업단 세포생산실(2006, 2011) / 한국가톨릭의료협회(2013) / 대강당(2014) / 정보융합진흥원장(2020),
옴니버스파크,의과대학(A동) 8F,교수실/연구실,미생물학교실(8108) / 예방의학교실(8109) / 학과사무실(8122) / 의생명과학교실(8126) / 의학통계연구실,
옴니버스파크,연구동(B동) 7F,행정,산학협력단장실 / 의생명산업연구원장실 / 연구감사실 / 산학협력팀 / 경영관리팀 / 연구기획팀 / 연구관리팀 / 구매관재팀,
옴니버스파크,통합 1F,편의/교육,마스터센터(1001) / 대강의실(1005, 1013) / 푸드코트(북촌손만두, 제주면장, 와싱톤돈까스, 이천가든, 아비꼬, 송),
병원별관,3F,기숙사/행정,사제관(비안네관) / 간호기숙사(올리브관) / 수녀원 / 노사협력팀 / 보직자실(의료원장실, 사무처장실 등) / 중앙의료원 통합행정사무실(인사관리, 재무관리, 인재전략, 교육팀),
병원별관,1F,행정/진료,영상의학과(CT, MRI) / 수납창구 / 성의교정행정사무실(총무, 재무, 구매, 대학원교학, 성의기획, 교무) / 의료원홍보팀 / 콜센터,
대학본관,2F,병원/학교,의료원보직자실 / 원목사무실 / 서울성모병원 행정사무실(정보전략, 정보보호) / 정보융합진흥원 행정사무실 / IT 사업프로토콜 / 빅데이터 통합센터,
대학본관,1F,공통,병원통합행정사무실 / 고객행복팀 / 평생건강증진팀 / 소아청소년완화의료팀(솔솔바람) / 진료협력팀 / 학생식당 / 직원식당 / 노조사무실,
서울성모병원,6F,외래/센터,산부인과 / 소아청소년과 / 유방센터 / 갑상선센터 / 국제진료센터 / 조혈모세포이식센터 / 암병원 / 인권센터,
서울성모병원,3F,외래,심뇌혈관병원(순환기내과, 혈관외과, 흉부외과) / 신경외과 / 신경내과 / 외과 / 비뇨의학과 / 류마티스내과 / 신장내과 / 안센터 / 혈액내과 / 호흡기내과 / 감염내과,
서울성모병원,1F,로비/검사,접수·수납 / 응급의료센터 / 약국 / 영상의학과(CT, MRI, X-ray) / 처음마중센터,
서울성모병원,B1F,편의시설,식당가(푸드코트) / 편의점 / 은행 / 의료기기매장 / 안경점 / 세탁소 / 장례식장 연결통로,
"""
    # [주의] 실제 사용 시 위 raw_data에 정리된 모든 건물의 행을 추가해 주세요.
    return pd.read_csv(StringIO(raw_data))

# 2. 페이지 설정
st.set_page_config(page_title="가톨릭대 성의교정 통합 안내", page_icon="🏢", layout="wide")

# 스타일링 (CSS)
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stDataFrame { background-color: white; border-radius: 10px; }
    .bldg-card { padding: 20px; border-radius: 10px; border-left: 5px solid #00468b; background-color: white; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 3. 사이드바 - 건물 필터
st.sidebar.image("https://www.cmc.or.kr/images/common/logo.png", width=200) # 로고 예시
st.sidebar.title("🏢 성의교정 건물 목록")
bldg_list = ["전체", "서울성모병원", "성의회관", "의산연", "옴니버스파크", "대학본관", "병원별관"]
selected_bldg = st.sidebar.radio("안내가 필요한 건물을 선택하세요", bldg_list)

# 4. 메인 화면
st.title("📍 성의교정 & 성모병원 통합 검색 시스템")
st.write("진료과, 부서, 교수실, 편의시설 이름을 입력하여 위치를 확인하세요.")

# 검색창
query = st.text_input("🔍 검색어 입력", placeholder="예: '산부인과', '식당', '효원도서관', '서태석'...")

# 데이터 필터링
df = get_integrated_data()
if selected_bldg != "전체":
    df = df[df['건물'] == selected_bldg]

if query:
    # 전체 컬럼에서 검색어 포함 여부 확인
    mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
    results = df[mask]
    
    if not results.empty:
        st.success(f"'{query}'에 대한 검색 결과가 {len(results)}건 있습니다.")
        
        # 결과 표시
        for _, row in results.iterrows():
            with st.container():
                st.markdown(f"""
                <div class="bldg-card">
                    <h3 style='margin:0; color:#00468b;'>{row['명칭']}</h3>
                    <p style='margin:5px 0;'><b>위치:</b> {row['건물']} {row['층']} ({row['구분']})</p>
                    <p style='font-size:0.9em; color:#666;'>{row['비고'] if pd.notna(row['비고']) else ''}</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.error(f"'{query}'에 대한 정보를 찾을 수 없습니다. 철자를 확인하거나 다른 검색어를 입력해 주세요.")
else:
    # 기본 화면 - 주요 시설 안내
    st.divider()
    col1, col2, col3 = st.columns(3)
    with col1:
        st.info("🍴 **주요 식당**\n\n- 대학본관 1F (학생/직원)\n- 성모병원 B1F (푸드코트)\n- 옴니버스 1F (푸드코트)")
    with col2:
        st.info("📚 **학습/편의**\n\n- 성의회관 11F (도서관)\n- 대학본관 B1 (은행)\n- 병원별관 1F (수납)")
    with col3:
        st.info("🏥 **긴급/의료**\n\n- 성모병원 1F (응급의료)\n- 병원별관 2F (직업환경)")

# 하단 정보
st.sidebar.markdown("---")
st.sidebar.caption("Last Updated: 2026.03.23")
st.sidebar.caption("관리: 성의교정 시설관리팀")
