import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 비상연락망", layout="wide")

# 2. 데이터 통합 (CSV 파일 대신 코드 내에 직접 삽입)
@st.cache_data
def get_integrated_data():
    data = [
        [span_0](start_span)# PDF 데이터를 바탕으로 구성
        {"구분": "인원", "이름": "박현욱", "직책": "팀장", "연락처": "010-6245-0589", "표기": "010-6245-0589", "업무": "부서업무 총괄[span_0](end_span)"},
        [span_1](start_span){"구분": "인원", "이름": "김종래", "직책": "차장", "연락처": "010-9056-3701", "표기": "010-9056-3701", "업무": "시설 및 자산 관리(대학본관, 의산연, 성의회관 등)[span_1](end_span)"},
        [span_2](start_span){"구분": "인원", "이름": "장영섭", "직책": "차장", "연락처": "010-5072-0919", "표기": "010-5072-0919", "업무": "예비군, 민방위, 병무행정, 행사[span_2](end_span)"},
        [span_3](start_span){"구분": "인원", "이름": "주종호", "직책": "과장", "연락처": "010-3324-1187", "표기": "010-3324-1187", "업무": "보안, 미화, 대관, 게스트하우스[span_3](end_span)"},
        [span_4](start_span){"구분": "인원", "이름": "윤호열", "직책": "UM", "연락처": "010-2623-7963", "표기": "010-2623-7963", "업무": "소방/방재, 시설관리(옴니버스, 기숙사 등)[span_4](end_span)"},
        [span_5](start_span){"구분": "인원", "이름": "곽정승", "직책": "과장", "연락처": "010-5218-6504", "표기": "010-5218-6504", "업무": "사업계획, 예산, 주차/차량관리[span_5](end_span)"},
        [span_6](start_span){"구분": "인원", "이름": "박일용", "직책": "과장", "연락처": "010-6205-7751", "표기": "010-6205-7751", "업무": "계약(임대차, 용역), 교원기숙사[span_6](end_span)"},
        [span_7](start_span){"구분": "인원", "이름": "이규용", "직책": "보안소장", "연락처": "010-8883-6580", "표기": "010-8883-6580", "업무": "보안 총괄[span_7](end_span)"},
        [span_8](start_span){"구분": "인원", "이름": "신성휴", "직책": "미화소장", "연락처": "010-7161-2201", "표기": "010-7161-2201", "업무": "미화 총괄[span_8](end_span)"},
        [span_9](start_span){"구분": "시설", "이름": "전기팀", "직책": "지원", "연락처": "02-2258-5672", "표기": "*1-5672", "업무": "전기 시설 관리[span_9](end_span)"},
        [span_10](start_span){"구분": "시설", "이름": "설비팀", "직책": "지원", "연락처": "02-2258-5624", "표기": "*1-5624", "업무": "설비 시설 관리[span_10](end_span)"},
        [span_11](start_span){"구분": "시설", "이름": "영선팀", "직책": "지원", "연락처": "02-2258-5605", "표ig": "*1-5605", "업무": "영선 시설 관리[span_11](end_span)"},
        [span_12](start_span){"구분": "시설", "이름": "통합관제", "직책": "상황실", "연락처": "02-2258-5555", "표기": "2258-5555", "업무": "재난/보안 통합 관제[span_12](end_span)"},
        [span_13](start_span){"구분": "시설", "이름": "성의교정상황실", "직책": "본관", "연락처": "02-3147-8000", "표기": "3147-8000", "업무": "교정 메인 상황실[span_13](end_span)"},
        [span_14](start_span){"구분": "시설", "이름": "옴니버스파크", "직책": "건물", "연락처": "02-3147-8500", "표기": "8500", "업무": "옴니버스파크 안내[span_14](end_span)"},
    ]
    return pd.DataFrame(data)

df = get_integrated_data()

# 3. UI 구성
st.title("📱 성의교정 비상연락망")
search = st.text_input("🔍 이름 또는 업무 검색", placeholder="예: 보안, 박현욱, 전기")

# 4. 검색 로직 (대소문자 무시 및 공백 제거 검색)
if search:
    q = search.strip()
    mask = (
        df['이름'].str.contains(q, na=False) | 
        df['업무'].str.contains(q, na=False) |
        df['구분'].str.contains(q, na=False)
    )
    display_df = df[mask]
else:
    display_df = df

# 5. 리스트 출력
if display_df.empty:
    st.info("검색 결과가 없습니다.")
else:
    for _, row in display_df.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"### {row['이름']} <small>{row['직책']}</small>", unsafe_allow_html=True)
                st.write(f"📞 {row['표기']}")
                st.caption(f"💡 {row['업무']}")
            with col2:
                # 전화번호에서 하이픈 제거 후 tel 링크 생성
                clean_phone = row['연락처'].replace("-", "")
                st.markdown(f"""
                    <a href="tel:{clean_phone}" style="text-decoration:none;">
                        <div style="background-color:#28a745; color:white; text-align:center; padding:15px; border-radius:10px; font-weight:bold; margin-top:15px;">
                            연결
                        </div>
                    </a>
                """, unsafe_allow_html=True)
            st.divider()
