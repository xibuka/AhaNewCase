#!/usr/bin/python3

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

# store the case which has been sent before
caseSent=[]
    
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
    try:
        element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.LINK_TEST, "click here to login"))
                    )
    except:
        driver.save_screenshot('noLoginLinkFound.png')
        print("Can not login! Check noLoginLinkFound.png")
        exit(1)
    
    driver.find_element_by_link_text("click here to login").click()

    try:
        element = WebDriverWait(driver, 60).until(
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

    #"https://unified.gsslab.rdu2.redhat.com/#/SBRPlate/Gluster"
    unified_url="https://unified.gsslab.rdu2.redhat.com/#/SBRPlate/Cloud Prods & Envs,Stack,Ceph,Gluster,CFME"

    driver = webdriver.Firefox() # or webdriver.Chrome()

    driver.get(unified_url)

    login(driver)

    # wait the page to be totally loaded
    try:
        element = WebDriverWait(driver, 300).until(
                EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
                )
    except:
        driver.save_screenshot('timeout.png')
        printTime("Time Out! Will retry")

        continue

    # get the HTML source code and analyze it
  
    case_html = driver.find_element_by_class_name("panel-body").get_attribute('innerHTML')

    analyzeCaseHtml(case_html)

    printTime("New Case Checked.")

    driver.close()
    driver.quit()

def analyzeCaseHtml(case_html):

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

    while True :
        newCaseSearch()
        time.sleep(300)
        printTime("Refreshing...")

    display.stop()
