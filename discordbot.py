# discord.pyの読み込み
import discord
import requests
import notiontest2
from pprint import pprint


#　discord botのアクセストークン
TOKEN = ''
#　botが発言するdiscordチャンネルのID（一般）
CHANNEL_ID = 873153988332245005
CHANNEL_SEND_ID = 873175549042888764


# 接続に必要なオブジェクトを生成
client = discord.Client()


# 起動時にbotが挨拶するプログラム
async def greet():
    channel = client.get_channel(CHANNEL_ID)
    await channel.send('botが起動しました。おはよう')


@client.event
async def on_ready():
    # 起動したらターミナルにログイン通知が表示される
    print('ログインしましたよ')
    await greet()


# メッセージ受信時に動作する処理
@client.event
async def on_message(message):
    # Botのメッセージは除外
    if message.author.bot:
        return

    # 条件に当てはまるメッセージかチェックし正しい場合は返す
    def check(msg):
        return msg.author == message.author

    # /getとチャンネル上に打ち込むとBotが反応を示す
    if message.content.startswith("/get"):

        # /getと打ち込まれたチャンネル上に下記の文章を出力
        await message.channel.send("作成する記事のタイトルを入力してください")

        # ユーザーからのメッセージを待つ
        page_title = await client.wait_for("message", check=check)

        # メッセージを打ち込まれたのを確認すると下記の文章を出力

        await message.channel.send("転送したいメッセージのIDを入力してください。")

        # ユーザーからのメッセージを待つ
        message_id_1 = await client.wait_for("message", check=check)

        # メッセージを打ち込まれたのを確認すると下記の文章を出力

        await message.channel.send("転送したいメッセージのIDをもう一つ入力してください。")

        # ユーザーからのメッセージを待つ
        message_id_2 = await client.wait_for("message", check=check)

        # メッセージを打ち込まれたのを確認すると下記の文章を出力
        await message.channel.send("保存したメッセージはこちらになるよ！")

        #チャンネルからメッセージを取得
        channel = client.get_channel(CHANNEL_ID)
        get_message_by_id_1 = await channel.fetch_message(message_id_1.content)
        get_message_by_id_2 = await channel.fetch_message(message_id_2.content)

        print('作成された記事のタイトル：', page_title.content)
        print('転送内容1：', get_message_by_id_1.content)
        print('転送内容2：', get_message_by_id_2.content)

        # 取得したメッセージを書き込まれたチャンネルへ送信
        await message.channel.send(page_title.content)
        await message.channel.send(get_message_by_id_1.content)
        await message.channel.send(get_message_by_id_2.content)

        # 取得したメッセージを書き込まれたチャンネルへ送信
        channel_send = client.get_channel(CHANNEL_SEND_ID)
        await channel_send.send(page_title.content)
        await channel_send.send(get_message_by_id_1.content)
        notiontest2.send_to_notion(page_title.content, get_message_by_id_1.content, get_message_by_id_2.content)
        # 転送したことを伝えるメッセージ
        await message.channel.send("転送先チャンネルとNotionにメッセージを転送しました")

# botの起動とDiscordサーバーへの接続
client.run(TOKEN)

