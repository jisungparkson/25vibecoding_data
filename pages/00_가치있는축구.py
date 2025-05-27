import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지 설정
st.set_page_config(page_title="유럽 축구 클럽 가치 비교", layout="wide")

# 제목
st.markdown("<h1 style='text-align: center; color: darkblue;'>⚽ 유럽 축구 클럽 가치 비교 시각화</h1>", unsafe_allow_html=True)
st.markdown("---")

try:
    # CSV 불러오기
    df = pd.read_csv("pages/most_valuable_teams.csv")

    # 열 이름 한글로 매핑
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

    # 사이드바 구성
    st.sidebar.header("📌 사용 방법")
    st.sidebar.write("비교할 클럽과 항목을 선택하세요.")

    selected_clubs = st.sideba_
