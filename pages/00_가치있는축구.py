import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="축구 팀 가치 변화", layout="wide")
st.title("⚽ 유럽 축구 클럽 팀 가치 변화 시각화")

# CSV 파일 로컬에서 불러오기
CSV_FILE_PATH = "most_valuable_teams.csv"

if not os.path.exists(CSV_FILE_PATH):
    st.error(f"{CSV_FILE_PATH} 파일을 찾을 수 없습니다. 업로드되어 있는지 확인하세요.")
    st.stop()

# CSV 파일 불러오기
try:
    df = pd.read_csv(CSV_FILE_PATH, parse_dates=["date"])
except Exception as e:
    st.error("CSV 데이터를 불러오는 데 실패했습니다.")
    st.stop()

# 최신 날짜 기준 상위 10개 팀 선택
latest_date = df["date"].max()
top10_teams = df[df["date"] == latest_date].nlargest(10, "value_million_eur")["team"].tolist()
filtered_df = df[df["team"].isin(top10_teams)]

# 시각화
fig = px.line(
    filtered_df,
    x="date",
    y="value_million_eur",
    color="team",
    markers=True,
    title="최근 1년간 유럽 상위 10개 축구 클럽 팀 가치 변화",
    labels={
        "date": "날짜",
        "value_million_eur": "팀 가치 (백만 유로)",
        "team": "팀 이름"
    }
)

st.plotly_chart(fig, use_container_width=True)
