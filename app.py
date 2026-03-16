import streamlit as st
import cv2
import numpy as np
from PIL import Image

st.set_page_config(page_title="식단표 자동 분석", layout="wide")

st.title("🍱 식단표 자동 인식")

uploaded = st.file_uploader("식단표 이미지 업로드", type=["png","jpg","jpeg"])


def detect_table_cells(image):

    img = np.array(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # 이진화
    thresh = cv2.adaptiveThreshold(
        gray,255,
        cv2.ADAPTIVE_THRESH_MEAN_C,
        cv2.THRESH_BINARY_INV,
        15,5
    )

    # 수직선 검출
    vertical_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(1,40))
    vertical = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, vertical_kernel)

    # 수평선 검출
    horizontal_kernel = cv2.getStructuringElement(cv2.MORPH_RECT,(40,1))
    horizontal = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, horizontal_kernel)

    table = cv2.add(vertical,horizontal)

    contours,_ = cv2.findContours(
        table,
        cv2.RETR_TREE,
        cv2.CHAIN_APPROX_SIMPLE
    )

    cells = []

    for c in contours:

        x,y,w,h = cv2.boundingRect(c)

        if w>120 and h>80:
            cells.append((x,y,w,h))

    cells = sorted(cells,key=lambda b:(b[1],b[0]))

    return cells,img


if uploaded:

    image = Image.open(uploaded)

    st.image(image,caption="업로드된 식단표")

    cells,img = detect_table_cells(image)

    st.subheader("자동 인식된 메뉴 영역")

    cols = st.columns(7)

    i=0

    for (x,y,w,h) in cells:

        crop = img[y:y+h,x:x+w]

        cols[i%7].image(crop)

        i+=1
