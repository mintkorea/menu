import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

# 1. 25명 전체 명단 데이터 (이미지 기반 추출)
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
    {"근무지": "성의기숙사", "조별": "공통", "직위": "보안조원", "성명": "유시균", "연락처": "010-8737-5770"},
    {"근무지": "성의기숙사", "조별": "공통", "직위": "보안조원", "성명": "이상헌", "연락처": "010-4285-4231"},
]

# 페이지 설정
st.set_page_config(page_title="보안팀 관리 시스템", layout="wide")

# 세션 상태 초기화 (연차 데이터 임시 저장)
if 'leave_db' not in st.session_state:
    st.session_state.leave_db = pd.DataFrame(columns=['날짜', '성명', '맞대근자'])

# --- 스타일 정의 ---
st.markdown("""
<style>
    .contact-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(130px, 1fr)); gap: 12px; }
    .contact-card {
        background-color: #ffffff; border: 1px solid #e0e0e0; border-radius: 10px;
        padding: 15px; text-align: center; transition: 0.3s; cursor: pointer; height: 100px;
        display: flex; flex-direction: column; justify-content: center;
    }
    .contact-card:hover { background-color: #2e7d32; color: white; transform: translateY(-3px); }
    .phone-info { display: none; font-size: 0.8em; font-weight: bold; }
    .contact-card:hover .name-info { display: none; }
    .contact-card:hover .phone-info { display: block; }
    .call-btn { color: #ffeb3b; text-decoration: none; border: 1px solid #ffeb3b; padding: 2px 5px; border-radius: 5px; margin-top: 5px; display: inline-block; }
</style>
""", unsafe_allow_html=True)

# --- 메인 메뉴 ---
tab1, tab2, tab3 = st.tabs(["📱 비상연락망", "📝 연차신청", "📅 연차현황판"])

with tab1:
    st.subheader("📱 클릭/호버 시 전화연결")
    df_contacts = pd.DataFrame(CONTACT_DATA)
    groups = ["전체"] + list(df_contacts['조별'].unique())
    selected_group = st.selectbox("조별 필터", groups)
    
    display_df = df_contacts if selected_group == "전체" else df_contacts[df_contacts['조별'] == selected_group]
    
    grid_html = '<div class="contact-grid">'
    for _, row in display_df.iterrows():
        p_link = f"tel:{row['연락처'].replace('-', '')}"
        grid_html += f"""
        <div class="contact-card">
            <div class="name-info">
                <div style="font-weight:bold;">{row['성명']}</div>
                <div style="font-size:0.7em; color:gray;">{row['직위']}</div>
            </div>
            <div class="phone-info">
                {row['연락처']}<br>
                <a href="{p_link}" class="call-btn">📞 통화</a>
            </div>
        </div>
        """
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

with tab2:
    st.subheader("📝 연차 신청")
    with st.form("leave_form"):
        name = st.selectbox("신청자", df_contacts['성명'].unique())
        l_date = st.date_input("날짜")
        sub_name = st.text_input("맞대근자")
        if st.form_submit_button("등록"):
            new_data = pd.DataFrame([[str(l_date), name, sub_name]], columns=['날짜', '성명', '맞대근자'])
            st.session_state.leave_db = pd.concat([st.session_state.leave_db, new_data]).drop_duplicates()
            st.success("등록되었습니다.")

with tab3:
    st.subheader("📅 월간 연차 현황 (가로)")
    now = datetime.now()
    month = st.selectbox("월 선택", range(1, 13), index=now.month-1)
    
    last_day = calendar.monthrange(now.year, month)[1]
    days = [f"{month}/{d:02d}" for d in range(1, last_day + 1)]
    matrix = pd.DataFrame("", index=df_contacts['성명'].unique(), columns=days)
    
    for _, r in st.session_state.leave_db.iterrows():
        try:
            dt = datetime.strptime(r['날짜'], '%Y-%m-%d')
            if dt.month == month:
                d_str = f"{month}/{dt.day:02d}"
                matrix.at[r['성명'], d_str] = "연차"
        except: continue
        
    st.dataframe(matrix.style.applymap(lambda x: 'background-color: #ffcdd2' if x == '연차' else ''))
