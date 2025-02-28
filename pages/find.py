import streamlit as st
from streamlit_modal import Modal
import pandas as pd

modal = Modal(key="boot_modal", title="자세한 정보 보기")

# CSV 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv("./data/boots.csv")
    return df

df = load_data()

# 정렬 옵션 저장 (초기화)
if "sort_order" not in st.session_state:
    st.session_state["sort_order"] = "가나다순"

# 페이지 번호 저장 (초기화)
if "page_number" not in st.session_state:
    st.session_state["page_number"] = 1

# 필터링 페이지
def filter_page():
    st.title("⚽ 축구화 찾기")

    # 필터링 UI (사이드바)
    st.sidebar.header("🔍 검색 옵션")

    # 제목 검색 기능 추가
    search_title = st.sidebar.text_input("🔍 제목 검색", "")

    # 가격대 필터
    price_ranges = ['10만원 미만', '10~15만원', '15~20만원', '20~25만원', '25~30만원', '30만원 초과']
    selected_price = st.sidebar.multiselect("💰 가격대", price_ranges)

    # 브랜드 필터 (한글 변환)
    brand_mapping = {'NIKE': '나이키', 'mizuno': '미즈노', 'adidas': '아디다스', 'PUMA': '푸마'}
    selected_brand = st.sidebar.multiselect("🏷️ 브랜드", list(brand_mapping.values()))

    # 소재 필터
    upper_options = ['니트', '소가죽', '인조가죽', '캥거루', '합성가죽']
    selected_upper = st.sidebar.multiselect("👟 소재", upper_options)

    # 길이 필터
    selected_len = st.sidebar.multiselect("📏 길이", ['short', 'medium', 'long'])

    # 발볼 필터
    selected_foot = st.sidebar.multiselect("🦶 발볼", ['narrow', 'medium', 'wide'])

    # 무게 필터
    weight_categories = ['light', 'medium', 'heavy']
    selected_weight = st.sidebar.multiselect("⚖️ 무게", weight_categories)

    # 특징 필터
    feature_options = df['feature'].dropna().unique().tolist()
    selected_features = st.sidebar.multiselect("✨ 특징", feature_options)

    # 필터링 로직 적용
    filtered_df = df.copy()

    # 제목 검색 필터 적용
    if search_title:
        filtered_df = filtered_df[filtered_df['title'].str.contains(search_title, case=False)]

    # 가격대 필터 적용
    if selected_price:
        price_conditions = []
        if '10만원 미만' in selected_price:
            price_conditions.append(filtered_df["sale_price"] < 100000)
        if '10~15만원' in selected_price:
            price_conditions.append(filtered_df["sale_price"].between(100000, 149999))
        if '15~20만원' in selected_price:
            price_conditions.append(filtered_df["sale_price"].between(150000, 199999))
        if '20~25만원' in selected_price:
            price_conditions.append(filtered_df["sale_price"].between(200000, 249999))
        if '25~30만원' in selected_price:
            price_conditions.append(filtered_df["sale_price"].between(250000, 299999))
        if '30만원 초과' in selected_price:
            price_conditions.append(filtered_df["sale_price"] > 300000)
        if price_conditions:
            filtered_df = filtered_df[pd.concat(price_conditions, axis=1).any(axis=1)]

    # 브랜드 필터 적용
    if selected_brand:
        selected_brands = [key for key, value in brand_mapping.items() if value in selected_brand]
        filtered_df = filtered_df[filtered_df["brand"].isin(selected_brands)]

    # 소재 필터 적용
    if selected_upper:
        filtered_df = filtered_df[filtered_df["upper"].apply(lambda x: set(x.split(", ")) == set(selected_upper))]    
        
    # 길이 필터 적용
    if selected_len:
        length_mapping = {
            'short': df['len_score'] <= 2,
            'medium': df['len_score'] == 3,
            'long': df['len_score'] >= 4
        }
        length_conditions = [length_mapping[len_type] for len_type in selected_len]
        filtered_df = filtered_df[pd.concat(length_conditions, axis=1).any(axis=1)]

    # 발볼 필터 적용
    if selected_foot:
        foot_mapping = {
            'narrow': df['foot_score'] <= 2,
            'medium': df['foot_score'] == 3,
            'wide': df['foot_score'] >= 4
        }
        foot_conditions = [foot_mapping[foot_type] for foot_type in selected_foot]
        filtered_df = filtered_df[pd.concat(foot_conditions, axis=1).any(axis=1)]

    # 무게 필터 적용
    if selected_weight:
        weight_conditions = []
        if 'light' in selected_weight:
            weight_conditions.append(filtered_df["weight(g)"] < 190)
        if 'medium' in selected_weight:
            weight_conditions.append(filtered_df["weight(g)"].between(190, 230))
        if 'heavy' in selected_weight:
            weight_conditions.append(filtered_df["weight(g)"] > 230)
        
        filtered_df = filtered_df[pd.concat(weight_conditions, axis=1).any(axis=1)]

    # 특징 필터 적용
    if selected_features:
        filtered_df = filtered_df[filtered_df["feature"].isin(selected_features)]

    # 정렬 옵션 버튼 추가
    col_sort1, col_sort2, col_sort3, col_sort4 = st.columns(4)
    with col_sort1:
        if st.button("가나다순"):
            st.session_state["sort_order"] = "가나다순"
    with col_sort2:
        if st.button("가나다 역순"):
            st.session_state["sort_order"] = "가나다 역순"
    with col_sort3:
        if st.button("낮은 가격순"):
            st.session_state["sort_order"] = "낮은 가격순"
    with col_sort4:
        if st.button("높은 가격순"):
            st.session_state["sort_order"] = "높은 가격순"

    # 정렬 적용
    if st.session_state["sort_order"] == "가나다순":
        filtered_df = filtered_df.sort_values(by="title", ascending=True)
    elif st.session_state["sort_order"] == "가나다 역순":
        filtered_df = filtered_df.sort_values(by="title", ascending=False)
    elif st.session_state["sort_order"] == "낮은 가격순":
        filtered_df = filtered_df.sort_values(by="sale_price", ascending=True)
    elif st.session_state["sort_order"] == "높은 가격순":
        filtered_df = filtered_df.sort_values(by="sale_price", ascending=False)
    
    # 페이지네이션 적용
    items_per_page = 10
    total_pages = max(1, -(-len(filtered_df) // items_per_page))  # 최소 1페이지 보장
    current_page = min(st.session_state["page_number"], total_pages)  # 현재 페이지가 total_pages를 초과하지 않도록 보정

    start_idx = (current_page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    paginated_df = filtered_df.iloc[start_idx:end_idx]

    # 필터링 결과 출력
    st.subheader("🔍 검색 결과")

    if not filtered_df.empty:
        for _, row in paginated_df.iterrows():  # ⬅️ `paginated_df` 사용
            with st.container():
                col1, col2 = st.columns([1, 3])  # 비율로 열 크기 조정
                with col1:
                    st.image(row["image_url"], width=100)
                with col2:
                    st.markdown(f"<p style='margin: 0; font-size: 16px;'>{row['title']}</p>", unsafe_allow_html=True)
                    st.markdown(f"<p style='margin: 2px 0; font-size: 14px;'>💰 가격: {row['sale_price']}원</p>", unsafe_allow_html=True)

                    # 팝업 창 열기 버튼
                    if st.button(f"📝 자세한 정보 보기", key=f"modal_{row['title']}"):
                        st.session_state["modal_data"] = row  # 선택된 데이터 저장
                        modal.open()  # 모달 열기
                # 구분선 추가
                st.markdown(
                    """
                    <hr style="border: 1px solid lightgray; margin: 10px 0;">
                    """,
                    unsafe_allow_html=True
                )

        # 모달 창 (모달이 열릴 때만 데이터 표시)
        if modal.is_open():
            with modal.container():
                row = st.session_state.get("modal_data", None)
                if row is not None:
                    st.image(row["image_url"], width=300)
                    st.write(f"### {row['title']}")
                    # 각 정보의 존재 여부에 따라 표시
                    price_display = f"💰 가격: {row['sale_price']}원" if pd.notna(row['sale_price']) else "💰 가격: ❌"
                    upper_display = f"👟 소재: {row['upper']}" if pd.notna(row['upper']) else "👟 소재: ❌"
                    ground_display = f"🏟️ 바닥 재질: {row['ground']}" if pd.notna(row['ground']) else "🏟️ 바닥 재질: ❌"
                    weight_display = f"⚖️ 무게: {row['weight(g)']}g" if pd.notna(row['weight(g)']) else "⚖️ 무게: ❌"
                    length_display = f"📏 길이: {row['len_score']}" if pd.notna(row['len_score']) else "📏 길이: ❌"
                    foot_display = f"🦶 발폭: {row['foot_score']}" if pd.notna(row['foot_score']) else "🦶 발폭: ❌"
                    url_display = f"[🔗 제품 링크]({row['url']})" if pd.notna(row['url']) else "🔗 제품 링크: ❌"

                    # 각 정보 출력
                    st.write(price_display)
                    st.write(upper_display)
                    st.write(ground_display)
                    st.write(weight_display)
                    st.write(length_display)
                    st.write(foot_display)
                    st.write(url_display)

                    if st.button("닫기"):
                        modal.close()
    else:
        st.write("❌ 해당 조건에 맞는 축구화가 없습니다.")
    
    # 페이지네이션 UI (가운데 정렬)
    col_center = st.columns(1)[0]  # 중앙 정렬을 위한 단일 컬럼

    with col_center:
        col_prev, col_page, col_next = st.columns([1, 3, 1])  # 이전 버튼, 페이지 번호, 다음 버튼 정렬

        with col_prev:
            if st.button("⬅️ 이전", key="prev_page") and st.session_state["page_number"] > 1:
                st.session_state["page_number"] -= 1

        with col_page:
            st.markdown(
                f"<h5 style='text-align: center;'>{st.session_state['page_number']} / {total_pages}</h5>",
                unsafe_allow_html=True
            )

        with col_next:
            if st.button("다음 ➡️", key="next_page") and st.session_state["page_number"] < total_pages:
                st.session_state["page_number"] += 1


def show_Find():
    st.query_params["pages"] = "축구화"
    filter_page()

    