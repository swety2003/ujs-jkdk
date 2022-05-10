import sqlite3
import time

from GlobalData import get_value, set_value
from main import dbfile
from .log1 import l
from .Login import Login
from .mailsender import mailer
from random import randint
from .getdata import getdata
from datetime import datetime
from Models import *



def showRedirectHistory(reditList):
    text = f'重定向次数:{len(reditList)}\n'
    l.info(text)
    for item in reditList:
        l.info(f'重定向链接:{item.headers["location"]}')
        ''
def test(id):
    print(f"打卡{id}")
    # dbfile = "db/users.db"

    conn = sqlite3.connect(f"{dbfile}")
    c = conn.cursor()
    us = GetAllUsers(c)
    cfg: Config = GetCFG(c)

    conn.close()

    for i in us:
        user: User = i
        if user.id==id:
            l.info(f'正在打卡{user.id}...')
            lg = Login(cfg)
            mail = mailer(target=user.recv, cfg=cfg)

            username = user.id
            password = user.pwd
            try1 = 0
            notlogin = None
            while notlogin == None:
                ses = lg.Login(username=username, password=password)
                notlogin = ses
                try1 += 1
                if try1 > 50:
                    mail.mailText("登陆失败，无法打卡")
                    l.error('超过50次未能成功登陆')
            try:
                daka(ses, mail)
            except:
                mail.mailText("打卡失败，未知错误!")
                pass
            return


def daka(ses, mail):
    dakaAPI = "http://yun.ujs.edu.cn/xxhgl/yqsb/grmrsb"
    ses.headers = {
        # 'Host': 'yun.ujs.edu.cn',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.193 Safari/537.36 Edg/86.0.622.68'
    }


    response = ses.post(url=dakaAPI)
    reditList = response.history
    showRedirectHistory(reditList)


    response = ses.get(url=dakaAPI)
    try:
        text = response.content.decode("UTF-8")
    except:
        text = response.content.decode("GBK")

    data = getdata(text)

    tem1 = randint(355, 365) / 10
    tem2 = randint(355, 365) / 10
    l.info("随机体温为:{}和{}".format(tem1, tem2))

    data['xwwd'] = tem1
    data['swwd'] = tem2

    l.info("表单创建完毕!!" + "\n")

    l.info("提交表单ing...")

    response = ses.get(url=reditList[len(reditList) - 1].headers["location"])
    reditList = response.history
    showRedirectHistory(reditList)

    response = ses.post(url=dakaAPI, data=data)
    try:
        text = response.content.decode("UTF-8")
    except:
        text = response.content.decode("GBK")

    l.info('发送邮件....')

    mail.mailHtml(text)

    l.info("本次打卡执行完毕.")
    # with open("./tmp/log.txt", 'a')as fn:
    #     fn.write("本次打卡执行完毕。\n---------------------------------\n\n\n\n")

def GetAllUsers(c):
    results = c.execute("select * from USERS")
    users = results.fetchall()
    # conn.close()
    us = []
    for user in users:
        print(user)
        u = User(id=user[0], pwd=user[1], recv=user[2], enabled=user[3], extrainfo=user[4])
        us.append(u)
    return us

def GetCFG(c):
    results=c.execute("select * from CFG")
    cfg=results.fetchall()[0]

    return Config(senderaddress=cfg[0],mailkey=cfg[1],appid=cfg[2],apikey=cfg[3],secretkey=cfg[4])

def __run():
    # dbfile = "db/users.db"

    conn = sqlite3.connect(f"{dbfile}")
    c = conn.cursor()
    us = GetAllUsers(c)
    cfg: Config = GetCFG(c)

    conn.close()

    set_value("max",len(us))
    completed=0
    for i in us:
        user: User = i
        if not user.enabled:
            continue
        l.info(f'正在打卡{user.id}...')
        lg = Login(cfg)
        mail = mailer(target=user.recv, cfg=cfg)

        username = user.id
        password = user.pwd
        try1 = 0
        notlogin = None
        while notlogin == None:
            ses = lg.Login(username=username, password=password)
            notlogin = ses
            try1 += 1
            if try1 > 50:
                mail.mailText("登陆失败，无法打卡")
                l.error('超过50次未能成功登陆')
        try:
            daka(ses, mail)
        except:
            mail.mailText("打卡失败，未知错误!")
            pass
        completed+=1
        set_value("finished", completed)

def start():
    print("started")


    while True:
        try1 = 0
        notlogin = None
        time_now = datetime.now().strftime("%H:%M")  # 刷新时间
        sdtime=get_value("targetTime")
        statue=get_value("state")



        print(f"状态 {statue} 当前 {time_now} 设定 {sdtime} \r",end="")

        time.sleep(1)

        if time_now == sdtime:  # 此处设置每天定时的时间
            # 此处替换为需要执行的动作

            if statue:
                l.info("时间到,开始打卡!!!")

                # __run()
                th=threading.Thread(target=__run,)
                th.start()





            l.info('休息1200秒后等候下次打卡...')
            time.sleep(1200)  # 因为以秒定时，所以暂停1200秒，使之不会在一天内执行多次
        else:
            time.sleep(1)







def settime():
    a = input()
    try:
        date_object = datetime.strptime(a, '%H:%M')
        return date_object
    except Exception:
        if a == "":
            l.info("开始打卡一次。")
            start()
            exit()
        l.error("输入格式错误，请重试。")
        return None
    pass


if __name__ == '__main__':



    start()


    exit(0)
    sdtime = None
    print("请输入打卡时间：（不输入则立即打卡一次）")
    while sdtime == None:
        sdtime = settime()
    l.info(f'设定的时间:每日{sdtime.strftime("%H:%M")}')
    l.info('等候打卡...')
    while True:
        try1 = 0
        notlogin = None
        time_now = datetime.now().strftime("%H:%M")  # 刷新时间
        if time_now == sdtime.strftime("%H:%M"):  # 此处设置每天定时的时间
            # 此处替换为需要执行的动作
            l.info("时间到,开始打卡!!!")
            start()
            l.info('休息1200秒后等候下次打卡...')
            time.sleep(1200)  # 因为以秒定时，所以暂停1200秒，使之不会在一天内执行多次
        else:
            time.sleep(5)
            msg = datetime.now().strftime("%H:%M")
            print(f"{msg}\r", end='')
