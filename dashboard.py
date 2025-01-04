# import streamlit as st
# import pandas as pd
# import folium
# from streamlit.components.v1 import html

# # 장소와 값 데이터 정의
# locations = [
#     {'name': '을지로', 'lat': 37.5665, 'lon': 126.9780, 'value': 10},
#     {'name': '광화문', 'lat': 37.5736, 'lon': 126.9790, 'value': 20},
#     {'name': '서촌', 'lat': 37.5795, 'lon': 126.9798, 'value': 30},
#     {'name': '춘천', 'lat': 37.8801, 'lon': 127.7316, 'value': 10},
#     {'name': '강릉', 'lat': 37.7513, 'lon': 128.8760, 'value': 10},
#     {'name': '남산', 'lat': 37.5512, 'lon': 126.9917, 'value': 10},
#     {'name': '춘천', 'lat': 37.8801, 'lon': 127.7316, 'value': 10},
#     {'name': '잠실', 'lat': 37.5104, 'lon': 127.0994, 'value': 30},
#     {'name': '코엑스', 'lat': 37.5158, 'lon': 127.0625, 'value': 20},
#     {'name': '선릉', 'lat': 37.5055, 'lon': 127.0474, 'value': 40},
#     {'name': '서울 숲', 'lat': 37.5512, 'lon': 127.0352, 'value': 15},
#     {'name': '천호', 'lat': 37.5382, 'lon': 127.1235, 'value': 18},
#     {'name': '노량진', 'lat': 37.5110, 'lon': 126.9400, 'value': 22}
# ]

# # DataFrame으로 변환
# map_data = pd.DataFrame(locations)

# # 지도 객체 생성
# my_map = folium.Map(
#     location=[map_data['lat'].mean(), map_data['lon'].mean()],
#     zoom_start=8,
#     tiles='CartoDB positron'  # 깔끔한 기본 타일 스타일
# )

# # 지도에 원형 마커와 핀 추가
# for index, row in map_data.iterrows():
#     folium.CircleMarker(
#         location=[row['lat'], row['lon']],
#         radius=row['value'] / 2,  # 원의 반지름 조정
#         color='lightblue',  # 원 테두리 색상
#         fill=True,
#         fill_color='lightblue',  # 원 내부 색상
#         fill_opacity=0.7,  # 내부 투명도 조정
#         weight=1  # 테두리 두께
#     ).add_to(my_map)

#     folium.Marker(
#         location=[row['lat'], row['lon']],
#         icon=folium.Icon(color='blue', icon='info-sign'),
#         popup=folium.Popup(f"<b>{row['name']}</b>", max_width=200)  # 클릭 시 장소 이름 표시
#     ).add_to(my_map)

# # 지도 제목과 캡션 추가
# st.markdown("""
#     <head>
#         <!-- Font Awesome -->
#         <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
#     </head>
#     <h1 style="text-align: center;">
#         <i class="fas fa-map-marker-alt"></i> 우리의 추억이 담긴 지도
#     </h1>
#     <p style="text-align: center;">지도 표시는 연지와 데이트 이후 업데이트 예정</p>
#     """, unsafe_allow_html=True)

# # 지도 시각화
# html(my_map._repr_html_(), width=800, height=600)


import streamlit as st
import pandas as pd
import folium
from streamlit.components.v1 import html

# 장소와 값 데이터 정의
locations = [
    {'name': '을지로', 'lat': 37.5665, 'lon': 126.9780, 'value': 10},
    {'name': '광화문', 'lat': 37.5736, 'lon': 126.9790, 'value': 20},
    {'name': '서촌', 'lat': 37.5795, 'lon': 126.9798, 'value': 30},
    {'name': '춘천', 'lat': 37.8801, 'lon': 127.7316, 'value': 10},
    {'name': '강릉', 'lat': 37.7513, 'lon': 128.8760, 'value': 10},
    {'name': '남산', 'lat': 37.5512, 'lon': 126.9917, 'value': 10},
    {'name': '춘천', 'lat': 37.8801, 'lon': 127.7316, 'value': 10},
    {'name': '잠실', 'lat': 37.5104, 'lon': 127.0994, 'value': 30},
    {'name': '코엑스', 'lat': 37.5158, 'lon': 127.0625, 'value': 20},
    {'name': '선릉', 'lat': 37.5055, 'lon': 127.0474, 'value': 40},
    {'name': '서울 숲', 'lat': 37.5512, 'lon': 127.0352, 'value': 15},
    {'name': '천호', 'lat': 37.5382, 'lon': 127.1235, 'value': 18},
    {'name': '노량진', 'lat': 37.5110, 'lon': 126.9400, 'value': 22}
]

# DataFrame으로 변환
map_data = pd.DataFrame(locations)

# 'value' 기준으로 순위 추가
map_data['rank'] = map_data['value'].rank(ascending=False, method='min')

# 색상 설정 (value가 높을수록 더 진한 색)
color_scale = ['#7aa8f0']  # 연한 파랑에서 진한 파랑

# 지도 객체 생성
my_map = folium.Map(
    location=[map_data['lat'].mean(), map_data['lon'].mean()],
    zoom_start=8,
    tiles='CartoDB positron'  # 깔끔한 기본 타일 스타일
)

# 지도에 원형 마커와 핀 추가
for index, row in map_data.iterrows():
    color = color_scale[int(row['rank']) % len(color_scale)]  # 순위에 따라 색상 결정, 색상 순환
    folium.CircleMarker(
        location=[row['lat'], row['lon']],
        radius=row['value'] / 2,  # 원의 반지름 조정
        color=color,  # 원 테두리 색상
        fill=True,
        fill_color=color,  # 원 내부 색상
        fill_opacity=0.7,  # 내부 투명도 조정
        weight=1  # 테두리 두께
    ).add_to(my_map)

    folium.Marker(
        location=[row['lat'], row['lon']],
        icon=folium.Icon(color='blue', icon='info-sign'),
        popup=folium.Popup(f"<b>{row['name']}</b><br>순위: {int(row['rank'])}", max_width=200)  # 클릭 시 장소 이름과 순위 표시
    ).add_to(my_map)

# 지도 제목과 캡션 추가
st.markdown("""
    <head>
        <!-- Font Awesome -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    </head>
    <h1 style="text-align: center;">
        <i class="fas fa-map-marker-alt"></i> 우리의 추억이 담긴 지도
    </h1>
    <p style="text-align: center;">지도 표시는 연지와 데이트 이후 업데이트 예정</p>
    """, unsafe_allow_html=True)

# 지도 시각화
html(my_map._repr_html_(), width=800, height=600)

# 대시보드 섹션: value 기준으로 순위와 색깔 표시
st.subheader("장소 순위 및 값")
ranked_data = map_data[['rank', 'name', 'value', 'lat', 'lon']].sort_values(by='rank')

# 1. Top 5 장소
st.subheader("Top 5 장소 (Value 기준)")
top5_data = ranked_data.head(5)  # 상위 5개 장소
st.write(top5_data[['rank', 'name']])
