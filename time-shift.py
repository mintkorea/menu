import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# --- 1. 기본 설정 및 로직 ---
START_DATE = datetime(2026, 3, 24).date()
RANK = ["김태언", "이태원", "이정석"]  # 선임 -> 후임
HALL_ROTATION = ["김태언", "이정석", "이태원"] # 회관 2회 연속
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "이정석": "#FFFDE7", "김태언": "#E8F5E9"}

def get_daily_layout(target_date):
    diff = (target_date - START_DATE).days
    if diff % 3 != 0: return None
    seq = (diff // 3) + 5 
    hall_worker = HALL_ROTATION[(seq // 2) % 3]
    others = [p for p in RANK if p != hall_worker]
    if seq % 2 == 0: return hall_worker, others[0], others[1]
    else: return hall_worker, others[1], others[0]

# --- 2. UI 설정 ---
st.set_page_config(page_title="성의교정 C조", layout="centered")

with st.sidebar:
    st.header("👤 설정")
    menu = st.radio("메뉴", ["📅 근무 편성표", "📍 오늘 상황판"])
    selected_user = st.selectbox("강조할 이름 선택", ["안 함", "황재업"] + RANK)

# --- 3. HTML/CSS 스타일링 함수 (핵심) ---
def render_styled_table(df, highlight_name):
    # 요일별 색상 및 강조 색상 적용 로직
    def apply_styles(row):
        styles = ['text-align: center; border: 1px solid #ddd; padding: 8px;'] * len(row)
        
        # 1. 요일 색상 (날짜 컬럼 기준)
        if "토" in row["날짜"]: styles[0] += " color: #1E88E5; font-weight: bold;"
        elif "일" in row["날짜"]: styles[0] += " color: #E53935; font-weight: bold;"
        
        # 2. 이름 강조 (행 전체 배경색)
        if highlight_name != "안 함" and highlight_name in row.values:
            bg_color = WORKER_COLORS.get(highlight_name, "#f9f9f9")
            for i in range(len(styles)):
                styles[i] += f" background-color: {bg_color}; font-weight: bold;"
        
        return styles

    # Pandas Styler 적용
    styled = df.style.apply(apply_styles, axis=1)
    
    # HTML로 변환하여 출력 (중앙 정렬 CSS 포함)
    html = styled.hide(axis='index').to_html()
    st.write(f"""
        <style>
            table {{ margin-left: auto; margin-right: auto; width: 100%; border-collapse: collapse; }}
            th {{ background-color: #f2f2f2; text-align: center !important; padding: 10px; border: 1px solid #ddd; }}
        </style>
        {html}
    """, unsafe_allow_html=True)

# --- 4. 메인 화면 ---
if menu == "📅 근무 편성표":
    st.markdown("<h3 style='text-align:center;'>📅 성의교정 C조 근무 편성표</h3>", unsafe_allow_html=True)
    
    data = []
    for i in range(60):
        d = START_DATE + timedelta(days=i)
        res = get_daily_layout(d)
        if res:
            h, a, b = res
            data.append({
                "날짜": f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][d.weekday()]})",
                "조장": "황재업", "회관": h, "의산A": a, "의산B": b
            })
    
    render_styled_table(pd.DataFrame(data), selected_user)

elif menu == "📍 오늘 상황판":
    st.markdown("<h3 style='text-align:center;'>📍 C조 실시간 상황판</h3>", unsafe_allow_html=True)
    sel_date = st.date_input("날짜 선택", datetime.now().date())
    res = get_daily_layout(sel_date)
    
    if res:
        h, a, b = res
        st.info(f"📅 **{sel_date} 근무자:** 조장(황재업), 회관({h}), 의산A({a}), 의산B({b})")
        
        # 실제 시간표 데이터
        board_data = pd.DataFrame([
            {"시간": "07:00", "황재업(조)": "안내실", f"{h}(회)": "로비", f"{a}(A)": "휴게", f"{b}(B)": "로비"},
            {"시간": "08:00", "황재업(조)": "안내실", f"{h}(회)": "휴게", f"{a}(A)": "로비", f"{b}(B)": "휴게"},
            {"시간": "09:00", "황재업(조)": "안내실", f"{h}(회)": "순찰", f"{a}(A)": "로비", f"{b}(B)": "휴게"},
            {"시간": "10:00", "황재업(조)": "휴게", f"{h}(회)": "안내실", f"{a}(A)": "순찰/휴", f"{b}(B)": "로비"},
        ])
        
        # 상황판은 날짜가 없으므로 첫 번째 열 요일 색상 제외하고 렌더링
        html_board = board_data.style.apply(lambda row: [f"text-align: center; border: 1px solid #ddd; background-color: {WORKER_COLORS.get(selected_user) if selected_user in row.values else 'white'};" for _ in row], axis=1).hide(axis='index').to_html()
        st.write(f"<style>table {{ margin: auto; width: 100%; }} th {{ text-align: center !important; }}</style>{html_board}", unsafe_allow_html=True)
    else:
        st.warning("오늘은 C조 비번입니다.")
