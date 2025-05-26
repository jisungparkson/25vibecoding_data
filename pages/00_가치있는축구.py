import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚽ 유럽 축구 클럽 팀 가치 변화 시각화")

# CSV 파일 GitHub에서 불러오기
csv_url = "https://raw.githubusercontent.com/jsungparkson/25vibecoding_data/main/most_valuable_teams.csv"

try:
    df = pd.read_csv(csv_url, parse_dates=["date"])
except Exception as e:
    st.error("CSV 데이터를 불러오는 데 실패했습니다.")
    st.stop()

# 최근 날짜 기준 상위 10개 팀 선정
latest_date = df["date"].max()
top10 = df[df["date"] == latest_date].nlargest(10, "value_million_eur")["team"].tolist()
filtered_df = df[df["team"].isin(top10)]

# Plotly 시각화
fig = px.line(
    filtered_df,
    x="date",
    y="value_million_eur",
    color="team",
    title="최근 1년간 유럽 상위 10개 축구 클럽 팀 가치 변화",
    markers=True,
    labels={"date": "날짜", "value_million_eur": "팀 가치 (백만 유로)", "team": "팀 이름"}
)

st.plotly_chart(fig)

