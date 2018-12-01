############################
###### Trading System
###### Team: 666
###### Tina Yang
###### Created: 20181111
###########################

from flask import Flask, render_template, json, request
from random import random
from time import sleep
from threading import Thread, Event
import datetime
import Database, Socket
import User



app = Flask(__name__)


# export FLASK_DEBUG=1

db = Database.Database()
user = User.User()

# refresh_price = ()
####################################
##### Comment Out Before Run #######
@app.before_first_request
def activate_job():
    # print("in activate_job")
    def run_job(stock):
        s = Socket.Socket(stock)
        # refresh_price = s.refresh_web_price()
        # print(refresh_price)
        # while True:
        #     s = Socket.Socket(stock)
            # refresh_price = s.refresh_web_price()
            # print(refresh_price)
            # time.sleep(30)

    for i in ["BTC-USD", "LTC-USD", "ETH-USD"]:
        thread = Thread(target=run_job, args=(i,))
        thread.start()

####################################



def get_updated_price(newest_currency_price):
    sql = "select price from price where currency_id = %s and time_stamp = (select max(time_stamp) from price where currency_id = %s);"
    for c in newest_currency_price:
        price = db.get_data(sql%(c,c))
        # price: list of tuple
        newest_currency_price[c] = price[0][0]
    return newest_currency_price


# Dictionary with latest currency price
# 1.BTC 2.LTC 3.ETH
newest_currency_price = {1:0, 2:0, 3:0}

@app.route('/')
def main():
    # sym = db.get_data("select * from symbol")
    # db.close()
    return render_template('index.html', updated_price = newest_currency_price)


@app.route('/signUp')
def signUp():
    return render_template('signUp.html')

@app.route('/userCreate', methods = ['POST'])
def userCreate():
    userName = request.form['Create_userName']
    password = request.form['Create_password']

    # create user and insert into the database
    user.set_credential(userName, password)
    res = user.create_user_in_DB(db)
    if not res:
        return render_template('signUp.html')
    else:
        return render_template('portfolio.html')

@app.route('/userLogIn', methods = ['POST'])
def userLogIn():
    userName = request.form['LogInUserName']
    password = request.form['LogInPassword']
    # Check credentail
    user.set_credential(userName, password)
    if user.verify_user(db):
        return render_template('portfolio.html')
    else:
        return "user name or password is invalid."


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/trade', methods = ['GET','POST']) 
def trade():
    global newest_currency_price 
    def update_currency():
        global newest_currency_price 
        while True:
            print("trade: update currency")
            newest_currency_price = get_updated_price(newest_currency_price)
            print(newest_currency_price)
            sleep(30)
    
    thread1 = Thread(target=update_currency)
    thread1.start()

    return render_template('trade.html', updated_price = newest_currency_price)

@app.route('/bitcoin')
def bitcoin():
    return render_template('bitcoin.html')

@app.route('/order', methods = ['POST'])
def order():
    # 1.BTC 2.LTC 3.ETH
    currency = int(request.form['itemOrdered'])
    # 1.sell 2.buy
    side = int(request.form['saleorbuy'])
    quant = int(request.form['orderQty'])
    timestamp = datetime.datetime.now()
    user.insert_tracation(db, currency, side, quant, timestamp)
    return "order success"

@app.route('/portfolio')
def protfoilo():
    return render_template('portfolio.html')



if __name__ == '__main__':
    app.run(threaded = True, debug = True)
    # t = Thread(target=Socket.Socket, args=('BTC-USD'))
    # t.start()
    # socketio.run(app, debug=True)
    # # socket = Socket.Socket("BTC-USD")
    # wst = threading.Thread(target=Socket.Socket, args=("BTC-USD",))
    # wst.daemon = False
    # wst.start()