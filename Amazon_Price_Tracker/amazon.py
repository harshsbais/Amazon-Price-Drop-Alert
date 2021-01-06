import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import smtplib
import time
from lxml import html

url = ""
p = 0
ex_price = 0.0
usr_email = ""
flag=0

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'Amazon-Price-Drop-Alert'
        self.left = 10
        self.top = 10
        self.width = 330
        self.height = 140
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
    
        # Create textbox
        self.textbox = QLineEdit(self)
        self.textbox.move(20, 10)
        self.textbox.resize(280,20)
        
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(20, 30)
        self.textbox2.resize(280,20)

        self.textbox3 = QLineEdit(self)
        self.textbox3.move(20, 50)
        self.textbox3.resize(280,20)

        # Create a button in the window
        self.button = QPushButton('Give Result', self)
        self.button.move(100,90)
        
        # connect button to function on_click
        self.button.clicked.connect(self.on_click)
        self.show()
    
    @pyqtSlot()

    def on_click(self):
        url = self.textbox.text()
        p = self.textbox2.text()
        usr_email = self.textbox3.text()
        # QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
        # self.textbox.setText("")
        print(url+"\n")
        print(p+"\n")
        print(usr_email+"\n")
        ex_price = float(p)
        url = "https://www.amazon.in/Test-Exclusive-550/dp/B077Q7GW9V/ref=lp_22426818031_1_1"
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get(url)
        source = driver.page_source
        soup = BeautifulSoup(source, 'html.parser')
        title=soup.find('span', id ='productTitle').get_text().strip()
        print(title)
        try:
            price = soup.find('span', id ='priceblock_dealprice').get_text().strip()
            x="The item is currently discounted at : "+price
        except AttributeError:
            try:
                price = soup.find('span', id ='priceblock_ourprice').get_text().strip()
                x = "The product is not discounted currently and the price is : "+price
            except AttributeError:
                x = "Product Unavailable!!"
                exit()
        print(x)
        px = ""
        for ch in price:
            if(ch.isdigit()):
                px=px+ch
        converted_price=float(px)
        converted_price=converted_price/100
        if(converted_price < ex_price):
            self.smail(url, usr_email)
        else: 
            x = "The price is not currently below the price at which you would like to buy"
            print(x)
    def smail(self, name, usr_email):
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
        print(x)
        server.quit()



if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())