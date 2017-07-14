import time
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
def send_email(html_str):

    # setup to list
    tolist= ['wenshi@redhat.com']

    # login 
    fromaddr = "mail.walker.shi@gmail.com"
    fromaddr_pw = "gmailshi1985"

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


def test_soap(case_html):
    soup = BeautifulSoup(case_html, "html.parser")

    case_table_unassigned = soup.find('table', {'id': 'table_unassigned'})
    case_table_unassigned = str(case_table_unassigned)
    #print(case_table_unassigned)
    send_email(case_table_unassigned)
 
if __name__ == "__main__":

    with open('ex.html', 'r') as f:
        test_soap(f.read())

