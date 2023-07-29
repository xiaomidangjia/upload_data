# coding: utf-8

import json
import base64
from flask import Flask, request
import requests
import numpy as np
import pandas as pd
import csv
from datetime import datetime,timedelta
from dingtalkchatbot.chatbot import DingtalkChatbot
dingding_url = 'https://oapi.dingtalk.com/robot/send?access_token=c628ad1cf8cc3a6b5c7fb104e9d6ba407728b6891c6a465d9bbdb301d1412d41'

app = Flask(__name__)


@app.route("/upload_date", methods=['post'])
def upload_date():
    data_list = request.form.get('data_list')
    print(data_list)
    data_list = eval(data_list)
    df = pd.DataFrame()
    for i in range(len(data_list)):
        crypto_name = data_list[i]['crypto_name']
        crypto_direction = data_list[i]['crypto_direction']
        crypto_open = data_list[i]['crypto_open']
        crypto_close = data_list[i]['crypto_close']
        sub_df = pd.DataFrame({'crypto_name':crypto_name,'crypto_direction':crypto_direction,'crypto_open':crypto_open,'crypto_open':crypto_open},index=[0])
        df = pd.concat([df,sub_df])

    df.to_csv('csv_from_chen.csv',encoding='utf-8-sig',index=False)
    print(df)

    date = pd.to_datetime(str(datetime.utcnow())[0:19]) + timedelta(hours=8)

    content = '北京时间%s文件上传成功'%(date)
    
    DingtalkChatbot(dingding_url).send_text(msg=content,is_auto_at=True)

    res = {'value':'Finish'}
    return res

if __name__ == '__main__':
    app.run("0.0.0.0", port=5090)

