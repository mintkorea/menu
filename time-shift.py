import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

# --- 1. 기본 설정 및 보안 ---
ADMIN_PW = "1234" # 삭제용 비번
PATTERN_START = datetime(2026, 3, 9).date()
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의 C조 관리", layout="wide")

# --- 2. CSS: 모바일 최적화 (가독성 극대화) ---
st.markdown("""
    <style>
    .block-container { padding: 0.5rem !important; }
    .main-title { font-size: 18px !important; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 10px; }
    .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 10px; }
    .card { background: #f8f9fa; border: 1px solid #dee2e6; border-radius: 5px; padding: 10px; text-align: center; }
    .card-title { font-size: 11px; color: #666; margin-bottom: 2px; }
    .card-value { font-size: 15px; font-weight: bold; color: #1E3A8A; }
    [data-testid="stDataFrame"] { font-size: 12px !important; }
    </style>
    """, unsafe_allow_html=True)

# 시간 계산 (KST 기준)
now_kst = datetime.now(timezone(timedelta(hours=9)))
today = now_kst.date()
now_total = now_kst.hour * 60 + now_kst.minute
if now_total < 420: now_total += 1440 # 07:00 이전은 전날 근무 연장

# --- 3. 데이터 핸들링 ---
def load_vac():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df.sort_values('날짜')
    return pd.DataFrame(columns=['날짜', '이름', '사유'])

if 'vac_df' not in st.session_state:
    st.session_state.vac_df = load_vac()

# --- 4. 사이드바 메뉴 ---
with st.sidebar:
    st.header("⚙️ 메뉴")
    menu = st.radio("이동", ["📍 실시간 상황판", "📅 근무 편성표", "🌴 연차 신청/관리"])
    user_focus = st.selectbox("👤 본인 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])
    st.divider()
    view_start = st.date_input("조회 시작일", value=today - timedelta(days=3))
    view_days = st.slider("조회 일수", 7, 60, 21)

# --- 5. [메뉴] 실시간 상황판 (2x2 카드 + 1시간 단위 표) ---
if menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>📍 실시간 근무 현황</div>", unsafe_allow_html=True)
    
    diff = (today - PATTERN_START).days
    if diff % 3 == 0:
        # 사용자 원본 로직 기반 근무자 배정
        sc = diff // 3
        ci, is_2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: h_n, a_n, b_n = "김태언", ("이정석" if is_2 else "이태원"), ("이태원" if is_2 else "이정석")
        elif ci == 1: h_n, a_n, b_n = "이정석", ("이태원" if is_2 else "김태언"), ("김태언" if is_2 else "이태원")
        else: h_n, a_n, b_n = "이태원", ("이정석" if is_2 else "김태언"), ("김태언" if is_2 else "이정석")

        # 1시간 단위 스케줄 (취침시간 포함 24시간 쪼개기)
        sched_1h = [
            ("07:00", "08:00", "안내실", "로비", "로비", "휴게"),
            ("08:00", "09:00", "안내실", "휴게", "휴게", "로비"),
            ("09:00", "10:00", "안내실", "순찰", "휴게", "로비"),
            ("10:00", "11:00", "휴게", "안내실", "로비", "순찰/휴"),
            ("11:00", "12:00", "안내실", "중식", "로비", "중식"),
            ("12:00", "13:00", "중식", "안내실", "중식", "로비"),
            ("13:00", "14:00", "안내실", "휴게", "순찰/로", "로비"),
            ("14:00", "15:00", "순찰", "안내실", "로비", "휴게"),
            ("15:00", "16:00", "안내실", "휴게", "로비", "휴게"),
            ("16:00", "17:00", "휴게", "안내실", "휴게", "로비"),
            ("17:00", "18:00", "안내실", "휴게", "휴게", "로비"),
            ("18:00", "19:00", "안내실", "석식", "로비", "석식"),
            ("19:00", "20:00", "안내실", "안내실", "석식", "로비"),
            ("20:00", "21:00", "석식", "안내실", "로비", "휴게"),
            ("21:00", "22:00", "안내실", "순찰", "로비", "휴게"),
            ("22:00", "23:00", "순찰", "휴게", "순찰", "로비"),
            ("23:00", "00:00", "안내실", "취침", "취침", "로비"),
            ("00:00", "01:40", "안내실", "취침", "취침", "로비"), # 취침 구간
            ("01:40", "05:00", "취침", "안내실", "로비", "취침"),
            ("05:00", "06:00", "안내실", "순찰", "로비", "순찰"),
            ("06:00", "07:00", "안내실", "안내실", "휴게", "로비")
        ]
        
        # 현재 상태 카드 (2x2)
        curr = next((r for r in sched_1h if (int(r[0][:2])*60+int(r[0][3:])) <= now_total < (int(r[1][:2])*60+int(r[1][3:]) if r[1]!="00:00" else 1440)), sched_1h[-1])
        st.markdown(f"""
        <div class="grid-container">
            <div class="card"><div class="card-title">조장(황재업)</div><div class="card-value">{curr[2]}</div></div>
            <div class="card"><div class="card-title">성희({h_n})</div><div class="card-value">{curr[3]}</div></div>
            <div class="card"><div class="card-title">의산A({a_n})</div><div class="card-value">{curr[4]}</div></div>
            <div class="card"><div class="card-title">의산B({b_n})</div><div class="card-value">{curr[5]}</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.divider()
        # 시간표 가독성 처리
        df_s = pd.DataFrame(sched_1h, columns=["From", "To", "조장", "대원", "의산A", "의산B"])
        def hl_row(row):
            s = int(row['From'][:2])*60 + int(row['From'][3:])
            e = int(row['To'][:2])*60 + int(row['To'][3:])
            if e <= s: e += 1440
            return ['background-color: #e9ecef; font-weight: bold'] * 6 if s <= now_total < e else [''] * 6
        st.dataframe(df_s.style.apply(hl_row, axis=1), use_container_width=True, hide_index=True)
    else: st.warning("오늘은 비번입니다.")

# --- 6. [메뉴] 근무 편성표 (연차 반영) ---
elif menu == "📅 근무 편성표":
    st.markdown("<div class='main-title'>📅 C조 월간 근무편성표</div>", unsafe_allow_html=True)
    cal = []
    curr_d = view_start
    while curr_d <= view_start + timedelta(days=view_days):
        d_diff = (curr_d - PATTERN_START).days
        if d_diff % 3 == 0:
            sc = d_diff // 3
            ci, i2 = (sc // 2) % 3, sc % 2 == 1
            if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
            elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
            else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
            
            # 연차 데이터 대조
            v_list = st.session_state.vac_df[st.session_state.vac_df['날짜'] == curr_d]['이름'].tolist()
            cal.append({
                "날짜": curr_d.strftime("%m/%d(%a)"),
                "조장": "황재업",
                "성희": f"🌴{h}" if h in v_list else h,
                "의산A": f"🌴{a}" if a in v_list else a,
                "의산B": f"🌴{b}" if b in v_list else b
            })
        curr_d += timedelta(days=1)
    
    df_cal = pd.DataFrame(cal)
    def style_cal(v):
        if user_focus != "안 함" and str(v).replace("🌴", "") == user_focus: return 'background-color: #FFF9C4;'
        return ''
    st.dataframe(df_cal.style.applymap(style_cal), use_container_width=True, hide_index=True)

# --- 7. [메뉴] 연차 관리 (입력/조회/보안삭제) ---
elif menu == "🌴 연차 신청/관리":
    st.markdown("<div class='main-title'>🌴 연차 신청 및 현황</div>", unsafe_allow_html=True)
    
    with st.expander("➕ 새 연차 신청"):
        with st.form("add_v"):
            d, n = st.date_input("날짜", value=today), st.selectbox("성함", ["이태원", "김태언", "이정석"])
            if st.form_submit_button("신청하기"):
                st.session_state.vac_df = pd.concat([st.session_state.vac_df, pd.DataFrame([{"날짜": d, "이름": n}])]).drop_duplicates()
                st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()

    st.subheader("📋 전체 연차 목록")
    st.dataframe(st.session_state.vac_df, use_container_width=True, hide_index=True)

    st.divider()
    with st.expander("🔐 관리자 수정/삭제"):
        pw = st.text_input("비밀번호", type="password")
        if pw == ADMIN_PW:
            for idx, row in st.session_state.vac_df.iterrows():
                c1, c2 = st.columns([4, 1])
                c1.write(f"{row['날짜']} - {row['이름']}")
                if c2.button("삭제", key=f"del_{idx}"):
                    st.session_state.vac_df = st.session_state.vac_df.drop(idx)
                    st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()
