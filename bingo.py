import streamlit as st
import random

def get_session_state():
    if "selected_numbers" not in st.session_state:
        st.session_state.selected_numbers = []
    return st.session_state

session_state = get_session_state()

st.set_page_config(layout="wide")
st.title('システム本部 ビンゴ抽選')
col1, col2 = st.columns([1, 1])
columns1, columns2, columns3, columns4, columns5, columns6 = st.columns([1, 1, 1, 1, 1, 5])

# ボタンを抽選
with col2:
    if st.button("抽選する"):
        # 未選択の数字のリストを作成
        remaining_numbers = [num for num in range(1, 76) if num not in session_state.selected_numbers]

        # 未選択の数字がある場合にのみ抽選を行う
        if remaining_numbers:
            # ランダムに数字を選ぶ
            selected_number = random.choice(remaining_numbers)

            # 選ばれた数字をリストに追加
            session_state.selected_numbers.append(selected_number)

            # 選ばれた数字を表示
            with columns6:
                st.markdown(f"<h1 style='font-size: 48px; color: navy;'>当たり番号</h1>", unsafe_allow_html=True)
                st.markdown(f"<h1 style='font-size: 480px; color: navy;'>{selected_number}</h1>", unsafe_allow_html=True)
        else:
            with columns6:
                st.markdown(f"<h1 style='font-size: 48px; color: navy;'>すべての数字が選ばれました！</h1>", unsafe_allow_html=True)

# 選ばれた数字の一覧を表示
with col1:
    st.subheader("過去に選ばれた数字の一覧")

# 各列に数字を表示
for i, num in enumerate(session_state.selected_numbers):
    if i % 5 == 0:
        with columns1:
            st.markdown(f"<h1 style='font-size: 60px; '>{num}</h1>", unsafe_allow_html=True)
    elif i % 5 == 1:
        with columns2:
            st.markdown(f"<h1 style='font-size: 60px; '>{num}</h1>", unsafe_allow_html=True)
    elif i % 5 == 2:
        with columns3:
            st.markdown(f"<h1 style='font-size: 60px; '>{num}</h1>", unsafe_allow_html=True)
    elif i % 5 == 3:
        with columns4:
            st.markdown(f"<h1 style='font-size: 60px; '>{num}</h1>", unsafe_allow_html=True)
    elif i % 5 == 4:
        with columns5:
            st.markdown(f"<h1 style='font-size: 60px; '>{num}</h1>", unsafe_allow_html=True)