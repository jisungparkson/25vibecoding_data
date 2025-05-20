import streamlit as st
import folium
from streamlit_folium import st_folium

# --- 데이터 정의 ---
# 프리미어리그 경기장 정보 (이름, 위도, 경도)
# 실제 2023-2024 시즌 또는 대표적인 경기장 위주로 일부만 포함했습니다.
# 더 많은 경기장을 추가할 수 있습니다.
epl_stadiums = [
    {"name": "에미레이트 스타디움 (아스날)", "lat": 51.5549, "lon": -0.1084},
    {"name": "빌라 파크 (아스톤 빌라)", "lat": 52.5092, "lon": -1.8847},
    {"name": "바이탈리티 스타디움 (본머스)", "lat": 50.7352, "lon": -1.8385},
    {"name": "지테크 커뮤니티 스타디움 (브렌트포드)", "lat": 51.4907, "lon": -0.2890},
    {"name": "아멕스 스타디움 (브라이튼)", "lat": 50.8618, "lon": -0.0830},
    {"name": "스탬포드 브릿지 (첼시)", "lat": 51.4817, "lon": -0.1910},
    {"name": "셀허스트 파크 (크리스탈 팰리스)", "lat": 51.3983, "lon": -0.0854},
    {"name": "구디슨 파크 (에버튼)", "lat": 53.4388, "lon": -2.9663},
    {"name": "크레이븐 코티지 (풀럼)", "lat": 51.4749, "lon": -0.2218},
    {"name": "안필드 (리버풀)", "lat": 53.4308, "lon": -2.9609},
    {"name": "에티하드 스타디움 (맨체스터 시티)", "lat": 53.4831, "lon": -2.2004},
    {"name": "올드 트래포드 (맨체스터 유나이티드)", "lat": 53.4631, "lon": -2.2913},
    {"name": "세인트 제임스 파크 (뉴캐슬)", "lat": 54.9756, "lon": -1.6217},
    {"name": "시티 그라운드 (노팅엄 포레스트)", "lat": 52.9399, "lon": -1.1324},
    {"name": "토트넘 홋스퍼 스타디움 (토트넘)", "lat": 51.6042, "lon": -0.0662},
    {"name": "런던 스타디움 (웨스트햄)", "lat": 51.5386, "lon": -0.0166},
    {"name": "몰리뉴 스타디움 (울버햄튼)", "lat": 52.5902, "lon": -2.1301},
    # 필요시 더 많은 경기장 추가
]

# 런던 주요 출발지 정보
london_locations = {
    "킹스크로스 역 (King's Cross)": {"lat": 51.5308, "lon": -0.1238},
    "패딩턴 역 (Paddington)": {"lat": 51.5152, "lon": -0.1754},
    "워털루 역 (Waterloo)": {"lat": 51.5032, "lon": -0.1126},
    "빅토리아 역 (Victoria)": {"lat": 51.4952, "lon": -0.1439},
    "리버풀 스트리트 역 (Liverpool Street)": {"lat": 51.5188, "lon": -0.0814},
    "히드로 공항 (Heathrow Airport)": {"lat": 51.4700, "lon": -0.4543},
    "개트윅 공항 (Gatwick Airport)": {"lat": 51.1537, "lon": -0.1821}
}

# --- Streamlit UI 구성 ---
st.set_page_config(page_title="EPL 경기장 길찾기", layout="wide")
st.title("🗺️ EPL 프리미어리그 경기장 길찾기 (런던 출발)")
st.write("런던 내 주요 출발지에서 프리미어리그 경기장까지 가는 방법을 구글 지도로 확인해보세요.")

# --- 입력 섹션 (사이드바에 배치) ---
st.sidebar.header("🚀 경로 설정")

# 1. 런던 출발지 선택
london_start_point_name = st.sidebar.selectbox(
    "런던 출발지를 선택하세요:",
    list(london_locations.keys())
)
start_coords = london_locations[london_start_point_name]

# 2. 경기장 선택
stadium_names = [s["name"] for s in epl_stadiums]
selected_stadium_name = st.sidebar.selectbox(
    "목표 경기장을 선택하세요:",
    stadium_names,
    index=stadium_names.index("토트넘 홋스퍼 스타디움 (토트넘)") # 기본값 설정
)

# 선택된 경기장 정보 찾기
selected_stadium_data = next(s for s in epl_stadiums if s["name"] == selected_stadium_name)

# --- 지도 및 길찾기 정보 표시 ---
col1, col2 = st.columns([3, 1]) # 지도 영역을 더 넓게

with col1:
    st.subheader("🏟️ 경기장 위치")
    # 지도 초기 중심: 선택된 경기장 또는 영국 중심
    map_center_lat = selected_stadium_data["lat"]
    map_center_lon = selected_stadium_data["lon"]
    map_zoom = 8 # 선택된 경기장이 잘 보이도록 줌 레벨 조정

    m = folium.Map(location=[map_center_lat, map_center_lon], zoom_start=map_zoom)

    # 모든 경기장 마커 추가
    for stadium in epl_stadiums:
        icon_color = "blue"
        popup_html = f"<b>{stadium['name']}</b>"
        if stadium["name"] == selected_stadium_name:
            icon_color = "red" # 선택된 경기장은 빨간색
            popup_html = f"<b>📍 {stadium['name']} (선택됨)</b>"

        folium.Marker(
            [stadium["lat"], stadium["lon"]],
            tooltip=stadium["name"],
            popup=popup_html,
            icon=folium.Icon(color=icon_color, icon="futbol" if icon_color == "red" else "info-sign", prefix="fa" if icon_color == "red" else "glyphicon")
        ).add_to(m)

    # 선택된 런던 출발지 마커 추가 (초록색)
    folium.Marker(
        [start_coords["lat"], start_coords["lon"]],
        tooltip=f"출발: {london_start_point_name}",
        popup=f"<b>출발: {london_start_point_name}</b>",
        icon=folium.Icon(color="green", icon="flag", prefix="fa")
    ).add_to(m)


    # 경로 그리기 (Folium 기능은 아니지만, 시각적으로 출발지와 목적지를 선으로 이어줄 수 있음)
    # 실제 길찾기는 구글맵 링크로 제공
    points = [
        (start_coords["lat"], start_coords["lon"]),
        (selected_stadium_data["lat"], selected_stadium_data["lon"])
    ]
    folium.PolyLine(points, color="purple", weight=2.5, opacity=1, dash_array='5, 5', tooltip="경로 (참고용 직선)").add_to(m)


    st_folium(m, width=None, height=600, returned_objects=[]) # returned_objects를 빈 리스트로 하면 클릭 이벤트 처리 안함

with col2:
    st.subheader("📍 길찾기 정보")
    st.markdown(f"**출발:** {london_start_point_name}")
    st.markdown(f"**도착:** {selected_stadium_name}")

    # 구글 지도 길찾기 URL 생성
    # https://www.google.com/maps/dir/?api=1&origin=lat,lng&destination=lat,lng&travelmode=transit (대중교통)
    # travelmode: driving, walking, bicycling, transit
    google_maps_url_transit = (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={start_coords['lat']},{start_coords['lon']}"
        f"&destination={selected_stadium_data['lat']},{selected_stadium_data['lon']}"
        f"&travelmode=transit" # 대중교통 우선
    )
    google_maps_url_driving = (
        f"https://www.google.com/maps/dir/?api=1"
        f"&origin={start_coords['lat']},{start_coords['lon']}"
        f"&destination={selected_stadium_data['lat']},{selected_stadium_data['lon']}"
        f"&travelmode=driving" # 자동차 우선
    )

    st.markdown(f"---")
    st.markdown(f"##### 🚇 대중교통 길찾기")
    st.markdown(f"[구글 지도로 보기 (대중교통)]({google_maps_url_transit})", unsafe_allow_html=True)
    # HTML 버튼으로 더 보기 좋게 만들 수도 있습니다.
    st.link_button("구글 지도로 보기 (대중교통)", google_maps_url_transit, use_container_width=True)


    st.markdown(f"---")
    st.markdown(f"##### 🚗 자동차 길찾기")
    st.markdown(f"[구글 지도로 보기 (자동차)]({google_maps_url_driving})", unsafe_allow_html=True)
    st.link_button("구글 지도로 보기 (자동차)", google_maps_url_driving, use_container_width=True)

    st.markdown(f"---")
    st.caption("팁: '구글 지도로 보기'를 클릭하면 새 탭에서 길찾기 결과가 열립니다.")


st.sidebar.markdown("---")
st.sidebar.markdown("만든이: [AI Assistant]")
st.sidebar.markdown("데이터 출처: 위키피디아 등 공개 정보 (좌표는 근사치일 수 있음)")
