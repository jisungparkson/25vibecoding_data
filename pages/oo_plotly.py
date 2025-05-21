import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# CSV 파일 불러오기
df = pd.read_csv("202504_202504_연령별인구현황_월간 남녀구분.csv", encoding='cp949')

# '합계' 제외한 연령별 데이터만 추출
df_age = df[df['세부항목'] != '합계']

# 남자 인구: 문자열 → 정수 변환 후 음수로 (왼쪽에 그리기 위해)
male_data = df_age['남자'].apply(lambda x: int(str(x).replace(',', '')) * -1)

# 여자 인구: 문자열 → 정수 변환
female_data = df_age['여자'].apply(lambda x: int(str(x).replace(',', '')))

# 연령 (문자열 그대로 사용)
ages = df_age['세부항목']

# Plotly 피라미드 그래프 그리기
fig = go.Figure()

fig.add_trace(go.Bar(
    y=ages,
    x=male_data,
    name='남자',
    orientation='h',
    marker=dict(color='blue')
))

fig.add_trace(go.Bar(
    y=ages,
    x=female_data,
    name='여자',
    orientation='h',
    marker=dict(color='pink')
))

fig.update_layout(
    title='연령별 남녀 인구 피라미드 (2025년 4월)',
    barmode='relative',
    xaxis=dict(title='인구 수', tickvals=[-3000000, -2000000, -1000000, 0, 1000000, 2000000, 3000000],
               ticktext=['3M', '2M', '1M', '0', '1M', '2M', '3M']),
    yaxis=dict(title='연령'),
    template='plotly_white'
)

# Streamlit에 출력
st.plotly_chart(fig)
