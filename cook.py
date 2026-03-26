import streamlit as st
import pandas as pd

# 1. 초기 설정 및 세션 상태 관리
st.set_page_config(layout="wide", page_title="AI Personal Recipe Book")

if 'recipe_db' not in st.session_state:
    st.session_state.recipe_db = {} # 확정된 레시피 저장소

# 2. 사이드바 메뉴 (모드 전환)
with st.sidebar:
    st.title("👨‍🍳 Recipe Hub")
    app_mode = st.radio("기능 선택", ["새 레시피 분석/생성", "나만의 레시피 보관함"])
    st.divider()
    st.info("💡 팁: 유튜브, 블로그 등 어떤 링크든 붙여넣기만 하세요.")

# --- 모드 1: 새 레시피 분석/생성 (PC 대시보드) ---
if app_mode == "새 레시피 분석/생성":
    st.header("🔍 멀티 소스 레시피 비교 분석")
    
    # 입력 영역
    with st.container(border=True):
        col1, col2, col3 = st.columns(3)
        src1 = col1.text_input("레시피 소스 1", placeholder="유튜브/블로그 URL")
        src2 = col2.text_input("레시피 소스 2", placeholder="유튜브/블로그 URL")
        src3 = col3.text_input("레시피 소스 3", placeholder="유튜브/블로그 URL")
        
        if st.button("🚀 AI 분석 및 데이터 추출", use_container_width=True):
            # 실제 구현 시 여기서 scraping 및 OpenAI API 호출 로직이 들어갑니다.
            st.toast("AI가 데이터를 분석 중입니다...")
            st.session_state.temp_compare = True

    if st.session_state.get('temp_compare'):
        st.divider()
        # 비교 영역 (PC의 넓은 화면 활용)
        st.subheader("📊 소스별 핵심 차이점 비교")
        
        # 가상의 분석 데이터 (샘플)
        compare_data = {
            "비교 항목": ["당면 처리", "단맛 비결", "핵심 양념", "조리 방식"],
            "소스 1 (백종원)": ["끓는 물에 삶기", "설탕 2T", "진간장 베이스", "팬에서 한꺼번에"],
            "소스 2 (김수미)": ["찬물에 불리기", "매실액 1T", "양조간장 베이스", "재료별 따로 볶기"],
            "소스 3 (블로그)": ["삶은 후 볶기", "올리고당 1T", "굴소스 추가", "당면 색 입히기"]
        }
    
        st.table(pd.DataFrame(compare_data))

        # 편집 및 저장 영역
        st.subheader("✍️ 나만의 최종 레시피 확정")
        edit_col1, edit_col2 = st.columns(2)
        
        with edit_col1:
            f_name = st.text_input("요리 제목", value="인생 잡채")
            f_ingred = st.text_area("최종 재료 (수정 가능)", "당면 250g\n돼지고기 100g\n진간장 5T\n설탕 1.5T")
        with edit_col2:
            f_steps = st.text_area("최종 조리 순서", "1. 당면을 11분 삶는다.\n2. 야채를 따로 볶아 합친다.")
            if st.button("💾 내 레시피북에 최종 저장"):
                st.session_state.recipe_db[f_name] = {
                    "ingredients": f_ingred.split('\n'),
                    "steps": f_steps.split('\n'),
                    "date": "2026-03-26"
                }
                st.success(f"'{f_name}' 저장 완료!")

# --- 모드 2: 나만의 레시피 보관함 (PC 열람용) ---
elif app_mode == "나만의 레시피 보관함":
    st.header("📖 나의 황금 레시피 도서관")
    
    if not st.session_state.recipe_db:
        st.warning("아직 저장된 레시피가 없습니다. 분석 모드에서 레시피를 만들어보세요!")
    else:
        selected_recipe = st.selectbox("열람할 요리 선택", list(st.session_state.recipe_db.keys()))
        recipe = st.session_state.recipe_db[selected_recipe]
        
        # PC용 와이드 상세 열람 화면
        st.divider()
        view_col1, view_col2 = st.columns([1, 2])
        
        with view_col1:
            st.image("https://via.placeholder.com/400x300?text=Recipe+Image", use_container_width=True)
            st.subheader("🛒 필수 재료")
            for ing in recipe['ingredients']:
                st.write(f"• {ing}")
            
        with view_col2:
            st.subheader("👨‍🍳 조리 단계")
            for i, step in enumerate(recipe['steps']):
                st.info(f"**{i+1}단계:** {step}")
            
            st.divider()
            st.subheader("📝 요리 메모")
            st.write(f"마지막 수정일: {recipe['date']}")
            st.text_area("오늘의 피드백", placeholder="이번엔 조금 짰음. 다음엔 간장 줄이기.")
            
            if st.button("🖨️ 인쇄 / PDF 저장"):
                st.write("PDF 생성 기능을 준비 중입니다.")
