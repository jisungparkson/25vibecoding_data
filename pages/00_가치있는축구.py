import streamlit as st
import pandas as pd
import plotly.express as px
import os
import requests # requests 라이브러리 추가

st.set_page_config(page_title="축구 팀 가치 변화", layout="wide")
st.title("⚽ 유럽 축구 클럽 팀 가치 변화 시각화")

# 1단계에서 확인한 정확한 GitHub Raw URL을 여기에 붙여넣으세요.
# 예시 (직접 확인 필요):
github_raw_url = "https://raw.githubusercontent.com/jisungparkson/25vibecoding.data/main/25vibecoding_data/pages/most_valuable_teams.csv"


# CSV 파일 불러오기
try:
    # URL에서 데이터를 직접 읽어옴
    # 'requests'를 사용하여 스트림으로 읽는 것이 안정적일 수 있습니다.
    # response = requests.get(github_raw_url)
    # response.raise_for_status() # HTTP 오류가 발생하면 예외를 발생시킵니다.
    # from io import StringIO
    # df = pd.read_csv(StringIO(response.text), parse_dates=["date"])

    # 또는 pandas의 read_csv가 URL을 직접 처리할 수 있습니다.
    df = pd.read_csv(github_raw_url, parse_dates=["date"])

    st.success("CSV 데이터를 성공적으로 불러왔습니다. (GitHub Raw URL 사용)")
except requests.exceptions.RequestException as e: # requests 관련 오류 처리
    st.error(f"GitHub에서 데이터를 불러오는 데 실패했습니다 (네트워크/URL 문제): {e}")
    st.stop()
except Exception as e: # 그 외 오류 처리
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
