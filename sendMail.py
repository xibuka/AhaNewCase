#!/usr/bin/python3
import time
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def loginToGmail(mailaddr, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mailaddr, password)

    return server

def send(html_str, caseType, toList, fromAddr, fromAddrPW):

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

