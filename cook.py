import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from openai import OpenAI

# 0. OpenAI 클라이언트 설정 (API 키 입력 필요)
# 보안을 위해 st.secrets["OPENAI_API_KEY"] 사용을 권장합니다.
client = OpenAI(api_key=st.secrets["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"])

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

# --- 2. AI 분석 함수 (핵심) ---
def analyze_recipes_with_ai(recipe_list):
    # AI에게 던질 프롬프트 구성
    prompt = "다음 3개 레시피의 차이점을 분석해서 표 형태로 요약해줘.\n\n"
    for i, r in enumerate(recipe_list):
        prompt += f"레시피{i+1} ({r['title']}): 재료 - {', '.join(r['ingredients'])}, 순서 요약 - {r['steps'][0]}...\n"
    
    prompt += "\n출력 형식: '비교 항목', '레시피1', '레시피2', '레시피3' 컬럼을 가진 마크다운 표로 작성해줘."
    prompt += "비교 항목은 '당면 조리법', '간장/설탕 비율', '특별한 팁', '전체적인 특징'으로 구성해줘."

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

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
