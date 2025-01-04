import streamlit as st
import os

# 현재 스크립트 파일의 경로를 얻습니다.
current_dir = os.path.dirname(os.path.abspath(__file__))

# 페이지 정의
pages = {
    "Home": os.path.join(current_dir, "home.py"),
    #"Love": os.path.join(current_dir, "app.py"),
    "Dashboard": os.path.join(current_dir, "dashboard.py")
}

# 사이드바에 페이지 선택 위젯 추가
selection = st.sidebar.selectbox("Select a Page", list(pages.keys()))

# 선택한 페이지 파일 로드
if selection:
    page_path = pages[selection]
    with open(page_path, "r") as file:
        code = file.read()
    exec(code)
