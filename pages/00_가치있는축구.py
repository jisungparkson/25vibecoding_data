import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="유럽 축구 클럽 가치 비교", layout="wide")

st.markdown("<h1 style='text-align: center; color: darkblue;'>⚽ 유럽 축구 클럽 가치 비교 시각화</h1>", unsafe_allow_html=True)
st.markdown("---")

try:
    df = pd.read_csv("pages/most_valuable_teams.csv")

    col_map = {
        "Club": "클럽",
        "Competition": "리그",
        "Age": "평균 연령",
        "Squad_size": "선수단 규모",
        "Market_value": "전체 시장 가치",
        "Market_value_of_players": "선수 시장 가치 합계",
        "MV_Top_18_players": "주전 18명 가치",
        "Share_of_MV": "주전 18명 가치 비율"
    }
    df.rename(columns=col_map, inplace=True)

    st.sidebar.header("📌 사용 방법")
    st.sidebar.write("비교할 클럽과 항목을 선택하세요.")

    selected_clubs = st.sidebar.multiselect(
        "⚽ 비교할 클럽 선택",
        sorted(df["클럽"].unique()),
        default=["Real Madrid", "Manchester City"]
    )

    selected_metric = st.sidebar.selectbox(
        "📊 비교 항목 선택",
        options=[
            "전체 시장 가치",
            "선수 시장 가치 합계",
            "주전 18명 가치",
            "주전 18명 가치 비율"
        ],
        index=0
    )

    filtered_df = df[df["클럽"].isin(selected_clubs)]

    # 값 전처리
    if selected_metric == "주전 18명 가치 비율":
        filtered_df["비율 (%)"] = filtered_df["주전 18명 가치 비율"] * 100
        y_col = "비율 (%)"
        suffix = "%"
    else:
        y_col = selected_metric
        suffix = "€"

    st.subheader(f"📈 선택한 항목: {selected_metric}")

    fig = px.bar(
        filtered_df,
        x="클럽",
        y=y_col,
        color="클럽",
        text=y_col,
        title=f"{selected_metric} 비교",
        labels={"클럽": "클럽명", y_col: selected_metric},
        template="plotly_white"
    )

    fig.update_traces(
        texttemplate="%{text:.2s}" if suffix == "€" else "%{text:.1f}%",
        textposition="outside",
        marker_line_color='black',
        marker_line_width=1.2
    )

    fig.update_layout(
        yaxis_title=None,
        xaxis_title=None,
        uniformtext_minsize=8,
        uniformtext_mode='hide'
    )

    st.plotly_chart(fig, use_container_width=True)

    with st.expander("🔍 선택된 클럽의 데이터 보기"):
        st.dataframe(filtered_df)

except Exception as e:
    st.error(f"❌ 오류 발생: {e}")
