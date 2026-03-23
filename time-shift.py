elif menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>📍 실시간 근무 및 안내</div>", unsafe_allow_html=True)
    
    # --- 1. 근무 시간표 안내 (상단 고정) ---
    with st.expander("⏰ C조 표준 근무 시간표 확인", expanded=True):
        st.info("💡 성의교정 C조는 3일 주기(24시간 교대)로 근무합니다.")
        st.table(pd.DataFrame({
            "구분": ["주간", "야간", "휴게/대기"],
            "시간": ["08:00 ~ 18:00", "18:00 ~ 익일 08:00", "편성표 및 현장 지침 준수"],
            "비고": ["정상 근무", "심야 순찰 포함", "회관/의산 위치 사수"]
        }))

    # --- 2. 오늘 상태 계산 ---
    today = datetime.now().date()
    diff_days = (today - PATTERN_START_DATE).days
    is_work_day = (diff_days % 3 == 0)

    st.divider()

    if is_work_day:
        st.subheader("📢 오늘은 [근무일] 입니다")
        # 오늘 근무자 계산 로직
        shift_count = diff_days // 3
        cycle_idx = (shift_count // 2) % 3 
        is_second_day = shift_count % 2 == 1
        
        if cycle_idx == 0: h_p, a_p, b_p = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
        elif cycle_idx == 1: h_p, a_p, b_p = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
        else: h_p, a_p, b_p = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
        
        cols = st.columns(4)
        positions = [("조장", "황재업"), ("회관", h_p), ("의산(A)", a_p), ("의산(B)", b_p)]
        for i, (pos, name) in enumerate(positions):
            status = check_vacation(today, name)
            with cols[i]:
                st.metric(pos, status)
                if status == "연차": st.error("❌ 부재중")
                else: st.success("✅ 근무중")
    else:
        # 비근무일일 때 메시지
        st.subheader("😴 오늘은 [비번/휴무] 입니다")
        
        # 다음 근무일 계산
        days_left = 3 - (diff_days % 3)
        if diff_days % 3 < 0: # 과거 기준일 이전일 경우 보정
            days_left = abs(diff_days % 3)
            
        next_work_day = today + timedelta(days=days_left)
        
        st.warning(f"다음 C조 근무일은 **{next_work_day.strftime('%m월 %d일')}** 입니다. ({days_left}일 남음)")
        st.caption("🚨 비상시에는 비상 연락망을 통해 조장님께 보고해 주세요.")

    st.divider()
    st.write("💡 상세한 월간 일정은 **'📅 근무 편성표'** 메뉴에서 확인하실 수 있습니다.")
