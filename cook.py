import streamlit as st
import pandas as pd

# 페이지 설정
st.set_page_config(layout="wide", page_title="AI Personal Recipe Book")

# 사이드바 메뉴
st.sidebar.title("👨‍🍳 레시피 매니저")
menu = st.sidebar.radio("메뉴 선택", ["레시피 비교 및 생성", "나만의 레시피북 열람"])

# 샘플 데이터 (나중에 DB나 파일로 대체 가능)
if 'my_recipes' not in st.session_state:
    st.session_state.my_recipes = {
        "인생 잡채": {
            "tags": "잔치음식, 한식",
            "difficulty": "보통",
            "time": "40분",
            "ingredients": ["당면 250g", "돼지고기 100g", "시금치 1단", "양파 1/2개", "진간장 5T", "설탕 2T", "참기름 2T"],
            "steps": [
                "당면은 끓는 물에 11분간 삶아 건져둔다 (백종원 팁).",
                "고기와 버섯은 간장, 설탕으로 밑간을 미리 한다 (김수미 팁).",
                "야채를 각각 볶아 식힌 후 모든 재료를 볼에서 버무린다."
            ],
            "note": "설탕을 2T 넣으니 딱 적당함. 다음엔 노추를 넣어 색을 진하게 낼 것."
        }
    }

# --- MODE 1: 레시피 비교 및 생성 ---
if menu == "레시피 비교 및 생성":
    st.header("🔍 레시피 AI 비교 분석")
    
    # 1. 입력 섹션
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        url1 = col1.text_input("후보 1 (유튜브/웹)", placeholder="백종원 레시피 URL")
        url2 = col2.text_input("후보 2 (유튜브/웹)", placeholder="김수미 레시피 URL")
        url3 = col3.text_input("후보 3 (유튜브/웹)", placeholder="만개의 레시피 URL")
        
    if st.button("AI 분석 실행"):
        st.success("AI가 동영상을 요약하고 차이점을 분석했습니다! (가상 데이터 출력)")

    # 2. 비교 데이터 시각화
    st.subheader("📊 스타일별 핵심 차이점")
    compare_df = pd.DataFrame({
        "구분": ["당면처리", "간맞추기", "특이사항"],
        "후보 1": ["삶기 (바로)", "설탕 위주", "파기름 활용"],
        "후보 2": ["불리기 (길게)", "간장 위주", "재료 밑간 강조"],
        "후보 3": ["삶기 (불린후)", "다진마늘 필수", "깔끔한 채썰기"]
    })
    st.table(compare_df)

    # 3. 최종 편집 (PC 대화형 화면)
    st.divider()
    st.subheader("📝 나만의 최종 레시피 확정")
    c1, c2 = st.columns(2)
    with c1:
        new_title = st.text_input("요리명", value="인생 잡채")
        new_ingred = st.text_area("재료 리스트 (한 줄에 하나씩)", value="당면 250g\n진간장 5T\n설탕 2T")
    with c2:
        new_steps = st.text_area("조리 순서", value="1. 당면을 삶는다\n2. 양념을 넣고 볶는다")
        if st.button("레시피북에 저장"):
            st.balloons()
            st.info(f"'{new_title}' 레시피가 저장되었습니다.")

# --- MODE 2: 나만의 레시피북 열람 ---
elif menu == "나만의 레시피북 열람":
    st.header("📖 확정 레시피 아카이브")
    
    target_recipe = st.selectbox("열람할 레시피 선택", list(st.session_state.my_recipes.keys()))
    data = st.session_state.my_recipes[target_recipe]

    # PC용 와이드 열람 레이아웃
    col_img, col_main, col_side = st.columns([1, 2, 1])

    with col_img:
        st.image("https://via.placeholder.com/300x400.png?text=Recipe+Image", use_container_width=True)
        st.metric("난이도", data['difficulty'])
        st.metric("소요 시간", data['time'])

    with col_main:
        st.subheader("🛒 재료 리스트")
        m1, m2 = st.columns(2)
        mid = len(data['ingredients']) // 2 + 1
        with m1:
            for i in data['ingredients'][:mid]: st.write(f"✅ {i}")
        with m2:
            for i in data['ingredients'][mid:]: st.write(f"✅ {i}")
        
        st.divider()
        st.subheader("👨‍🍳 조리 단계")
        for idx, step in enumerate(data['steps']):
            st.info(f"**Step {idx+1}:** {step}")

    with col_side:
        st.subheader("💡 요리 노트")
        st.success(data['note'])
        st.write(f"**태그:** {data['tags']}")
        if st.button("📱 모바일용 QR 생성"):
            st.write("QR 코드를 스캔하여 폰으로 전송합니다.")
