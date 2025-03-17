import streamlit as st
import pandas as pd

def show_dashboard():
    # 데이터 로드 함수
    @st.cache_data
    def load_data():
        df = pd.read_csv("./data/player.csv")  # 데이터 불러오기

        # 필요한 컬럼 선택 및 컬럼명 변경 (color, img 컬럼 제외)
        selected_columns = {
            "name_ko": "이름",
            "country_ko": "국가",
            "position_ko": "포지션",
            "team_name": "팀",
            "age": "나이",
            "height": "키",
            "img": "이미지",
            "img_src": "배경 이미지",
            "boots_ko": "축구화",
            "boots_img": "축구화 이미지"
        }

        df = df[list(selected_columns.keys())]  # 필요한 컬럼만 선택
        df = df.rename(columns=selected_columns)  # 컬럼명 변경
        return df

    # 유효한 이미지 URL 가져오기
    def get_valid_image(url):
        if pd.isna(url) or url == "":
            return "https://via.placeholder.com/150"  # 기본 이미지
        return url

    # Streamlit UI
    st.title("선수 목록")
    st.write("사이드바에서 선수를 검색하여 상세 목록을 확인하세요!")

    # 데이터 로드
    df = load_data()

    # 사이드바에서 선수 이름 선택
    selected_name = st.sidebar.selectbox("선수 이름을 선택하세요", [""] + df["이름"].unique().tolist())

    # 검색 버튼 추가
    search_button = st.sidebar.button("검색하기")

    # 🎯 **선수가 선택되지 않은 경우 → 데이터프레임 표시**
    if not search_button:
        df_display = df.drop(columns=["이미지", "배경 이미지", "축구화 이미지"])  # 이미지 컬럼 제거
        st.dataframe(df_display)
    elif selected_name:  # 🎯 **검색 버튼이 눌리면 → 선수 정보 표시**
        player_info = df.loc[df["이름"] == selected_name].iloc[0].to_dict()

        img_1 = get_valid_image(player_info.get("배경 이미지"))
        img_2 = get_valid_image(player_info.get("이미지"))  # 선수 이미지
        boots_img = get_valid_image(player_info.get("축구화 이미지"))  # 축구화 이미지

        # HTML로 이미지 순서대로 표시
        html_content = f"""
        <div style="padding: 20px; border-radius: 10px; text-align: center;">
            <!-- 선수 이미지 -->
            <div style="position: relative; width: 200px; height: 200px; margin: auto;">
                <img src="{img_1}" style="width: 120%; opacity: 0.5; border-radius: 10px;">
                <img src="{img_2}" style="position: absolute; top: 75px; left: 50px; width: 60%;">
            </div>
            <div>
            <img src="{boots_img}" style="width: 200px; margin-top: 10px;">
            </div>
            <!-- 선수 정보 -->
            <p><strong>이름:</strong> {player_info.get('이름')}</p>
            <p><strong>포지션:</strong> {player_info.get('포지션')}</p>
            <p><strong>축구화:</strong> {player_info.get('축구화')}</p>
            <p><strong>팀:</strong> {player_info.get('팀')}</p>
            <p><strong>국가:</strong> {player_info.get('국가')}</p>
            <p><strong>나이:</strong> {player_info.get('나이')}</p>
            <p><strong>키:</strong> {player_info.get('키')} cm</p>
            
            
        </div>
        """
        st.markdown(html_content, unsafe_allow_html=True)
