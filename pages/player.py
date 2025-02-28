import streamlit as st
import pandas as pd
import requests
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from streamlit_modal import Modal
import numpy as np

@st.cache_data
def load_data():
    df = pd.read_csv("./data/player.csv")
    return df

def get_valid_image(url):
    try:
        response = requests.get(url, timeout=3)
        if response.status_code == 200:
            return url
        else:
            return "./image/man.png"
    except Exception:
        return "./image/man.png"

def get_text_color_for_bg(bg_color: str) -> str:
    if not (isinstance(bg_color, str) and bg_color.startswith('#') and len(bg_color) == 7):
        return "#000000"
    try:
        r = int(bg_color[1:3], 16)
        g = int(bg_color[3:5], 16)
        b = int(bg_color[5:7], 16)
    except ValueError:
        return "#000000"
    luminance = (0.299 * r + 0.587 * g + 0.114 * b) / 255.0
    return "#FFFFFF" if luminance < 0.5 else "#000000"

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

    positions = df['position'].dropna().unique().tolist()
    selected_position = st.sidebar.selectbox("포지션을 골라주세요", positions)
    selected_height = st.sidebar.number_input("키를 입력하세요 (cm)",
                                              min_value=140.0,
                                              max_value=220.0,
                                              value=180.0,
                                              step=0.1)

    if st.sidebar.button("Start!"):
        features = pd.concat([
            pd.get_dummies(df['position'], prefix='pos'),
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
                st.image(get_valid_image(row["image_url"]), width=100)
                st.write(row["name_en"])
            # 오른쪽 컬럼: boots_image와 boots 정보 출력
            with cols[1]:
                boots_img_url = row.get("boots_image", None)
                if boots_img_url and pd.notnull(boots_img_url):
                    # boots 이미지가 있는 경우, 이미지 크기를 150px로 출력하고 boots 정보도 표시
                    st.image(get_valid_image(boots_img_url), width=200)
                    st.write(f"{row['boots']}")
                else:
                    # boots 이미지가 NaN인 경우, 기본 boots 이미지와 메시지 출력
                    st.image("image/boots.png", width=150)
                    st.write("축구화 데이터가 없습니다!💿")
            # '정보 보기' 버튼 클릭 시 모달 팝업 열기
            if st.button("정보 보기", key=f"btn_{row['name_en']}_{row_idx}"):
                st.session_state["modal_open"] = True
                st.session_state["selected_player"] = row["name_en"]
                modal.open()
            st.markdown("---")

    if modal.is_open():
        with modal.container():
            selected_name = st.session_state["selected_player"]
            if selected_name:
                player_info = df.loc[df["name_en"] == selected_name].iloc[0].to_dict()
                img = get_valid_image(player_info.get("image_url"))
                player_color = player_info.get("color", "#B53D3D")
                text_color = get_text_color_for_bg(player_color)

                html_content = f"""
                <div style="background-color: {player_color}; color: {text_color};
                            padding: 20px; border-radius: 10px;">
                    <h3>선수 상세 정보</h3>
                    <img src="{img}" width="150">
                    <p><strong>이름:</strong> {player_info.get('name_en')}</p>
                    <p><strong>팀:</strong> {player_info.get('club')}</p>
                    <p><strong>포지션:</strong> {player_info.get('position')}</p>
                    <p><strong>키:</strong> {player_info.get('height')} cm</p>
                </div>
                """
                st.markdown(html_content, unsafe_allow_html=True)
            else:
                st.write("선수를 찾을 수 없습니다.")

def show_player():
    st.query_params["pages"] = "축구선수"
    main()









