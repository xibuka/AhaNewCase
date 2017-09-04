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
newCaseSent=[]
ftsCaseSent=[]
ftsCaseSentSbtBreached=[]
ftsCaseSentSbtUnder10Min=[]
ftsCaseSentSbtUnder30Min=[]

productionList=["stack", "ceph", "gluster", "cloudform", "ansible"]
productionToUrl={
        "stack":"Cloud Prods & Envs,Stack",
        "ceph":"Ceph",
        "gluster":"Gluster",
        "cloudform":"CFME",
        "ansible":"Ansible"
        }

    // Cloud Prods & Envs,Stack,Ceph,Gluster,CFME
def printTime(msg):
    print(time.strftime("%a, %d %b %H:%M:%S", time.localtime()), " - ", msg)

def loginToGmail(mailaddr, password):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(mailaddr, password)

    return server

# send
def send_email(html_str, caseType, toList):

    server = loginToGmail(FROM_ADDR,FROM_ADDR_PW)

    # make up the mail
    msg = MIMEMultipart()
    msg['Subject'] = caseType + "[" + time.strftime("%a, %d %b", time.gmtime()) + "]"
    msg['From'] = fromaddr
    msg['To'] = ", ".join(tolist)
    msg.attach(MIMEText(html_str, 'html')) # plain will send plain text

    # send the message
    server.sendmail(fromaddr, tolist, msg.as_string())

    # logout
    server.quit()

def loginToUnified(username, password):

    unified_url="https://unified.gsslab.rdu2.redhat.com/#/"

    driver = webdriver.Firefox() # or webdriver.Chrome()

    driver.get(unified_url)

    try:
        element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.ID, "username"))
                    )
    except:
        driver.save_screenshot('CanNotLogin.png')
        print("Can not login! Check CanNotLogin.png")
        exit(1)

    driver.find_element_by_id("username").send_keys(username)
    driver.find_element_by_id("password").send_keys(password)
    driver.find_element_by_id("_eventId_submit").click()

    printTime("Login Successful")

    return driver

def caseSearch():

    // login 
    driver = loginToUnified(RH_ADDR, RH_ADDR_PW)

    unifiedUrlBase="https://unified.gsslab.rdu2.redhat.com/#/SBRPlate/"
    
    for prod in productionList:

        prodURL=unifiedUrlBase + productionToUrl[prod]

        driver.get(prodURL)

        # wait the page to be totally loaded
        try:
            printTime("Waiting case info to show up")
            element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
                    )
        except:
            driver.save_screenshot('timeout.png')
            printTime("Time Out! Will retry")
            return None
    
        # get the HTML source code and analyze it
        case_html = driver.find_element_by_class_name("panel-body").get_attribute('innerHTML')
    
        analyzeForNCQ(case_html)

    driver.quit()

def analyzeForNCQ(case_html):

    soup = BeautifulSoup(case_html, "html.parser")

    # find new case
    caseTable = soup.find('table', {'id': "table_unassigned"})

    if caseTable is Null: 
        printTime("No New Case exists")
    else: 
        for case_row in caseTable.find('tbody').find_all('tr'):
            case_NoTitle      = (case_row.find_all('td'))[0]
            case_NoTitle_text = (case_row.find_all('td'))[0].text
            case_sev          = (case_row.find_all('td'))[1]
            case_sbr          = (case_row.find_all('td'))[7]

            if case_NoTitle_text not in newCaseSent:
                newCaseSent.append(case_NoTitle_text)
                case_summary = str(case_NoTitle) + "Sev:" + str(case_sev) + str(case_sbr)
                send_email(case_summary, "NCQ", [TO_ADDR])

        printTime("NCQ Case Checked.")

def analyzeForFTS(case_html):

    # find active fts case
    ftsCaseTable = soup.find('table', {'id': 'table_fts'})

    if ftsCaseTable is Null: 
        printTime("No active fts case exists, WoW")
    else: 
        for case_row in ftsCaseTable.find('tbody').find_all('tr'):
            case_NoTitle      = (case_row.find_all('td'))[0]
            case_NoTitle_text = (case_row.find_all('td'))[0].text
            case_sev          = (case_row.find_all('td'))[1]
            case_sbt          = (case_row.find_all('td'))[X].text
            case_WoWho        = (case_row.find_all('td'))[X].text
            case_sbr          = (case_row.find_all('td'))[7]

            # will not send WoC fts case 
            if case_WoWho == "WoCustomer":
                continue

            # will not send fts case which has sbt more than 1 hour
            #sbrTime = case_sbt..TODO should be int
            if sbtTime > 60 :
                continue

            # ftsCaseSent=[]
            # ftsCaseSentSbtBreached=[]
            # ftsCaseSentSbtUnder10Min=[]
            # ftsCaseSentSbtUnder30Min=[]

            if sbtTime < 0
               
            if case_NoTitle_text not in newCaseSent:
                newCaseSent.append(case_NoTitle_text)
                case_summary = str(case_NoTitle) + "Sev:" + str(case_sev) + str(case_sbr)
                send_email(case_summary, "active FTS alert", [TO_ADDR])

    printTime("NCQ Case Checked.")

# start from here
if __name__ == "__main__":

    # get the arguments from command line
    parser = argparse.ArgumentParser()
    parser.add_argument("--toAddr",    \
            help="the email address where the notice should be send to.")
    parser.add_argument("--fromAddr",  \
            help="send from email address.")
    parser.add_argument("--fromAddrPW",\
            help="password of the send from email address.")
    parser.add_argument("--rhuser",    \
            help="RH account to access unified web site")
    parser.add_argument("--rhpass",    \
            help="password for RH account")
    args = parser.parse_args()
    args = vars(args)

    TO_ADDR=args['toAddr']
    FROM_ADDR=args['fromAddr']
    FROM_ADDR_PW=args['fromAddrPW']
    RH_ADDR=args['rhuser']
    RH_ADDR_PW=args['rhpass']

    # make a virtual display for headless broswer
    display = Display(visible=0, size=(1280, 720))
    display.start()

    # main loop
    caseSearch()
    #printTime("sleeping for 300s...")
    #time.sleep(300)
     
    # stop the virtual display
    display.stop()
