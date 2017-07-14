import unittest
import time
# For get the code
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
# For html paser
from bs4 import BeautifulSoup
# For email
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

TO_ADDR='YOURMAIL@YOU.com'
FROM_ADDR='FROM@gmail.com'
FROM_ADDR_PW='PASSWORD'

TIMEOUT=30
RH_ADDR='RHNAME'
RH_ADDR_PW='RHPASS'

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

class PythonOrgSearch(unittest.TestCase):
 
    def setUp(self):
        self.driver = webdriver.Chrome()
 
    def test_search_in_python_org(self):
        driver = self.driver
        #driver.get("https://unified.gsslab.rdu2.redhat.com/#/SBRPlate/Gluster")
        driver.get("https://unified.gsslab.rdu2.redhat.com/#/SBRPlate/Cloud Prods & Envs,Stack,Ceph,Gluster,CFME")

        # follow http://selenium-python.readthedocs.io/locating-elements.html#
        driver.find_element_by_link_text("click here to login").click()
        driver.find_element_by_id("username").send_keys(RH_ADDR)
        driver.find_element_by_id("password").send_keys(RH_ADDR_PW)
        driver.find_element_by_id("_eventId_submit").click()

        # driver.refresh()
        # wait the page to be totally loaded
        try:
            element = WebDriverWait(driver, TIMEOUT).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "btn-toolbar"))
                    )
        finally:
            pass
        
        case_html = driver.find_element_by_class_name("panel-body").get_attribute('innerHTML')

        soup = BeautifulSoup(case_html, "html.parser")

        case_table_unassigned = soup.find('table', {'id': 'table_unassigned'})
        case_table_unassigned = str(case_table_unassigned)
        
        if case_table_unassigned is not "None":
            send_email(case_table_unassigned)
 
    def tearDown(self):
        self.driver.close()
 
if __name__ == "__main__":
    unittest.main()
