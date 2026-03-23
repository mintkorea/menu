import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

# --- 1. 기본 및 보안 설정 ---
ADMIN_PW = "1234"
PATTERN_START = datetime(2026, 3, 9).date()
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의 C조 관리", layout="wide")

# --- 2. CSS: 가독성 끝판왕 (이름 크게, 요일 색상) ---
st.markdown("""
    <style>
    .block-container { padding: 0.5rem !important; }
    .main-title { font-size: 20px !important; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 10px; }
    /* 2x2 카드: 이름 크기 대폭 확대 */
    .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
    .card { background: #f8f9fa; border: 2px solid #1E3A8A; border-radius: 10px; padding: 12px; text-align: center; }
    .card-name { font-size: 18px !important; font-weight: bold; color: #333; margin-bottom: 5px; border-bottom: 1px solid #ddd; }
    .card-value { font-size: 22px !important; font-weight: 900; color: #D32F2F; } /* 장소 강조 */
    /* 요일 색상 */
    .sun { color: red !important; font-weight: bold; }
    .sat { color: blue !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# 시간 계산
now_kst = datetime.now(timezone(timedelta(hours=9)))
today = now_kst.date()
now_total = now_kst.hour * 60 + now_kst.minute
if now_total < 420: now_total += 1440 

# --- 3. 데이터 로드 ---
def load_vac():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df
    return pd.DataFrame(columns=['날짜', '이름'])

if 'vac_df' not in st.session_state:
    st.session_state.vac_df = load_vac()

# --- 4. 사이드바 메뉴 ---
with st.sidebar:
    st.header("⚙️ 메뉴")
    menu = st.radio("선택", ["📍 실시간 상황판", "📅 근무 편성표", "🌴 연차 관리"])
    user_focus = st.selectbox("👤 본인 강조", ["안 함", "황재업", "김태언", "이태원", "이정석"])
    st.divider()
    view_start = st.date_input("시작일", value=today - timedelta(days=2))
    view_days = st.slider("기간", 7, 60, 21)

# --- 5. [메뉴] 실시간 상황판 (2x2 + 1시간 단위) ---
if menu == "📍 실시간 상황판":
    st.markdown("<div class='main-title'>📍 현재 근무 위치</div>", unsafe_allow_html=True)
    
    diff = (today - PATTERN_START).days
    if diff % 3 == 0:
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: h_n, a_n, b_n = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: h_n, a_n, b_n = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: h_n, a_n, b_n = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")

        # 1시간 단위 데이터
        sched = [
            ("07:00", "08:00", "안내실", "로비", "로비", "휴게"), ("08:00", "09:00", "안내실", "휴게", "휴게", "로비"),
            ("09:00", "10:00", "안내실", "순찰", "휴게", "로비"), ("10:00", "11:00", "휴게", "안내실", "로비", "순찰/휴"),
            ("11:00", "12:00", "안내실", "중식", "로비", "중식"), ("12:00", "13:00", "중식", "안내실", "중식", "로비"),
            ("13:00", "14:00", "안내실", "휴게", "순찰/로", "로비"), ("14:00", "15:00", "순찰", "안내실", "로비", "휴게"),
            ("15:00", "16:00", "안내실", "휴게", "로비", "휴게"), ("16:00", "17:00", "휴게", "안내실", "휴게", "로비"),
            ("17:00", "18:00", "안내실", "휴게", "휴게", "로비"), ("18:00", "19:00", "안내실", "석식", "로비", "석식"),
            ("19:00", "20:00", "안내실", "안내실", "석식", "로비"), ("20:00", "21:00", "석식", "안내실", "로비", "휴게"),
            ("21:00", "22:00", "안내실", "순찰", "로비", "휴게"), ("22:00", "23:00", "순찰", "휴게", "순찰", "로비"),
            ("23:00", "00:00", "안내실", "취침", "취침", "로비"), ("00:00", "01:40", "안내실", "취침", "취침", "로비"),
            ("01:40", "03:00", "취침", "안내실", "로비", "취침"), ("03:00", "05:00", "취침", "안내실", "로비", "취침"),
            ("05:00", "06:00", "안내실", "순찰", "로비", "순찰"), ("06:00", "07:00", "안내실", "안내실", "휴게", "로비")
        ]
        
        curr = next((r for r in sched if (int(r[0][:2])*60+int(r[0][3:])) <= now_total < (int(r[1][:2])*60+int(r[1][3:]) if r[1]!="00:00" else 1440)), sched[-1])
        
        # 2x2 카드: 이름(상단), 장소(하단 강조)
        st.markdown(f"""
        <div class="grid-container">
            <div class="card"><div class="card-name">황재업</div><div class="card-value">{curr[2]}</div></div>
            <div class="card"><div class="card-name">{h_n}</div><div class="card-value">{curr[3]}</div></div>
            <div class="card"><div class="card-name">{a_n}</div><div class="card-value">{curr[4]}</div></div>
            <div class="card"><div class="card-name">{b_n}</div><div class="card-value">{curr[5]}</div></div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        st.dataframe(pd.DataFrame(sched, columns=["From", "To", "조장", "성희", "의산A", "의산B"]), use_container_width=True, hide_index=True)
    else: st.warning("오늘은 비번입니다.")

# --- 6. [메뉴] 근무 편성표 (요일 색상 적용) ---
elif menu == "📅 근무 편성표":
    st.markdown("<div class='main-title'>📅 C조 근무편성표</div>", unsafe_allow_html=True)
    cal = []
    c_d = view_start
    while c_d <= view_start + timedelta(days=view_days):
        diff = (c_d - PATTERN_START).days
        if diff % 3 == 0:
            sc = diff // 3
            ci, i2 = (sc // 2) % 3, sc % 2 == 1
            if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
            elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
            else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
            
            v = st.session_state.vac_df[st.session_state.vac_df['날짜'] == c_d]['이름'].tolist()
            cal.append({"날짜": c_d.strftime("%m/%d"), "요일": c_d.strftime("%a"), 
                        "조장": "황재업", "성희": f"🌴{h}" if h in v else h, 
                        "의산A": f"🌴{a}" if a in v else a, "의산B": f"🌴{b}" if b in v else b})
        c_d += timedelta(days=1)
    
    # 데이터프레임 스타일링 (요일 색상)
    def style_df(row):
        styles = [''] * len(row)
        if row['요일'] == 'Sun': styles[1] = 'color: red; font-weight: bold'
        elif row['요일'] == 'Sat': styles[1] = 'color: blue; font-weight: bold'
        return styles
    st.dataframe(pd.DataFrame(cal).style.apply(style_df, axis=1), use_container_width=True, hide_index=True)

# --- 7. [메뉴] 연차 관리 (누락 없이 통합) ---
elif menu == "🌴 연차 관리":
    st.markdown("<div class='main-title'>🌴 연차 신청 및 조회</div>", unsafe_allow_html=True)
    with st.form("v"):
        d, n = st.date_input("날짜"), st.selectbox("성함", ["이태원", "김태언", "이정석"])
        if st.form_submit_button("신청"):
            st.session_state.vac_df = pd.concat([st.session_state.vac_df, pd.DataFrame([{"날짜": d, "이름": n}])]).drop_duplicates()
            st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()
    st.dataframe(st.session_state.vac_df, use_container_width=True)
    with st.expander("🔐 삭제(관리자)"):
        if st.text_input("비번", type="password") == ADMIN_PW:
            for i, r in st.session_state.vac_df.iterrows():
                if st.button(f"삭제: {r['날짜']} {r['이름']}", key=i):
                    st.session_state.vac_df = st.session_state.vac_df.drop(i)
                    st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()
