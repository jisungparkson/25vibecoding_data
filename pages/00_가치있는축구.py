# streamlit_app.py
import streamlit as st
import pandas as pd
import plotly.express as px

# 제목
st.title("유럽 축구 상위 10개 클럽 팀 가치 변화 (최근 1년)")

# CSV 업로드
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요.", type=["csv"])

if uploaded_file:
    # CSV 읽기
    df = pd.read_csv(uploaded_file, parse_dates=["date"])

    # 팀 가치 상위 10개 팀 선택 (가장 최근 날짜 기준)
    latest_date = df["date"].max()
    latest_values = df[df["date"] == latest_date]
    top10_teams = latest_values.nlargest(10, "value_million_eur")["team"].tolist()

    # 상위 10개 팀의 과거 기록 필터링
    filtered_df = df[df["team"].isin(top10_teams)]

    # Plotly 시각화
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
else:
    st.warning("CSV 파일을 먼저 업로드해주세요.")
