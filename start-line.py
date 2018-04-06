from flask import Flask, request, abort

from linebot import (
 LineBotApi, WebhookHandler
)
from linebot.exceptions import (
 InvalidSignatureError
)
from linebot.models import (
 MessageEvent, TextMessage, TextSendMessage,
)
from UtteranceGenerator import DialogSystem

app = Flask(__name__)

line_bot_api = LineBotApi('Il5ntJJbGapc2265f9neBuJBQ9xyV/08zLfnwicaWsO80JyIOPFy8topmAtZOsggneggfMgPkZmQEvdbd1o5Qc2fYPMEnQEH7rsJButuhDQQtDO336AIon4dcFe2QfUgXNGteVZdgGGPAjFuD4+trwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('f5a89be9136ceacd3bfaf63709a8df4b')


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    event.message.text
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=dia.main(event.message.text)))


if __name__ == "__main__":
    dia = DialogSystem()
    dia.preprocessor.GTPP[0] = ["NEWGAME!",None]
    dia.url = None
    app.run()
