<style>
    /* 전체 앱 컨테이너 폭 고정 */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 400px !important;
        margin: 0 auto !important;
        padding: 1rem 10px !important;
    }
    header { visibility: hidden; }

    /* 날짜 및 네비게이션 */
    .date-box { text-align: center; background: #F4F7FF; padding: 15px; border-radius: 15px; font-weight: 800; border: 1px solid #D6DCEC; }
    .nav-row { display: flex; justify-content: space-between; margin: 10px 0; gap: 5px; }
    .nav-btn { 
        flex: 1; text-align: center; padding: 8px; background: white; border: 1px solid #EEE; 
        border-radius: 8px; text-decoration: none; color: #1E3A5F; font-size: 14px; font-weight: 700;
    }

    /* ⭐ 인덱스 탭 가독성 개선 ⭐ */
    .tab-container {
        display: flex;
        width: 100%;
        margin-top: 15px;
        gap: 2px;
    }
    .tab-item {
        flex: 1;
        text-align: center;
        padding: 12px 0;
        font-size: 13px;
        font-weight: 800;
        color: #444; /* 비활성 상태 글자색을 진하게 변경 */
        text-decoration: none;
        border-radius: 10px 10px 0 0;
        opacity: 0.7; /* 투명도를 0.35에서 0.7로 높임 */
        transition: 0.2s;
    }
    .tab-item.active {
        opacity: 1;
        color: white !important; /* 활성 상태 글자색은 흰색 */
        transform: translateY(-2px);
        font-weight: 900;
    }

    /* 메뉴 카드 */
    .menu-card {
        border: 2px solid {sel_c};
        border-top: 5px solid {sel_c};
        border-radius: 0 0 20px 20px;
        padding: 40px 15px;
        text-align: center;
        background: white;
        margin-top: -1px;
        box-shadow: 0 8px 20px rgba(0,0,0,0.05);
    }
</style>
