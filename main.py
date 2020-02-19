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
from linebot.models import *
import re
import time
import psycopg2
import os

app = Flask(__name__)
#access token
line_bot_api = LineBotApi('g9TEMiJ1wz9FER70S1GDtDo/1cdn1kw4GrJqH6H/jb2Dl/qXBzLyQisGb3eJrv2oND8NwFM0yyYhBd0ZFfVuiH2muZ9L0YwdBSAKT33lzFSmDs3D5xAF87F8yHOwT8MPM2l65JCRRs4mikJL7N7qyQdB04t89/1O/w1cDnyilFU=')
#chanel secret
handler = WebhookHandler('7df54a8e601725208e7bda78be90d634')

def db():
    connection = psycopg2.connect(user="jgdzuegjyzrqki",
                                        password="ee8990b454a75de5ef6a9f3232743cd0247b48430f6122efb9872c39b49ba629",
                                        host="ec2-54-163-226-238.compute-1.amazonaws.com",
                                        port="5432",
                                        database="denfkj5rv5tjoc")
    cursor = connection.cursor()
    return cursor

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
#建立rechmenu
@app.route("/richmenu", methods=["GET"])
def rich_menu():
    #creat rich menu
    rich_menu_to_create = RichMenu(
        size=RichMenuSize(width=1200, height=405),
        selected=False,
        name="Nice richmenu",
        chat_bar_text="Tap here",
        areas=[RichMenuArea(
            bounds=RichMenuBounds(x=0, y=0, width=2500, height=1686),
            action=URIAction(label='Go to line.me', uri='https://line.me'))]   
    )          
        #action=URIAction(label='Go to line.me', uri='https://line.me'))]   
    rich_menu_id = line_bot_api.create_rich_menu(rich_menu=rich_menu_to_create)
    print(rich_menu_id)

    #set_rich_menu_image
    content_type = "image/jpeg"
    with open('72890300_520706825417159_8288948115734528000_n.jpg', 'rb') as f:
        line_bot_api.set_rich_menu_image(rich_menu_id, content_type, f)

    # 
    #line_bot_api.set_default_rich_menu(rich_menu_id)
    
    #get_default_rich_menu
    # line_bot_api.get_default_rich_menu()
    return 'OK', 200

#刪除richmenu
@app.route("/richmenu/<id123>", methods=["POST"])
def drich_menu(id123):
    rich_menu_id = id123
    #delete rich menu
    line_bot_api.delete_rich_menu(rich_menu_id)
 
    return 'OK', 200
#時刻表
def buttons_message11():
    message = TemplateSendMessage(
        alt_text='查詢時刻表',
        template=ButtonsTemplate(
            title="查詢時刻表",
            text="請問要查詢哪一個",
            actions=[
                MessageTemplateAction(
                    label="營業日期",
                    text="查詢營業日期"
                ),
                MessageTemplateAction(
                    label="班次",
                    text="查詢班次"
                )
            ]
        )
    )
    return message

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    user_id = event.source.user_id  
    if 'essaim880913' in msg:
        rich_menu_id = 'richmenu-2cee31ae90f88cb370e04f9efe1ce952'
        line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)
    if '574983261' in msg:
        rich_menu_id = 'richmenu-ed75132381729538800fc4ee274be208'
        line_bot_api.link_rich_menu_to_user(user_id, rich_menu_id)
    rich_menu_list = line_bot_api.get_rich_menu_list()
    for rich_menu in rich_menu_list:
        print(rich_menu.rich_menu_id)
    if '查詢時刻表' == msg:
        message = buttons_message11()
        line_bot_api.reply_message(event.reply_token, message)
    if '查詢營業日期' == msg:
        image_message = ImageSendMessage(
        original_content_url='https://imgur.com/HVn3HTo.jpg',
        preview_image_url='https://imgur.com/Osi6gUd.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    if '查詢班次' == msg:
        image_message = ImageSendMessage(
        original_content_url='https://imgur.com/fUlpm2P.jpg',
        preview_image_url='https://imgur.com/MCWyo68.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message)
    if '聯絡資訊' == msg:
        ddd = TextSendMessage(text='Fb：XXXXXX\nGmail：XXXXXX@gmail.com\n電話：02—XXXX XXXX')
        line_bot_api.reply_message(event.reply_token, ddd)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)