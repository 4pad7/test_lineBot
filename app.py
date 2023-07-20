import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import openai

app = Flask(__name__)

line_bot_api = LineBotApi('2NgMj6XDHl/pILJ6UYZi8yp47m/tgB4uN2ywiIPTyDh5nkJ0Gxhw1ewaleAQsGAecr7pSfffKnyLN6LOsnL4/HgFN9FDSSvpGc4Og7oHqyNiLOAyBuUIv643iKd72HJ1/Ndubl/JNQZXIS6LhntsLQdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('b1dfd7aac117f17aba8bfc8671aa30c5')

def generate_chat_response(user_input):
    # 調用OpenAI API取得ChatGPT的回應
    openai.api_key = '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'
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=user_input,
        max_tokens=150
    )

    return response.choices[0].text.strip()

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_input = event.message.text

    # 使用OpenAI GPT-3.5 API進行回應
    response = generate_chat_response(user_input)

    # 回傳ChatGPT的回應給用戶
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response)
    )
