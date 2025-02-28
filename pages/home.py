import streamlit as st
import pages as pg

def show_home():
    st.query_params["pages"] = "홈"
# 제목 중앙 정렬
    st.markdown("<h1 style='text-align: center; font-size: 50px;'>Soccerly-축구하게?</h1>", unsafe_allow_html=True)
    st.image("image/soccer_image.jpg", use_container_width=True)
    
    # 상태 초기화
    # 목적 버튼 누르고 끄기
    if 'show_text1' not in st.session_state:
        st.session_state.show_text1 = False
    if 'show_text2' not in st.session_state:
        st.session_state.show_text2 = False
    if 'show_text3' not in st.session_state:
        st.session_state.show_text3 = False

    col1, col2, col3 = st.columns(3)

    # 첫 번째 컬럼에 축구화 추천 버튼
    with col1:
        if st.button("⚽ 축구화 추천 사용설명", use_container_width=True):
            st.session_state.show_text1 = not st.session_state.show_text1
        if st.session_state.show_text1:
            st.write("발볼과 길이를 선택하여 최적의 축구화를 찾아보세요")

    # 두 번째 컬럼에 선수 추천 버튼
    with col2:
        if st.button("👤 선수 찾기", use_container_width=True):
            st.session_state.show_text2 = not st.session_state.show_text2
        if st.session_state.show_text2:
            st.write("자신의 키와 포지션을 선택하여 비슷한 선수를 확인할 수 있습니다")

    with col3:
        if st.button("🏆 대시보드", use_container_width=True):
            st.session_state.show_text3 = not st.session_state.show_text3
        if st.session_state.show_text3:
            st.write("")
