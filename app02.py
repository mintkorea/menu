import streamlit as st
import pandas as pd
import re
from datetime import datetime
from collections import Counter

st.set_page_config(page_title="카톡 게시판", layout="wide")

# ---------------------------
# 1. 카톡 TXT 파싱
# ---------------------------
def parse_kakao(text):
    pattern = r"(\d{4}.\s\d{1,2}.\s\d{1,2}.\s오[전후]\s\d{1,2}:\d{2}),\s(.+?)\s:\s(.+)"
    matches = re.findall(pattern, text)

    data = []
    for m in matches:
        data.append({
            "datetime": m[0],
            "user": m[1],
            "message": m[2]
        })
    return pd.DataFrame(data)

# ---------------------------
# 2. 간단 요약
# ---------------------------
def summarize(messages):
    text = " ".join(messages)

    keywords = Counter(re.findall(r'\w+', text))
    top_keywords = [k for k, v in keywords.most_common(5)]

    summary = " / ".join(top_keywords)

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
    else:
        return "일반"

# ---------------------------
# UI
# ---------------------------
st.title("📊 카카오톡 요약 게시판")

uploaded = st.file_uploader("카톡 TXT 파일 업로드", type="txt")

if uploaded:
    text = uploaded.read().decode("utf-8")
    df = parse_kakao(text)

    # 토픽 분류
    df["topic"] = df["message"].apply(classify)

    # 날짜 컬럼
    df["date"] = df["datetime"].str.split(",").str[0]

    st.sidebar.title("🔍 필터")
    topic_filter = st.sidebar.multiselect("토픽 선택", df["topic"].unique(), default=df["topic"].unique())

    df = df[df["topic"].isin(topic_filter)]

    # 날짜별 그룹
    grouped = df.groupby("date")

    for date, group in grouped:
        st.markdown(f"## 📅 {date}")

        summary, keywords = summarize(group["message"].tolist())

        with st.container():
            st.markdown("### 🧠 요약")
            st.info(summary)

            st.markdown("### 🏷 키워드")
            st.write(", ".join(keywords))

            with st.expander("📄 원본보기"):
                for _, row in group.iterrows():
                    st.write(f"**{row['user']}**: {row['message']}")

            st.divider()
