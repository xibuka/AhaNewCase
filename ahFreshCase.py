#!/usr/bin/python3

import time
import os.path
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
# For Args
import configparser
# For DB access
import db_control
import sqlite3
# For mail
import sendMail

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

dbname='ecs.db'

def printTime(msg):
    print(time.strftime("%a, %d %b %H:%M:%S", time.localtime()), " - ", msg)

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

    # login 
    driver = loginToUnified(RH_ADDR, RH_ADDR_PW)

    unifiedUrlBase="https://unified.gsslab.rdu2.redhat.com/#/SBRPlate/"
    
    for prod in productionList:

        prodURL=unifiedUrlBase + productionToUrl[prod]

        driver.get(prodURL)

        # wait the page to be totally loaded
        try:
            tmpStr="Waiting case info to show up : " + prod
            printTime(tmpStr)
            element = WebDriverWait(driver, 60).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
                    )
        except:
            driver.save_screenshot('timeout.png')
            printTime("Time Out! Will retry")
            return None
    
        # get the HTML source code
        case_html = driver.find_element_by_class_name("panel-body").get_attribute('innerHTML')
        # parse it by BS4
        soup = BeautifulSoup(case_html, "html.parser")

        # get mails who has subscriped prod
        conn = sqlite3.connect(dbname)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()

        mailList=db_control.selectMailListBySBR(c,prod)
    
        analyzeForNCQ(soup, mailList)
        analyzeForFTS(soup, mailList)

    driver.quit()

def analyzeForNCQ(soup, toMailList):

    # find new case
    newCaseTable = soup.find('table', {'id': "table_unassigned"})

    if newCaseTable is None: 
        printTime("No New Case exists")
        return 

    for case_row in newCaseTable.find('tbody').find_all('tr'):
        case_NoTitle      = (case_row.find_all('td'))[0]
        case_NoTitle_text = (case_row.find_all('td'))[0].text
        case_sev          = (case_row.find_all('td'))[1]
        case_sbr          = (case_row.find_all('td'))[7]

        if case_NoTitle_text not in newCaseSent:
            newCaseSent.append(case_NoTitle_text)

            thead = newCaseTable.find('thead')
            case_summary = str(thead) + str(case_row)
            
            sendMail.send(case_summary, "NCQ", toMailList, FROM_ADDR, FROM_ADDR_PW)

    printTime("NCQ Case Checked.")

def analyzeForFTS(soup, toMailList):

    # find active fts case
    ftsCaseTable = soup.find('table', {'id': 'table_fts'})

    if ftsCaseTable is None: 
        printTime("No active fts case exists, WoW")
        return

    for case_row in ftsCaseTable.find('tbody').find_all('tr'):
        case_NoTitle      = (case_row.find_all('td'))[0]
        case_NoTitle_text = (case_row.find_all('td'))[0].text
        case_sev          = (case_row.find_all('td'))[1]
        case_sbt          = (case_row.find_all('td'))[3].text
        case_status       = (case_row.find_all('td'))[4].text
        case_sbr          = (case_row.find_all('td'))[8]

        # will not send WoC fts case 
        if case_status == "WoCustomer":
            # remove from sent list is to make sure 
            # the case will be send when it move to WoOnwer again
            if case_NoTitle_text in ftsCaseSent:
                ftsCaseSent.remove(case_NoTitle_text)

            continue


        if case_NoTitle_text not in ftsCaseSent:
            ftsCaseSent.append(case_NoTitle_text)

            thead = ftsCaseTable.find('thead')
            case_summary = str(thead) + str(case_row)

            sendMail.send(case_summary, "active FTS alert", toMailList, FROM_ADDR, FROM_ADDR_PW)

    printTime("FTS Case Checked.")

# start from here
if __name__ == "__main__":

    if os.path.exists('./auth.cfg') if False:
        print("run ./initConfig.py first !!")
        return 1

    config = configparser.RawConfigParser()
    config.read('./auth.cfg') 

    FROM_ADDR=config2["config"]['fromAddr']
    FROM_ADDR_PW=config2['config']['fromAddrPW']
    RH_ADDR=config2['config']['rhuser']
    RH_ADDR_PW=config2['config']['rhpass']

    # make a virtual display for headless broswer
    display = Display(visible=0, size=(1280, 720))
    display.start()

    caseSearch()
     
    # stop the virtual display
    display.stop()
