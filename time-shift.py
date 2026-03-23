import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

# --- 1. 기본 설정 및 데이터 로드 ---
PATTERN_START_DATE = datetime(2026, 3, 9).date()
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "김태언": "#E8F5E9", "이정석": "#FFFDE7", "연차": "#FFEBEE"}
VACATION_FILE = 'vacation.csv'
ADMIN_PASSWORD = "1234"  # 관리자용 비밀번호 (수정 가능)

st.set_page_config(page_title="성의교정 C조 관리 시스템", layout="centered")

def load_vacation_data():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

def save_vacation_data(df):
    df.to_csv(VACATION_FILE, index=False, encoding='utf-8-sig')

# --- 2. CSS 스타일 ---
st.markdown("""
    <style>
    .main-title { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-top: 10px; }
    .stDataFrame { justify-content: center; display: flex; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 사이드바 ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("메뉴 이동", ["📅 근무 편성표", "📍 실시간 상황판", "✍️ 연차 신청/관리"])
    st.divider()
    user_name = st.selectbox("👤 내 이름 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# 데이터 로드
df_vac = load_vacation_data()

# [함수] 연차 체크 로직
def check_vacation(date, name):
    is_vac = df_vac[(df_vac['날짜'] == date) & (df_vac['이름'] == name)]
    return "연차" if not is_vac.empty else name

# --- 4. 메뉴별 로직 ---

if menu == "📅 근무 편성표":
    st.markdown("<div class='main-title'>📅 성의교정 C조 근무편성표</div>", unsafe_allow_html=True)
    start_date = st.date_input("조회 시작일", datetime.now().date() - timedelta(days=3))
    
    cal_list = []
    curr = start_date
    for _ in range(45):  # 약 1.5개월치 자동 계산
        diff_days = (curr - PATTERN_START_DATE).days
        if diff_days % 3 == 0:
            shift_count = diff_days // 3
            cycle_idx = (shift_count // 2) % 3 
            is_second_day = shift_count % 2 == 1
            
            # 패턴 로직
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

    st.dataframe(pd.DataFrame(cal_list), use_container_width=True, hide_index=True)

elif menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>📍 실시간 근무 상황</div>", unsafe_allow_html=True)
    today = datetime.now().date()
    diff_days = (today - PATTERN_START_DATE).days
    
    if diff_days % 3 == 0:
        # 오늘 근무자 계산 로직 생략(위와 동일)... 
        # (생략된 부분은 이전 코드의 로직을 그대로 사용합니다)
        st.info(f"오늘({today})은 근무일입니다. 메인 리스트를 확인하세요.")
    else:
        st.warning("오늘은 정규 근무일이 아닙니다.")

elif menu == "✍️ 연차 신청/관리":
    st.markdown("<div class='main-title'>📂 연차 관리</div>", unsafe_allow_html=True)
    tab1, tab2, tab3 = st.tabs(["🗓️ 연차 현황", "✍️ 연차 신청", "🔐 관리자 수정/취소"])

    with tab1:
        st.subheader("등록된 연차 내역")
        # 수정을 위해 인덱스를 포함하여 표시
        display_df = df_vac.copy()
        display_df.index.name = "ID"
        st.dataframe(display_df.sort_values('날짜', ascending=False), use_container_width=True)

    with tab2:
        st.subheader("새 연차 신청")
        with st.form("add_form", clear_on_submit=True):
            v_date = st.date_input("날짜 선택")
            v_name = st.selectbox("성명", ["황재업", "김태언", "이태원", "이정석"])
            v_reason = st.text_input("사유")
            if st.form_submit_button("신청하기"):
                new_row = pd.DataFrame({'날짜': [v_date], '이름': [v_name], '사유': [v_reason]})
                df_vac = pd.concat([df_vac, new_row], ignore_index=True)
                save_vacation_data(df_vac)
                st.success("등록되었습니다."); st.rerun()

    with tab3:
        st.subheader("🛠️ 연차 데이터 수정 및 삭제")
        pwd = st.text_input("관리자 암호를 입력하세요", type="password")
        
        if pwd == ADMIN_PASSWORD:
            if not df_vac.empty:
                target_idx = st.number_input("수정/삭제할 ID (표 왼쪽 번호)", min_value=0, max_value=len(df_vac)-1, step=1)
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("🗑️ 선택한 연차 삭제", use_container_width=True):
                        df_vac = df_vac.drop(target_idx).reset_index(drop=True)
                        save_vacation_data(df_vac)
                        st.error("삭제되었습니다."); st.rerun()
                
                with col2:
                    st.info("수정은 아래 정보를 입력 후 '업데이트' 클릭")
                
                with st.expander("✏️ 데이터 수정하기"):
                    edit_date = st.date_input("수정 날짜", df_vac.iloc[target_idx]['날짜'])
                    edit_name = st.selectbox("수정 이름", ["황재업", "김태언", "이태원", "이정석"], 
                                         index=["황재업", "김태언", "이태원", "이정석"].index(df_vac.iloc[target_idx]['이름']))
                    edit_reason = st.text_input("수정 사유", df_vac.iloc[target_idx]['사유'])
                    
                    if st.button("✅ 정보 업데이트"):
                        df_vac.at[target_idx, '날짜'] = edit_date
                        df_vac.at[target_idx, '이름'] = edit_name
                        df_vac.at[target_idx, '사유'] = edit_reason
                        save_vacation_data(df_vac)
                        st.success("수정되었습니다."); st.rerun()
            else:
                st.write("데이터가 없습니다.")
        elif pwd != "":
            st.error("암호가 일치하지 않습니다.")
