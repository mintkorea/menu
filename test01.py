import streamlit as st
import pandas as pd

# 1. 데이터 설정 (CSV 문자열 형태)
csv_data = """층,호수,명칭,비고
14F,1404호~1410호,게스트하우스 (포스텍 사용),기숙사 개념 (김미주 팀장 담당)
14F,1413호~1421호,게스트하우스 (학교관리),개인사용 개념 (총무팀 주종호 과장 담당)
14F,1416호,성기현 교수실,게스트하우스
14F,1417호,백종호 교수실,게스트하우스
14F,1418호,박은호 교수실,게스트하우스
14F,1419호,김평만 교수실,게스트하우스
14F,1420호,김수정 교수실,게스트하우스
14F,1421호,최진일 교수실,게스트하우스
13F,1301호,김정훈 교수실,
13F,1304호,포스텍 서울공유오피스,
13F,1307호,(주)플럼라인생명과학,
12F,1217호,윤승규 교수(부원장실),
11F,-,효원도서관,24시간 출입문 폐쇄
10F,-,효원도서관,20:00 시간 통제
9F,-,강한성열람실,24시간 개방 및 휴게실
8F,-,START 의학시뮬레이션센터,시뮬레이션교육실
1F,-,로비,마리아홀/써니문구/매점/커피숍
"""
# (실제 운영 시에는 별도의 CSV 파일을 로드하도록 처리 가능)
from io import StringIO
df = pd.read_csv(StringIO(csv_data))

# 2. 페이지 설정
st.set_page_config(page_title="성의회관 안내 시스템", page_icon="🏢")

st.title("🏢 성의회관 입주현황 안내")
st.markdown("찾으시는 **부서, 교수실 또는 시설명**을 입력하세요.")

# 3. 검색 기능
search_query = st.text_input("🔍 검색어 입력 (예: 교수실, 도서관, 14F)", placeholder="검색어를 입력하세요...")

if search_query:
    # 명칭, 층, 호수, 비고 전체에서 검색어 포함 여부 확인
    mask = df.apply(lambda row: row.astype(str).str.contains(search_query, case=False).any(), axis=1)
    result = df[mask]

    if not result.empty:
        st.success(f"총 {len(result)}건의 결과를 찾았습니다.")
        
        # 결과 출력 (카드 형태)
        for _, row in result.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 4])
                col1.metric("위치", row['층'])
                with col2:
                    st.subheader(f"{row['명칭']}")
                    st.write(f"📍 **호수:** {row['호수']} | 📝 **비고:** {row['비고'] if pd.notna(row['비고']) else '-'}")
                st.divider()
    else:
        st.warning("검색 결과가 없습니다. 철자를 확인해 주세요.")

# 4. 층별 전체 보기 (사이드바)
st.sidebar.header("층별 전체 보기")
floor_list = sorted(df['층'].unique(), reverse=True)
selected_floor = st.sidebar.selectbox("층을 선택하세요", ["전체"] + floor_list)

if selected_floor != "전체":
    st.subheader(f"📍 {selected_floor} 입주 현황")
    st.table(df[df['층'] == selected_floor][['호수', '명칭', '비고']])

st.sidebar.info("본 시스템은 내방객 편의를 위해 제공됩니다.")
