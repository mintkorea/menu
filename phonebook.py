import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import calendar

# 1. 기본 데이터 (25명 명단)
CONTACT_DATA = [
    {"근무지": "성의교정", "조별": "공통", "직위": "보안소장", "성명": "이규용", "연락처": "010-8883-6580"},
    {"근무지": "성의교정", "조별": "공통", "직위": "보안부소장", "성명": "박상현", "연락처": "010-3193-4603"},
    {"근무지": "성의교정", "조별": "공통", "직위": "보안반장", "성명": "유정수", "연락처": "010-5316-8065"},
    {"근무지": "옴니버스", "조별": "공통", "직위": "보안반장", "성명": "오제준", "연락처": "010-3352-8933"},
    {"근무지": "성의기숙사", "조별": "공통", "직위": "보안반장", "성명": "이강택", "연락처": "010-9048-6708"},
    {"근무지": "성의회관", "조별": "A조", "직위": "보안조장", "성명": "배준용", "연락처": "010-4717-7065"},
    {"근무지": "성의회관", "조별": "A조", "직위": "보안조원", "성명": "이명구", "연락처": "010-8638-5819"},
    {"근무지": "의산연", "조별": "A조", "직위": "보안조원", "성명": "김영중", "연락처": "010-7726-5963"},
    {"근무지": "의산연", "조별": "A조", "직위": "보안조원", "성명": "김삼동", "연락처": "010-2345-8081"},
    {"근무지": "성의회관", "조별": "B조", "직위": "보안조장", "성명": "심규천", "연락처": "010-8287-9895"},
    {"근무지": "성의회관", "조별": "B조", "직위": "보안조원", "성명": "임종현", "연락처": "010-7741-6732"},
    {"근무지": "의산연", "조별": "B조", "직위": "보안조원", "성명": "권영국", "연락처": "010-4085-9982"},
    {"근무지": "의산연", "조별": "B조", "직위": "보안조원", "성명": "전준수", "연락처": "010-5687-7107"},
    {"근무지": "성의회관", "조별": "C조", "직위": "보안조장", "성명": "황재업", "연락처": "010-9278-6622"},
    {"근무지": "성의회관", "조별": "C조", "직위": "보안조원", "성명": "이태원", "연락처": "010-9265-7881"},
    {"근무지": "의산연", "조별": "C조", "직위": "보안조원", "성명": "김태언", "연락처": "010-5386-5386"},
    {"근무지": "의산연", "조별": "C조", "직위": "보안조원", "성명": "이정석", "연락처": "010-2417-1173"},
    {"근무지": "옴니버스", "조별": "A조", "직위": "보안조장", "성명": "손병휘", "연락처": "010-9966-2090"},
    {"근무지": "옴니버스", "조별": "A조", "직위": "보안조원", "성명": "권순호", "연락처": "010-2539-1799"},
    {"근무지": "옴니버스", "조별": "A조", "직위": "보안조원", "성명": "김진식", "연락처": "010-3277-0808"},
    {"근무지": "옴니버스", "조별": "B조", "직위": "보안조장", "성명": "황일범", "연락처": "010-8929-4294"},
    {"근무지": "옴니버스", "조별": "B조", "직위": "보안조원", "성명": "이상길", "연락처": "010-9904-0247"},
    {"근무지": "옴니버스", "조별": "B조", "직위": "보안조원", "성명": "허용", "연락처": "010-8845-0163"},
    {"근무지": "옴니버스", "조별": "C조", "직위": "보안조장", "성명": "피재영", "연락처": "010-9359-2569"},
    {"근무지": "옴니버스", "조별": "C조", "직위": "보안조원", "성명": "남형민", "연락처": "010-8767-7073"},
    {"근무지": "옴니버스", "조별": "C조", "직위": "보안조원", "성명": "강경훈", "연락처": "010-3436-6107"},
    {"근무지": "성의기숙사", "조별": "기숙사", "직위": "보안조원", "성명": "유시균", "연락처": "010-8737-5770"},
    {"근무지": "성의기숙사", "조별": "기숙사", "직위": "보안조원", "성명": "이상헌", "연락처": "010-4285-4231"},
]

# 앱 설정
st.set_page_config(page_title="보안팀 통합 관리", layout="wide")

# 세션 데이터 (연차 정보)
if 'leave_db' not in st.session_state:
    st.session_state.leave_db = pd.DataFrame(columns=['날짜', '성명', '맞대근자'])

# CSS 스타일 (마우스 온 효과 및 그리드)
st.markdown("""
<style>
    .contact-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 10px; }
    .contact-card {
        background-color: #ffffff; border: 1px solid #ddd; border-radius: 10px;
        padding: 15px; text-align: center; transition: 0.3s; height: 100px;
        display: flex; flex-direction: column; justify-content: center; align-items: center;
    }
    .contact-card:hover { background-color: #2e7d32; color: white; }
    .phone-info { display: none; font-size: 0.8em; font-weight: bold; }
    .contact-card:hover .name-info { display: none; }
    .contact-card:hover .phone-info { display: block; }
    .call-btn { 
        color: #ffeb3b !important; text-decoration: none; border: 1px solid #ffeb3b; 
        padding: 2px 8px; border-radius: 5px; margin-top: 8px; display: inline-block; 
    }
</style>
""", unsafe_allow_html=True)

# 탭 구성
tabs = st.tabs(["📱 비상연락망", "📝 연차신청", "📅 연차현황판", "🗓️ C조 근무표"])

# --- TAB 1: 비상연락망 ---
with tabs[0]:
    df_contacts = pd.DataFrame(CONTACT_DATA)
    selected_group = st.selectbox("조별 필터", ["전체"] + list(df_contacts['조별'].unique()))
    
    display_df = df_contacts if selected_group == "전체" else df_contacts[df_contacts['조별'] == selected_group]
    
    grid_html = '<div class="contact-grid">'
    for _, row in display_df.iterrows():
        p_link = f"tel:{row['연락처'].replace('-', '')}"
        grid_html += f"""
        <div class="contact-card">
            <div class="name-info">
                <div style="font-weight:bold;">{row['성명']}</div>
                <div style="font-size:0.7em;">{row['직위']}</div>
            </div>
            <div class="phone-info">
                {row['연락처']}<br>
                <a href="{p_link}" class="call-btn">📞 통화</a>
            </div>
        </div>
        """
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

# --- TAB 2: 연차신청 ---
with tabs[1]:
    st.subheader("연차 등록")
    with st.form("l_form"):
        name = st.selectbox("신청자", df_contacts['성명'].unique())
        l_date = st.date_input("날짜", datetime.now())
        sub_name = st.text_input("맞대근자")
        if st.form_submit_button("등록"):
            new_row = pd.DataFrame([[l_date.strftime('%Y-%m-%d'), name, sub_name]], columns=['날짜', '성명', '맞대근자'])
            st.session_state.leave_db = pd.concat([st.session_state.leave_db, new_row]).drop_duplicates()
            st.success("등록 완료")

# --- TAB 3: 연차현황판 ---
with tabs[2]:
    now = datetime.now()
    month = st.selectbox("월 선택", range(1, 13), index=now.month-1)
    
    last_day = calendar.monthrange(now.year, month)[1]
    days = [f"{month}/{d:02d}" for d in range(1, last_day + 1)]
    matrix = pd.DataFrame("", index=df_contacts['성명'].unique(), columns=days)
    
    for _, r in st.session_state.leave_db.iterrows():
        dt = datetime.strptime(r['날짜'], '%Y-%m-%d')
        if dt.month == month:
            matrix.at[r['성명'], f"{month}/{dt.day:02d}"] = "연차"
    
    st.dataframe(matrix.style.applymap(lambda x: 'background-color: #ffcdd2' if x == "연차" else ''))

# --- TAB 4: C조 근무표 (ABC 순환 로직) ---
with tabs[3]:
    st.subheader("🗓️ C조 월간 근무편성")
    start_date = st.date_input("편성 시작일", datetime(2026, 3, 1))
    period = st.number_input("편성 일수", 30, 90, 31)
    
    c_names = ["김태언", "이정석", "이태원"] # 순환 대상자
    schedule = []
    
    for i in range(period):
        curr = start_date + timedelta(days=i)
        curr_str = curr.strftime('%Y-%m-%d')
        
        # 기본 순환 (2회씩)
        base = (i // 2) % 3
        a_p, b_p, c_p = c_names[base], c_names[(base+1)%3], c_names[(base+2)%3]
        if i % 2 == 1: b_p, c_p = c_p, b_p # B, C 교대
            
        # 연차 반영
        leave_row = st.session_state.leave_db[st.session_state.leave_db['날짜'] == curr_str]
        leave_info, sub_info = "", ""
        if not leave_row.empty:
            leave_info = leave_row.iloc[0]['성명']
            sub_info = leave_row.iloc[0]['맞대근자']
            if leave_info in [a_p, b_p, c_p]: a_p = leave_info # 연차자는 A로 고정
            
        schedule.append([curr.strftime('%m/%d(%a)'), "황재업", a_p, b_p, c_p, leave_info, sub_info])

    df_sch = pd.DataFrame(schedule, columns=["일자", "조장", "A(회관)", "B(의산연)", "C(의산연)", "연차", "맞대근"])
    st.dataframe(df_sch)
    
    # 엑셀 다운로드
    csv = df_sch.to_csv(index=False).encode('utf-8-sig')
    st.download_button("엑셀 다운로드", csv, "근무표.csv", "text/csv")
