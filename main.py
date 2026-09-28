```python
import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------------------------------
# 페이지 설정
# ------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 2 - 분포와 관계",
    page_icon="🎬",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 2 - 분포와 관계")

st.write(
    "1년간 박스오피스 10위권에 든 영화 가운데 "
    "이 기간에 개봉한 216편의 데이터를 살펴봅니다."
)

# ------------------------------------------
# 데이터 불러오기
# ------------------------------------------
DATA_URL = "https://raw.githubusercontent.com/happykth/data/main/kobis_movies.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_URL)

    # 장르가 여러 개라면 첫 번째 장르만 사용
    df["genre"] = (
        df["genre"]
        .fillna("미상")
        .astype(str)
        .str.split("|")
        .str[0]
        .str.strip()
    )

    # 총 관객을 숫자로 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    )

    return df


df = load_data()


# ==========================================
# 1. 장르별 영화 편수
# ==========================================
st.header("1. 장르별 영화 편수")

genre_counts = df["genre"].value_counts()

fig1 = px.pie(
    values=genre_counts.values,
    names=genre_counts.index,
    hole=0.5,
    title="장르별 영화 편수"
)

fig1.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편<br>"
        "비율: %{percent}"
        "<extra></extra>"
    )
)

fig1.update_layout(
    height=550
)

st.plotly_chart(
    fig1,
    use_container_width=True
)

st.markdown("---")

st.subheader("이 그래프로 알 수 있는 것")
st.write("")


# ==========================================
# 2. 장르별 영화 트리맵
# ==========================================
st.header("2. 장르별 영화와 총 관객")

# 필요한 데이터만 사용
treemap_data = df[
    ["genre", "movieNm", "total_audi"]
].dropna()

fig2 = px.treemap(
    treemap_data,
    path=["genre", "movieNm"],
    values="total_audi"
)

fig2.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "총 관객: %{value:,}명"
        "<extra></extra>"
    )
)

fig2.update_layout(
    title="장르별 영화 트리맵",
    height=700
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

st.markdown("---")

st.subheader("이 그래프로 알 수 있는 것")
st.write("")


# ==========================================
# 데이터 확인
# ==========================================
with st.expander("📋 데이터 확인하기"):
    st.dataframe(
        df,
        use_container_width=True
    )
```
