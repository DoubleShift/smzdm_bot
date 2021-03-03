"""
什么值得买自动签到脚本
使用github actions 定时执行
@author : stark
"""
import requests
import config
import urllib.parse
import json
import os
from sys import argv

TG_TOKEN = ""
TG_USERID = ""

#telegram
if os.environ["TG_TOKEN"] != "":
    TG_TOKEN = os.environ["TG_TOKEN"]
if os.environ["TG_USERID"] != "":
    TG_USERID = os.environ["TG_USERID"]
    
def sendTg(text, desp):
    if TG_TOKEN != '' or TG_USERID != '':

        url = 'https://api.telegram.org/bot' + TG_TOKEN + '/sendMessage'
        headers = {'Content-type': "application/x-www-form-urlencoded"}
        body = 'chat_id=' + TG_USERID + '&text=' + urllib.parse.quote(text) + '\n\n' + urllib.parse.quote(desp) + '&disable_web_page_preview=true'
        response = json.dumps(requests.post(url, data=body,headers=headers).json(),ensure_ascii=False)

        data = json.loads(response)
        if data['ok'] == True:
            print('\nTelegram发送通知消息完成\n')
        elif data['error_code'] == 400:
            print('\n请主动给bot发送一条消息并检查接收用户ID是否正确。\n')
        elif data['error_code'] == 401:
            print('\nTelegram bot token 填写错误。\n')
        else:
            print('\n发送通知调用API失败！！\n')
            print(data)
    else:
        print('\n您未提供Telegram的APP推送Token，取消Bark推送消息通知\n')
        pass



class SMZDM_Bot(object):
    def __init__(self):
        self.session = requests.Session()
        # 添加 headers
        self.session.headers = config.DEFAULT_HEADERS

    def __json_check(self, msg):
        """
        对请求 盖乐世社区 返回的数据进行进行检查
        1.判断是否 json 形式
        """
        try:
            result = msg.json()
            print(result)
            return True
        except Exception as e:
            print(f'Error : {e}')            
            return False

    def load_cookie_str(self, cookies):
        """
        起一个什么值得买的，带cookie的session
        cookie 为浏览器复制来的字符串
        :param cookie: 登录过的社区网站 cookie
        """
        self.session.headers['Cookie'] = cookies    

    def checkin(self):
        """
        签到函数
        """
        url = 'https://zhiyou.smzdm.com/user/checkin/jsonp_checkin'
        msg = self.session.get(url)
        if self.__json_check(msg):
            return msg.json()
        return msg.content




if __name__ == '__main__':
    sb = SMZDM_Bot()
    # sb.load_cookie_str(config.TEST_COOKIE)
    cookies = os.environ["COOKIES"]
    sb.load_cookie_str(cookies)
    res = sb.checkin()
    print(res)


    sendTg('什么值得买每日签到',str(res))
    print('代码完毕')
