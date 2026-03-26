import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from openai import OpenAI

# 0. OpenAI 클라이언트 설정 (API 키 입력 필요)
# 보안을 위해 st.secrets["OPENAI_API_KEY"] 사용을 권장합니다.
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
st.set_page_config(layout="wide", page_title="AI 레시피 비교 분석기")

# --- 1. 데이터 추출 함수 ---
def crawl_recipe(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        title = soup.select_one('.view2_summary h3').get_text(strip=True)
        ingre = [tag.get_text(" ", strip=True).replace(" 구매", "") for tag in soup.select('.ready_ingre3 ul li')]
        steps = [tag.get_text(strip=True) for tag in soup.select('.view_step_cont .media-body')]
        return {"title": title, "ingredients": ingre, "steps": steps}
    except:
        return None

# AI 분석 없이 재료만 표로 보여주는 임시 코드
def simple_compare(results):
    df_data = {
        "항목": ["재료 목록"],
        "레시피 1": [", ".join(results[0]['ingredients'][:5]) + "..."],
        "레시피 2": [", ".join(results[1]['ingredients'][:5]) + "..."],
        "레시피 3": [", ".join(results[2]['ingredients'][:5]) + "..."]
    }
    return pd.DataFrame(df_data)

# --- UI 레이아웃 ---
st.title("🤖 AI 멀티 레시피 비교 엔진")

with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    u1 = c1.text_input("레시피 1", "https://www.10000recipe.com/recipe/6907285")
    u2 = c2.text_input("레시피 2", "https://www.10000recipe.com/recipe/6903050")
    u3 = c3.text_input("레시피 3", "https://www.10000recipe.com/recipe/6840346")
    
    if st.button("🚀 AI 데이터 추출 및 비교 분석 시작", use_container_width=True):
        results = []
        for u in [u1, u2, u3]:
            data = crawl_recipe(u)
            if data: results.append(data)
        
        if len(results) >= 2:
            st.divider()
            # AI 분석 결과 출력
            with st.spinner("AI가 레시피를 열공하며 비교 분석표를 만들고 있습니다..."):
                analysis_table = analyze_recipes_with_ai(results)
                st.subheader("📊 AI 선정: 레시피 핵심 차이점")
                st.markdown(analysis_table) # AI가 만든 표 출력
            
            st.divider()
            # 원문 데이터 나열 (편집 참고용)
            cols = st.columns(len(results))
            for i, res in enumerate(results):
                with cols[i]:
                    st.success(f"**후보 {i+1}: {res['title']}**")
                    with st.expander("🛒 상세 재료 및 순서"):
                        st.write("**재료:**", ", ".join(res['ingredients']))
                        for s in res['steps']: st.write(f"- {s}")
        else:
            st.error("최소 2개 이상의 유효한 레시피 URL이 필요합니다.")
