import streamlit as st

def render_pc_recipe_view(recipe_data):
    # 상단 제목 및 태그
    st.title(f"📖 {recipe_data['title']}")
    st.caption(f"최종 수정일: {recipe_data['last_updated']} | 태그: {recipe_data['tags']}")
    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col1:
        st.image(recipe_data['image_url'], use_container_width=True)
        st.metric("난이도", recipe_data['difficulty'])
        st.metric("조리시간", recipe_data['time'])
        
    with col2:
        st.subheader("🛒 재료 및 양념")
        # 재료를 2열로 배치
        m_col1, m_col2 = st.columns(2)
        items = recipe_data['ingredients']
        mid = len(items) // 2
        with m_col1:
            for i in items[:mid]: st.write(f"- {i}")
        with m_col2:
            for i in items[mid:]: st.write(f"- {i}")
            
        st.divider()
        st.subheader("👨‍🍳 조리 순서")
        for i, step in enumerate(recipe_data['steps']):
            st.info(f"**Step {i+1}**: {step}")

    with col3:
        st.subheader("💡 나만의 요리 노트")
        st.warning(recipe_data['my_tip'])
        st.write("**참고 소스 비교**")
        st.json(recipe_data['reference_summary']) # 분석 데이터 요약본
        
        if st.button("프린트용 PDF 내보내기"):
            st.write("PDF 생성 중...")
