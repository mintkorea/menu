import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- 페이지 설정 (PC 넓은 화면 최적화) ---
st.set_page_config(layout="wide", page_title="AI 나만의 레시피북", page_icon="🍳")

# --- 스타일 설정 (가독성 향상) ---
st.markdown("""
    <style>
    .recipe-card {
        background-color: #f8f9fa;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #dee2e6;
        margin-bottom: 10px;
    }
    .stButton>button {
        width: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 1. 실시간 데이터 추출 함수 (만개의 레시피 전용) ---
def crawl_recipe(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 제목
        title = soup.select_one('.view2_summary h3').get_text(strip=True) if soup.select_one('.view2_summary h3') else "제목 없음"
        
        # 재료 (양념과 주재료 구분 없이 추출)
        ingre_tags = soup.select('.ready_ingre3 ul li')
        ingredients = [tag.get_text(" ", strip=True).replace(" 구매", "") for tag in ingre_tags]
        
        # 조리 순서
        step_tags = soup.select('.view_step_cont .media-body')
        steps = [tag.get_text(strip=True) for tag in step_tags]
        
        return {"title": title, "ingredients": ingredients, "steps": steps, "url": url}
    except Exception as e:
        st.error(f"URL 분석 실패: {url} ({e})")
        return None

# --- 세션 상태 초기화 (데이터 보존) ---
if 'recipe_db' not in st.session_state:
    st.session_state.recipe_db = {}

# --- UI 레이아웃 ---
st.title("🍳 AI 멀티 소스 레시피 비교 분석기")
st.caption("여러 사이트의 레시피를 한눈에 비교하고 나만의 황금 레시피를 완성하세요.")

# 사이드바 메뉴
with st.sidebar:
    st.header("📂 메뉴")
    mode = st.radio("모드 선택", ["레시피 비교 및 생성", "나만의 레시피 보관함"])

# --- MODE 1: 레시피 비교 및 생성 ---
if mode == "레시피 비교 및 생성":
    # 1. URL 입력 영역
    with st.container():
        st.subheader("🔗 분석할 레시피 주소 (만개의 레시피 권장)")
        c1, c2, c3 = st.columns(3)
        u1 = c1.text_input("레시피 1", value="https://www.10000recipe.com/recipe/6907285")
        u2 = c2.text_input("레시피 2", value="https://www.10000recipe.com/recipe/6903050")
        u3 = c3.text_input("레시피 3", value="https://www.10000recipe.com/recipe/6840346")
        
        analyze_btn = st.button("🚀 실시간 데이터 추출 및 분석 시작")

    if analyze_btn:
        urls = [u for u in [u1, u2, u3] if u]
        results = []
        
        with st.spinner("웹사이트 데이터를 읽어오는 중..."):
            for url in urls:
                data = crawl_recipe(url)
                if data: results.append(data)
        
        if results:
            st.divider()
            # 2. 실시간 데이터 출력 (3열 배치)
            st.subheader("📊 추출된 레시피 본문 비교")
            cols = st.columns(len(results))
            for i, res in enumerate(results):
                with cols[i]:
                    st.success(f"**후보 {i+1}: {res['title']}**")
                    with st.expander("🛒 재료 리스트", expanded=True):
                        for ing in res['ingredients']:
                            st.write(f"- {ing}")
                    with st.expander("👨‍🍳 상세 조리 단계"):
                        for idx, step in enumerate(res['steps']):
                            st.write(f"**{idx+1}.** {step}")

            # 3. 나만의 레시피 확정 편집창
            st.divider()
            st.subheader("📝 나만의 최종 레시피 확정 (PC 편집)")
            edit_col1, edit_col2 = st.columns([1, 1])
            
            with edit_col1:
                final_title = st.text_input("최종 요리 제목", value=f"{results[0]['title']} (내 버전)")
                # 기본 재료를 첫 번째 후보 데이터로 미리 채워줌
                initial_ing = "\n".join(results[0]['ingredients'])
                final_ingred = st.text_area("최종 재료 확정 (비교하며 수정하세요)", value=initial_ing, height=300)
            
            with edit_col2:
                initial_steps = "\n".join([f"{i+1}. {s}" for i, s in enumerate(results[0]['steps'])])
                final_steps = st.text_area("최종 조리 순서 확정", value=initial_steps, height=300)
                
                if st.button("💾 내 레시피북에 저장하기"):
                    st.session_state.recipe_db[final_title] = {
                        "ingredients": final_ingred.split('\n'),
                        "steps": final_steps.split('\n'),
                        "source_urls": urls
                    }
                    st.balloons()
                    st.success(f"'{final_title}' 레시피가 보관함에 저장되었습니다!")

# --- MODE 2: 나만의 레시피 보관함 (PC 열람용) ---
elif mode == "나만의 레시피 보관함":
    st.header("📖 확정 레시피 아카이브")
    
    if not st.session_state.recipe_db:
        st.info("아직 저장된 레시피가 없습니다. 분석 모드에서 나만의 레시피를 만들어보세요.")
    else:
        selected = st.selectbox("열람할 레시피 선택", list(st.session_state.recipe_db.keys()))
        data = st.session_state.recipe_db[selected]
        
        view_col1, view_col2 = st.columns([1, 2])
        
        with view_col1:
            st.subheader("🛒 재료 리스트")
            for item in data['ingredients']:
                st.write(f"✅ {item}")
            st.divider()
            st.write("**참고 소스:**")
            for url in data['source_urls']:
                st.caption(url)
                
        with view_col2:
            st.subheader("👨‍🍳 조리 순서")
            for i, step in enumerate(data['steps']):
                if step.strip():
                    st.info(f"**Step {i+1}:** {step}")
            
            st.divider()
            if st.button("🖨️ 인쇄용 화면 보기"):
                st.write("인쇄 기능을 준비 중입니다.")
