import streamlit as st
import os
from streamlit_navigation_bar import st_navbar
import pages as pg  

st.set_page_config(page_title="Soccerly", initial_sidebar_state='auto', layout="wide")

st.query_params["pages"] = "홈"

# ✅ 스크롤 문제 해결 (iPhone Safari 대응)
st.markdown("""
    <style>
    /* 전체 HTML 및 Body에 스크롤 허용 */
    html, body {
        height: auto !important;
        overflow-y: scroll !important;
        -webkit-overflow-scrolling: touch !important;  /* iPhone 스크롤 부드럽게 */
    }

    /* Streamlit 컨테이너 스크롤 허용 */
    [data-testid="stAppViewContainer"] {
        height: 100% !important;
        overflow-y: auto !important; /* 세로 스크롤 활성화 */
    }

    /* iFrame 크기 및 스크롤 가능하게 설정 */
    iframe {
        height: 100% !important;
        overflow-y: auto !important;
    }

    /* 사이드바 스크롤 허용 */
    [data-testid="stSidebarContent"] {
        height: 100% !important;
        overflow-y: auto !important;
    }
    </style>
""", unsafe_allow_html=True)

# 폰트 적용 (네비게이션 바 제외)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css?family=Nanum+Gothic+Coding:400');

/* 모든 요소에 Nanum Gothic Coding 폰트 적용 */
body, .stButton button, .stTextInput input, .stSelectbox, .stMultiselect,
h1, h2, h3, h4, h5, h6, p, div, span, li, a {
    font-family: 'Nanum Gothic Coding', monospace !important;
}
</style>
""", unsafe_allow_html=True)

# 웹페이지에 로고 삽입
st.image('image/logo.png', use_column_width=True)

# 네비게이션 바에 표시할 페이지 이름
pages = ["Home", "Boots", "Player", "Dashboard"]

# 네비게이션 바 스타일 설정
styles = {
    "nav": {
        "background-color": "#d3d3d3",
    },
    "div": {
        "max-width": "20rem",
    },
    "span": {
        "color": "white",
        "padding": "5px",
        "font-family": "Poor Story",
    },
    "active": {
        "background-color": "white",
        "color": "var(--text-color)",
        "font-weight": "bold",
        "padding": "14px",
    },
    "hover": {
        "background-color": "rgba(255, 255, 255, 0.35)",
    },
}

# 네비게이션 바 옵션 설정
options = {
    "show_menu": False,
    "show_sidebar": True,
    "use_padding": True,
}

# 네비게이션 바 생성
page = st_navbar(
    pages,
    styles=styles,
    options=options,
)

# 각 페이지에 해당하는 함수 매핑
functions = {
    "Home": pg.show_home,
    "Boots": pg.show_Find,
    "Player": pg.show_player,
    "Dashboard": pg.show_dashboard
}

# 선택한 페이지의 함수를 호출하여 해당 페이지 내용 표시
go_to = functions.get(page)
if go_to:
    go_to()


