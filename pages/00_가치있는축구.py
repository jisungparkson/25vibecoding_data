import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests # requests 라이브러리 추가

st.set_page_config(page_title="축구 팀 가치 변화", layout="wide")
st.title("⚽ 유럽 축구 클럽 팀 가치 변화 시각화")

# GitHub Raw URL 사용 (임시 방편)
# 'YOUR_GITHUB_USERNAME'과 'YOUR_REPO_NAME'을 실제 값으로 변경하세요.
# 파일이 있는 브랜치도 'main'으로 변경해주세요.
github_raw_url = "https://raw.githubusercontent.com/jisungparkson/25vibecoding.data/main/25vibecoding_data/pages/most_valuable_teams.csv"

# CSV 파일 불러오기
try:
    # URL에서 데이터를 직접 읽어옴
    df = pd.read_csv(github_raw_url, parse_dates=["date"])
    st.success("CSV 데이터를 성공적으로 불러왔습니다. (GitHub Raw URL 사용)")
except Exception as e:
    st.error(f"CSV 데이터를 불러오는 데 실패했습니다: {e}")
    st.stop()

# 이후 코드는 동일
latest_date = df["date"].max()
top10_teams = df[df["date"] == latest_date].nlargest(10, "value_million_eur")["team"].tolist()
filtered_df = df[df["team"].isin(top10_teams)]

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
