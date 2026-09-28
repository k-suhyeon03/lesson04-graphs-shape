import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("영화 데이터 그래프 도감 2 - 분포와 관계")

st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 216편의 데이터를 분석합니다."
)

# 데이터 불러오기
DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 여러 장르가 있는 경우 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 총 관객 수를 숫자로 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    ).fillna(0)

    return df


df = load_data()


# ============================================================
# 1. 장르별 영화 편수
# ============================================================

st.header("1. 장르별 영화 편수")

genre_counts = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_counts.columns = ["genre", "count"]

fig1 = px.pie(
    genre_counts,
    names="genre",
    values="count",
    hole=0.55,
    title="장르별 영화 편수"
)

fig1.update_traces(
    textposition="outside",
    textinfo="label+percent",
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}<extra></extra>"
    )
)

fig1.update_layout(
    legend_title="장르",
    margin=dict(t=70, b=30, l=30, r=30)
)

st.plotly_chart(fig1, use_container_width=True)

st.info("이 그래프로 알 수 있는 것: ________________________________")

st.divider()


# ============================================================
# 2. 장르별 영화 트리맵
# ============================================================

st.header("2. 장르별 영화 총 관객 트리맵")

st.write(
    "각 장르 안에 영화가 들어 있으며, "
    "영화의 총 관객 수가 많을수록 더 큰 칸으로 표시됩니다."
)

fig2 = px.treemap(
    df,
    path=["genre", "movieNm"],
    values="total_audi",
    title="장르별 영화 총 관객 트리맵"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,.0f}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    margin=dict(t=70, b=30, l=20, r=20)
)

st.plotly_chart(fig2, use_container_width=True)

st.info("이 그래프로 알 수 있는 것: ________________________________")

st.divider()
