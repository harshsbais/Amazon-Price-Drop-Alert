import requests
from bs4 import BeautifulSoup
import smtplib
import time
import os

headers = {"User-Agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'}

name = raw_input("Enter URL\n")
p = raw_input("Enter the price at which you would like to be alerted\n")
ex_price = float(p)
usr_email = raw_input("Enter your email\n") 
def check_price():
    page = requests.get(name, headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    print("\n")

    title=soup.find(id="productTitle").get_text().strip()
    print(title)
    try:
        price = soup.find(id="priceblock_dealprice").get_text().strip()
        print("The item is currently discounted at : "+price)
    except AttributeError:
        print("The product is not discounted currently")
        price = soup.find(id="priceblock_ourprice").get_text().strip()
        print("Currently the price is : "+price)

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
        print("The price is not currently below the price at which you would like to buy")

def send_mail():
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.ehlo()

    server.login('amazon.price.drop1@gmail.com', 'cjyugozvpqgukutq')

    SUBJECT = 'Price fell down'
    TEXT = 'Check amazon link'+name
    message = 'Subject: {}\n\n{}'.format(SUBJECT, TEXT)

    server.sendmail('amazon.price.drop1@gmail.com', usr_email, message)
    print("Mail has been sent")

    server.quit()

check_price()