import streamlit as st
import pandas as pd
import re
from collections import Counter

st.set_page_config(page_title="카톡 게시판 시스템", layout="wide")

# ---------------------------
# 1. 카톡 TXT 파싱
# ---------------------------
def parse_kakao(text):
    lines = text.split("\n")
    data = []
    current = None

    for line in lines:
        if "," in line and ":" in line:
            try:
                date_part, rest = line.split(",", 1)
                user, message = rest.split(":", 1)

                current = {
                    "datetime": date_part.strip(),
                    "user": user.strip(),
                    "message": message.strip()
                }
                data.append(current)
            except:
                continue
        else:
            if current:
                current["message"] += " " + line.strip()

    return pd.DataFrame(data)

# ---------------------------
# 2. 요약
# ---------------------------
def summarize(messages):
    text = " ".join(messages)
    words = re.findall(r'\w+', text)
    keywords = Counter(words)

    top_keywords = [k for k, v in keywords.most_common(5)]
    summary = " / ".join(top_keywords) if top_keywords else "요약 없음"

    return summary, top_keywords

# ---------------------------
# 3. 토픽 분류
# ---------------------------
def classify(msg):
    if "회의" in msg:
        return "회의"
    elif "공지" in msg:
        return "공지"
    elif "자료" in msg or "파일" in msg:
        return "업무"
    elif "일정" in msg:
        return "일정"
    else:
        return "일반"

# ---------------------------
# UI 시작
# ---------------------------
st.title("📊 카카오톡 게시판 시스템")

uploaded = st.file_uploader("📂 카톡 TXT 업로드", type="txt")

if uploaded:
    text = uploaded.read().decode("utf-8")
    df = parse_kakao(text)

    # 방어
    if df.empty or "message" not in df.columns:
        st.error("❌ 파일 형식 인식 실패")
        st.stop()

    # 세션 상태 저장 (이동 기능용)
    if "df" not in st.session_state:
        df["topic"] = df["message"].apply(classify)
        df["date"] = df["datetime"].apply(lambda x: x.split(",")[0] if "," in x else x)
        st.session_state.df = df

    df = st.session_state.df

    # ---------------------------
    # 탭 (게시판)
    # ---------------------------
    topics = ["전체"] + sorted(df["topic"].unique().tolist())
    tabs = st.tabs(topics)

    for i, topic in enumerate(topics):
        with tabs[i]:
            if topic == "전체":
                filtered = df
            else:
                filtered = df[df["topic"] == topic]

            if filtered.empty:
                st.write("데이터 없음")
                continue

            grouped = filtered.groupby("date")

            for date, group in grouped:
                st.markdown(f"## 📅 {date}")

                summary, keywords = summarize(group["message"].tolist())

                st.markdown("### 🧠 요약")
                st.info(summary)

                st.markdown("### 🏷 키워드")
                st.write(", ".join(keywords) if keywords else "없음")

                # 원본보기 + 이동기능
                with st.expander("📄 원본보기"):
                    for idx, row in group.iterrows():
                        col1, col2 = st.columns([4,1])

                        with col1:
                            st.write(f"**[{row['topic']}] {row['user']}**: {row['message']}")

                        with col2:
                            new_topic = st.selectbox(
                                "이동",
                                ["회의", "공지", "업무", "일정", "일반"],
                                key=f"{idx}"
                            )

                            if st.button("변경", key=f"btn_{idx}"):
                                st.session_state.df.at[idx, "topic"] = new_topic
                                st.success("이동 완료")
                                st.rerun()

                st.divider()
