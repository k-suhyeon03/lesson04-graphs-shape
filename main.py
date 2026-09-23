import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

st.markdown(
    """
    1년간 박스오피스 10위권에 든 영화 중 해당 기간에 개봉한
    216편의 영화 데이터를 이용해 영화의 분포와 관계를 살펴봅니다.
    """
)

# -----------------------------
# 데이터 불러오기
# -----------------------------
DATA_URL = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_movies.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 장르가 여러 개라면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("장르 미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 빈 문자열 처리
    df.loc[df["genre"] == "", "genre"] = "장르 미상"

    return df


df = load_data()

# -----------------------------
# 첫 번째 그래프
# 장르별 영화 편수
# -----------------------------
st.header("1. 장르별 영화 편수")

genre_count = (
    df["genre"]
    .value_counts()
    .reset_index()
)

genre_count.columns = ["genre", "count"]

fig = px.pie(
    genre_count,
    names="genre",
    values="count",
    hole=0.55,
    title="장르별 영화 편수"
)

fig.update_traces(
    textinfo="label+percent",
    hovertemplate="<b>%{label}</b><br>영화 편수: %{value}편<br>비율: %{percent}<extra></extra>"
)

fig.update_layout(
    height=550,
    legend_title="장르"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 그래프 설명 영역
# -----------------------------
st.markdown("---")
st.subheader("📝 이 그래프로 알 수 있는 것")

st.info("여기에 장르별 영화 편수와 그 비율을 통해 알 수 있는 내용을 한 문장으로 작성하세요.")

# -----------------------------
# 데이터 확인
# -----------------------------
with st.expander("📋 사용한 데이터 확인"):
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
