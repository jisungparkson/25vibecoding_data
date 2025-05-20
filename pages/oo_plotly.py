import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# 데이터 불러오기
df1 = pd.read_csv("202504_202504_연령별인구현황_남녀합계.csv", encoding="cp949")
df2 = pd.read_csv("202504_202504_연령별인구현황_월간 남녀구분.csv", encoding="cp949")

# 서울시 전체 데이터 추출
male_cols = [col for col in df1.columns if "2025년04월_남_" in col and "세" in col]
female_cols = [col for col in df1.columns if "2025년04월_여_" in col and "세" in col]
ages = [col.split('_')[-1].replace('세', '') for col in male_cols]

df_pop = df1[df1["행정구역"].str.contains("서울특별시") & ~df1["행정구역"].str.contains("구")].iloc[0]

# 남녀 인구 데이터 전처리
male_data = df_pop[male_cols].str.replace(',', '').astype(int) * -1
female_data = df_pop[female_cols].str.replace(',', '').astype(int)

# 피라미드 그래프
fig1 = go.Figure()
fig1.add_trace(go.Bar(y=ages, x=male_data, name='남성', orientation='h', marker_color='blue'))
fig1.add_trace(go.Bar(y=ages, x=female_data, name='여성', orientation='h', marker_color='red'))
fig1.update_layout(
    title='서울특별시 연령별 인구 피라미드 (2025년 4월)',
    barmode='relative',
    bargap=0.1,
    xaxis_title='인구 수',
    yaxis_title='연령',
    template='plotly_white',
    height=800
)

# 전체 인구 막대 그래프
df_total = df2[df2["행정구역"].str.contains("서울특별시") & ~df2["행정구역"].str.contains("구")].iloc[0]
total_cols = [col for col in df_total.index if "2025년04월_계_" in col and "세" in col]
total_ages = [col.split('_')[-1].replace('세', '') for col in total_cols]
total_data = df_total[total_cols].str.replace(',', '').astype(int)

fig2 = go.Figure()
fig2.add_trace(go.Bar(x=total_ages, y=total_data, marker_color='green'))
fig2.update_layout(
    title='서울특별시 연령별 전체 인구 (2025년 4월)',
    xaxis_title='연령',
    yaxis_title='인구 수',
    template='plotly_white'
)

# Streamlit 출력
st.title("서울특별시 연령별 인구 시각화")
st.subheader("1. 인구 피라미드 (남녀 구분)")
st.plotly_chart(fig1)

st.subheader("2. 연령별 전체 인구 막대그래프")
st.plotly_chart(fig2)

