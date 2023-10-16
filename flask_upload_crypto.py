# coding: utf-8

import json
import base64
from flask import Flask, request
import requests
import numpy as np
import pandas as pd
import csv
from datetime import datetime,timedelta
#from dingtalkchatbot.chatbot import DingtalkChatbot
dingding_url = 'https://oapi.dingtalk.com/robot/send?access_token=c628ad1cf8cc3a6b5c7fb104e9d6ba407728b6891c6a465d9bbdb301d1412d41'

app = Flask(__name__)


@app.route("/upload_date", methods=['post'])
def upload_date():
    crypto_time = request.form.get('crypto_time')
    crypto_id = request.form.get('crypto_id')
    crypto_name = request.form.get('crypto_name')
    crypto_direction = request.form.get('crypto_direction')
    crypto_type = request.form.get('crypto_type')
    crypto_open = request.form.get('crypto_open')
    crypto_win = request.form.get('crypto_win')
    crypto_loss = request.form.get('crypto_loss')

    sub_df = pd.DataFrame({'crypto_time':crypto_time,'crypto_id':crypto_id,'crypto_name':crypto_name,'crypto_direction':crypto_direction,'crypto_type':crypto_type,'crypto_open':crypto_open,'crypto_win':crypto_win,'crypto_loss':crypto_loss},index=[0])

    # 读取历史开单记录
    p = []
    with open("/root/upload_data/csv_from_chen.csv", 'r', encoding="UTF-8") as fr:
        reader = csv.reader(fr)
        for index, line in enumerate(reader):
            if index == 0:
                continue
            p.append(line)
    res_data = pd.DataFrame(p)
    res_data['crypto_time'] = res_data.iloc[:,0]
    res_data['crypto_id'] = res_data.iloc[:,1]
    res_data['crypto_name'] = res_data.iloc[:,2]
    res_data['crypto_direction'] = res_data.iloc[:,3]
    res_data['crypto_type'] = res_data.iloc[:,4]
    res_data['crypto_open'] = res_data.iloc[:,5]
    res_data['crypto_win'] = res_data.iloc[:,6]
    res_data['crypto_loss'] = res_data.iloc[:,7]

    res_data = res_data[['crypto_time','crypto_id','crypto_name','crypto_direction','crypto_type','crypto_open','crypto_win','crypto_loss']]

    ins = pd.concat([res_data,sub_df])
    ins['crypto_time'] = pd.to_datetime(res_data['crypto_time'])

    ins = ins[['crypto_time','crypto_id','crypto_name','crypto_direction','crypto_type','crypto_open','crypto_win','crypto_loss']]

    ins.to_csv('/root/upload_data/csv_from_chen.csv',encoding='utf-8-sig',index=False)

    #DingtalkChatbot(dingding_url).send_text(msg=content,is_auto_at=True)

    res = {'value':'Finish'}
    return res

if __name__ == '__main__':
    app.run("0.0.0.0", port=5090)

