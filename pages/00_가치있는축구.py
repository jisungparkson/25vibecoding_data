import streamlit as st
import pandas as pd
import plotly.express as px

# 제목
st.title("⚽ 유럽 축구 클럽 팀 가치 변화 시각화")

# CSV 파일 불러오기
try:
    df = pd.read_csv("pages/most_valuable_teams.csv")

    # 데이터 확인
    st.subheader("데이터 미리보기")
    st.dataframe(df.head())

    # 연도 선택 (슬라이더)
    year = st.slider("연도를 선택하세요", int(df['year'].min()), int(df['year'].max()), step=1)

    # 해당 연도의 데이터만 필터링
    filtered_df = df[df['year'] == year]

    # 시각화: 팀 가치 순위 바 차트
    st.subheader(f"💰 {year}년 팀 가치 순위")
    fig = px.bar(
        filtered_df.sort_values(by='value', ascending=False),
        x='value',
        y='club',
        orientation='h',
        color='club',
        labels={'value': '팀 가치 (백만 유로)', 'club': '클럽 이름'},
        height=600
    )
    fig.update_layout(yaxis={'categoryorder': 'total ascending'})
    st.plotly_chart(fig)

except FileNotFoundError:
    st.error("❌ CSV 파일을 찾을 수 없습니다. 경로를 확인하세요.")
except Exception as e:
    st.error(f"❌ 데이터를 불러오는 데 문제가 발생했습니다: {e}")
