import requests
from bs4 import BeautifulSoup
import smtplib
from lxml import html
import time
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage


print(
"    ___                                         ____       _              ______                __   \n"+         
"   /   |  ____ ___  ____ _____  ____  ____     / __ \_____(_)_______     /_  __/________ ______/ /_____  _____ \n"+
"  / /| | / __ `__ \/ __ `/_  / / __ \/ __ \   / /_/ / ___/ / ___/ _ \     / / / ___/ __ `/ ___/ //_/ _ \/ ___/ \n"+
" / ___ |/ / / / / / /_/ / / /_/ /_/ / / / /  / ____/ /  / / /__/  __/    / / / /  / /_/ / /__/ ,< /  __/ / \n"+   
"/_/  |_/_/ /_/ /_/\__,_/ /___/\____/_/ /_/  /_/   /_/  /_/\___/\___/    /_/ /_/   \__,_/\___/_/|_|\___/_/ \n"                                                                                                              
)
print(
  "         _    _  _____ ____  \n"+
  "        | |  | |/ ____|  _ \ \n"+
  " ______ | |__| | (___ | |_) | \n"+
  " ______ | |__  |\___ \|  _ <  \n"+
  "        | |  | |____) | |_) | \n"+
  "        |_|  |_|_____/|____/ \n"
)


class Client(QWebEnginePage): 
    def __init__(self, url): 
        self.app = QApplication(sys.argv) 
        QWebEnginePage.__init__(self) 
        self.html = '' 
        self.loadFinished.connect(self._on_load_finished) 
        self.load(QUrl(url)) 
        self.app.exec_() 
    def _on_load_finished(self): 
        self.html = self.toHtml(self.Callable) 
    def Callable(self, html_str): 
        self.html = html_str 
        self.app.quit() 


name = input("Enter URL\n") 
p = input("Enter the price at which you would like to be alerted\n")
ex_price = float(p)
usr_email = input("Enter your email\n") 


def check_price():
    client_response = Client(name)
    source = client_response.html
    soup = BeautifulSoup(source, 'html.parser')
    print("\n")
    title=soup.find('span', id ='productTitle').get_text().strip()
    print(title)
    try:
        price = soup.find('span', id ='priceblock_dealprice').get_text().strip()
        print("The item is currently discounted at : "+price)
    except AttributeError:
        print("The product is not discounted currently")
        try:
            price = soup.find('span', id ='priceblock_ourprice').get_text().strip()
            print("\nCurrently the price is : "+price+"\n")
        except AttributeError:
            print("\nProduct Unavailable!!\n")
            exit()
    print("\n")
    px = ""
    for ch in price:
        if(ch.isdigit()):
            px=px+ch
    converted_price=float(px)
    converted_price=converted_price/100
    if(converted_price < ex_price):
        send_mail()
    else:
        print("The price is not currently below the price at which you would like to buy\n")


def send_mail():
    flag = 1 
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('amazon.price.drop1@gmail.com', 'cjyugozvpqgukutq')

    SUBJECT = 'Price fell down'
    TEXT = 'Check amazon link '+name+'\n \n \n\t \t -By HSB'
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    server.sendmail('amazon.price.drop1@gmail.com', usr_email, message)
    print("Mail has been sent \n")
    server.quit()


check_price()