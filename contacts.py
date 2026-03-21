import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="성의교정 비상연락망", layout="wide")

# 2. 데이터 (코드 내 직접 포함)
@st.cache_data
def load_all_data():
    data = [
        [span_1](start_span){"구분": "인원", "이름": "박현욱", "직책": "팀장", "연락처": "010-6245-0589", "표기": "010-6245-0589", "업무": "부서업무 총괄[span_1](end_span)"},
        [span_2](start_span){"구분": "인원", "이름": "주종호", "직책": "과장", "연락처": "010-3324-1187", "표기": "010-3324-1187", "업무": "보안, 미화, 대관, 게스트하우스[span_2](end_span)"},
        [span_3](start_span){"구분": "인원", "이름": "윤호열", "직책": "UM", "연락처": "010-2623-7963", "표기": "010-2623-7963", "업무": "소방/방재, 시설/자산관리[span_3](end_span)"},
        [span_4](start_span){"구분": "인원", "이름": "곽정승", "직책": "과장", "연락처": "010-5218-6504", "표기": "010-5218-6504", "업무": "사업계획, 예산, 주차관리[span_4](end_span)"},
        [span_5](start_span){"구분": "인원", "이름": "이규용", "직책": "보안소장", "연락처": "010-8883-6580", "표기": "010-8883-6580", "업무": "보안 총괄[span_5](end_span)"},
        [span_6](start_span){"구분": "인원", "이름": "신성휴", "직책": "미화소장", "연락처": "010-7161-2201", "표기": "010-7161-2201", "업무": "미화 총괄[span_6](end_span)"},
        [span_7](start_span){"구분": "시설", "이름": "전기팀", "직책": "지원", "연락처": "02-2258-5672", "표기": "*1-5672", "업무": "전기 시설 관리[span_7](end_span)"},
        [span_8](start_span){"구분": "시설", "이름": "설비팀", "직책": "지원", "연락처": "02-2258-5624", "표기": "*1-5624", "업무": "설비 시설 관리[span_8](end_span)"},
        [span_9](start_span){"구분": "시설", "이름": "통합관제", "직책": "상황실", "연락처": "02-2258-5555", "표ig": "2258-5555", "업무": "재난/보안 통합 관제[span_9](end_span)"},
        [span_10](start_span){"구분": "시설", "이름": "성의교정상황실", "직책": "본관", "연락처": "02-3147-8000", "표기": "3147-8000", "업무": "교정 메인 상황실[span_10](end_span)"}
    ]
    return pd.DataFrame(data)

df = load_all_data()

# 3. UI 구성
st.title("📱 성의교정 비상연락망")
search = st.text_input("🔍 이름이나 업무를 검색하세요", placeholder="예: 보안, 박현욱, 전기")

# 4. 검색 로직
if search:
    q = search.strip()
    mask = (df['이름'].str.contains(q, na=False) | df['업무'].str.contains(q, na=False))
    display_df = df[mask]
else:
    display_df = df

# 5. 출력
for _, row in display_df.iterrows():
    with st.container():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"### {row['이름']} <small>{row['직책']}</small>", unsafe_allow_html=True)
            st.write(f"📞 {row['표기']}")
            st.caption(f"💡 {row['업무']}")
        with col2:
            st.markdown(f'''<a href="tel:{row['연락처'].replace("-", "")}" style="text-decoration:none;">
                            <div style="background-color:#28a745; color:white; text-align:center; padding:15px; border-radius:10px; font-weight:bold; margin-top:10px;">연결</div>
                         </a>''', unsafe_allow_html=True)
        st.divider()
