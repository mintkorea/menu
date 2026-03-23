import streamlit as st
from datetime import datetime, timedelta

# --- 1. 기본 설정 및 로직 ---
START_DATE = datetime(2026, 3, 24).date()
RANK = ["김태언", "이태원", "이정석"]  # 선임 순서
HALL_ROTATION = ["김태언", "이정석", "이태원"] # 회관 순번
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
    st.header("⚙️ 설정")
    menu = st.radio("메뉴", ["📅 근무 편성표", "📍 오늘 상황판"])
    selected_user = st.selectbox("👤 이름 강조", ["안 함", "황재업"] + RANK)

# --- 3. HTML 생성 함수 (중앙 정렬 + 요일 색상 강제) ---
def render_custom_table(data_list, highlight_name):
    html = """
    <style>
        .custom-container { display: flex; justify-content: center; width: 100%; }
        .custom-table { width: 100%; border-collapse: collapse; font-family: sans-serif; }
        .custom-table th, .custom-table td { 
            border: 1px solid #ddd; padding: 10px; text-align: center !important; 
        }
        .custom-table th { background-color: #f4f4f4; font-weight: bold; }
        .sat { color: blue !important; font-weight: bold; }
        .sun { color: red !important; font-weight: bold; }
    </style>
    <div class='custom-container'>
    <table class='custom-table'>
        <thead>
            <tr><th>날짜</th><th>조장</th><th>회관</th><th>의산A</th><th>의산B</th></tr>
        </thead>
        <tbody>
    """
    
    for row in data_list:
        bg_color = WORKER_COLORS.get(highlight_name, "white") if highlight_name in row.values() else "white"
        row_style = f"style='background-color: {bg_color};'" if highlight_name in row.values() else ""
        
        day_class = ""
        if "토" in row["날짜"]: day_class = "class='sat'"
        elif "일" in row["날짜"]: day_class = "class='sun'"
        
        html += f"""
            <tr {row_style}>
                <td {day_class}>{row['날짜']}</td>
                <td>{row['조장']}</td>
                <td>{row['회관']}</td>
                <td>{row['의산A']}</td>
                <td>{row['의산B']}</td>
            </tr>
        """
    html += "</tbody></table></div>"
    # st.markdown의 unsafe_allow_html을 사용해야 태그가 깨지지 않습니다.
    st.markdown(html, unsafe_allow_html=True)

# --- 4. 메인 화면 ---
if menu == "📅 근무 편성표":
    st.markdown("<h2 style='text-align:center;'>성의교정 C조 근무편성표</h2>", unsafe_allow_html=True)
    
    display_data = []
    for i in range(45):
        d = START_DATE + timedelta(days=i)
        res = get_daily_layout(d)
        if res:
            h, a, b = res
            display_data.append({
                "날짜": f"{d.strftime('%m/%d')}({['월','화','수','목','금','토','일'][d.weekday()]})",
                "조장": "황재업", "회관": h, "의산A": a, "의산B": b
            })
    
    render_custom_table(display_data, selected_user)

elif menu == "📍 오늘 상황판":
    st.markdown("<h2 style='text-align:center;'>C조 실시간 근무 상황판</h2>", unsafe_allow_html=True)
    sel_date = st.date_input("조회 날짜", datetime.now().date())
    res = get_daily_layout(sel_date)
    
    if res:
        h, a, b = res
        st.success(f"📅 **{sel_date} 근무자:** 조장(황재업), 회관({h}), A({a}), B({b})")
        # 상황판 데이터 (예시)
        board = [{"시간": "07:00", "조": "안내실", "회": "로비", "A": "휴게", "B": "로비"}]
        # 상황판도 동일한 HTML 방식으로 렌더링하면 중앙정렬이 유지됩니다.
    else:
        st.warning("비번입니다.")
