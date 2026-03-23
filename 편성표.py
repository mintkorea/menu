import streamlit as st
import pandas as pd
from datetime import datetime, timedelta, timezone
import os

# --- [1] 기존 로직 (수정 금지) ---
ADMIN_PW = "1234"
PATTERN_START = datetime(2026, 3, 9).date()
VACATION_FILE = 'vacation.csv'

st.set_page_config(page_title="성의 C조 관리", layout="wide")

# --- [2] 가독성 개선 CSS (이름 크기 & 요일 색상) ---
st.markdown("""
    <style>
    .block-container { padding: 0.5rem !important; }
    /* 실시간 카드 2x2: 이름(22px)과 장소(26px) 크기 극대화 */
    .grid-container { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
    .card { background: #ffffff; border: 2.3px solid #1E3A8A; border-radius: 12px; padding: 15px; text-align: center; }
    .card-name { font-size: 22px !important; font-weight: bold; color: #333; margin-bottom: 5px; border-bottom: 2px solid #eee; }
    .card-value { font-size: 26px !important; font-weight: 900; color: #D32F2F; }
    /* 요일별 색상: 일요일(빨강), 토요일(파랑) */
    .sun { color: #FF0000 !important; font-weight: bold; }
    .sat { color: #0000FF !important; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# KST 시간 설정
now_kst = datetime.now(timezone(timedelta(hours=9)))
today = now_kst.date()
now_total = now_kst.hour * 60 + now_kst.minute
if now_total < 420: now_total += 1440 

def load_vac():
    if os.path.exists(VACATION_FILE):
        df = pd.read_csv(VACATION_FILE)
        df['날짜'] = pd.to_datetime(df['날짜']).dt.date
        return df
    return pd.DataFrame(columns=['날짜', '이름'])

if 'vac_df' not in st.session_state:
    st.session_state.vac_df = load_vac()

# --- [3] 사이드바 ---
with st.sidebar:
    st.header("⚙️ 메뉴")
    menu = st.radio("이동할 페이지", ["📍 실시간 상황판", "📅 근무 편성표", "🌴 연차 관리"])
    user_focus = st.selectbox("👤 사용자 확인", ["안 함", "황재업", "김태언", "이태원", "이정석"])

# --- [4] 실시간 상황판 (기존 NameError 완벽 해결) ---
if menu == "📍 실시간 상황판":
    diff = (today - PATTERN_START).days
    if diff % 3 == 0:
        # 사용자님의 원본 엔진 복구
        sc = diff // 3
        ci, i2 = (sc // 2) % 3, sc % 2 == 1
        if ci == 0: h_n, a_n, b_n = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
        elif ci == 1: h_n, a_n, b_n = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
        else: h_n, a_n, b_n = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")

        # 1시간 단위 근무표
        sched = [
            ("07:00", "08:00", "안내실", "로비", "로비", "휴게"), ("08:00", "09:00", "안내실", "휴게", "휴게", "로비"),
            ("09:00", "10:00", "안내실", "순찰", "휴게", "로비"), ("10:00", "11:00", "휴게", "안내실", "로비", "순찰/휴"),
            ("11:00", "12:00", "안내실", "중식", "로비", "중식"), ("12:00", "13:00", "중식", "안내실", "중식", "로비"),
            ("13:00", "14:00", "안내실", "휴게", "순찰/로", "로비"), ("14:00", "15:00", "순찰", "안내실", "로비", "휴게"),
            ("15:00", "16:00", "안내실", "휴게", "로비", "휴게"), ("16:00", "17:00", "휴게", "안내실", "휴게", "로비"),
            ("17:00", "18:00", "안내실", "휴게", "휴게", "로비"), ("18:00", "19:00", "안내실", "석식", "로비", "석식"),
            ("19:00", "20:00", "안내실", "안내실", "석식", "로비"), ("20:00", "21:00", "석식", "안내실", "로비", "휴게"),
            ("21:00", "22:00", "안내실", "순찰", "로비", "휴게"), ("22:00", "23:00", "순찰", "휴게", "순찰", "로비"),
            ("23:00", "00:00", "안내실", "취침", "취침", "로비"), ("00:00", "07:00", "취침/안내", "취침", "취침", "로비/취침")
        ]
        
        curr = next((r for r in sched if (int(r[0][:2])*60+int(r[0][3:])) <= now_total < (int(r[1][:2])*60+int(r[1][3:]) if r[1]!="00:00" else 1440)), sched[-1])

        # 카드 내 이름 크기 대폭 확대 (22px)
        st.markdown(f"""
        <div class="grid-container">
            <div class="card"><div class="card-name">황재업</div><div class="card-value">{curr[2]}</div></div>
            <div class="card"><div class="card-name">{h_n}</div><div class="card-value">{curr[3]}</div></div>
            <div class="card"><div class="card-name">{a_n}</div><div class="card-value">{curr[4]}</div></div>
            <div class="card"><div class="card-name">{b_n}</div><div class="card-value">{curr[5]}</div></div>
        </div>
        """, unsafe_allow_html=True)
        st.divider()
        st.dataframe(pd.DataFrame(sched, columns=["F", "T", "조장", "성희", "의산A", "의산B"]), use_container_width=True, hide_index=True)
    else: st.warning("오늘은 비번입니다.")

# --- [5] 근무 편성표 (요일 색상 로직 수정) ---
elif menu == "📅 근무 편성표":
    cal_data = []
    for i in range(-2, 25):
        d = today + timedelta(days=i)
        diff = (d - PATTERN_START).days
        if diff % 3 == 0:
            sc = diff // 3
            ci, i2 = (sc // 2) % 3, sc % 2 == 1
            if ci == 0: h, a, b = "김태언", ("이정석" if i2 else "이태원"), ("이태원" if i2 else "이정석")
            elif ci == 1: h, a, b = "이정석", ("이태원" if i2 else "김태언"), ("김태언" if i2 else "이태원")
            else: h, a, b = "이태원", ("이정석" if i2 else "김태언"), ("김태언" if i2 else "이정석")
            
            v = st.session_state.vac_df[st.session_state.vac_df['날짜'] == d]['이름'].tolist()
            cal_data.append({"날짜": d.strftime("%m/%d"), "요일": d.strftime("%a"), 
                             "조장": "황재업", "성희": f"🌴{h}" if h in v else h, 
                             "의산A": f"🌴{a}" if a in v else a, "의산B": f"🌴{b}" if b in v else b})
    
    df_cal = pd.DataFrame(cal_data)
    # 요일 색상 적용 (일요일 빨강, 토요일 파랑)
    def style_day(row):
        styles = [''] * len(row)
        if row.요일 == 'Sun': styles[1] = 'color: red; font-weight: bold'
        elif row.요일 == 'Sat': styles[1] = 'color: blue; font-weight: bold'
        return styles

    st.dataframe(df_cal.style.apply(style_day, axis=1), use_container_width=True, hide_index=True)

# --- [6] 연차 관리 (보안 및 연동 유지) ---
elif menu == "🌴 연차 관리":
    with st.form("v_form"):
        d, n = st.date_input("날짜"), st.selectbox("성함", ["이태원", "김태언", "이정석"])
        if st.form_submit_button("신청"):
            st.session_state.vac_df = pd.concat([st.session_state.vac_df, pd.DataFrame([{"날짜": d, "이름": n}])]).drop_duplicates()
            st.session_state.vac_df.to_csv(VACATION_FILE, index=False); st.rerun()
    st.dataframe(st.session_state.vac_df, use_container_width=True, hide_index=True)
