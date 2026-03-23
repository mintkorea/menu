import streamlit as st
from datetime import datetime, timedelta

# --- 1. 기본 데이터 및 로직 (사용자 규칙 완벽 반영) ---
START_DATE = datetime(2026, 3, 24).date()
RANK = ["김태언", "이태원", "이정석"]  # 선임 -> 후임 서열
HALL_ROTATION = ["김태언", "이정석", "이태원"] # 회관 근무 순서
WORKER_COLORS = {"황재업": "#E1F5FE", "이태원": "#F3E5F5", "이정석": "#FFFDE7", "김태언": "#E8F5E9"}

def get_daily_layout(target_date):
    diff = (target_date - START_DATE).days
    if diff % 3 != 0: return None
    # 이미지 흐름에 맞춘 순번 계산 (3/27부터 김태언 2회 시작)
    seq = (diff // 3) + 5 
    hall_worker = HALL_ROTATION[(seq // 2) % 3]
    others = [p for p in RANK if p != hall_worker]
    # 1회차 선임A-후임B, 2회차 맞교대
    if seq % 2 == 0: return hall_worker, others[0], others[1]
    else: return hall_worker, others[1], others[0]

# --- 2. UI 및 CSS ---
st.set_page_config(page_title="성의교정 C조", layout="centered")

with st.sidebar:
    st.header("👤 설정")
    menu = st.radio("메뉴", ["📅 근무 편성표", "📍 오늘 상황판"])
    selected_user = st.selectbox("강조할 이름 선택", ["안 함", "황재업"] + RANK)

# --- 3. 직접 HTML 생성 함수 (중앙 정렬 및 색상 고정) ---
def build_html_table(data_list, highlight_name):
    # 테이블 헤더
    html = """
    <style>
        .custom-table { width: 100%; border-collapse: collapse; margin: 20px 0; font-size: 16px; text-align: center; }
        .custom-table th { background-color: #f8f9fa; padding: 12px; border: 1px solid #dee2e6; }
        .custom-table td { padding: 12px; border: 1px solid #dee2e6; text-align: center !important; }
        .sat { color: #1E88E5; font-weight: bold; } /* 토요일 파랑 */
        .sun { color: #E53935; font-weight: bold; } /* 일요일 빨강 */
    </style>
    <table class="custom-table">
        <thead>
            <tr><th>날짜</th><th>조장</th><th>회관</th><th>의산A</th><th>의산B</th></tr>
        </thead>
        <tbody>
    """
    
    for row in data_list:
        # 강조 색상 결정
        bg_style = ""
        if highlight_name != "안 함" and highlight_name in row.values():
            bg_color = WORKER_COLORS.get(highlight_name, "#ffffff")
            bg_style = f'style="background-color: {bg_color}; font-weight: bold;"'
        
        # 요일 클래스 결정
        day_class = ""
        if "토" in row["날짜"]: day_class = 'class="sat"'
        elif "일" in row["날짜"]: day_class = 'class="sun"'
        
        html += f"""
            <tr {bg_style}>
                <td {day_class}>{row['날짜']}</td>
                <td>{row['조장']}</td>
                <td>{row['회관']}</td>
                <td>{row['의산A']}</td>
                <td>{row['의산B']}</td>
            </tr>
        """
    
    html += "</tbody></table>"
    return html

# --- 4. 메인 화면 출력 ---
if menu == "📅 근무 편성표":
    st.markdown("<h2 style='text-align:center;'>📅 성의교정 C조 근무편성표</h2>", unsafe_allow_html=True)
    
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
    
    # HTML 직접 렌더링 (가장 확실함)
    st.write(build_html_table(display_data, selected_user), unsafe_allow_html=True)

elif menu == "📍 오늘 상황판":
    st.markdown("<h2 style='text-align:center;'>📍 C조 실시간 상황판</h2>", unsafe_allow_html=True)
    # 상황판도 동일한 방식으로 시간대별 데이터 구축 가능
    st.info("편성표의 로직과 강조 기능이 정상 작동하는지 먼저 확인해주세요.")
