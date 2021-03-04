import os
import json

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, FollowEvent,
    TextMessage, TextSendMessage,
    FlexSendMessage, CarouselContainer, BubbleContainer
)


app = Flask(__name__)

line_bot_api = LineBotApi(os.environ['CHANNEL_ACCESS_TOKEN'])
handler = WebhookHandler(os.environ['CHANNEL_SECRET'])


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(FollowEvent)
def handle_follow(event):
    print(event)
    with open('./test.json', 'r', encoding='utf-8') as f:
        json_dict = json.load(f)
        flex_message = FlexSendMessage(
            alt_text='hello',
            contents=CarouselContainer.new_from_json_dict(json_dict)
        )
        line_bot_api.reply_message(
            event.reply_token,
            flex_message
        )


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    if event.message.text == 'test-for-concurrency':
        with open('./test.json', 'r', encoding='utf-8') as f:
            json_dict = json.load(f)
            flex_message = FlexSendMessage(
                alt_text='hello',
                contents=CarouselContainer.new_from_json_dict(json_dict)
            )
            line_bot_api.reply_message(
                event.reply_token,
                flex_message
            )


# if __name__ == "__main__":
#     app.run()

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=os.environ['PORT'])
