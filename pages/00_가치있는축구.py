import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚽ 유럽 축구 클럽 팀 가치 비교")

try:
    df = pd.read_csv("pages/most_valuable_teams.csv")
    st.subheader("📌 데이터 열 이름:")
    st.write(df.columns.tolist())

    # 팀 선택
    selected_clubs = st.multiselect(
        "비교할 팀(클럽)을 선택하세요",
        options=sorted(df['Club'].unique()),
        default=["Manchester City", "Real Madrid"]
    )

    # 선택된 팀 필터링
    filtered_df = df[df['Club'].isin(selected_clubs)]

    # 막대그래프 그리기
    fig = px.bar(
        filtered_df,
        x='Club',
        y='Market_value',
        color='Club',
        text='Market_value',
        title='선택한 클럽들의 시장 가치 비교',
        labels={'Market_value': '시장 가치 (백만 유로)'}
    )
    st.plotly_chart(fig)

except Exception as e:
    st.error(f"❌ 데이터를 불러오는 데 문제가 발생했습니다: {e}")
