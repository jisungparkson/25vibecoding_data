# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

st.title("유럽 축구 상위 10개 클럽 팀 가치 변화 (최근 1년)")

# ✅ GitHub에 있는 CSV 파일 URL (raw 형식)
csv_url = "https://raw.githubusercontent.com/사용자이름/저장소이름/브랜치이름/파일경로/most_valuable_teams.csv"

# 데이터 불러오기
try:
    df = pd.read_csv(csv_url, parse_dates=["date"])
except Exception as e:
    st.error("CSV 파일을 불러오는 데 문제가 발생했습니다.")
    st.stop()

# 최근 날짜 기준 상위 10개 팀 추출
latest_date = df["date"].max()
latest_values = df[df["date"] == latest_date]
top10_teams = latest_values.nlargest(10, "value_million_eur")["team"].tolist()

# 상위 팀들만 필터링
filtered_df = df[df["team"].isin(top10_teams)]

# Plotly 그래프 생성
fig = px.line(
    filtered_df,
    x="date",
    y="value_million_eur",
    color="team",
    markers=True,
    title="최근 1년간 유럽 축구 상위 10개 클럽 팀 가치 변화",
    labels={"date": "날짜", "value_million_eur": "팀 가치 (백만 유로)"}
)

st.plotly_chart(fig)
