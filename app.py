import streamlit as st
from datetime import datetime

# 1. 데이터 업데이트의 편의성을 위해 딕셔너리 구조로 데이터화
# 나중에는 이 부분을 Google Sheets나 JSON 파일로 대체하면 편리합니다.
menu_data = {
    "2026-03-16(월)": {
        "조식": ["두유스프", "단호박에그마요샌드", "맛살마요범벅", "오리엔탈샐러드"],
        "간편식": ["정보 없음"],
        "중식": ["차돌해물짬뽕밥", "김말이튀김", "그린샐러드", "매실주스"],
        "석식": ["어항가지돈육덮밥", "사골파국", "감자채햄볶음", "망고샐러드"],
        "야식": ["날치알볶음밥", "후랑크소시지", "연근조림", "요구르트"]
    },
    "2026-03-17(화)": {
        "조식": ["제철미나리쭈꾸미연포탕", "매운두부찜", "모둠장아찌", "누룽지"],
        "간편식": ["고로케양배추샌드위치", "삶은계란", "플레인요거트"],
        "중식": ["버섯불고기", "우엉채레몬튀김", "수수기장밥", "얼큰어묵탕", "수정과"],
        "석식": ["양배추멘치카츠", "가쓰오장국", "시저드레싱샐러드", "열무김치"],
        "야식": ["소고기미역죽", "돈육장조림", "블루베리요플레"]
    },
    "2026-03-18(수)": {
        "조식": ["감자수제비", "돈채가지볶음", "양념고추지", "깍두기"],
        "간편식": ["닭가슴살샐러드", "바나나"],
        "중식": ["뼈없는닭볶음탕", "혼합잡곡밥", "유부겨자냉채", "복분자주스"],
        "석식": ["하이디라오마라탕", "탕수육", "짜사이무침", "열무김치"],
        "야식": ["돈사태떡찜", "유채된장국", "멸치볶음", "요구르트"]
    }
}

# 2. 현재 시간 기반 초기값 설정 (로직)
now = datetime.now()
curr_date_str = "2026-03-17(화)" # 테스트용 (실제로는 now.strftime 활용)
curr_hour = now.hour

if curr_hour < 9: initial_meal = "조식"
elif 9 <= curr_hour < 11: initial_meal = "간편식"
elif 11 <= curr_hour < 14: initial_meal = "중식"
elif 14 <= curr_hour < 19: initial_meal = "석식"
else: initial_meal = "야식"

# 3. 사이드바 및 레이아웃 설정
st.set_page_config(page_title="스마트 식단 카드", layout="centered")

# CSS를 활용해 카드 형태의 가독성 극대화
st.markdown("""
    <style>
    .meal-card {
        background-color: #ffffff;
        padding: 20px;
        border-radius: 15px;
        border: 1px solid #e1e4e8;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .main-menu { color: #d32f2f; font-weight: bold; font-size: 1.2em; }
    .side-menu { color: #555555; font-size: 0.9em; }
    .badge { background-color: #ff4b4b; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7em; }
    </style>
""", unsafe_allow_html=True)

st.title("🍱 Daily Menu Card")

# 상단 인터페이스: 날짜와 식사 시간 선택
col1, col2 = st.columns([1, 1])
with col1:
    selected_date = st.selectbox("📅 날짜 선택", list(menu_data.keys()), index=1)
with col2:
    selected_meal = st.radio("⏰ 식사 구분", ["조식", "간편식", "중식", "석식", "야식"], 
                             index=["조식", "간편식", "중식", "석식", "야식"].index(initial_meal), 
                             horizontal=True)

st.divider()

# 4. 카드 렌더링 (선택된 식단이 무조건 가장 위에 노출됨)
meal_list = ["조식", "간편식", "중식", "석식", "야식"]

# 선택된 메뉴 먼저 출력 (가장 큰 카드)
target_menu = menu_data[selected_date].get(selected_meal, ["정보가 없습니다."])
st.markdown(f"""
    <div class="meal-card" style="border-left: 8px solid #ff4b4b;">
        <span class="badge">NOW SELECT</span>
        <h3>{selected_meal}</h3>
        <p class="main-menu">🍲 {target_menu[0]}</p>
        <p class="side-menu">{', '.join(target_menu[1:])}</p>
    </div>
""", unsafe_allow_html=True)

# 나머지 메뉴들을 아래에 배치
st.subheader("나머지 식단")
for meal in meal_list:
    if meal != selected_meal:
        other_menu = menu_data[selected_date].get(meal, ["정보가 없습니다."])
        with st.expander(f"{meal} 식단 확인"):
            st.markdown(f"**{other_menu[0]}**")
            st.caption(", ".join(other_menu[1:]))
