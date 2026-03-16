import streamlit as st
import pytesseract
from PIL import Image
import pandas as pd
import cv2
import numpy as np

# tesseract 경로 (Windows)
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

st.set_page_config(page_title="주간 식단표", layout="wide")

st.title("🍱 주간 식단표 자동 분석")

uploaded = st.file_uploader("식단표 이미지를 업로드하세요", type=["png","jpg","jpeg"])

def extract_text(image):

    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    text = pytesseract.image_to_string(gray, lang="kor+eng")

    return text


def parse_menu(text):

    lines = text.split("\n")

    meals = {
        "조식":[],
        "중식":[],
        "석식":[],
        "간편식":[],
        "야식":[]
    }

    current = None

    for line in lines:

        line = line.strip()

        if "조식" in line:
            current = "조식"
            continue

        if "중식" in line:
            current = "중식"
            continue

        if "석식" in line:
            current = "석식"
            continue

        if "간편식" in line:
            current = "간편식"
            continue

        if "야식" in line:
            current = "야식"
            continue

        if current and len(line) > 2:
            meals[current].append(line)

    return meals


if uploaded:

    image = Image.open(uploaded)

    st.image(image, caption="업로드된 식단표", use_column_width=True)

    with st.spinner("식단 분석 중..."):

        text = extract_text(image)

        meals = parse_menu(text)

    st.success("분석 완료")

    col1,col2,col3,col4,col5 = st.columns(5)

    with col1:
        st.subheader("🍳 조식")
        for m in meals["조식"]:
            st.write(m)

    with col2:
        st.subheader("🍱 중식")
        for m in meals["중식"]:
            st.write(m)

    with col3:
        st.subheader("🍽 석식")
        for m in meals["석식"]:
            st.write(m)

    with col4:
        st.subheader("🥪 간편식")
        for m in meals["간편식"]:
            st.write(m)

    with col5:
        st.subheader("🌙 야식")
        for m in meals["야식"]:
            st.write(m)

    df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in meals.items()]))

    st.download_button(
        "엑셀 다운로드",
        df.to_csv(index=False).encode("utf-8-sig"),
        "menu.csv"
    )
