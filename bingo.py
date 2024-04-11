import streamlit as st
import pandas as pd
import boto3
import json
import os

# ページの設定
st.set_page_config(layout="wide")
st.title('在籍一覧')

def load_config():
    with open('config.json', 'r') as f:
        config = json.load(f)
    return config

# configからAWSのアクセスキーとシークレットアクセスキーを取得
config = load_config()
aws_access_key = config.get('aws_access_key')
aws_secret_key = config.get('aws_secret_key')
aws_region_name = 'ap-northeast-1'

# DynamoDBのテーブル名を設定
dynamodb_table = 'MST_EMP_LOCATION_INFO_TEST'

# AWSの認証情報を設定
session = boto3.Session(
    aws_access_key_id=aws_access_key,
    aws_secret_access_key=aws_secret_key,
    region_name=aws_region_name
)
dynamodb = session.client('dynamodb')

# DynamoDBからデータを取得する関数を定義
def get_dynamodb_data():
    response = dynamodb.scan(TableName=dynamodb_table)
    data = response['Items']
    while 'LastEvaluatedKey' in response:
        response = dynamodb.scan(TableName=dynamodb_table, ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])
    return data

# データをPandas DataFrameに変換する関数を定義
def convert_to_dataframe(data):
    df = pd.DataFrame([{k: (v.get('S') if isinstance(v, dict) else v) for k, v in item.items()} for item in data])
    df = df.apply(lambda x: x.get('S', x) if isinstance(x, dict) else x)
    return df

# 画像のURLやファイルパスを持つ列を追加 (全ての行に同じ値を設定)
image_path = "daiko-area.png"

col1, col2 = st.columns([1,1])

batch_size = 25  # ページサイズを指定

# DynamoDBからデータを取得
data = get_dynamodb_data()

# データをPandas DataFrameに変換
dataset = convert_to_dataframe(data)

# スタートIndexを1からに変更
dataset.index = range(1, len(dataset) + 1)

# 総ページ数を計算
total_pages = (len(dataset) // batch_size) + 1

with col1:
    current_page = st.number_input("ページ", min_value=1, max_value=total_pages, step=1, key="current_page")

with col1:
    st.markdown(f"Page **{current_page}** of **{total_pages}**")

start_idx = (current_page - 1) * batch_size
end_idx = min(start_idx + batch_size, len(dataset))

# 特定の列のみを表示
selected_columns = ["EMPLOYEEID", "EMPLOYEENAME", "DEPARTMENTNAME"]
column_names = {
    "EMPLOYEEID": "社員番号",
    "EMPLOYEENAME": "名前",
    "DEPARTMENTNAME": "所属"
}

renamed_columns = [column_names.get(col, col) for col in selected_columns]

with col1:
    st.dataframe(dataset[selected_columns].iloc[start_idx:end_idx].rename(columns=column_names), width=800, height=915)

with col2:
    st.image(image_path, caption='Daiko Area', width=800)
