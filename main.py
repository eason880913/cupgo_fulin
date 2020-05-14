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
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
#access token
line_bot_api = LineBotApi('g9TEMiJ1wz9FER70S1GDtDo/1cdn1kw4GrJqH6H/jb2Dl/qXBzLyQisGb3eJrv2oND8NwFM0yyYhBd0ZFfVuiH2muZ9L0YwdBSAKT33lzFSmDs3D5xAF87F8yHOwT8MPM2l65JCRRs4mikJL7N7qyQdB04t89/1O/w1cDnyilFU=')
#chanel secret
handler = WebhookHandler('7df54a8e601725208e7bda78be90d634')

def db():
    connection = psycopg2.connect(user="wauaiqrkqsuefu",
                                        password="e7c10d0a0ff7f85b02ba84fb4260fe1629b1e467348f8f10dd4cd286223ccb84",
                                        host="ec2-3-213-192-58.compute-1.amazonaws.com",
                                        port="5432",
                                        database="da325phvld21q5")
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
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text='Are you sure?',
            actions=[
                PostbackAction(
                    label='postback',
                    text='postback text',
                    data='action=buy&itemid=1'
                ),
                MessageAction(
                    label='message',
                    text='message text1 '
                )
            ]
        )
    )
    return message

def ButtonsTemplate_send_message(product):
# 這是一個傳送按鈕的模板，架構解說
    buttons_template = TemplateSendMessage(
        alt_text='CUP&GO_預購訊息',
        template=ButtonsTemplate(
            title=f'將您要的{product}加入購物車',
            text='請選擇您要的數量',
            actions=[
                MessageTemplateAction(
                    label='1',
                    text='ButtonsTemplate'
                ),
                MessageTemplateAction(
                    label='2',
                    text='ButtonsTemplate'
                ),
                MessageTemplateAction(
                    label='3',
                    text='ButtonsTemplate'
                ),
                MessageTemplateAction(
                    label='4',
                    text='ButtonsTemplate'
                )
            ]
        )
    )
    return buttons_template

def menu_Carousel_Template():
    message = TemplateSendMessage(
        alt_text='CUP&GO_預購訊息',
        template=CarouselTemplate(
            columns=[
                CarouselColumn(
                    # thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/88/Number_1_in_green_rounded_square.svg/200px-Number_1_in_green_rounded_square.svg.png',
                    title='訂購鬆餅',
                    text='請選擇您要的商品',
                    actions=[
                        MessageTemplateAction(
                            label='原味鬆餅 $35',
                            text='訂購原味鬆餅'
                        ),
                        MessageTemplateAction(
                            label='巧克力鬆餅 $40',
                            text='訂購巧克力鬆餅'
                        ),
                        MessageTemplateAction(
                            label='蜂蜜鬆餅 $40',
                            text='訂購蜂蜜鬆餅'
                        )
                    ]
                ),
                CarouselColumn(
                    # thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRuo7n2_HNSFuT3T7Z9PUZmn1SDM6G6-iXfRC3FxdGTj7X1Wr0RzA',
                    title='訂購拿鐵咖啡',
                    text='請選擇您要的商品',
                    actions=[
                        MessageTemplateAction(
                            label='Hot/S $35',
                            text='訂購小杯熱拿鐵'
                        ),
                        MessageTemplateAction(
                            label='Hot/M $45',
                            text='訂購中杯熱拿鐵'
                        ),
                        MessageTemplateAction(
                            label='Ice/M $45',
                            text='訂購中杯冰拿鐵'
                        )
                    ]
                ),
                CarouselColumn(
                    # thumbnail_image_url='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRuo7n2_HNSFuT3T7Z9PUZmn1SDM6G6-iXfRC3FxdGTj7X1Wr0RzA',
                    title='訂購美式咖啡',
                    text='請選擇您要的商品',
                    actions=[
                        MessageTemplateAction(
                            label='Hot/S $35',
                            text='訂購小杯熱美式'
                        ),
                        MessageTemplateAction(
                            label='Hot/M $45',
                            text='訂購中杯熱美式'
                        ),
                        MessageTemplateAction(
                            label='Ice/M $45',
                            text='訂購中杯冰美式'
                        )
                    ]
                ),
                CarouselColumn(
                    # thumbnail_image_url='https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Number_3_in_yellow_rounded_square.svg/200px-Number_3_in_yellow_rounded_square.svg.png',
                    title='購物車',
                    text='請選擇您要的操作',
                    actions=[
                        MessageTemplateAction(
                            label='查詢我的購物車',
                            text='查詢我的購物車'
                        ),
                        MessageTemplateAction(
                            label='清空我的購物車',
                            text='清空我的購物車'
                        ),
                        MessageTemplateAction(
                            label='送出我的購物車',
                            text='送出我的購物車'
                        )
                    ]
                )
            ]
        )
    )
    return message

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    msg = event.message.text
    user_id = event.source.user_id  
    if '查詢menu' == msg:
        image_message = ImageSendMessage(
        original_content_url='https://i.imgur.com/TtPRnen.jpg',
        preview_image_url='https://i.imgur.com/TtPRnen.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message)

    if '最近活動' == msg:
        image_message = ImageSendMessage(
        original_content_url='https://i.imgur.com/yxkG6KD.jpg',
        preview_image_url='https://i.imgur.com/yxkG6KD.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message)

    if '今日油價' == msg:
        ans1 = requests.get('https://gas.goodlife.tw/')
        ans1.encoding = 'utf-8'
        soup1 = BeautifulSoup(ans1.text,'html.parser')
        a = soup1.select("[id='cpc'] ul")[0].text
        a=a.replace(' ','')
        a=a.replace('\n','')
        a=a.replace('92:','92油價:')
        a=a.replace('95油價:','\n95油價:')
        a=a.replace('98:','\n98油價:')
        a=a.replace('柴油:','\n柴油油價:')  
        ddd = TextSendMessage(text=a)
        line_bot_api.reply_message(event.reply_token, ddd)

    if '555' == msg:
        message = buttons_message11()
        line_bot_api.reply_message(event.reply_token, message)

    if '線上點餐' == msg:
        message = menu_Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    
    if '訂購原味鬆餅' == msg:
        product = '原味鬆餅'
        message = ButtonsTemplate_send_message(product)
        line_bot_api.reply_message(event.reply_token, message)
    if '訂購巧克力鬆餅' == msg:
        product = '巧克力鬆餅'
        message = ButtonsTemplate_send_message(product)
        line_bot_api.reply_message(event.reply_token, message)
    if '訂購小杯熱拿鐵' == msg:
        product = '小杯熱拿鐵'
        message = ButtonsTemplate_send_message(product)
        line_bot_api.reply_message(event.reply_token, message)
    if '訂購中杯熱拿鐵' == msg:
        product = '中杯熱拿鐵'
        message = ButtonsTemplate_send_message(product)
        line_bot_api.reply_message(event.reply_token, message)
    if '訂購中杯冰拿鐵' == msg:
        product = '中杯冰拿鐵'
        message = ButtonsTemplate_send_message(product)
        line_bot_api.reply_message(event.reply_token, message)
    if '訂購小杯熱美式' == msg:
        product = '小杯熱美式'
        message = ButtonsTemplate_send_message(product)
        line_bot_api.reply_message(event.reply_token, message)
    if '訂購中杯熱美式' == msg:
        product = '中杯熱美式'
        message = ButtonsTemplate_send_message(product)
        line_bot_api.reply_message(event.reply_token, message)
    if '訂購中杯冰美式' == msg:
        product = '中杯冰美式'
        message = ButtonsTemplate_send_message(product)
        line_bot_api.reply_message(event.reply_token, message)



if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)