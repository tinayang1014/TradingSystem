############################
###### Trading System
###### Team: 666
###### Tina Yang
###### Created: 20181129
###########################


class User:
    def __init__(self):
        self.__userName = ''
        self.__password = ''
        self.__id = 0
        self.__transaction = []
        self.__cash_balance = 1000000
        self.__portfolio = {}
    
    def set_credential(self, userName, password):
        self.__userName = userName
        self.__password = password
    
    def get_userName(self):
        return self.__userName

    def get_userID(self):
        return self.__id
    
    def get_cash_balance(self):
        return self.__cash_balance
    
    def set_userID(self, db):
        sql = "select user_id from user where login=\'%s\'" % (self.__userName)
        result = db.get_data(sql)
        self.__id = result[0][0]
        # print("set userID", self.__id)

    def set_balance(self, balance):
        self.__cash_balance = balance

    def get_last_trans(self):
        return self.__transaction[-1]
    
    def reset_user(self):
        self.__init__()

    def set_portfolio(self, db):
        sql = "select currency_id, quant, vwap, rpl from portfolio where user_id = %s;" % (self.__id)
        result = db.get_data(sql)
        if result != []:
            for i in result:
                p = Portfolio(self.__id, i[0], i[1], i[2], i[3])
                self.__portfolio[i[0]] = p

    def init_port(self, db, side, currency, quant, vwap):
        new_p = Portfolio(self.__id, currency, quant, vwap, 0)
        self.__portfolio[currency] = new_p
        new_p.insert_portfolio(db)

    def __update_cash_balance(self, db, side, total):
        # 1.sell 2.buy
        if side == 1:
            self.__cash_balance += total
        else:
            self.__cash_balance -= total
        colValue = "cash_balance = %s" % (self.__cash_balance)
        condition = "user_id = %s" % (self.__id)
        db.update_data("user", colValue, condition)
        print("update cash_balance success")
            
    
    def create_user_in_DB(self, db):
        # check userName already exist
        sql = "select login from user;"
        result = db.get_data(sql)
        listUserName = []
        for user in result:
            listUserName.append(user[0])
        if self.__userName in listUserName:
            return False
        else:
            table = "user"
            colName = "login, password, cash_balance"
            value = (self.__userName, self.__password, self.__cash_balance)
            db.insert_data(table, colName, value)
            self.set_userID(db)
            self.set_portfolio(db)
            return True
    
    def verify_user(self,db):
        # verfity userName and password is matched in DB
        userNameSql = "select login from user;"
        result = db.get_data(userNameSql)
        listUserName = []
        for user in result:
            listUserName.append(user[0])
        if self.__userName in listUserName:
            passwordSql = "select password from user where login=\'%s\'"
            db_password = db.get_data(passwordSql%(self.__userName))
            if self.__password == db_password[0][0]:
                self.set_userID(db)
                balanceSql = "select cash_balance from user where user_id = %s" % (self.__id)
                cash_balance = db.get_data(balanceSql)
                self.set_balance(cash_balance[0][0])
                self.set_portfolio(db)
                return True 
        return False

    def insert_transaction(self, db, currency, side, quant, timestamp):
        t = Transaction(db, currency, self.__id, side, quant, timestamp)
        # Determine Buy or Sell, seperate check process => seperate update protfolio
        # 1.sell 2.buy
        if side == 1:
            # sql = "select quant from portfolio where user_id = %s and currency_id = %s;" % (self.__id, currency)
            # result = db.get_data(sql)
            if currency in self.__portfolio and t.check_quant(self.__portfolio[currency].get_quant()):
                self.__portfolio[currency].update(db, side, quant, t.get_display_price())
                t.insert_trans(db, self.__portfolio[currency].get_trans_rpl())
                self.__transaction.append(t)
                self.__update_cash_balance(db, side, t.get_trans_total())
                return True
        else:
            # When Buy, check cash balance
            if t.check_balance(self.__cash_balance):
                if currency in self.__portfolio:
                    self.__portfolio[currency].update(db, side, quant, t.get_display_price())
                else:
                    self.init_port(db, side, currency, quant,t.get_display_price())
                t.insert_trans(db, self.__portfolio[currency].get_trans_rpl())
                self.__transaction.append(t)
                self.__update_cash_balance(db, side, t.get_trans_total())
                return True
        return False

    def update_PL(self, db):
        pass


class Transaction:
    def __init__(self, db, currency_id, user_id, buy_sell, quant, timestamp):
        self.__currency_id = currency_id
        self.__user_id = user_id
        # 1.sell 2.buy
        if buy_sell == 1:
            self.__type = "Sell"
        elif buy_sell == 2:
            self.__type = "Buy"
        self.__quant = quant
        self.__timestamp = timestamp.strftime('%Y-%m-%d %H:%M:%S')
        self.__price = self.get_currency_price(db)
        self.__trans_rpl = 0

    def get_trans_total(self):
        return self.__quant * self.__price

    def check_balance(self, cash_balance):
        total = self.__quant * self.__price
        print("pass cash balance check")
        return cash_balance >= total

    def check_quant(self, avali_quant):
        return avali_quant >= self.__quant

    def get_display_price(self):
        return self.__price

    def get_currency_price(self, db):
        sql = "select price from price where currency_id = %s and time_stamp = (select max(time_stamp) from price where currency_id = %s and time_stamp<= \'%s\');" % (self.__currency_id, self.__currency_id, self.__timestamp)
        print(sql)
        price = db.get_data(sql)
        print("in Transacation price: ", price)
        return float(price[0][0])
    
    def insert_trans(self, db, trans_rpl):
        self.__trans_rpl = trans_rpl
        table = "transaction"
        print("in Transaction Insert", self.__user_id)
        if self.__type == "Sell":
            colName = "currency_id, user_id, type, quant, price, timestamp, trans_rpl"
            value = (self.__currency_id, self.__user_id, self.__type, self.__quant, self.__price, self.__timestamp, self.__trans_rpl)
        else:
            colName = "currency_id, user_id, type, quant, price, timestamp"
            value = (self.__currency_id, self.__user_id, self.__type, self.__quant, self.__price, self.__timestamp)
        db.insert_data(table, colName, value)

class Portfolio:
    def __init__(self, user_id, currency_id, quant, vwap, rpl):
        self.__user_id = user_id
        self.__currency_id = currency_id
        self.__quant = quant
        self.__vwap = vwap
        self.__rpl = rpl
        self.__trans_rpl = 0
    
    # first transaction must be buy, if sell--sorry
    #1. insert portfolio table if first time buy with quant and price
    #2. following transaction
    #if buy, update quant and vwap
    #if sell, update quant and rpl
        
    def get_quant(self):
        return self.__quant

    
    def insert_portfolio(self,db):
        table="portfolio"
        colName="user_id,currency_id,quant,vwap,rpl"
        value=(self.__user_id,self.__currency_id,self.__quant,self.__vwap,self.__rpl)
        db.insert_data(table,colName,value)
        
    def get_trans_rpl(self):
        return self.__trans_rpl

    #new_quant is transaction quantity, new_price is transaction price
    def update(self, db, side, new_quant, new_price):
        table="portfolio"
        #1.sell 2.buy
        print("in update protf: ", new_price)
        if side==2:
            self.__vwap=(self.__quant*self.__vwap + new_quant*new_price)/(self.__quant+new_quant)
            self.__quant+=new_quant
            colValue = "quant = %s, vwap=%s" % (self.__quant,self.__vwap)
        elif side==1:
            print(new_price - self.__vwap)
            self.__trans_rpl = (new_price - self.__vwap)*new_quant
            self.__rpl=self.__rpl+ self.__trans_rpl
            self.__quant-=new_quant
            colValue="quant = %s, rpl =%s"%(self.__quant,self.__rpl)
        condition = "user_id = %s and currency_id =%s" % (self.__user_id,self.__currency_id)
        db.update_data(table,colValue,condition)   

        
                

        

        