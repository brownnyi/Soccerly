import streamlit as st
import pandas as pd
import requests
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from streamlit_modal import Modal
import numpy as np

@st.cache_data
def load_data():
    return pd.read_csv("./data/player.csv")

def main():
    st.title("나와 비슷한 선수 찾기")
    st.write("👈 사이드바에 자신의 포지션과 키를 입력하세요.")

    if "similar_players" not in st.session_state:
        st.session_state["similar_players"] = None
    if "modal_open" not in st.session_state:
        st.session_state["modal_open"] = False
    if "selected_player" not in st.session_state:
        st.session_state["selected_player"] = None

    modal = Modal(key="player_modal", title="축구선수 정보 보기")
    df = load_data()

    positions = df['position_ko'].dropna().unique().tolist()
    selected_position = st.sidebar.selectbox("포지션을 골라주세요", positions)
    selected_height = st.sidebar.number_input("키를 입력하세요 (cm)",
                                              min_value=140.0,
                                              max_value=220.0,
                                              value=180.0,
                                              step=0.1)

    if st.sidebar.button("검색하기"):
        features = pd.concat([
            pd.get_dummies(df['position_ko'], prefix='pos'),
            df[['height']]
        ], axis=1)

        scaler = StandardScaler()
        features_scaled = scaler.fit_transform(features)

        knn = NearestNeighbors(n_neighbors=10)
        knn.fit(features_scaled)

        query_df = pd.DataFrame({
            "position": [selected_position],
            "height": [selected_height]
        })
        query_features = pd.concat([
            pd.get_dummies(query_df['position'], prefix='pos'),
            query_df[['height']]
        ], axis=1)
        query_features = query_features.reindex(columns=features.columns, fill_value=0)
        query_scaled = scaler.transform(query_features)

        distances, indices = knn.kneighbors(query_scaled)
        similar_players = df.iloc[indices[0]].copy()
        similar_players["distance"] = distances[0]

        st.session_state["similar_players"] = similar_players
        st.session_state["modal_open"] = False
        st.session_state["selected_player"] = None

    similar_players = st.session_state["similar_players"]
    if similar_players is not None:
        st.subheader("Player List")
        for row_idx, row in similar_players.iterrows():
            cols = st.columns(2)

            # 왼쪽 컬럼: 선수 이미지와 이름 출력
            with cols[0]:
                if pd.notnull(row["img"]):  # 이미지가 존재할 때만 표시
                    st.image(row["img"], width=100)
                st.write(row["name_ko"])

            # 오른쪽 컬럼: boots_image와 boots 정보 출력
            with cols[1]:
                if pd.notnull(row["boots_img"]):  # 축구화 이미지가 존재할 때만 표시
                    st.image(row["boots_img"], width=200)
                    st.write(f"{row['boots_ko']}")

            # '정보 보기' 버튼 클릭 시 모달 팝업 열기
            if st.button("정보 보기", key=f"btn_{row['name_ko']}_{row_idx}"):
                st.session_state["modal_open"] = True
                st.session_state["selected_player"] = row["name_ko"]
                modal.open()
            st.markdown("---")

    if modal.is_open():
        with modal.container():
            selected_name = st.session_state["selected_player"]
            if selected_name:
                player_info = df.loc[df["name_ko"] == selected_name].iloc[0].to_dict()

                img_1 = player_info.get("img_src")
                img_2 = player_info.get("img")  # 겹칠 이미지
                boots_img = player_info.get("boots_img")  # 축구화 이미지

                # HTML로 이미지 겹쳐서 표시
                html_content = f"""
                <div style="padding: 20px; border-radius: 10px;">
                    <div style="position: relative; width: 200px; height: 200px; margin: auto;">
                """
                if img_1 and pd.notnull(img_1):  # 배경 이미지가 존재할 때만 표시
                    html_content += f'<img src="{img_1}" style="position: absolute; top: 0; left: 0; width: 120%; opacity: 0.5; border-radius: 10px;">'

                if img_2 and pd.notnull(img_2):  # 선수 이미지가 존재할 때만 표시
                    html_content += f'<img src="{img_2}" style="position: absolute; top: 75px; left: 50px; width: 60%;">'

                html_content += """
                    </div>
                    <p><strong>이름:</strong> {}</p>
                    <p><strong>팀:</strong> {}</p>
                    <p><strong>국가:</strong> {}</p>
                    <p><strong>포지션:</strong> {}</p>
                    <p><strong>키:</strong> {} cm</p>
                """.format(player_info.get('name_ko'), player_info.get('team_name'),
                           player_info.get('country_ko'), player_info.get('position_ko'),
                           player_info.get('height'))


                html_content += "</div>"

                st.markdown(html_content, unsafe_allow_html=True)
            else:
                st.write("선수를 찾을 수 없습니다.")

def show_player():
    st.query_params["pages"] = "축구선수"
    main()








