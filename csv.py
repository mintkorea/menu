import pandas as pd

FILES = [
    "병원별관.csv",
    "서울성모병원.CSV",
    "성으회관0.csv",
    "옴니버스B.csv",
    "의산연01.csv"
]

def read_csv(file):
    for enc in ["utf-8", "cp949"]:
        try:
            return pd.read_csv(file, encoding=enc, on_bad_lines="skip")
        except:
            continue
    return pd.read_csv(file, engine="python", on_bad_lines="skip")

def normalize_floor(f):
    if pd.isna(f):
        return ""
    f = str(f).upper().replace("F", "")
    if f.startswith("-"):
        return "B" + f[1:] + "층"
    return f + "층"

def transform(df):
    df["층"] = df["floor"].apply(normalize_floor)
    df["호실"] = df["room"] if "room" in df.columns else ""
    df["구역"] = df["zone"] if "zone" in df.columns else ""
    df["시설명"] = df["name"]
    df["설명"] = df["description"] if "description" in df.columns else ""
    df["운영시간"] = df["hours"] if "hours" in df.columns else ""

    result = pd.DataFrame({
        "캠퍼스": df["campus"],
        "건물": df["building"],
        "층": df["층"],
        "호실": df["호실"],
        "구역": df["구역"],
        "시설명": df["시설명"],
        "카테고리": df["category"],
        "설명": df["설명"],
        "운영시간": df["운영시간"]
    })

    return result

all_df = []

for f in FILES:
    df = read_csv(f)
    df = transform(df)
    all_df.append(df)

final = pd.concat(all_df, ignore_index=True)
final = final.fillna("")
final = final.drop_duplicates()

final.to_csv("캠퍼스_위치_통합.csv", index=False, encoding="utf-8-sig")
