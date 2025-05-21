import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 📂 파일명
FILE_POP = '202504_202504_연령별인구현황_월간 남녀구분.csv'
FILE_TOTAL = '202504_202504_연령별인구현황_남녀합계.csv'

# 📊 데이터 읽기
df_pop = pd.read_csv(FILE_POP, encoding='cp949')
df_total = pd.read_csv(FILE_TOTAL, encoding='cp949')

# 🧹 필요한 한 줄만 추출 (예: 첫 번째 데이터행)
df_pop = df_pop.iloc[0:1]
df_total = df_total.iloc[0:1]

# 📈 연령대 정의
age_groups = [
    '0~4세', '5~9세', '10~14세', '15~19세', '20~24세', '25~29세',
    '30~34세', '35~39세', '40~44세', '45~49세', '50~54세',
    '55~59세', '60~64세', '65~69세', '70~74세', '75~79세',
    '80~84세', '85~89세', '90~94세', '95~99세', '100세 이상'
]

male_cols = [f'{age}_남자' for age in age_groups]
female_cols = [f'{age}_여자' for age in age_groups]
total_cols = [f'{age}_계' for age in age_groups]

# 문자열 → 숫자 변환
male_data = df_pop[male_cols].iloc[0].apply(lambda x: int(str(x).replace(',', ''))).values * -1
female_data = df_pop[female_cols].iloc[0].apply(lambda x: int(str(x).replace(',', ''))).values
total_data = df_total[total_cols].iloc[0].apply(lambda x: int(str(x).replace(',', ''))).values

# 👤 인구 피라미드
fig_pyramid = go.Figure()
fig_pyramid.add_trace(go.Bar(y=age_groups, x=male_data, name='남자', orientation='h', marker_color='blue'))
fig_pyramid.add_trace(go.Bar(y=age_groups, x=female_data, name='여자', orientation='h', marker_color='red'))

fig_pyramid.update_layout(
    title='연령별 인구 피라미드',
    barmode='relative',
    xaxis=dict(title='인구 수', tickvals=[-100000, -50000, 0, 50000, 100000],
               ticktext=['10만', '5만', '0', '5만', '10만']),
    yaxis=dict(title='연령'),
    template='plotly_white',
    height=800
)

# 👥 전체 인구 그래프
fig_total = go.Figure()
fig_total.add_trace(go.Bar(x=age_groups, y=total_data, name='전체', marker_color='green'))

fig_total.update_layout(
    title='연령별 전체 인구',
    xaxis=dict(title='연령'),
    yaxis=dict(title='인구 수'),
    template='plotly_white',
    height=600
)

# 🖥️ Streamlit 앱 출력
st.title('서울시 연령별 인구 시각화 (2025년 4월 기준)')
st.plotly_chart(fig_pyramid, use_container_width=True)
st.plotly_chart(fig_total, use_container_width=True)
