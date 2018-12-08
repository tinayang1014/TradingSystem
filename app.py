############################
###### Trading System
###### Team: 666
###### Tina Yang
###### Created: 20181111
###########################

from flask import Flask, render_template, json, request,Markup
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
# Dictionary with latest currency price
# 1.BTC 2.LTC 3.ETH
# newest_currency_price = {1:0, 2:0, 3:0}

# refresh_price = ()
####################################
##### Comment Out Before Run #######
@app.before_first_request
def activate_job():
    # print("in activate_job")
    def run_job(stock):
        s = Socket.Socket(stock)

    for i in ["BTC-USD", "LTC-USD", "ETH-USD"]:
        thread = Thread(target=run_job, args=(i,))
        thread.start()
        
####################################


def get_single_currency_price(currency_id):
    sql = "select price from price where currency_id = %s and time_stamp = (select max(time_stamp) from price where currency_id = %s);" % (currency_id, currency_id)
    result = db.get_data(sql)
    return result[0][0]


# def get_updated_price(newest_currency_price):
#     sql = "select price from price where currency_id = %s and time_stamp = (select max(time_stamp) from price where currency_id = %s);"
#     for c in newest_currency_price:
#         price = db.get_data(sql%(c,c))
#         # price: list of tuple
#         newest_currency_price[c] = price[0][0]
#     return newest_currency_price

def get_portfolio_balance(db, user_id):
    sql = "select s.currency_id,s.symbol, p.quant, p.vwap, p.rpl from portfolio as p join symbol as s on p.currency_id = s.currency_id where p.user_id = %s;" % (user_id)
    result = db.get_data(sql)
    return result

def get_trans_history(db, user_id):
    sql = "select s.symbol, t.type, t.quant, t.price, t.timestamp, t.trans_rpl from transaction as t join symbol as s on t.currency_id = s.currency_id where t.user_id = %s;" % (user_id)
    result = db.get_data(sql)
    result = sorted(result, key=lambda x:x[4])
    # print(result)
    return result

# def thread_refresh_currency_price():
#     global newest_currency_price 
#     def update_currency():
#         global newest_currency_price 
#         while True:
#             # print("trade: update currency")
#             newest_currency_price = get_updated_price(newest_currency_price)
#             # print(newest_currency_price)
#             sleep(30)
    
#     thread1 = Thread(target=update_currency)
#     thread1.start()



@app.route('/')
def main():
    return render_template('index.html')


@app.route('/signUp')
def signUp():
    db.reconnect_db()
    return render_template('signUp.html')

@app.route('/userCreate', methods = ['POST'])
def userCreate():
    db.reconnect_db()
    user.reset_user()
    userName = request.form['Create_userName']
    password = request.form['Create_password']

    # create user and insert into the database
    user.set_credential(userName, password)
    res = user.create_user_in_DB(db)
    if not res:
        return render_template('signUp.html')
    else:
        return render_template('userindex.html', 
                    userName = user.get_userName())

@app.route('/userLogIn', methods = ['POST'])
def userLogIn():
    db.reconnect_db()
    userName = request.form['LogInUserName']
    password = request.form['LogInPassword']
    # Check credentail
    user.set_credential(userName, password)
    if user.verify_user(db):
        return render_template('userindex.html',
                    userName = user.get_userName())
    else:
        return render_template('login.html')


@app.route('/login')
def login():
    db.reconnect_db()
    return render_template('login.html')

@app.route('/trade') 
def trade():
    db.reconnect_db()
    # global newest_currency_price 
    # def update_currency():
    #     global newest_currency_price 
    #     while True:
    #         # print("trade: update currency")
    #         global newest_currency_price
    #         newest_currency_price = get_updated_price(newest_currency_price)
    #         print("in update", newest_currency_price)
    #         # print(newest_currency_price)
    #         sleep(30)
    
    # thread1 = Thread(target=update_currency)
    # thread1.start()
    
    newest_currency_price = {1:0, 2:0, 3:0}
    for currency in newest_currency_price:
        newest_currency_price[currency] = get_single_currency_price(currency)

    return render_template('trade.html',userName = user.get_userName(), updated_price = newest_currency_price)

@app.route('/bitcoin')
def bitcoin():
    return render_template('bitcoin.html')

@app.route('/order', methods = ['POST'])
def order():
    db.reconnect_db()
    # 1.BTC 2.LTC 3.ETH
    currency = int(request.form['itemOrdered'])
    print("order currency id",currency)
    # 1.sell 2.buy
    side = int(request.form['saleorbuy'])
    quant = int(request.form['orderQty'])
    timestamp = datetime.datetime.now()
    if user.insert_transaction(db, currency, side, quant, timestamp):
        sql = "select symbol from symbol where currency_id = %s;"%(currency)
        sym = db.get_data(sql)[0][0]
        price = (user.get_last_trans()).get_display_price()
        return render_template('confirm.html', sym = sym, qty = quant, price = price)
    else:
        return render_template('sorry.html')

@app.route('/portfolio')
def protfoilo():
    db.reconnect_db()
    portfolio_balance = get_portfolio_balance(db, user.get_userID())
    trans_history = get_trans_history(db, user.get_userID())

    # global newest_currency_price 
    # newest_currency_price = get_updated_price(newest_currency_price)

    # global newest_currency_price 
    # def update_currency():
    #     global newest_currency_price 
    #     while True:
    #         # print("trade: update currency")
    #         newest_currency_price = get_updated_price(newest_currency_price)
    #         print(newest_currency_price)
    #         sleep(30)
    # thread1 = Thread(target=update_currency)
    # thread1.start()

    db.reconnect_db()
    newest_currency_price = {1:0, 2:0, 3:0}
    for currency in newest_currency_price:
        newest_currency_price[currency] = get_single_currency_price(currency)
    colors = [ "#F7464A", "#46BFBD", "#FDB45C" ]    
    symbol=[]
    equity=[]
    rpl=[]
    

    for i in portfolio_balance:
        symbol.append(i[1])
        equity.append(round(i[2]*i[3],2))
        rpl.append(i[4])
    


    return render_template('portfolio.html',
                    userName = user.get_userName(),
                    cashBalance = user.get_cash_balance(), 
                    portfolio_balance = portfolio_balance, 
                    trans_history = trans_history,
                    updated_price = newest_currency_price,
                    set=zip(symbol,equity,colors),
                    set2=zip(symbol,rpl)
                )

@app.route('/sorry')
def sorry():
    return render_template('sorry.html')

@app.route('/confirm')
def confirm():
    return render_template('confirm.html')

@app.route('/logout')
def logout():
    db.close()
    return render_template('index.html')


if __name__ == '__main__':
    app.run(threaded = True)
    # t = Thread(target=Socket.Socket, args=('BTC-USD'))
    # t.start()
    # socketio.run(app, debug=True)
    # # socket = Socket.Socket("BTC-USD")
    # wst = threading.Thread(target=Socket.Socket, args=("BTC-USD",))
    # wst.daemon = False
    # wst.start()