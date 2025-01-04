import streamlit as st
from PIL import Image
import os
import pandas as pd
from datetime import date
import psycopg2
import boto3
from botocore.exceptions import NoCredentialsError
import base64

# PostgreSQL 데이터베이스 연결 설정
conn = psycopg2.connect(
    dbname="lovedata",
    user="undo",
    password="1969",
    host="localhost",
    port="5432"
)

s3_client = boto3.client(
    's3',
    aws_access_key_id='minioadmin',
    aws_secret_access_key='minioadmin',
    endpoint_url='http://localhost:9000',
)

bucket_name = 'love'
local_storage_path = "/Users/undo/Desktop/love-storage/workspace/images"

# 데이터 삽입 함수
def insert_entry(entry_date, title, description, image_urls, location=None, time=None):
    with conn.cursor() as cur:
        if time:
            cur.execute("""
                INSERT INTO lovedata (date, title, description, location, time, filepath, rotation)
                VALUES (%s, %s, %s, %s, %s, %s, %s);
            """, (entry_date, title, description, location, time, ','.join(image_urls), None))
        else:
            cur.execute("""
                INSERT INTO lovedata (date, title, description, location, filepath, rotation)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (entry_date, title, description, location, ','.join(image_urls), None))
        conn.commit()

# 사진을 로컬에 저장하는 함수
def save_local_image(image_file, entry_date, folder_name="photos"):
    try:
        folder_path = f"{folder_name}/{entry_date.year}/{entry_date.month:02d}/{entry_date.day:02d}/"
        local_folder_path = os.path.join(local_storage_path, folder_path)

        os.makedirs(local_folder_path, exist_ok=True)

        local_image_path = os.path.join(local_folder_path, image_file.name)
        with open(local_image_path, "wb") as f:
            f.write(image_file.getbuffer())

        return local_image_path
    except Exception as e:
        st.error(f"로컬에 이미지 저장 중 오류가 발생했습니다: {e}")
        return None

# 사진을 S3에 날짜별로 업로드하는 함수
def upload_to_s3(image_file, entry_date, folder_name="photos"):
    try:
        folder_path = f"{folder_name}/{entry_date.year}/{entry_date.month:02d}/{entry_date.day:02d}/"
        s3_path = f"{folder_path}{image_file.name}"
        s3_client.upload_fileobj(image_file, bucket_name, s3_path)
        return f"http://localhost:9000/{bucket_name}/{s3_path}"
    except NoCredentialsError:
        st.error("MinIO 자격 증명이 잘못되었습니다.")
        return None
    except Exception as e:
        st.error(f"업로드 중 오류가 발생했습니다: {e}")
        return None

# 다이어리 항목 삭제 함수
def delete_entry(entry_id, image_urls):
    with conn.cursor() as cur:
        try:
            for image_url in image_urls.split(','):
                s3_client.delete_object(Bucket=bucket_name, Key=image_url.split("love/")[1])
        except Exception as e:
            st.error(f"S3에서 파일 삭제 중 오류가 발생했습니다: {e}")

        try:
            for image_url in image_urls.split(','):
                local_image_path = os.path.join(local_storage_path, image_url.split("love/")[1])
                if os.path.exists(local_image_path):
                    os.remove(local_image_path)
                    st.success(f"로컬에서 '{local_image_path}' 파일이 삭제되었습니다.")
                else:
                    st.warning(f"로컬에서 '{local_image_path}' 파일을 찾을 수 없습니다.")
        except Exception as e:
            st.error(f"로컬에서 파일 삭제 중 오류가 발생했습니다: {e}")

        cur.execute("DELETE FROM lovedata WHERE id = %s;", (entry_id,))
        conn.commit()

# Streamlit 애플리케이션
st.title("우리의 추억 다이어리")

# 날짜 선택
entry_date = st.date_input("날짜", date.today())

# 사진 업로드 폼
with st.form(key='diary_form'):
    title = st.text_input("제목")
    description = st.text_area("설명")
    location = st.text_input("위치")
    image_files = st.file_uploader("사진 업로드", type=["jpg", "jpeg", "png"], accept_multiple_files=True)

    submit_button = st.form_submit_button("저장")

    if submit_button:
        if image_files:
            image_urls = []
            for image_file in image_files:
                local_image_path = save_local_image(image_file, entry_date)
                if local_image_path:
                    image_url = upload_to_s3(image_file, entry_date)
                    if image_url:
                        image_urls.append(image_url)

            if image_urls:
                insert_entry(entry_date, title, description, image_urls, location)
                st.success("다이어리에 사진이 저장되었습니다!")
                st.session_state['refresh'] = True
        else:
            st.error("사진을 업로드해야 합니다.")

# 다이어리 항목 보기
st.subheader("다이어리 항목")
with conn.cursor() as cur:
    cur.execute("SELECT id, date, title, description, location, filepath FROM lovedata ORDER BY date DESC;")
    entries = cur.fetchall()

# 페이지네이션 설정
entries_per_page = 5
total_pages = (len(entries) + entries_per_page - 1) // entries_per_page

# 현재 페이지 상태 관리
if 'current_page' not in st.session_state:
    st.session_state['current_page'] = 1

# 이전, 다음 버튼
col1, col2, col3 = st.columns([1, 4, 1])

with col1:
    if st.button("이전 페이지") and st.session_state['current_page'] > 1:
        st.session_state['current_page'] -= 1

with col3:
    if st.button("다음 페이지") and st.session_state['current_page'] < total_pages:
        st.session_state['current_page'] += 1

# 현재 페이지에 맞는 항목 표시
current_page = st.session_state['current_page']
start_index = (current_page - 1) * entries_per_page
end_index = start_index + entries_per_page
paginated_entries = entries[start_index:end_index]

# 이미지 파일을 Base64로 변환하는 함수
def get_base64_image(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except Exception as e:
        st.error(f"이미지 변환 중 오류가 발생했습니다: {e}")
        return None

# 현재 페이지의 항목 표시
for entry in paginated_entries:
    entry_date = entry[1]
    st.subheader(f"{entry_date}")
    
    # 이미지를 4개의 열로 나누어 표시
    columns = st.columns(4)  # 4개의 열 생성
    image_index = 0
    local_image_paths = entry[5].split(',')

    for local_image_path in local_image_paths:
        local_image_path = os.path.join(local_storage_path, local_image_path.split("love/")[1])
        base64_image = get_base64_image(local_image_path)
        if base64_image:
            # 각 이미지에 대한 HTML 마크업
            with columns[image_index % 4]:  # 열을 순차적으로 할당
                st.markdown(
                    f"""
                    <div style="width: 100%; height: 300px; margin: 10px;">
                        <img src="data:image/jpeg;base64,{base64_image}" alt="image" style="width: 100%; height: 100%; object-fit: cover; border: 1px solid #ddd; border-radius: 5px;">
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            image_index += 1

    # 텍스트 정보 표시
    st.markdown(f"**제목:** {entry[2]}")
    st.markdown(f"**설명:** {entry[3]}")
    st.markdown(f"**위치:** {entry[4]}")

    delete_key = f"delete_{entry[0]}"
    if delete_key not in st.session_state:
        st.session_state[delete_key] = False

    if st.button(f"삭제 {entry[2]}", key=f"button_{delete_key}"):
        st.session_state[delete_key] = True

    if st.session_state[delete_key]:
        confirm = st.checkbox(f"이 항목을 정말로 삭제하시겠습니까?", key=f"checkbox_{entry[0]}")
        if confirm:
            delete_entry(entry[0], entry[5])
            st.success(f"'{entry[2]}' 항목이 삭제되었습니다.")
            st.session_state[delete_key] = False
        else:
            st.info(f"'{entry[2]}' 항목 삭제가 취소되었습니다.")

    st.write("---")

# PostgreSQL 연결 종료
conn.close()

# 페이지 새로 고침 처리
if 'refresh' in st.session_state and st.session_state['refresh']:
    st.session_state['refresh'] = False
    st.experimental_rerun()