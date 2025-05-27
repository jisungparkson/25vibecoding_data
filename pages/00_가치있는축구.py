import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚽ 유럽 축구 클럽 팀 가치 비교")

try:
    df = pd.read_csv("pages/most_valuable_teams.csv")

    st.subheader("📌 데이터 열 이름:")
    st.write(df.columns.tolist())

    # 사용자 선택
    selected_clubs = st.multiselect(
        "비교할 팀(클럽)을 선택하세요",
        options=sorted(df['Club'].unique()),
        default=["Manchester City", "Real Madrid"]
    )

    selected_column = st.selectbox(
        "시각화할 항목을 선택하세요",
        options=['Market_value', 'Market_value_of_players', 'MV_Top_18_players', 'Share_of_MV']
    )

    # 선택된 팀만 필터링
    filtered_df = df[df['Club'].isin(selected_clubs)]

    # 그래프 그리기
    fig = px.bar(
        filtered_df,
        x='Club',
        y=selected_column,
        color='Club',
        text=selected_column,
        title=f"{selected_column} 비교",
        labels={selected_column: selected_column.replace('_', ' ')}
    )

    st.plotly_chart(fig)

except Exception as e:
    st.error(f"❌ 데이터를 불러오는 데 문제가 발생했습니다: {e}")
