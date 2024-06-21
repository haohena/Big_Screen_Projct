# -*- coding: UTF-8 -*-
from flask import Flask, request, current_app
from flask_cors import CORS
import logging
import json
import datetime
import os
app_flask = Flask(__name__)
app_flask.logger.setLevel(logging.DEBUG)
CORS(app_flask, supports_credentials=True)
@app_flask.route('/api/camera/dataUpload',methods=['POST'])
def get_data():
    passflow = request.data.decode("utf-8")
    with open("passflow.txt","a") as file:
        file.write(passflow+ "\n")
        print('success write')
    current_app.logger.debug(passflow)

    current_date = datetime.date.today()
    now = datetime.datetime.now()
    current_hour = now.hour
    folder_month = "month"
    folder_day = 'day'
    folder_log = 'logger_day'
    os.makedirs(folder_day,exist_ok=True)
    os.makedirs(folder_month,exist_ok=True)
    os.makedirs(folder_log,exist_ok=True)
    file_day = f"{current_date.year}{current_date.month:02d}{current_date.day:02d}.txt"
    file_log = os.path.join(folder_log,file_day)
    file_month= f"{current_date.year}{current_date.month:02d}.txt"
    file_day = os.path.join(folder_day,file_day)
    file_month = os.path.join(folder_month,file_month)
    print('------输出新的客流数据-------')
    content = {"in": 0, "out":0, "stay": 0}
    best_content = {"inmax": 0,"staymax":0,"monthmax":0}
    hour_in = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0}
    hour_stay = {"0":0,"1":0,"2":0,"3":0,"4":0,"5":0,"6":0,"7":0,"8":0,"9":0,"10":0,"11":0,"12":0,"13":0,"14":0,"15":0,"16":0,"17":0,"18":0,"19":0,"20":0,"21":0,"22":0,"23":0}
    if not os.path.exists('best.txt'):
        with open('best.txt','a') as file:
            passflow = json.loads(passflow)
            best_content['inmax'] +=  passflow['in']
            best_content['monthmax'] += passflow['in']
            best_content['staymax'] = best_content['staymax'] +passflow['in']-passflow['out']
            file.write(json.dumps(best_content))#初始化 best文件
    if not os.path.exists('hour_in.txt'):
        with open('hour_in.txt','a') as file:
            file.write(json.dumps(hour_in))#初始化 小时客流文件
    if not os.path.exists('hour_stay.txt'):
        with open('hour_stay.txt','a') as file:
            file.write(json.dumps(hour_stay))#初始化 小时容纳文件
    if not os.path.exists(file_month):
        with open(file_month, "w") as file:
            #file.write(str(passflow['in']))#初始化 月文件
            file.write(str('0'))#初始化 月文件
    if not os.path.exists(file_log):#初始化 日志文件
            with open(file_log,'a',encoding='utf-8') as file:
                file.write('系统开始运行 时间：' + str(now) + '\n')
    if not os.path.exists(file_day):
        with open(file_day, "w") as file:
            passflow = json.loads(passflow)
            content['in'] += passflow['in']
            content['out'] += passflow['out']
            content['stay'] = content['stay'] + passflow['in'] - passflow['out']
            if content['stay'] < 0:
                content['stay'] = 0
            file.write(json.dumps(content))#初始化 日文件
    else:
        with open(file_day, "r") as file:
            last_line = file.readline()
            last_line = last_line.strip()
            day = json.loads(last_line)
            passflow = json.loads(passflow)
            day['in'] +=  passflow['in']
            day['out']+=  passflow['out']
            day['stay'] = day['stay'] + passflow['in'] - passflow['out']
            #inherit_stay = content['stay']
            if day['stay'] <=0:
                day['stay'] = 0
            
            
            
            with open(file_log,'a',encoding='utf-8') as file:
                file.write('时间：' + str(now) + '进入' + str(passflow['in']) + '人，外出' +str(passflow['out']) + '人,当前舱内有' +str(day['stay']) +'人' '\n')

            with open('hour_in.txt','r') as file:   #更新折线图客流数据
                last_line = file.readline()
                last_line = last_line.strip()
                hour_in_info = json.loads(last_line)
                hour_in_info[str(current_hour)] = day['in']
            with open('hour_in.txt','w') as file:
                file.write(json.dumps(hour_in_info))
            with open('hour_stay.txt','r') as file:  #更新折线图容纳客人数据
                last_line = file.readline()
                last_line = last_line.strip()
                hour_stay_info = json.loads(last_line)
                hour_stay_info[str(current_hour)] = day['stay']
            with open('hour_stay.txt','w') as file:
                file.write(json.dumps(hour_stay_info))
            with open(file_month,'r') as file:
                content = file.read()
                number = int(content) + passflow['in']
                with open('best.txt','r') as file:
                    best = file.readline()
                    best = json.loads(best)
                    if best['inmax'] < day['in']:
                        best['inmax'] = day['in']
                    if best['staymax'] < day['stay']:
                        best['staymax'] = day['stay']
                    if best['monthmax'] < number:
                        best['monthmax'] = number
                    with open('best.txt','w') as file:
                        file.write(json.dumps(best))
                with open(file_month,'w') as file:
                        file.write(str(number))
        with open(file_day,'w') as file:
            file.write(json.dumps(day))
        
    return 'data success.'
@app_flask.route('/api/camera/heartBeat',methods=['POST'])
def heartbeat():
    content=request.data.decode("utf-8")
    # 示例程序，仅打印接收内容    
    current_app.logger.debug(content)
    return 'heartbeat success.'
@app_flask.route('/getflow',methods=['POST','GET'])
def getflow():
    current_date = datetime.date.today()
    folder_month = "month"
    folder_day = 'day'
    os.makedirs(folder_day,exist_ok=True)
    os.makedirs(folder_month,exist_ok=True)
    file_day = f"{current_date.year}{current_date.month:02d}{current_date.day:02d}.txt"
    file_month= f"{current_date.year}{current_date.month:02d}.txt"
    file_day = os.path.join(folder_day,file_day)
    file_month = os.path.join(folder_month,file_month)

    # content = {"in": 0, "out":0, "stay": 0}
    # if not os.path.exists(file_day):
    #     with open(file_day, "w") as file:
    #         file.write(json.dumps(content))#初始化 日文件

    data_info = {"day_in":0,"day_stay":0,"inmax":0,"instay":0,"month":0,"monthmax":0,"hour_in":0,"hour_stay":0}

    with open(file_day, "r") as file:
        last_line = file.readline()
        last_line = last_line.strip()
        day = json.loads(last_line)
        data_info['day_in'] = day['in']
        data_info['day_stay'] = day['stay']
    with open(file_month, "r") as file:
        month = file.read()
        data_info['month'] = int(month)
    with open('best.txt', 'r') as file:
        best = file.readline()
        best = json.loads(best)
        data_info['inmax'] = best['inmax']
        data_info['staymax'] = best['staymax']
        data_info['monthmax'] = best['monthmax']
    with open('hour_in.txt','r') as file:
        hour_in_info = file.readline()
        hour_in_info = json.loads(hour_in_info)
        hour_in_info = list(hour_in_info.values())
        data_info['hour_in'] = hour_in_info
    with open('hour_stay.txt','r') as file:
        hour_stay_info = file.readline()
        hour_stay_info = json.loads(hour_stay_info)
        hour_stay_info = list(hour_stay_info.values())
        data_info['hour_stay'] = hour_stay_info
    #print(data_info,type(data_info))
    return data_info
@app_flask.route('/reset_stay',methods=['POST','GET'])
def reset_stay():
    print('置零成功')
    folder_day = 'day'
    current_date = datetime.date.today()
    file_day = f"{current_date.year}{current_date.month:02d}{current_date.day:02d}.txt"
    file_day = os.path.join(folder_day,file_day)
    with open(file_day,'r') as file:
        day = file.readline()
        day = json.loads(day)
        day['stay'] = 1
        with open(file_day,'w') as file:
            file.write(json.dumps(day))
            print('置零成功--------------------------------------------')
    return 'success'
if __name__=="__main__":
    print('hello')
    app_flask.run(host='169.254.8.200', port=8086)

