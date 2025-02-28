import streamlit as st

def show_dashboard():
    st.query_params["pages"] = "대시보드"
    st.markdown("[![image](https://github.com/user-attachments/assets/b8113fff-aec4-4c98-bc35-a10b55e7ed8f)](https://public.tableau.com/app/profile/seungwoo.lee5575/viz/_17315683602050/2_1)")
    st.write('👆 해당 태블로 이미지를 누르시면 대시보드를 이용할 수 있습니다.')

    st.title('대시보드 가이드')
    st.image('image/guide1.png')
    st.write('약 1만 5천명의 축구선수 데이터를 다루는 이 대시보드는 총 3가지의 필터를 통해 포지션별 축구화 선호도와 사일로(시리즈)별 선호도를 확인할 수 있습니다.')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image('image/filter1.png')
    with col2:
        st.image('image/filter2.png')
    with col3:
        st.image('image/filter3.png')

    st.write('축구선수 클럽팀 리그, 축구화 브랜드, 축구선수 출신지역을 통해 필터 처리를 할 수 있습니다.')

    st.image('image/guide2.png')
    st.image('image/guide3.png')

    st.write('만약 원하는 선수가 어떤 축구화를 신고있는지 바로 확인하고 싶다면 검색하여 찾아볼 수도 있습니다.')