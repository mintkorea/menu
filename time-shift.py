import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os
from streamlit_javascript import st_javascript

# --- 1. 기기-성함 매칭 데이터 (최종 정정본) ---
DEVICE_MAP = {
    "S918": "황재업",    # 황재업 조장님 (기존 설정 유지)
    "N971": "이정석",    # 이정석님: 갤럭시 노트 20 Ultra
    "N970": "김태언",    # 김태언님: 갤럭시 노트 10
    "V510": "김태언",    # 김태언님: LG V50S
    "G988": "이태원",    # 이태원님: 갤럭시 S20 Ultra
}

# --- 2. 기본 설정 및 데이터 로드 ---
PATTERN_START_DATE = datetime(2026, 3, 9).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7", "연차": "#FFEBEE"}
VACATION_FILE = 'vacation.csv'
ADMIN_PASSWORD = "1234" # 관리자 암호

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

# 연차 데이터 로드 함수
def load_vacation_data():
    if os.path.exists(VACATION_FILE):
        try:
            df = pd.read_csv(VACATION_FILE)
            df['날짜'] = pd.to_datetime(df['날짜']).dt.date
            return df
        except:
            return pd.DataFrame(columns=['날짜', '이름', '사유'])
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

def save_vacation_data(df):
    df.to_csv(VACATION_FILE, index=False, encoding='utf-8-sig')

# 기기 감지 함수
def get_device_user():
    ua = st_javascript("navigator.userAgent")
    if ua and ua != 0:
        ua_str = str(ua).upper()
        for model, name in DEVICE_MAP.items():
            if model in ua_str:
                return name
    return "안 함"

# 데이터 불러오기
df_vac = load_vacation_data()

# --- 3. CSS 스타일 ---
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 10px; }
    .stDataFrame { justify-content: center; display: flex; }
    </style>
    """, unsafe_allow_html=True)

# --- 4. 사이드바 (기기 인식 및 설정) ---
with st.sidebar:
    st.header("⚙️ 스마트 설정")
    menu = st.radio("메뉴 이동", ["📅 근무 편성표", "📍 실시간 상황판", "✍️ 연차 신청/관리"])
    
    st.divider()
    
    # 기기 인식 시도 및 이름 강조 설정
    detected = get_device_user()
    user_list = ["안 함", "황재업", "김태언", "이태원", "이정석"]
    
    if "selected_user" not in st.session_state:
        st.session_state.selected_user = detected if detected in user_list else "안 함"

    user_name = st.selectbox("👤 내 이름 강조", user_list, 
                             index=user_list.index(st.session_state.selected_user))
    
    if detected != "안 함":
        st.success(f"📱 기기 인식: **{detected}**님")

    # 근무 편성표 전용 슬라이더
    if menu == "📅 근무 편성표":
        st.subheader("📅 조회 설정")
        start_date = st.date_input("조회 시작일", datetime.now().date() - timedelta(days=3))
        duration = st.slider("조회 기간(일)", 7, 90, 30)

# --- 5. 메뉴별 로직 ---

# 연차 여부 확인 함수
def check_vacation(date, name):
    is_vac = df_vac[(df_vac['날짜'] == date) & (df_vac['이름'] == name)]
    return "연차" if not is_vac.empty else name

if menu == "📅 근무 편성표":
    st.markdown(f"<div class='main-title'>📅 {user_name if user_name != '안 함' else 'C조'} 근무 편성표</div>", unsafe_allow_html=True)
    
    cal_list = []
    curr = start_date
    end_date = start_date + timedelta(days=duration)
    
    while curr <= end_date:
        diff_days = (curr - PATTERN_START_DATE).days
        if diff_days % 3 == 0:
            shift_count = diff_days // 3
            cycle_idx = (shift_count // 2) % 3 
            is_second_day = shift_count % 2 == 1
            
            # 기본 패턴 계산
            if cycle_idx == 0: h_p, a_p, b_p = "김태언", ("이정석" if is_second_day else "이태원"), ("이태원" if is_second_day else "이정석")
            elif cycle_idx == 1: h_p, a_p, b_p = "이정석", ("이태원" if is_second_day else "김태언"), ("김태언" if is_second_day else "이태원")
            else: h_p, a_p, b_p = "이태원", ("이정석" if is_second_day else "김태언"), ("김태언" if is_second_day else "이정석")
            
            cal_list.append({
                "날짜": f"{curr.strftime('%m/%d')}({['월','화','수','목','금','토','일'][curr.weekday()]})",
                "조장": check_vacation(curr, "황재업"),
                "회관": check_vacation(curr, h_p),
                "의산(A)": check_vacation(curr, a_p),
                "의산(B)": check_vacation(curr, b_p)
            })
        curr += timedelta(days=1)

    if cal_list:
        df_display = pd.DataFrame(cal_list)
        def style_cells(val):
            if val == "연차": return 'background-color: #FFEBEE; color: #D32F2F; font-weight: bold;'
            if val == user_name and user_name != "안 함": 
                return f'background-color: {WORKER_COLORS.get(val)}; font-weight: bold; border: 1.5px solid #1E3A8A;'
            return ''
        st.dataframe(df_display.style.applymap(style_cells), use_container_width=True, hide_index=True, height=600)

elif menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>📍 실시간 근무 상황</div>", unsafe_allow_html=True)
    today = datetime.now().date()
    diff_days = (today - PATTERN_START_DATE).days
    
    if diff_days % 3 == 0:
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
        st.info("오늘은 정규 근무일이 아닙니다.")

elif menu == "✍️ 연차 신청/관리":
    st.markdown("<div class='main-title'>📂 연차 관리 시스템</div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🗓️ 연차 현황", "✍️ 연차 신청", "🔐 관리자 메뉴"])

    with tab1:
        st.dataframe(df_vac.sort_values('날짜', ascending=False), use_container_width=True)

    with tab2:
        with st.form("vac_form", clear_on_submit=True):
            v_date = st.date_input("날짜")
            v_name = st.selectbox("성명", ["황재업", "김태언", "이태원", "이정석"])
            v_reason = st.text_input("사유")
            if st.form_submit_button("신청하기"):
                new_row = pd.DataFrame({'날짜': [v_date], '이름': [v_name], '사유': [v_reason]})
                df_vac = pd.concat([df_vac, new_row], ignore_index=True)
                save_vacation_data(df_vac)
                st.success("등록 완료!"); st.rerun()

    with tab3:
        pwd = st.text_input("관리자 암호", type="password")
        if pwd == ADMIN_PASSWORD:
            if not df_vac.empty:
                df_with_id = df_vac.copy()
                st.dataframe(df_with_id)
                idx = st.number_input("삭제할 데이터 ID(번호)", 0, len(df_vac)-1, 0)
                if st.button("🗑️ 선택 항목 삭제"):
                    df_vac = df_vac.drop(idx).reset_index(drop=True)
                    save_vacation_data(df_vac)
                    st.success("삭제되었습니다."); st.rerun()
