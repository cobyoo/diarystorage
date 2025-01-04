# import streamlit as st
# from PIL import Image
# import os
# import pandas as pd
# import datetime

# # 기본 파일 저장 경로 및 메타데이터 저장 경로
# base_photo_path = '/home/elicer/downloads'
# metadata_path = os.path.join(base_photo_path, 'metadata.csv')

# # 메타데이터 초기화
# if not os.path.exists(metadata_path):
#     df = pd.DataFrame(columns=['Date', 'Time', 'Title', 'Description', 'Location', 'FilePath'])
#     df.to_csv(metadata_path, index=False)

# # 앱 제목 및 설명
# st.title("우리의 추억 갤러리❤️")
# st.write("날짜를 선택하고 사진을 확인해보세요.")

# # 날짜 선택
# selected_date = st.date_input("날짜 선택", datetime.date.today())

# # 선택한 날짜 디렉토리
# selected_date_str = selected_date.strftime('%Y-%m-%d')
# selected_photo_path = os.path.join(base_photo_path, selected_date_str)

# # 사진 업로드
# image_files = st.file_uploader("사진 업로드", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)

# if st.button("추억 저장하기"):
#     if image_files:
#         if not os.path.exists(selected_photo_path):
#             os.makedirs(selected_photo_path)
        
#         new_entries = []
#         for image in image_files:
#             file_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
#             save_file_path = os.path.join(selected_photo_path, file_name)
            
#             # 사진 저장
#             with open(save_file_path, "wb") as f:
#                 f.write(image.getbuffer())
            
#             # 메타데이터 추가
#             current_time_str = datetime.datetime.now().strftime('%H:%M:%S')
#             new_entries.append([selected_date_str, current_time_str, '', '', '', save_file_path])
        
#         # 메타데이터 파일 업데이트
#         new_entries_df = pd.DataFrame(new_entries, columns=['Date', 'Time', 'Title', 'Description', 'Location', 'FilePath'])
#         metadata_df = pd.concat([pd.read_csv(metadata_path), new_entries_df], ignore_index=True)
#         metadata_df.to_csv(metadata_path, index=False)
        
#         st.success("추억이 저장되었습니다!")
#     else:
#         st.error("사진을 업로드해주세요.")



import streamlit as st
from PIL import Image
import os
import pandas as pd
import datetime

# 기본 파일 저장 경로 및 메타데이터 저장 경로
base_photo_path = '/home/elicer/downloads'
metadata_path = os.path.join(base_photo_path, 'metadata.csv')

# 메타데이터 초기화
if not os.path.exists(metadata_path):
    df = pd.DataFrame(columns=['Date', 'Time', 'Title', 'Description', 'Location', 'FilePath', 'Rotation'])
    df.to_csv(metadata_path, index=False)

# 앱 제목 및 설명
st.title("우리의 추억 갤러리❤️")
st.write("날짜를 선택하고 사진을 확인해보세요.")

# 날짜 선택
selected_date = st.date_input("날짜 선택", datetime.date.today())

# 선택한 날짜 디렉토리
selected_date_str = selected_date.strftime('%Y-%m-%d')
selected_photo_path = os.path.join(base_photo_path, selected_date_str)

# 사진 업로드
image_files = st.file_uploader("사진 업로드", type=['jpg', 'png', 'jpeg'], accept_multiple_files=True)

# 회전 모드 선택
rotation_mode = st.selectbox("회전 모드 선택", ["Original", "270 Degrees"])

if st.button("추억 저장하기"):
    if image_files:
        if not os.path.exists(selected_photo_path):
            os.makedirs(selected_photo_path)
        
        new_entries = []
        for image in image_files:
            file_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}.jpg"
            save_file_path = os.path.join(selected_photo_path, file_name)
            
            # 사진 열기
            img = Image.open(image)
            
            # 회전 모드 적용
            if rotation_mode == "270 Degrees":
                img = img.rotate(270, expand=True)
            
            # 이미지 모드 변환 (RGBA -> RGB)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            
            # 사진 저장
            img.save(save_file_path)
            
            # 메타데이터 추가
            current_time_str = datetime.datetime.now().strftime('%H:%M:%S')
            new_entries.append([selected_date_str, current_time_str, '', '', '', save_file_path, rotation_mode])
        
        # 메타데이터 파일 업데이트
        new_entries_df = pd.DataFrame(new_entries, columns=['Date', 'Time', 'Title', 'Description', 'Location', 'FilePath', 'Rotation'])
        metadata_df = pd.concat([pd.read_csv(metadata_path), new_entries_df], ignore_index=True)
        metadata_df.to_csv(metadata_path, index=False)
        
        st.success("추억이 저장되었습니다!")
    else:
        st.error("사진을 업로드해주세요.")