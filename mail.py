#-*-coding:utf-8-*-
import smtplib
from email.mime.text import MIMEText
sender = "@qq.com"
password  = "授权码"
receiver  = "***"

msg = MIMEText(u"你好",'plain','utf-8')
msg["Subject"] = "Hi there."
msg["From"]    = sender
msg["To"]      = receiver

try:
    smtp = smtplib.SMTP_SSL("smtp.qq.com", 465)
    smtp.login(sender,password)
    smtp.sendmail(sender,receiver, msg.as_string())
    smtp.quit()
    print "Successfully sent!"
except smtplib.SMTPException,e:
    print "Falied,%s"%e 