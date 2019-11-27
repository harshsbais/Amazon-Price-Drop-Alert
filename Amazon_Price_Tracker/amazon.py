import requests
from bs4 import BeautifulSoup
import smtplib
from lxml import html
import time
import sys
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QUrl
from PyQt5.QtWebEngineWidgets import QWebEnginePage
from tkinter import *
import tkinter as tk


print(
"    ___                                         ____       _              ______                __   \n"+         
"   /   |  ____ ___  ____ _____  ____  ____     / __ \_____(_)_______     /_  __/________ ______/ /_____  _____ \n"+
"  / /| | / __ `__ \/ __ `/_  / / __ \/ __ \   / /_/ / ___/ / ___/ _ \     / / / ___/ __ `/ ___/ //_/ _ \/ ___/ \n"+
" / ___ |/ / / / / / /_/ / / /_/ /_/ / / / /  / ____/ /  / / /__/  __/    / / / /  / /_/ / /__/ ,< /  __/ / \n"+   
"/_/  |_/_/ /_/ /_/\__,_/ /___/\____/_/ /_/  /_/   /_/  /_/\___/\___/    /_/ /_/   \__,_/\___/_/|_|\___/_/ \n"                                                                                                              
)
print(
  "          _    _  _____ ____  \n"+
  "         | |  | |/ ____|  _ \ \n"+
  " ______  | |__| | (___ | |_) | \n"+
  " ______  | |__  |\___ \|  _ <  \n"+
  "         | |  | |____) | |_) | \n"+
  "         |_|  |_|_____/|____/ \n"
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


name = ""
p = 0
ex_price = 0.0
usr_email = ""


def check_price():
    name = entry_1.get()
    p = entry_2.get()
    ex_price = float(p)
    usr_email = entry_3.get()
    client_response = Client(name)
    source = client_response.html
    soup = BeautifulSoup(source, 'html.parser')
    title=soup.find('span', id ='productTitle').get_text().strip()
    label_4 = Label(root, text=title)
    label_4.grid(row=4, column=0)
    try:
        price = soup.find('span', id ='priceblock_dealprice').get_text().strip()
        x="The item is currently discounted at : "+price
        label_5 = Label(root, text=x)
        label_5.grid(row=5, column=0)
    except AttributeError:
        try:
            price = soup.find('span', id ='priceblock_ourprice').get_text().strip()
            x = "The product is not discounted currently and Currently the price is : "+price
            label_5 = Label(root, text=x)
            label_5.grid(row=5, column=0)
        except AttributeError:
            x = "Product Unavailable!!"
            label_5 = Label(root, text=x)
            label_5.grid(row=5, column=0)
            exit()
    px = ""
    for ch in price:
        if(ch.isdigit()):
            px=px+ch
    converted_price=float(px)
    converted_price=converted_price/100
    if(converted_price < ex_price):
        send_mail(name, usr_email)
    else: 
        x = "The price is not currently below the price at which you would like to buy"
        label_6 = Label(root, text=x)
        label_6.grid(row=6, column=0)


def send_mail(name, usr_email):
    # print("*************************\n")
    # print(name+" "+usr_email)
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login('amazon.price.drop1@gmail.com', 'cjyugozvpqgukutq')
    SUBJECT = 'Price fell down'
    TEXT = 'Check amazon link '+name+'\n \n \n\t \t -By HSB'
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
    server.sendmail('amazon.price.drop1@gmail.com', usr_email, message)
    x = "Mail has been sent"
    label_6 = Label(root, text=x)
    label_6.grid(row=6, column=0)
    server.quit()

#################################                    GUI                    ################################

root = tk.Tk()
root.title("Amazon Price Drop Alert")

label_1 = Label(root, text="Please Enter the URL:")
entry_1 = Entry(root)
#button_1 = Button(root, text="Click to enter URL", command=enter_url)

label_2 = Label(root, text="Please Enter the Price:")
entry_2 = Entry(root)
#button_2 = Button(root, text="Click to enter price", command=enter_price)

label_3 = Label(root, text="Please Enter your email address:")
entry_3 = Entry(root)
#button_3 = Button(root, text="Click to enter email", command=enter_email)

button_4 = Button(root, text="Click to check", command=check_price)

label_1.grid(row=0, column=0)
entry_1.grid(row=0, column=1)
#button_1.grid(row=0, column=2)

label_2.grid(row=1, column=0)
entry_2.grid(row=1, column=1)
#button_2.grid(row=1, column=2)

label_3.grid(row=2, column=0)
entry_3.grid(row=2, column=1)
#button_3.grid(row=2, column=2)

button_4.grid(row=3, column=1)

root.mainloop()