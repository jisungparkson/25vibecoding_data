import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚽ 유럽 축구 클럽 팀 가치 변화 시각화")

try:
    # CSV 불러오기
    df = pd.read_csv("pages/most_valuable_teams.csv")

    # 열 이름 확인해서 필요시 출력
    st.subheader("📌 데이터 열 이름:")
    st.write(df.columns.tolist())

    # long format으로 변환
    long_df = df.melt(
        id_vars=['Team', 'Country'],  # 실제 열 이름 사용
        var_name='year',
        value_name='market_value'
    )

    # 연도 열을 정수형으로 변환
    long_df['year'] = long_df['year'].astype(int)

    # 팀 선택 위젯
    selected_teams = st.multiselect("팀을 선택하세요", sorted(long_df['Team'].unique()), default=["Manchester City", "Real Madrid"])

    # 필터링
    filtered_df = long_df[long_df['Team'].isin(selected_teams)]

    # 그래프 출력
    st.subheader("📈 팀 가치 변화 그래프")
    fig = px.line(
        filtered_df,
        x='year',
        y='market_value',
        color='Team',
        markers=True,
        labels={'year': '연도', 'market_value': '팀 가치 (백만 유로)'},
        title="연도별 팀 가치 변화"
    )
    st.plotly_chart(fig)

except Exception as e:
    st.error(f"❌ 데이터를 불러오는 데 문제가 발생했습니다: {e}")
