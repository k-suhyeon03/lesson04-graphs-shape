```python
import streamlit as st
import pandas as pd
import plotly.express as px

# ==========================================
# 페이지 설정
# ==========================================
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

# ==========================================
# 데이터 불러오기
# ==========================================
DATA_URL = (
    "https://raw.githubusercontent.com/happykth/data/main/"
    "kobis_movies.csv"
)


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

    # 숫자 데이터 변환
    df["total_audi"] = pd.to_numeric(
        df["total_audi"],
        errors="coerce"
    )

    df["first_scrn"] = pd.to_numeric(
        df["first_scrn"],
        errors="coerce"
    )

    df["first_week_audi"] = pd.to_numeric(
        df["first_week_audi"],
        errors="coerce"
    )

    return df


df = load_data()


# ==========================================
# 1. 장르별 영화 편수 - 도넛 그래프
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

fig1.update_layout(height=550)

st.plotly_chart(fig1, use_container_width=True)

st.markdown("---")
st.subheader("이 그래프로 알 수 있는 것")
st.write("")


# ==========================================
# 2. 장르별 영화 - 트리맵
# ==========================================
st.header("2. 장르별 영화와 총 관객")

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

st.plotly_chart(fig2, use_container_width=True)

st.markdown("---")
st.subheader("이 그래프로 알 수 있는 것")
st.write("")


# ==========================================
# 3. 총 관객 히스토그램
# ==========================================
st.header("3. 영화별 총 관객 분포")

hist_data = df[
    ["movieNm", "total_audi"]
].dropna()

hist_data = hist_data[
    hist_data["total_audi"] >= 0
].copy()

bin_count = 20

bins = pd.cut(
    hist_data["total_audi"],
    bins=bin_count,
    include_lowest=True
)

bin_counts = bins.value_counts().sort_index()
most_common_bin = bin_counts.idxmax()

fig3 = px.histogram(
    hist_data,
    x="total_audi",
    nbins=bin_count,
    title="영화별 총 관객 분포",
    labels={
        "total_audi": "총 관객 수",
        "count": "영화 편수"
    }
)

fig3.update_traces(
    hovertemplate=(
        "총 관객 구간: %{x}<br>"
        "영화 편수: %{y}편"
        "<extra></extra>"
    )
)

fig3.update_layout(
    height=550,
    xaxis_title="총 관객 수",
    yaxis_title="영화 편수"
)

st.plotly_chart(fig3, use_container_width=True)

max_audi_row = hist_data.loc[
    hist_data["total_audi"].idxmax()
]

max_movie_name = max_audi_row["movieNm"]
max_audi = int(max_audi_row["total_audi"])

st.markdown("---")
st.subheader("이 그래프로 알 수 있는 것")

st.write(
    f"대부분의 영화는 총 관객 "
    f"**{most_common_bin.left:,.0f}명 ~ "
    f"{most_common_bin.right:,.0f}명** 구간에 몰려 있으며, "
    f"가장 관객이 많은 영화는 **{max_movie_name}**으로 "
    f"총 **{max_audi:,}명**의 관객을 기록했습니다."
)


# ==========================================
# 4. 개봉일 스크린수와 총 관객 - 산점도
# ==========================================
st.header("4. 개봉일 스크린수와 총 관객의 관계")

scatter_data = df[
    ["movieNm", "genre", "first_scrn", "total_audi"]
].dropna()

scatter_data = scatter_data[
    (scatter_data["first_scrn"] >= 0)
    & (scatter_data["total_audi"] >= 0)
].copy()

fig4 = px.scatter(
    scatter_data,
    x="first_scrn",
    y="total_audi",
    color="genre",
    hover_name="movieNm",
    title="개봉일 스크린수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "genre": "장르"
    }
)

fig4.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig4.update_layout(
    height=650,
    legend_title="장르"
)

st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.subheader("이 그래프로 알 수 있는 것")
st.write("")


# ==========================================
# 5. 장르별 총 관객 - 박스플롯
# ==========================================
st.header("5. 장르별 총 관객 분포")

genre_movie_counts = df["genre"].value_counts()

valid_genres = genre_movie_counts[
    genre_movie_counts >= 10
].index

box_data = df[
    df["genre"].isin(valid_genres)
][
    ["genre", "movieNm", "total_audi"]
].dropna()

box_data = box_data[
    box_data["total_audi"] >= 0
].copy()

fig5 = px.box(
    box_data,
    x="genre",
    y="total_audi",
    color="genre",
    points="outliers",
    custom_data=["movieNm"],
    title="영화가 10편 이상인 장르의 총 관객 분포",
    labels={
        "genre": "장르",
        "total_audi": "총 관객"
    }
)

fig5.update_traces(
    hovertemplate=(
        "<b>%{customdata[0]}</b><br>"
        "총 관객: %{y:,}명"
        "<extra></extra>"
    )
)

fig5.update_layout(
    height=650,
    showlegend=False,
    xaxis_title="장르",
    yaxis_title="총 관객"
)

st.plotly_chart(fig5, use_container_width=True)

st.markdown("---")
st.subheader("이 그래프로 알 수 있는 것")
st.write("")


# ==========================================
# 6. 첫 주 관객을 크기로 나타낸 버블 그래프
# ==========================================
st.header("6. 개봉일 스크린수와 총 관객 - 첫 주 관객 버블 그래프")

bubble_data = df[
    [
        "movieNm",
        "genre",
        "first_scrn",
        "total_audi",
        "first_week_audi"
    ]
].dropna()

bubble_data = bubble_data[
    (bubble_data["first_scrn"] >= 0)
    & (bubble_data["total_audi"] >= 0)
    & (bubble_data["first_week_audi"] >= 0)
].copy()

fig6 = px.scatter(
    bubble_data,
    x="first_scrn",
    y="total_audi",
    size="first_week_audi",
    color="genre",
    hover_name="movieNm",
    size_max=55,
    title="개봉일 스크린수와 총 관객의 관계",
    labels={
        "first_scrn": "개봉일 스크린수",
        "total_audi": "총 관객",
        "first_week_audi": "첫 주 관객",
        "genre": "장르"
    }
)

fig6.update_traces(
    marker=dict(
        opacity=0.7
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "장르: %{fullData.name}<br>"
        "개봉일 스크린수: %{x:,}개<br>"
        "총 관객: %{y:,}명<br>"
        "첫 주 관객: %{marker.size:,}명"
        "<extra></extra>"
    )
)

fig6.update_layout(
    height=700,
    xaxis_title="개봉일 스크린수",
    yaxis_title="총 관객",
    legend_title="장르"
)

st.plotly_chart(fig6, use_container_width=True)

st.markdown("---")
st.subheader("이 그래프로 알 수 있는 것")
st.write("")


# ==========================================
# 7. 제작 국가 → 장르 - 선버스트 그래프
# ==========================================
st.header("7. 제작 국가와 장르별 영화 편수")

sunburst_data = df[
    ["nation", "genre", "movieNm"]
].copy()

sunburst_data["nation"] = (
    sunburst_data["nation"]
    .fillna("미상")
    .astype(str)
    .str.strip()
)

sunburst_data["genre"] = (
    sunburst_data["genre"]
    .fillna("미상")
    .astype(str)
    .str.strip()
)

sunburst_data = sunburst_data[
    sunburst_data["movieNm"].notna()
].copy()

fig7 = px.sunburst(
    sunburst_data,
    path=["nation", "genre"],
    title="제작 국가 → 장르별 영화 편수"
)

fig7.update_traces(
    hovertemplate=(
        "<b>%{label}</b><br>"
        "영화 편수: %{value}편"
        "<extra></extra>"
    )
)

fig7.update_layout(
    height=700,
    margin=dict(
        t=70,
        b=20,
        l=20,
        r=20
    )
)

st.plotly_chart(fig7, use_container_width=True)

st.markdown("---")
st.subheader("이 그래프로 알 수 있는 것")
st.write("")


# ==========================================
# 8. 개봉일 스크린수와 첫 주 관객 - 산점도
# ==========================================
question = "개봉일 스크린수가 많을수록 첫 주 관객도 많은가?"

st.header("8. " + question)

scatter_week_data = df[
    ["movieNm", "first_scrn", "first_week_audi"]
].dropna()

scatter_week_data = scatter_week_data[
    (scatter_week_data["first_scrn"] >= 0)
    & (scatter_week_data["first_week_audi"] >= 0)
].copy()

fig8 = px.scatter(
    scatter_week_data,
    x="first_scrn",
    y="first_week_audi",
    hover_name="movieNm",
    title=question,
    labels={
        "first_scrn": "개봉일 스크린 수",
        "first_week_audi": "첫 주 관객 수"
    }
)

fig8.update_traces(
    marker=dict(
        size=10,
        opacity=0.75
    ),
    hovertemplate=(
        "<b>%{hovertext}</b><br>"
        "개봉일 스크린 수: %{x:,}개<br>"
        "첫 주 관객 수: %{y:,}명"
        "<extra></extra>"
    )
)

fig8.update_layout(
    height=650,
    xaxis_title="개봉일 스크린 수",
    yaxis_title="첫 주 관객 수"
)

st.plotly_chart(
    fig8,
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
