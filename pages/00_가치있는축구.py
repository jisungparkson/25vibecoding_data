import streamlit as st
import pandas as pd
import plotly.express as px

st.title("⚽ 유럽 축구 클럽 팀 가치 변화 시각화")

try:
    # CSV 불러오기
    df = pd.read_csv("pages/most_valuable_teams.csv")

    # 연도별 데이터를 긴 형식(long format)으로 변환
    # club, value, 2020, 2021, 2022, 2023 → club, nation, year, value
    long_df = df.melt(id_vars=['club', 'value'], var_name='year', value_name='market_value')

    # 연도는 숫자형으로 변환
    long_df['year'] = long_df['year'].astype(int)

    # 데이터 미리보기
    st.subheader("데이터 미리보기")
    st.dataframe(long_df.head())

    # 팀 선택
    selected_clubs = st.multiselect("클럽을 선택하세요", sorted(long_df['club'].unique()), default=["Man City", "Real Madrid"])

    # 선택한 팀만 필터링
    filtered_df = long_df[long_df['club'].isin(selected_clubs)]

    # 선 그래프 그리기
    st.subheader("📈 팀 가치 변화 그래프")
    fig = px.line(
        filtered_df,
        x='year',
        y='market_value',
        color='club',
        markers=True,
        labels={'year': '연도', 'market_value': '팀 가치 (백만 유로)'},
        title="연도별 팀 가치 변화"
    )
    st.plotly_chart(fig)

except FileNotFoundError:
    st.error("❌ CSV 파일을 찾을 수 없습니다. 경로를 확인하세요.")
except Exception as e:
    st.error(f"❌ 데이터를 불러오는 데 문제가 발생했습니다: {e}")
