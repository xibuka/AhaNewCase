#!/usr/bin/python

import time

# For login to get the source code
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# For headless brower
from pyvirtualdisplay import Display
from selenium import webdriver
# For html paser
from bs4 import BeautifulSoup
# For send email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
# For Args
import argparse

TO_ADDR=''
FROM_ADDR=''
FROM_ADDR_PW=''
RH_ADDR=''
RH_ADDR_PW=''

def send_email(html_str):

    tolist= [TO_ADDR]

    fromaddr = FROM_ADDR
    fromaddr_pw = FROM_ADDR_PW

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, fromaddr_pw)

    # make up and send the msg
    msg = MIMEMultipart()
    msg['Subject'] = "NCQ" + "[" + time.strftime("%a, %d %b", time.gmtime()) + "]"
    msg['From'] = fromaddr
    msg['To'] = ", ".join(tolist)
    msg.attach(MIMEText(html_str, 'html')) # plain will send plain text
    server.sendmail(fromaddr, tolist, msg.as_string())

    # logout
    server.quit()

def printTime(msg):
    print(time.strftime("%a, %d %b %H:%M:%S", time.localtime()), " - ", msg)

def login(driver):

    # follow http://selenium-python.readthedocs.io/locating-elements.html#
    driver.find_element_by_link_text("click here to login").click()
    
    try:
        element = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "username"))
                    )
    except:
        driver.save_screenshot('CanNotLogin.png')
        print("Can not login! Check CanNotLogin.png")
        exit(1)

    driver.find_element_by_id("username").send_keys(RH_ADDR)
    driver.find_element_by_id("password").send_keys(RH_ADDR_PW)
    driver.find_element_by_id("_eventId_submit").click()

    printTime("Login Successful")

def newCaseSearch():

    #driver = webdriver.Chrome()
    driver = webdriver.Firefox() 

    #driver.get("https://unified.gsslab.rdu2.redhat.com/#/SBRPlate/Gluster")
    driver.get("https://unified.gsslab.rdu2.redhat.com/#/SBRPlate/Cloud Prods & Envs,Stack,Ceph,Gluster,CFME")

    login(driver)

    caseSent=[]

    while True :

        # wait the page to be totally loaded
        driver.refresh()
        printTime("Refreshing...")

        #driver.save_screenshot('pic2.png')
        try:
            element = WebDriverWait(driver, 120).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
                    )
        except:
            driver.save_screenshot('timeout.png')
            printTime("Time Out!")

            continue

        try:
            case_html = driver.find_element_by_class_name("panel-body").get_attribute('innerHTML')

            analyzeCaseHtml(case_html, caseSent)

            printTime("New Case Checked.")
        except KeyboardInterrupt:
            print("Good Bye And Have A Nice Day")
            #driver.close()

        finally:
            pass

        time.sleep(120)

def analyzeCaseHtml(case_html,caseSent):

    soup = BeautifulSoup(case_html, "html.parser")

    case_table = soup.find('table', {'id': 'table_unassigned'})
    #case_table = soup.find('table', {'id': 'table_other'})

    if case_table is None:
        return

    for case_row in case_table.find('tbody').find_all('tr'):
        case_NoTitle      = (case_row.find_all('td'))[0]
        case_NoTitle_text = (case_row.find_all('td'))[0].text
        case_sev           = (case_row.find_all('td'))[1]
        case_sbr           = (case_row.find_all('td'))[7]

        if case_NoTitle_text not in caseSent:
            caseSent.append(case_NoTitle_text)
            case_summary = str(case_NoTitle) + "Sev:" + str(case_sev) + str(case_sbr)
            send_email(case_summary)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("--toAddr",    \
            help="the email address where the notice should be send to.")
    parser.add_argument("--fromAddr",  \
            help="send from email address.")
    parser.add_argument("--fromAddrPW",\
            help="password of the send from email address.")
    parser.add_argument("--rhuser",    \
            help="RH account to access unified.gsslab.rdu2.redhat.com")
    parser.add_argument("--rhpass",    \
            help="password for RH account")
    args = parser.parse_args()
    args = vars(args)

    TO_ADDR=args['toAddr']
    FROM_ADDR=args['fromAddr']
    FROM_ADDR_PW=args['fromAddrPW']
    RH_ADDR=args['rhuser']
    RH_ADDR_PW=args['rhpass']


    display = Display(visible=0, size=(1280, 720))
    display.start()

    newCaseSearch()

    display.stop()
