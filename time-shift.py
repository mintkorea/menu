import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os
from streamlit_javascript import st_javascript

# --- 1. 기본 설정 및 보안 설정 ---
ADMIN_PASSWORD = "1234" # 관리자용 비밀번호 (필요시 변경하세요)
DEVICE_MAP = {"S918": "황재업", "N971": "이정석", "N970": "김태언", "V510": "김태언", "G988": "이태원"}
PATTERN_START_DATE = datetime(2026, 3, 9).date()
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의 C조 관리", layout="wide")

# --- 2. CSS: 모바일 최적화 (여백 최소화 및 슬림 폰트) ---
st.markdown("""
    <style>
    .block-container { padding-top: 0.5rem !important; padding-bottom: 0rem !important; }
    .main-title { font-size: 18px !important; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 5px; }
    .status-card { background-color: #f8f9fa; border-radius: 8px; padding: 8px; margin-bottom: 5px; border-left: 4px solid #1E3A8A; }
    .status-label { font-size: 11px; color: #666; }
    .status-value { font-size: 14px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 시간 계산 (07시 투입 기준)
now_kst = datetime.now(timezone(timedelta(hours=9)))
today_val = now_kst.date()
now_min = now_kst.hour * 60 + now_kst.minute
if now_min < 420: now_min += 1440 # 07:00(420분) 이전은 전날 취급

# --- 3. 데이터 관리 함수 ---
def load_vac():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df.sort_values('날짜')
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

if 'vac_df' not in st.session_state:
    st.session_state.vac_df = load_vac()

# 기기 인식
ua = st_javascript("navigator.userAgent")
detected = "안 함"
if ua and ua != 0:
    for model, name in DEVICE_MAP.items():
        if model in str(ua).upper(): detected = name; break

# --- 4. 사이드바 설정 ---
with st.sidebar:
    st.header("⚙️ 설정")
    menu = st.radio("이동", ["📍 실시간 상황판", "📅 교대 근무표", "✍️ 연차 신청/관리"])
    user_name = st.selectbox("👤 본인 확인", ["안 함", "황재업", "김태언", "이태원", "이정석"], 
                             index=["안 함", "황재업", "김태언", "이태원", "이정석"].index(detected))
    st.divider()
    st.subheader("📅 조회 범위")
    view_start = st.date_input("시작일", value=today_val - timedelta(days=2))
    view_days = st.slider("조회 일수", 7, 60, 21)

# --- 5. [메뉴] 실시간 상황판 ---
if menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>📍 실시간 근무 현황</div>", unsafe_allow_html=True)
    diff = (today_val - PATTERN_START_DATE).days
    if diff % 3 == 0:
        # 로직: 김(0)->이정(1)->이태(2) 순환
        sc = diff // 3
        ci, is_2nd = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: h, a, b = "김태언", ("이정석" if is_2nd else "이태원"), ("이태원" if is_2nd else "이정석")
        elif ci == 1: h, a, b = "이정석", ("이태원" if is_2nd else "김태언"), ("김태언" if is_2nd else "이태원")
        else: h, a, b = "이태원", ("이정석" if is_2nd else "김태언"), ("김태언" if is_2nd else "이정석")

        # 엑셀 기반 타임라인 데이터
        sched = [
            {"F": "07:00", "T": "08:00", "조": "안내실", "대": "로비", "A": "로비", "B": "휴게"},
            {"F": "08:00", "T": "10:00", "조": "안내실", "대": "휴게/순찰", "A": "휴게", "B": "로비"},
            {"F": "10:00", "T": "11:00", "조": "휴게", "대": "안내실", "A": "로비", "B": "순찰/휴"},
            {"F": "11:00", "T": "13:00", "조": "안내/중식", "대": "중식/안내", "A": "로비/중식", "B": "중식/로비"},
            {"F": "13:00", "T": "15:00", "조": "안내/순찰", "대": "휴게/안내", "A": "순찰/로비", "B": "로비/휴게"},
            {"F": "15:00", "T": "17:00", "조": "안내/휴게", "대": "휴게/안내", "A": "로비/휴게", "B": "휴게/로비"},
            {"F": "17:00", "T": "19:00", "조": "안내실", "대": "휴게/석식", "A": "휴게/로비", "B": "로비/석식"},
            {"F": "19:00", "T": "21:00", "조": "안내/석식", "대": "안내실", "A": "석식/로비", "B": "로비/휴게"},
            {"F": "21:00", "T": "23:00", "조": "안내/순찰", "대": "순찰/휴게", "A": "로비/순찰", "B": "휴게/로비"},
            {"F": "23:00", "T": "07:00", "조": "안내/취침", "대": "취침/안내", "A": "취침/로비", "B": "로비/취침"}
        ]
        
        # 현재 행 찾기
        curr_r = next((r for r in sched if (int(r['F'][:2])*60+int(r['F'][3:])) <= now_min < (int(r['T'][:2])*60+int(r['T'][3:]) if r['T']!='07:00' else 1860)), sched[-1])
        
        c1, c2 = st.columns(2)
        with c1: st.markdown(f"<div class='status-card'><span class='status-label'>조장(황재업)</span><br><span class='status-value'>{curr_r['조']}</span></div>", unsafe_allow_html=True)
        with c1: st.markdown(f"<div class='status-card'><span class='status-label'>성희({h})</span><br><span class='status-value'>{curr_r['대']}</span></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='status-card'><span class='status-label'>의산A({a})</span><br><span class='status-value'>{curr_r['A']}</span></div>", unsafe_allow_html=True)
        with c2: st.markdown(f"<div class='status-card'><span class='status-label'>의산B({b})</span><br><span class='status-value'>{curr_r['B']}</span></div>", unsafe_allow_html=True)
        
        st.divider()
        st.dataframe(pd.DataFrame(sched), use_container_width=True, hide_index=True)
    else: st.warning("비번입니다.")

# --- 6. [메뉴] 교대 근무표 (연차 조회 포함) ---
elif menu == "📅 교대 근무표":
    st.markdown("<div class='main-title'>📅 C조 근무편성표 (연차 반영)</div>", unsafe_allow_html=True)
    cal = []
    curr = view_start
    while curr <= view_start + timedelta(days=view_days):
        d = (curr - PATTERN_START_DATE).days
        if d % 3 == 0:
            sc = d // 3
            ci, is_2nd = (sc // 2) % 3, sc % 2 == 1
            if ci == 0: h, a, b = "김태언", ("이정석" if is_2nd else "이태원"), ("이태원" if is_2nd else "이정석")
            elif ci == 1: h, a, b = "이정석", ("이태원" if is_2nd else "김태언"), ("김태언" if is_2nd else "이태원")
            else: h, a, b = "이태원", ("이정석" if is_2nd else "김태언"), ("김태언" if is_2nd else "이정석")
            
            # 연차 확인
            v_list = st.session_state.vac_df[st.session_state.vac_df['날짜'] == curr]['이름'].tolist()
            cal.append({"날짜": curr.strftime("%m/%d(%a)"), "조장": "황재업", 
                        "성희": f"🌴{h}" if h in v_list else h, 
                        "의산A": f"🌴{a}" if a in v_list else a, 
                        "의산B": f"🌴{b}" if b in v_list else b})
        curr += timedelta(days=1)
    st.dataframe(pd.DataFrame(cal), use_container_width=True, hide_index=True)

# --- 7. [메뉴] 연차 신청/관리 (보안 강화) ---
elif menu == "✍️ 연차 신청/관리":
    st.markdown("<div class='main-title'>✍️ 연차 신청 및 현황 조회</div>", unsafe_allow_html=True)
    
    # [입력] 누구나 가능
    with st.expander("➕ 연차 신청하기 (누구나 가능)"):
        with st.form("vac_form"):
            v_date = st.date_input("날짜", value=today_val)
            v_name = st.selectbox("이름", ["이태원", "김태언", "이정석"])
            v_reason = st.text_input("사유", value="개인")
            if st.form_submit_button("신청 완료"):
                new_data = pd.DataFrame([{"날짜": v_date, "이름": v_name, "사유": v_reason}])
                st.session_state.vac_df = pd.concat([st.session_state.vac_df, new_data]).drop_duplicates()
                st.session_state.vac_df.to_csv(VACATION_FILE, index=False)
                st.success(f"{v_name}님 {v_date} 연차 신청 완료!"); st.rerun()

    st.divider()
    st.subheader("📋 전체 연차 현황 (조회)")
    st.dataframe(st.session_state.vac_df, use_container_width=True, hide_index=True)

    # [수정/삭제] 관리자 전용
    st.divider()
    with st.expander("🔐 연차 수정/삭제 (관리자 전용)"):
        pw = st.text_input("관리자 비밀번호", type="password")
        if pw == ADMIN_PASSWORD:
            st.info("비밀번호 일치. 삭제할 항목을 선택하세요.")
            for idx, row in st.session_state.vac_df.iterrows():
                col1, col2 = st.columns([4, 1])
                col1.write(f"[{row['날짜']}] {row['이름']} ({row['사유']})")
                if col2.button("삭제", key=f"del_{idx}"):
                    st.session_state.vac_df = st.session_state.vac_df.drop(idx)
                    st.session_state.vac_df.to_csv(VACATION_FILE, index=False)
                    st.rerun()
        elif pw != "": st.error("비밀번호가 틀렸습니다.")
