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
cursor = db()

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

def lineNotifyMessage(token, msg):
    headers = {
        "Authorization": "Bearer " + token, 
        "Content-Type" : "application/x-www-form-urlencoded"
    }

    payload = {'message': msg}
    r = requests.post("https://notify-api.line.me/api/notify", headers = headers, params = payload)
    return r.status_code

def buttons_message11(sendtime):
    message = TemplateSendMessage(
        alt_text='Confirm template',
        template=ConfirmTemplate(
            text='確認要送出購物車嗎?',
            actions=[
                MessageAction(
                    label='確認',
                    text=f'確認送出購物車,{sendtime}0分鐘以後取餐'
                ),
                MessageAction(
                    label='稍後一下好了',
                    text='線上點餐'
                )
            ]
        )
    )
    return message

def ButtonsTemplate_time():
# 這是一個傳送按鈕的模板，架構解說
    buttons_template = TemplateSendMessage(
        alt_text='CUP&GO_預購訊息',
        template=ButtonsTemplate(
            title=f'請選擇幾分鐘後要取餐',
            text='請選擇您要的時間',
            actions=[
                MessageTemplateAction(
                    label='10分鐘後自行取餐',
                    text=f'送出購物車10分鐘後取餐'
                ),
                MessageTemplateAction(
                    label='20分鐘後自行取餐',
                    text=f'送出購物車20分鐘後取餐'
                ),
                MessageTemplateAction(
                    label='30分鐘後自行取餐',
                    text=f'送出購物車30分鐘後取餐'
                ),
                MessageTemplateAction(
                    label='回去繼續選購',
                    text=f'線上點餐'
                )
            ]
        )
    )
    return buttons_template

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
                    text=f'將1個{product}放入購物車'
                ),
                MessageTemplateAction(
                    label='2',
                    text=f'將2個{product}放入購物車'
                ),
                MessageTemplateAction(
                    label='3',
                    text=f'將3個{product}放入購物車'
                ),
                MessageTemplateAction(
                    label='4',
                    text=f'將4個{product}放入購物車'
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
        original_content_url='https://i.imgur.com/YAJzTII.jpg',
        preview_image_url='https://i.imgur.com/YAJzTII.jpg'
        )
        line_bot_api.reply_message(event.reply_token, image_message)

    if '優惠內容' == msg:
        image_message = ImageSendMessage(
        original_content_url='https://imgur.com/VgZmbie.jpg',
        preview_image_url='https://imgur.com/VgZmbie.jpg'
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

    if '分鐘後取餐' in msg:
        msg = re.findall('\\d',msg)
        num = msg[0]
        message = buttons_message11(num)
        line_bot_api.reply_message(event.reply_token, message)

    if '線上點餐' == msg:
        try:
            cursor.execute(f'INSERT INTO "public"."main" ("uid","choco_cake","origin_cake","honey_cake","hm_latte","hs_latte","im_latte","hm_coffee","hs_coffee","im_coffee","time")'+f"VALUES ('{user_id}','0','0','0','0','0','0','0','0','0','0');")
            cursor.execute("COMMIT")
        except:
            # print('fail')
            cursor.execute("ROLLBACK")
        message = menu_Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    
    if '已加入購物車' == msg:
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
    if '訂購蜂蜜鬆餅' == msg:
        product = '蜂蜜鬆餅'
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

    if '原味鬆餅放入購物車' in msg:
        msg = re.findall('\\d',msg)
        num = msg[0]
        # message = TextSendMessage(text='已加入購物車')
        cursor.execute(f'SELECT origin_cake FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        num = int(data[0][0])+int(num)
        cursor.execute(f'UPDATE "public"."main" SET "origin_cake"'+f"= '{num}'"+'WHERE "uid"'+f" = '{user_id}';")
        cursor.execute("COMMIT")
        # line_bot_api.reply_message(event.reply_token, message)
        message = menu_Carousel_Template()
        line_bot_api.reply_message(event.reply_token, message)
    if '巧克力鬆餅放入購物車' in msg:
        msg = re.findall('\\d',msg)
        num = msg[0]
        message = TextSendMessage(text='已加入購物車')
        cursor.execute(f'SELECT choco_cake FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        num = int(data[0][0])+int(num)
        cursor.execute(f'UPDATE "public"."main" SET "choco_cake"'+f"= '{num}'"+'WHERE "uid"'+f" = '{user_id}';")
        cursor.execute("COMMIT")
        line_bot_api.reply_message(event.reply_token, message)
    if '蜂蜜鬆餅放入購物車' in msg:
        msg = re.findall('\\d',msg)
        num = msg[0]
        message = TextSendMessage(text='已加入購物車')
        cursor.execute(f'SELECT honey_cake FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        num = int(data[0][0])+int(num)
        cursor.execute(f'UPDATE "public"."main" SET "honey_cake"'+f"= '{num}'"+'WHERE "uid"'+f" = '{user_id}';")
        cursor.execute("COMMIT")
        line_bot_api.reply_message(event.reply_token, message)
    if '小杯熱拿鐵放入購物車' in msg:
        msg = re.findall('\\d',msg)
        num = msg[0]
        message = TextSendMessage(text='已加入購物車')
        cursor.execute(f'SELECT hs_latte FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        num = int(data[0][0])+int(num)
        cursor.execute(f'UPDATE "public"."main" SET "hs_latte"'+f"= '{num}'"+'WHERE "uid"'+f" = '{user_id}';")
        cursor.execute("COMMIT")
        line_bot_api.reply_message(event.reply_token, message)
    if '中杯熱拿鐵放入購物車' in msg:
        msg = re.findall('\\d',msg)
        num = msg[0]
        message = TextSendMessage(text='已加入購物車')
        cursor.execute(f'SELECT hm_latte FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        num = int(data[0][0])+int(num)
        cursor.execute(f'UPDATE "public"."main" SET "hm_latte"'+f"= '{num}'"+'WHERE "uid"'+f" = '{user_id}';")
        cursor.execute("COMMIT")
        line_bot_api.reply_message(event.reply_token, message)
    if '中杯冰拿鐵放入購物車' in msg:
        msg = re.findall('\\d',msg)
        num = msg[0]
        message = TextSendMessage(text='已加入購物車')
        cursor.execute(f'SELECT im_latte FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        num = int(data[0][0])+int(num)
        cursor.execute(f'UPDATE "public"."main" SET "im_latte"'+f"= '{num}'"+'WHERE "uid"'+f" = '{user_id}';")
        cursor.execute("COMMIT")
        line_bot_api.reply_message(event.reply_token, message)
    if '小杯熱美式放入購物車' in msg:
        msg = re.findall('\\d',msg)
        num = msg[0]
        message = TextSendMessage(text='已加入購物車')
        cursor.execute(f'SELECT hs_coffee FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        num = int(data[0][0])+int(num)
        cursor.execute(f'UPDATE "public"."main" SET "hs_coffee"'+f"= '{num}'"+'WHERE "uid"'+f" = '{user_id}';")
        cursor.execute("COMMIT")
        line_bot_api.reply_message(event.reply_token, message)
    if '中杯熱美式放入購物車' in msg:
        msg = re.findall('\\d',msg)
        num = msg[0]
        message = TextSendMessage(text='已加入購物車')
        cursor.execute(f'SELECT hm_coffee FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        num = int(data[0][0])+int(num)
        cursor.execute(f'UPDATE "public"."main" SET "hm_coffee"'+f"= '{num}'"+'WHERE "uid"'+f" = '{user_id}';")
        cursor.execute("COMMIT")
        line_bot_api.reply_message(event.reply_token, message)
    if '中杯冰美式放入購物車' in msg:
        msg = re.findall('\\d',msg)
        num = msg[0]
        message = TextSendMessage(text='已加入購物車')
        cursor.execute(f'SELECT im_coffee FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        num = int(data[0][0])+int(num)
        cursor.execute(f'UPDATE "public"."main" SET "im_coffee"'+f"= '{num}'"+'WHERE "uid"'+f" = '{user_id}';")
        cursor.execute("COMMIT")
        line_bot_api.reply_message(event.reply_token, message)

    if '查詢我的購物車' == msg:
        cursor.execute(f'SELECT * FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        for i in data:
            price = 0
            price_list = [0,40,35,40,45,35,45,45,35,45]
            txt = ''
            lsit = [0,'巧克力鬆餅','原味鬆餅','蜂蜜鬆餅','中杯熱拿鐵','小杯熱拿鐵','中杯冰拿鐵','中杯熱美式','小杯熱美式','中杯冰美式']
            for j in range(1,len(i)):
                if str(i[j]) == '0':
                    continue
                txt = txt+str(i[j])+'個'+str(lsit[j]+',')
                price = price + int(price_list[j])*int(i[j])
            txt = re.sub(',$','',txt)    
            txt = txt+',共計'+str(price)+'元'
            if txt == ',共計0元':
                txt = '購物車裡沒有任何商品'
            message = TextSendMessage(text=txt)
            line_bot_api.reply_message(event.reply_token, message)

    if '清空我的購物車' == msg:
        cursor.execute(f'DELETE FROM "public"."main" WHERE "uid"'+f" = '{user_id}';")
        cursor.execute("COMMIT")
        cursor.execute(f'INSERT INTO "public"."main" ("uid","choco_cake","origin_cake","honey_cake","hm_latte","hs_latte","im_latte","hm_coffee","hs_coffee","im_coffee","time")'+f"VALUES ('{user_id}','0','0','0','0','0','0','0','0','0','0');")
        cursor.execute("COMMIT")
        message = TextSendMessage(text='已清空購物車')
        line_bot_api.reply_message(event.reply_token, message)

    if '送出我的購物車' == msg:
        cursor.execute(f'SELECT * FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        for i in data:
            price = 0
            price_list = [0,40,35,40,45,35,45,45,35,45]
            txt = ''
            lsit = [0,'巧克力鬆餅','原味鬆餅','蜂蜜鬆餅','中杯熱拿鐵','小杯熱拿鐵','中杯冰拿鐵','中杯熱美式','小杯熱美式','中杯冰美式']
            for j in range(1,len(i)):
                if str(i[j]) == '0':
                    continue
                txt = txt+str(i[j])+'個'+str(lsit[j]+',')
                price = price + int(price_list[j])*int(i[j])
            txt = re.sub(',$','',txt)    
            txt = txt+',共計'+str(price)+'元'
            if txt == ',共計0元':
                txt = '購物車裡沒有任何商品'
        if txt == '購物車裡沒有任何商品':
            message = TextSendMessage(text='購物車裡沒有任何商品')
            line_bot_api.reply_message(event.reply_token, message)
        else:
            message = ButtonsTemplate_time()
            line_bot_api.reply_message(event.reply_token, message)
    
    if '確認送出購物車' in msg:
        msg = re.findall('\\d',msg)
        num = msg[0]#單個字
        cursor.execute(f'SELECT * FROM "public"."main" WHERE "uid"'+ f"= '{user_id}';")
        data = cursor.fetchall()
        for i in data:
            price = 0
            price_list = [0,40,35,40,45,35,45,45,35,45]
            txt = ''
            lsit = [0,'巧克力鬆餅','原味鬆餅','蜂蜜鬆餅','中杯熱拿鐵','小杯熱拿鐵','中杯冰拿鐵','中杯熱美式','小杯熱美式','中杯冰美式']
            for j in range(1,len(i)):
                if str(i[j]) == '0':
                    continue
                txt = txt+str(i[j])+'個'+str(lsit[j]+',')
                price = price + int(price_list[j])*int(i[j])
            txt = re.sub(',$','',txt)    
            txt = txt+',共計'+str(price)+'元'
            if txt == ',共計0元':
                txt = '購物車裡沒有任何商品'
            message = f'顧客編號（{user_id}）'+str(txt)+f"{num}0分鐘後取餐"
        token = 'bMehRmUFrwZziaZJmHOqkF5Xen4QmMh0bVz6TlHFaqq' #for 測試
        lineNotifyMessage(token, message)
        message = TextSendMessage(text='您的預購訂單已成功，請務必來取餐喔')
        line_bot_api.reply_message(event.reply_token, message)
        cursor.execute(f'DELETE FROM "public"."main" WHERE "uid"'+f" = '{user_id}';")
        cursor.execute("COMMIT")
        cursor.execute(f'INSERT INTO "public"."main" ("uid","choco_cake","origin_cake","honey_cake","hm_latte","hs_latte","im_latte","hm_coffee","hs_coffee","im_coffee","time")'+f"VALUES ('{user_id}','0','0','0','0','0','0','0','0','0','0');")
        cursor.execute("COMMIT")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)