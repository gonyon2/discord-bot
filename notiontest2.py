import requests
from pprint import pprint

import json
import datetime


from notion.client import NotionClient
from notion.block import BasicBlock, BulletedListBlock, TodoBlock
from notion.block import PageBlock


def send_to_notion(title, message1, message2):
    page_title = title
    page_content1 = message1
    page_content2 = message2

    def get_request_url(end_point):
        return f'https://api.notion.com/v1/{end_point}'

    notion_api_key = 'your api key'
    databases_id = 'your database id'
    headers = {"Authorization": f"Bearer {notion_api_key}",
               "Content-Type": "application/json",
               "Notion-Version": "2021-07-27",
               }

    property_name = {"title": [{"text": {"content": page_title}}]}
    property_date = {"date": {"start": datetime.datetime(
        year=2021, month=8, day=4).isoformat()}}
    property_select = {"select": {"name": "カツオ"}}
    body = {
        "parent": {
            "database_id": databases_id},
        "properties": {
            "Name": property_name,
            "日付": property_date,
            "作成者": property_select
        }}

    response = requests.request('POST', url=get_request_url(
        'pages'), headers=headers, data=json.dumps(body))
    pprint(response.json())

    added_page_json_obj = response.json()
    added_page_url = added_page_json_obj['url']
    pprint(added_page_url)


    token_v2 = 'your token_v2'  # 持っているtoken_v2
    client = NotionClient(token_v2=token_v2)

    # 対象ページのURL
    print("対象ページのurl :", added_page_url)
    url = "your page url"
    page = client.get_block(url)

    print("Page hoga  :", page.title)

    ################################
    # API の呼び出しに PageBlock 追加
    ################################
    print(page.children.add_new(PageBlock, title = page_title))

    ####################################
    # PageBlockにTodoBlock追加
    ####################################
    for child in page.children:
        child_page = client.get_block(child.id)
        child_page.children.add_new(BulletedListBlock, title = page_content1)
        child_page.children.add_new(BulletedListBlock, title = page_content2)

