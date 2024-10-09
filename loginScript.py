# _*_coding:utf-8_*_
import re
import json
import time
import requests

'''
读取配置信息
'''
with open('config.json', 'r') as f:
    config = json.load(f)
StudentNumber = config['User']['StudentNumber']
Password = config['User']['Password']
SleepTime = config['SleepTime']
LogPath = config['LogPath']

'''
发送登录请求的数据

headers用于伪装成浏览器防止拦截
url请求地址
param请求参数
'''
headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Mobile Safari/537.36'
}
url = 'http://192.168.10.6/drcom/login'
param = {
    "callback": "dr1003",
    "DDDDD": StudentNumber,
    "upass": Password,
    "0MKKey": "123456",
    "R1": "0",
    "R2": "",
    "R3": "0",
    "R6": "0",
    "para": "00",
    "v6ip": "2001%3A0250%3A6009%3A0100%3A0078%3A0000%3A0000%3A01bc",
    "terminal_type": "1",
    "lang": "zh-cn",
    "jsVersion": "4.2.1",
    "v": "6227",
    "lang": "zh",
}

def checkIsLoginSuccess(content):

    """
    检查登录是否成功
    :param content: 请求返回内容
    :return:
            1表示登录成功
            0表示登录失败
    """
    match = re.search(r'"result":(\d+)', content)
    if match:
        if match.group(1):
            return 1
    return 0

def takeLog(file, isSuccess, content):
    with file as df:
        timestamp = time.time()
        if isSuccess == 1:
            df.write("[" + str(timestamp) + "]" + content + "\r\n")
        else:
            df.write("[" + str(timestamp) + "]" + "连接失败请检查网线或连接的网络是否正确" + "\r\n")

while(True):
    try:
        logFile = open(LogPath+"log.txt", 'a+', encoding='utf-8')
        # 发送请求
        response = requests.get(url=url, params=param, headers=headers)
    except :
        takeLog(logFile, 0, "   连接失败请检查网线或连接的网络是否正确")
    else:
        # 获取结果
        result = response.text
        isSucces = checkIsLoginSuccess(result)
        takeLog(logFile, isSucces, result)

    # 间隔SleepTime时间后检查连接
    time.sleep(SleepTime)