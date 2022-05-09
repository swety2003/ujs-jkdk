import smtplib
from email.mime.text import MIMEText
from email.utils import formataddr
from .log1 import log
import json

l = log()


class mailer():
    def __init__(self, target,cfg):
        self.target=target
        self.config = cfg

    def mailHtml(self,html):
        config = self.config
        my_sender = config.senderaddress
        my_pass = config.mailkey
        my_user = self.target
        try:
            mail_msg = html
            msg = MIMEText(mail_msg, 'html', 'utf-8')
            msg['From'] = formataddr(["FUCK打卡", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr(["结果", my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = "打卡结果反馈"  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            l.info("邮件发送失败")
        l.info("邮件发送成功")


    def mailText(self,text):
        config = self.config
        my_sender = config.senderaddress
        my_pass = config.mailkey
        my_user = self.target
        # with open('./log.txt', 'r') as fn:
        #     log = fn.read()
        try:
            mail_msg = '打卡失败!\n' + log
            msg = MIMEText(mail_msg, 'html', 'utf-8')
            msg['From'] = formataddr(["FUCK打卡", my_sender])  # 括号里的对应发件人邮箱昵称、发件人邮箱账号
            msg['To'] = formataddr([my_user, my_user])  # 括号里的对应收件人邮箱昵称、收件人邮箱账号
            msg['Subject'] = text  # 邮件的主题，也可以说是标题

            server = smtplib.SMTP_SSL("smtp.qq.com", 465)  # 发件人邮箱中的SMTP服务器，端口是25
            server.login(my_sender, my_pass)  # 括号中对应的是发件人邮箱账号、邮箱密码
            server.sendmail(my_sender, [my_user, ], msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
            server.quit()  # 关闭连接
        except Exception:  # 如果 try 中的语句没有执行，则会执行下面的 ret=False
            l.info("邮件发送失败")
        l.info("邮件发送成功")
