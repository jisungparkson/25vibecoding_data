import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="유럽 축구 클럽 가치 시각화", layout="wide")

# 헤더
st.markdown("<h1 style='text-align: center; color: navy;'>⚽ 유럽 축구 클럽 가치 비교 시각화</h1>", unsafe_allow_html=True)
st.markdown("---")

# 데이터 불러오기
try:
    df = pd.read_csv("pages/most_valuable_teams.csv")

    # ✅ 칼럼 목록 확인
    st.sidebar.header("📌 데이터 열 목록")
    st.sidebar.write(df.columns.tolist())

    # ✅ 사용자 입력: 비교할 클럽
    st.sidebar.subheader("🔎 비교할 팀(클럽)을 선택하세요")
    clubs = sorted(df["Club"].unique())
    selected_clubs = st.sidebar.multiselect("클럽 선택", clubs, default=["Real Madrid", "Manchester City"])

    # ✅ 사용자 입력: 비교 항목
    st.sidebar.subheader("📊 비교할 항목을 선택하세요")
    metric = st.sidebar.selectbox(
        "항목 선택",
        options=[
            "Market_value",
            "Market_value_of_players",
            "MV_Top_18_players",
            "Share_of_MV"
        ],
        index=0
    )

    # ✅ 선택된 클럽으로 필터링
    filtered_df = df[df["Club"].isin(selected_clubs)]

    # ✅ 그래프 출력
    st.subheader(f"📈 선택한 항목: `{metric}`")
    fig = px.bar(
        filtered_df,
        x="Club",
        y=metric,
        color="Club",
        text=metric,
        title=f"{metric.replace('_', ' ')} 비교",
        labels={"Club": "클럽", metric: metric.replace("_", " ")},
        template="plotly_white"
    )
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    st.plotly_chart(fig, use_container_width=True)

    # ✅ 데이터 테이블 보여주기
    with st.expander("📄 원본 데이터 미리 보기"):
        st.dataframe(filtered_df)

except Exception as e:
    st.error(f"❌ 데이터를 불러오는 데 문제가 발생했습니다:\n\n{e}")
