import streamlit as st
import random

# スクリプトの最初にページの設定を行う
st.set_page_config(layout="wide")

# セッション状態を管理するための関数
def get_session_state():
    if "selected_numbers" not in st.session_state:
        st.session_state.selected_numbers = []
    return st.session_state

session_state = get_session_state()

import base64

def get_base64_encoded_image(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode('utf-8')

image_path = "test.png"  # 背景画像パス
encoded_image = get_base64_encoded_image(image_path)

# CSS文字列にdata:image/png;base64,プレフィックスを追加
css = f'''
<style>
    .stApp {{
        background-image: url("data:image/png;base64,{encoded_image}");
        background-size: cover;
        background-position: center;
        background-attachment: scroll;
        background-color:rgba(255,255,255,0.4);
    }}
    .stApp > header {{
        background-color: transparent;
    }}
</style>
'''
st.markdown(css, unsafe_allow_html=True)

# ボタンのカスタムスタイルを定義
button_css = """
<style>
div.stButton > button:first-child {
    font-weight: bold;                /* 文字: 太字 */
    border: 20px solid #FF9999;       /* 枠線: 薄めの赤色で20ピクセルの実線 */
    border-radius: 10px;              /* 枠線: 半径10ピクセルの角丸 */
    background-color: #FF9999;        /* 背景色: 薄めの赤 */
    color: #fff;                      /* 文字色: 白 */
}

div.stButton > button:first-child:hover,
div.stButton > button:first-child:active,
div.stButton > button:first-child:focus {
    background-color: #FF9999;        /* 背景色: 薄めの赤 */
    border: 20px solid #FF9999;       /* 枠線: 薄めの赤色で20ピクセルの実線 */
    color: #fff;                      /* 文字色: 白 */
}
</style>
"""

# スタイルをページに適用
st.markdown(button_css, unsafe_allow_html=True)

# タイトルと抽選ボタンの配置
col1, col2 , col3 = st.columns([4, 2, 6])
columns1, columns2, columns3, columns4, columns5, columns6, columns7, columns8 = st.columns([2, 2, 2, 2, 2, 3, 7, 3])

with col1:
    st.title('システム本部 ビンゴ抽選')

with col2:    
    image = "dchan.png"
    st.image(image, width=140)

# 抽選ボタンの配置と機能
with col3:
    if st.button("抽選する"):
        remaining_numbers = [num for num in range(1, 76) if num not in session_state.selected_numbers]
        # 未選択の数字がある場合にのみ抽選を行う
        if remaining_numbers:
            # ランダムに数字を選ぶ
            selected_number = random.choice(remaining_numbers)

            # 選ばれた数字をリストに追加
            session_state.selected_numbers.append(selected_number)

            # 選ばれた数字を表示
            with col3:
                st.markdown(f"<h1 style='font-size: 48px; color: navy;'>当たり番号</h1>", unsafe_allow_html=True)
            with columns7:
                st.markdown(f"<h1 style='text-align: right; font-size: 480px; color: navy;'>{selected_number}</h1>", unsafe_allow_html=True)
        else:
            with columns7:
                st.markdown(f"<h1 style='font-size: 48px; color: navy;'>すべての数字が選ばれました！</h1>", unsafe_allow_html=True)

# 選ばれた数字の一覧を表示
with col1:
    st.subheader("過去に選ばれた数字の一覧")

# 各列に数字を表示
for i, num in enumerate(session_state.selected_numbers[::-1]):  # リストを逆順にする
    html_code = f"<h1 style='text-align: right; font-size: 60px;'>{num}</h1>"
    if i % 5 == 0:
        with columns1:
            st.markdown(html_code, unsafe_allow_html=True)
    elif i % 5 == 1:
        with columns2:
            st.markdown(html_code, unsafe_allow_html=True)
    elif i % 5 == 2:
        with columns3:
            st.markdown(html_code, unsafe_allow_html=True)
    elif i % 5 == 3:
        with columns4:
            st.markdown(html_code, unsafe_allow_html=True)
    elif i % 5 == 4:
        with columns5:
            st.markdown(html_code, unsafe_allow_html=True)
