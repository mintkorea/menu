import streamlit as st
import numpy as np
import cv2
from PIL import Image

st.set_page_config(page_title="주간 식단표", layout="wide")

st.title("🍱 주간 식단표 자동 분석")

uploaded = st.file_uploader("식단표 이미지를 업로드하세요", type=["png","jpg","jpeg"])


days = ["월","화","수","목","금","토","일"]
meals = ["조식","중식","일품","석식","야식"]


def split_fixed_grid(image):

    img = np.array(image)

    h, w, _ = img.shape

    # 식단표 실제 표 영역 (비율 기준)
    top = int(h * 0.20)
    bottom = int(h * 0.88)

    left = int(w * 0.06)
    right = int(w * 0.97)

    table = img[top:bottom, left:right]

    th, tw, _ = table.shape

    rows = 5
    cols = 7

    cell_h = th // rows
    cell_w = tw // cols

    cells = []

    for r in range(rows):

        row = []

        for c in range(cols):

            y1 = r * cell_h
            y2 = (r + 1) * cell_h

            x1 = c * cell_w
            x2 = (c + 1) * cell_w

            crop = table[y1:y2, x1:x2]

            row.append(crop)

        cells.append(row)

    return cells


if uploaded:

    image = Image.open(uploaded)

    st.image(image, caption="업로드된 식단표", use_column_width=True)

    cells = split_fixed_grid(image)

    st.markdown("---")

    day = st.selectbox("요일 선택", days)

    d = days.index(day)

    st.header(f"{day}요일 식단")

    cols = st.columns(len(meals))

    for i,meal in enumerate(meals):

        with cols[i]:

            st.subheader(meal)

            st.image(cells[i][d], use_column_width=True)
