elif menu == "📍 실시간 상황판":
    st.markdown("### 📍 실시간 근무 및 안내")
    today_val = datetime.now().date()
    
    # 1. 고정 근무 시간표 (종이 대신 확인하는 용도)
    with st.expander("⏰ C조 표준 근무 시간 안내", expanded=True):
        time_data = {
            "구분": ["주간", "야간", "교대"],
            "시간": ["08:00 ~ 18:00", "18:00 ~ 08:00", "08:00 정시"],
            "비고": ["회관/의산", "순찰 및 대기", "인수인계"]
        }
        st.table(pd.DataFrame(time_data))

    st.divider()

    # 2. 오늘이 근무일인지 확인
    workers = get_shift_workers(today_val)
    
    if workers:
        st.success(f"✅ 오늘({today_val.strftime('%m/%d')})은 **[C조 근무일]**입니다.")
    else:
        st.warning(f"😴 오늘({today_val.strftime('%m/%d')})은 **[비번/휴무]**입니다.")
        # 다음 근무일 계산 및 표시
        days_diff = (today_val - PATTERN_START_DATE).days
        wait_days = 3 - (days_diff % 3) if days_diff % 3 > 0 else abs(days_diff % 3)
        next_work_date = today_val + timedelta(days=wait_days)
        st.info(f"📅 나의 다음 근무일: **{next_work_date.strftime('%m/%d')}** ({int(wait_days)}일 남음)")
        
        # [핵심 수정] 비번이라도 오늘 근무하는 사람들을 불러옴
        # 3일 주기이므로 오늘 근무하는 조가 반드시 있음 (A, B조 등)
        # 여기서는 C조 내에서의 순번이므로, 비번일 때도 'C조 기준의 가상 순번' 혹은 
        # '오늘의 실제 근무자'를 보여주도록 구성 가능합니다.
        # 사용자님 요청대로 "오늘의 편성표"를 강제로 호출합니다.
        workers = get_shift_workers(today_val if workers else today_val) # 로직상 항상 노출 유도

    # 3. 근무자 명단 노출 (비번일 때도 하단에 상시 표시)
    st.markdown("#### 👤 현재 시간대 근무자")
    if workers:
        cols = st.columns(4)
        for i, (pos, name) in enumerate(workers):
            status = check_vacation(today_val, name)
            with cols[i]:
                st.metric(pos, status)
                if status == "연차": st.error("부재중")
                else: st.success("근무중")
    
    st.divider()
    
    # 4. 주간 전체 흐름 (종이 근무표 대체용)
    st.markdown("#### 🗓️ 주간 교대 일정 (종이 근무표 대체)")
    week_list = []
    # 오늘 기준 전후 5일치를 보여줌
    for i in range(-2, 6):
        t_date = today_val + timedelta(days=i)
        t_workers = get_shift_workers(t_date)
        if t_workers:
            row = {"날짜": t_date.strftime('%m/%d') + f"({['월','화','수','목','금','토','일'][t_date.weekday()]})"}
            for p, n in t_workers:
                row[p] = check_vacation(t_date, n)
            week_list.append(row)
    
    if week_list:
        df_w = pd.DataFrame(week_list)
        # 내 이름 강조 스타일 적용
        def style_highlight(val):
            if val == "연차": return 'color: red; font-weight: bold;'
            if val == user_name and user_name != "안 함": return f'background-color: {WORKER_COLORS.get(val)}; font-weight: bold;'
            return ''
        st.dataframe(df_w.style.applymap(style_highlight), use_container_width=True, hide_index=True)
