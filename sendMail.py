#!/usr/bin/python3
import time
import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def loginToGmail(mailaddr, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mailaddr, password)

    return server

def apacIsWorking():

    now = datetime.datetime.now()

    # apac team is working between 22:00 - 10:00 in UTC
    if now.hour > 10 and now.hour < 22:
        return False
    else
        return True

def send(html_str, caseType, toList, fromAddr, fromAddrPW):

    # send mail only in APAC business hours
    if apacIsWorking() is False:
        return

    server = loginToGmail(fromAddr,fromAddrPW)

    # make up the mail
    msg = MIMEMultipart()
    msg['Subject'] = caseType + "[" + time.strftime("%a, %d %b", time.gmtime()) + "]"
    msg['From'] = fromAddr
    msg['To'] = ", ".join(toList)
    msg.attach(MIMEText(html_str, 'html')) # plain will send plain text

    # send the message
    server.sendmail(fromAddr, toList, msg.as_string())

    # logout
    server.quit()

