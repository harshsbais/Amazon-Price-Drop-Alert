import sys
from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from PyQt5.QtGui import QIcon, QValidator, QDoubleValidator,  QRegExpValidator
from PyQt5.QtCore import pyqtSlot, QRegExp
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
from bs4 import BeautifulSoup
import smtplib
import time
from lxml import html
from gui.amazonGUI import Ui_MainWindow

url = ""
p = 0
ex_price = 0.0
usr_email = ""
flag=0

class App(Ui_MainWindow):
    def __init__(self):
        super().__init__()
    
class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.pushButton.clicked.connect(self.on_click)


    @pyqtSlot()
    def on_click(self):
        check = self.validator()
        if check != "":
            self.msgbox("Aleart", "WRONG INPUT", check)
        else:
            # QMessageBox.question(self, 'Message - pythonspot.com', "You typed: " + textboxValue, QMessageBox.Ok, QMessageBox.Ok)
            print(self.url+"\n")
            print(self.p+"\n")
            print(self.usr_email+"\n")
            ex_price = float(self.p)
            # url = "https://www.amazon.in/Test-Exclusive-550/dp/B077Q7GW9V/ref=lp_22426818031_1_1"
            self.driver = webdriver.Chrome(ChromeDriverManager().install())
            self.driver.get(self.url)
            source = self.driver.page_source
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
                    title = "PRODUCT UNAVAILABLE"
                    x = title
                    self.driver.quit()
                    self.msgbox("Aleart", title, x)
                    exit()
            self.driver.quit()
            self.msgbox("Info","DISCOUNT INFO.", x)
            px = ""
            for ch in price:
                if(ch.isdigit()):
                    px=px+ch
            converted_price=float(px)
            converted_price=converted_price/100
            if(converted_price < ex_price):
                try:
                    self.smail()
                except:
                    title = "Unable to Send Mail"
                    x = "* Check your internet Connection\n * Check you enter right email address"
                    self.msgbox("Warning",title,  x)
            else: 
                title = "HIGH PRICE"
                x = "The price is not currently below the price at which you would like to buy"
                self.msgbox("Info", title, x)
            self.txtUrl.clear()
            self.txtPrice.clear()
            self.txtEmail.clear()
    
    def validator(self):
        url_validate = QRegExpValidator(QRegExp(r'^.*[.amazon.in].*$'))
        price_validate = QDoubleValidator(bottom=0, decimals=0)
        email_validate = QRegExpValidator(QRegExp(r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'))

        again = ""
        self.url = self.txtUrl.toPlainText()
        self.p = self.txtPrice.toPlainText()
        self.usr_email = self.txtEmail.toPlainText()

        if url_validate.validate(self.url, 0)[0] != QValidator.Acceptable:
            print(url_validate.validate(self.url, 0))
            again = again + "URL : url must be of www.amazon.in\n"
            self.txtUrl.clear()

        if price_validate.validate(self.p, 4)[0] != QValidator.Acceptable:
            print(price_validate.validate(self.p , 4))
            again = again + "Price : It must be Number without , and .\n"
            self.txtPrice.clear()
        
        if email_validate.validate(self.usr_email, 0)[0] != QValidator.Acceptable:
            print(email_validate.validate(self.usr_email, 0))
            again = again + "Email : Please enter right email\n"
            self.txtEmail.clear()
        return again

    def msgbox(self, condition,title, x):
        font = QtGui.QFont()
        font.setFamily("Bahnschrift SemiLight")
        font.setPointSize(14)
        
        msg = QMessageBox()
        if condition == "Accept":
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Close)
        elif condition == "Warning":
            msg.setIcon(QMessageBox.Warning)
            msg.setStandardButtons(QMessageBox.Close)
        elif condition == "Info":
            msg.setIcon(QMessageBox.Information)
            msg.setStandardButtons(QMessageBox.Close)
        elif condition == "Aleart":
            msg.setIcon(QMessageBox.Critical)
            msg.setStandardButtons(QMessageBox.Ok)
            
        msg.setFont(font)

        msg.setWindowTitle("Amazon Price Tracker")
        msg.setText(title)
        msg.setInformativeText(x)
        x = msg.exec_()
        
    def smail(self):
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.ehlo()
        server.starttls()
        server.ehlo()
        server.login('amazon.price.drop1@gmail.com', 'cjyugozvpqgukutq')
        SUBJECT = 'Price fell down'
        TEXT = 'Check amazon link '+self.url+'\n \n \n\t \t -By HSB'
        message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)
        try:
            server.sendmail('amazon.price.drop1@gmail.com', self.usr_email, message)
        except:
            title = "Unable to Send Mail"
            x = "* Check your internet Connection\n * Check you enter right email address"
            self.msgbox("Warning",title,  x)
        server.quit()
        title = "MAIL SENT"
        x = "check your mail inbox"
        self.msgbox("Accept", title, x)
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    # ex = App()
    w = MainWindow()
    # ui = App()
    # ui.setupUi(MainWindow)
    w.show()
    sys.exit(app.exec_())