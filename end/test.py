import datetime
import os

def log_create():
    current_date = datetime.date.today()
    now = datetime.datetime.now()
    current_hour = now.hour
    current_min = now.minute
    current_sec = now.second
    folder_log = 'logger'
    os.makedirs(folder_log,exist_ok=True)
    file_day = f"{current_date.year}{current_date.month:02d}{current_date.day:02d}.txt"
    log_day = os.path.join(folder_log,file_day)
    if not os.path.exists(log_day):
        with open(log_day,'a',encoding='utf-8') as file:
            file.write('系统运行 时间：' + str(now) + '\n')#初始化 best文件
    else:
        with open(log_day,'a',encoding='utf-8') as file:
            file.write('时间：' + str(now) + '进入' + str(current_min) + '人，外出' +str(current_min) + '人' + '\n')#初始化 best文件

if __name__=="__main__":
    while True:
        log_create()
        print('zhixing')