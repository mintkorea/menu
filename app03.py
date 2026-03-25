# 5. 리스트 출력
for p in data:
    # 검색 필터링 (기존 동일)
    search_targets = [p.get('name', ''), p.get('dept', ''), p.get('work', ''), p.get('pos', '')]
    if query and not any(query.lower() in str(val).lower() for val in search_targets):
        continue
    
    # [사전 처리 1] 내선번호(T) 처리 - 로직 강화
    t_tag = ""
    ext_val = str(p.get('ext', '')).strip() # 공백 제거 및 문자열 변환
    
    if ext_val: # 내선번호가 실제로 존재할 때만 생성
        # 번호 체계 설정
        prefix = "022258" if p['name'] == "주상건" else "023147"
        full_ext = f"{prefix}{ext_val}"
        t_tag = f'<a href="tel:{full_ext}" class="icon-link" style="text-decoration:none;">T</a>'
    
    # [사전 처리 2] 휴대폰(M) 처리
    m_tag = ""
    mobile_val = str(p.get('mobile', '')).replace('-', '').strip()
    if mobile_val:
        m_tag = f'<a href="tel:{mobile_val}" class="icon-link" style="text-decoration:none;">M</a>'
    
    # [사전 처리 3] 텍스트 정보
    pos = p.get('pos', '')
    dept = p.get('dept', '')
    sep = " · " if pos and dept else ""
    work_text = p.get('work', '')
    work_display = f'<div class="work-text">- {work_text}</div>' if work_text else ""

    # [최종 출력] f-string 구조 단순화
    html_content = f"""
    <div class="contact-card">
        <div class="info-section">
            <div class="name-row">
                <span class="name-text">{p['name']}</span>
                <span class="pos-dept">{pos}{sep}{dept}</span>
            </div>
            {work_display}
        </div>
        <div class="icon-section">
            {t_tag}
            {m_tag}
        </div>
    </div>
    """
    st.markdown(html_content, unsafe_allow_html=True)
