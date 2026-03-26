import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# 1. 레시피 데이터 추출 함수 (만개의 레시피 전용)
def crawl_recipe(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 제목 추출
        title = soup.select_one('.view2_summary h3').get_text(strip=True) if soup.select_one('.view2_summary h3') else "제목 없음"
        
        # 재료 추출
        ingre_tags = soup.select('.ready_ingre3 ul li')
        ingredients = [tag.get_text(" ", strip=True).replace(" 구매", "") for tag in ingre_tags]
        
        # 조리 순서 추출
        step_tags = soup.select('.view_step_cont .media-body')
        steps = [tag.get_text(strip=True) for tag in step_tags]
        
        return {"title": title, "ingredients": ingredients, "steps": steps}
    except Exception as e:
        return None

# --- UI 시작 ---
st.set_page_config(layout="wide", page_title="AI 실시간 레시피 분석기")
st.title("🔍 실시간 레시피 데이터 추출 & 비교")

# URL 입력 섹션
with st.container(border=True):
    col1, col2, col3 = st.columns(3)
    url1 = col1.text_input("레시피 소스 1", value="https://www.10000recipe.com/recipe/6907285")
    url2 = col2.text_input("레시피 소스 2", value="https://www.10000recipe.com/recipe/6903050")
    url3 = col3.text_input("레시피 소스 3", value="https://www.10000recipe.com/recipe/6840346")
    
    analyze_btn = st.button("🚀 실제 데이터 추출 시작", use_container_width=True)

if analyze_btn:
    urls = [url1, url2, url3]
    results = []
    
    with st.spinner("웹사이트에서 레시피 정보를 가져오는 중..."):
        for url in urls:
            if url:
                data = crawl_recipe(url)
                if data:
                    results.append(data)
    
    if results:
        st.divider()
        st.subheader("📋 추출된 실시간 레시피 정보")
        
        # PC 넓은 화면을 활용해 3개 레시피 본문 나란히 배치
        cols = st.columns(len(results))
        for i, res in enumerate(results):
            with cols[i]:
                st.success(f"**후보 {i+1}: {res['title']}**")
                
                with st.expander("🛒 재료 확인", expanded=True):
                    for ing in res['ingredients']:
                        st.write(f"- {ing}")
                
                with st.expander("👨‍🍳 조리 순서", expanded=False):
                    for idx, step in enumerate(res['steps']):
                        st.write(f"**{idx+1}.** {step}")

        # 분석용 텍스트 묶기 (나중에 AI에게 던질 데이터)
        all_text = ""
        for i, res in enumerate(results):
            all_text += f"\n[레시피{i+1}: {res['title']}]\n재료: {', '.join(res['ingredients'])}\n"
        
        st.info("💡 이제 위 데이터들이 준비되었습니다. 여기에 OpenAI API만 연결하면 '비교 분석표'가 자동으로 생성됩니다.")
    else:
        st.error("데이터를 가져오지 못했습니다. URL을 확인해주세요.")
