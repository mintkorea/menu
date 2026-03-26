import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
from openai import OpenAI

# 1. OpenAI 클라이언트 설정 (Secrets 사용)
try:
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
except:
    st.error("⚠️ OpenAI API 키가 설정되지 않았습니다. Streamlit Secrets를 확인해주세요.")

# --- 페이지 설정 ---
st.set_page_config(layout="wide", page_title="AI 레시피 비교 분석기", page_icon="🍳")

# --- 함수 정의 ---
def crawl_recipe(url):
    """만개의 레시피 사이트에서 데이터를 추출합니다."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        title = soup.select_one('.view2_summary h3').get_text(strip=True)
        ingre = [tag.get_text(" ", strip=True).replace(" 구매", "") for tag in soup.select('.ready_ingre3 ul li')]
        steps = [tag.get_text(strip=True) for tag in soup.select('.view_step_cont .media-body')]
        
        return {"title": title, "ingredients": ingre, "steps": steps}
    except Exception as e:
        return None

def analyze_recipes_with_ai(recipe_list):
    """AI를 사용하여 레시피의 차이점을 분석합니다."""
    prompt = "다음 3개 레시피의 차이점을 분석해서 요약해줘.\n\n"
    for i, r in enumerate(recipe_list):
        prompt += f"레시피{i+1} ({r['title']}): 재료 - {', '.join(r['ingredients'])}\n"
    
    prompt += "\n출력 형식: 반드시 '비교 항목', '레시피 1', '레시피 2', '레시피 3'를 컬럼으로 하는 리스트 형식의 데이터를 만들어줘."

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": "너는 요리 전문가야. 레시피의 차이점을 표 형식으로 정리하는 데 능숙해."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"AI 분석 중 오류 발생: {str(e)}"

# --- UI 레이아웃 ---
st.title("👨‍🍳 AI 멀티 레시피 비교 엔진")
st.info("URL 3개를 넣으면 AI가 실제 내용을 읽어와 차이점을 분석해 드립니다.")

with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    u1 = c1.text_input("레시피 1", "https://www.10000recipe.com/recipe/6907285")
    u2 = c2.text_input("레시피 2", "https://www.10000recipe.com/recipe/6903050")
    u3 = c3.text_input("레시피 3", "https://www.10000recipe.com/recipe/6840346")
    
    analyze_btn = st.button("🚀 AI 데이터 추출 및 비교 분석 시작", use_container_width=True)

if analyze_btn:
    results = []
    with st.spinner("웹사이트에서 데이터를 긁어오는 중..."):
        for u in [u1, u2, u3]:
            if u:
                data = crawl_recipe(u)
                if data: results.append(data)
    
    if len(results) >= 2:
        st.divider()
        # 1. AI 분석표 출력
        st.subheader("📊 AI 선정: 레시피 핵심 차이점")
        with st.spinner("AI가 레시피를 분석하고 있습니다..."):
            analysis_result = analyze_recipes_with_ai(results)
            st.markdown(analysis_result) # AI가 생성한 마크다운 표 출력
            
        st.divider()
        # 2. 원본 데이터 비교 열람 (PC 레이아웃)
        st.subheader("📝 추출된 원본 데이터")
        cols = st.columns(len(results))
        for i, res in enumerate(results):
            with cols[i]:
                st.success(f"**후보 {i+1}: {res['title']}**")
                with st.expander("🛒 상세 재료 및 순서 보기", expanded=True):
                    st.write("**[재료]**")
                    for ing in res['ingredients']: st.write(f"- {ing}")
                    st.write("**[조리 순서]**")
                    for idx, s in enumerate(res['steps']): st.write(f"{idx+1}. {s}")
    else:
        st.error("최소 2개 이상의 유효한 레시피 URL을 입력해주세요.")

# 나만의 레시피 저장 섹션 (하단 고정)
if 'results' in locals() and len(results) > 0:
    st.divider()
    st.subheader("💡 나만의 레시피로 확정하기")
    col_final1, col_final2 = st.columns(2)
    with col_final1:
        st.text_input("레시피 이름", value="나만의 인생 잡채")
        st.text_area("최종 재료", value="\n".join(results[0]['ingredients']))
    with col_final2:
        st.text_area("최종 순서", value="\n".join(results[0]['steps']))
        st.button("💾 내 레시피북에 최종 저장")
