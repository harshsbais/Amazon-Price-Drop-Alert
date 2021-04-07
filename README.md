# Amazon-Price-Drop-Alert

![](./images/icon.png)

This script will send you an email when the price for specific items you followed on Amazon drops beneath a certain price you set.


**You can parse the price without Amazon API !**

## Running the Project 
* Download the project
* Install dependencies through `$ pip install -r requirements.txt `
* After installing all the dependencies run `$ python amazon.py`
* Enter all information
* Push the button and let the magic happen.

## Inputs Required
#### URL
Get url from your amazon of your location. For example : URL of Amazon IN is `https://www.amazon.in/dp/...`
 

#### Price
You need to put the price at which you would like to buy

#### Email_Address
Enter email address of which you have access as mail will be sent when price drops below your expected price


## Contributing

### Setting-up the Python project 
* Download and install Git.
* Fork the Repository.
* Clone the repository to your local machine `$ git clone https://github.com/<your-github-username>/Amazon-Price-Drop-Alert.git`
* Change directory to DogeChat `$ cd Amazon-Price-Drop-Alert`
* Add a reference to the original repository  
   `$ git remote add upstream https://github.com/harshsbais/Amazon-Price-Drop-Alert.git`
* `$ pip install -r requirements.txt`
* `$ cd App`
* `$ python amazon.py`
### Contributing Guidelines 
  * Feel free to open an issue to report a bug or request a new feature.
  * Before starting to work on an issue, comment on that issue that you want to work on this and then only start to code.
  * Create a new branch with a related name of the motive i.e. bug/refactor/feature and commit your changes in that branch
  * For more extensive guidelines, kindly check the [CONTRIBUTING.md](https://github.com/harshsbais/Amazon-Price-Drop-Alert/blob/master/CONTRIBUTING.md)🤝

## Limitation
#### Checking interval time limitation
This code use some skill preventing banned by Amazon. However, the best interval time between each time of price checking is around 15 minutes.

### Why my script can't get price from Amazon?
There may be two problem of it.

* Your IP was banned by Amazon

	* Change your IP or wait for unban.


* The item selector changed

### App-Format
![](./images/app.png)

### Email-Format
![](./images/screen.png)


## Dependencies
```text
Python 3
BS4
PyQtWebEngine
SMTPlib
lxml
Webdriver-Manager
Selenium
```

## Future feature
```text
** Script running in background for long and checking after every 1 hour **

** Complete standalone GUI app for MacOS and later for Windows **

** Mail will include a graph of price using matplotlib **
```
