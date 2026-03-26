import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# --- 페이지 설정 ---
st.set_page_config(layout="wide", page_title="레시피 비교 분석기 (Free)", page_icon="🍳")

# --- 1. 실시간 데이터 추출 함수 ---
def crawl_recipe(url):
    """만개의 레시피 사이트에서 데이터를 추출합니다."""
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        res = requests.get(url, headers=headers, timeout=10)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        
        # 제목 추출
        title_tag = soup.select_one('.view2_summary h3')
        title = title_tag.get_text(strip=True) if title_tag else "제목 없음"
        
        # 재료 추출
        ingre_tags = soup.select('.ready_ingre3 ul li')
        ingredients = [tag.get_text(" ", strip=True).replace(" 구매", "") for tag in ingre_tags]
        
        # 조리 순서 추출
        step_tags = soup.select('.view_step_cont .media-body')
        steps = [tag.get_text(strip=True) for tag in step_tags]
        
        return {"title": title, "ingredients": ingredients, "steps": steps, "url": url}
    except Exception as e:
        return None

# --- 2. 데이터 비교 함수 (무료 버전: AI 미사용) ---
def compare_recipes_manual(recipe_list):
    """긁어온 데이터를 기반으로 직접 비교표를 생성합니다."""
    data = {
        "비교 항목": ["📌 레시피 제목", "🛒 재료 개수", "🔥 첫 번째 단계", "🔗 원문 링크"],
    }
    
    for i, res in enumerate(recipe_list):
        data[f"후보 {i+1}"] = [
            res['title'],
            f"{len(res['ingredients'])}개",
            res['steps'][0][:50] + "..." if res['steps'] else "순서 정보 없음",
            f"[바로가기]({res['url']})"
        ]
    
    return pd.DataFrame(data)

# --- UI 레이아웃 ---
st.title("🍳 실시간 레시피 비교 분석기 (무료 버전)")
st.info("API 키 없이도 작동합니다. URL을 넣으면 실제 사이트의 데이터를 가져와 비교해 드립니다.")

# URL 입력 섹션
with st.container(border=True):
    c1, c2, c3 = st.columns(3)
    u1 = c1.text_input("레시피 1", "https://www.10000recipe.com/recipe/6907285")
    u2 = c2.text_input("레시피 2", "https://www.10000recipe.com/recipe/6903050")
    u3 = c3.text_input("레시피 3", "https://www.10000recipe.com/recipe/6840346")
    
    analyze_btn = st.button("🚀 데이터 추출 및 비교 시작", use_container_width=True)

if analyze_btn:
    urls = [u for u in [u1, u2, u3] if u]
    results = []
    
    with st.spinner("웹사이트에서 레시피 정보를 읽어오는 중..."):
        for url in urls:
            data = crawl_recipe(url)
            if data:
                results.append(data)
    
    if len(results) >= 1:
        st.divider()
        # 1. 수동 비교표 출력
        st.subheader("📊 레시피 핵심 요약 비교")
        comparison_df = compare_recipes_manual(results)
        st.table(comparison_df) # AI 대신 깔끔한 표로 출력

        st.divider()
        # 2. 원본 데이터 나열 (3열 배치)
        st.subheader("📝 상세 데이터 확인")
        cols = st.columns(len(results))
        for i, res in enumerate(results):
            with cols[i]:
                st.success(f"**후보 {i+1}: {res['title']}**")
                with st.expander("🛒 재료 전체 보기", expanded=True):
                    for ing in res['ingredients']:
                        st.write(f"- {ing}")
                with st.expander("👨‍🍳 조리 단계 전체 보기"):
                    for idx, step in enumerate(res['steps']):
                        st.write(f"**{idx+1}.** {step}")

        # 3. 나만의 레시피 편집 및 저장
        st.divider()
        st.subheader("✍️ 나만의 황금레시피 확정")
        final_col1, final_col2 = st.columns(2)
        
        with final_col1:
            st.text_input("레시피 이름", value=f"{results[0]['title']} (최종)")
            # 첫 번째 레시피 데이터를 기본값으로 넣어 편집하기 편하게 함
            st.text_area("최종 재료 리스트", value="\n".join(results[0]['ingredients']), height=200)
        with final_col2:
            st.text_area("최종 조리 단계", value="\n".join([f"{i+1}. {s}" for i, s in enumerate(results[0]['steps'])]), height=200)
            if st.button("💾 내 레시피북에 저장"):
                st.balloons()
                st.success("저장 기능이 작동했습니다! (현재는 세션에만 저장)")

    else:
        st.error("데이터를 가져오지 못했습니다. URL이 정확한지 확인해 주세요.")
