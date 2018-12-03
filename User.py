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
        self.__cash_balance = 100000
    
    def set_credential(self, userName, password):
        self.__userName = userName
        self.__password = password
    
    def get_userName(self):
        return self.__userName

    def get_userID(self):
        return self.__id
    
    def set_userID(self, db):
        sql = "select user_id from user where login=\'%s\'" % (self.__userName)
        result = db.get_data(sql)
        self.__id = result[0][0]
        # print("set userID", self.__id)

    def set_balance(self, balance):
        self.__cash_balance = balance

    def get_last_trans(self):
        return self.__transaction[-1]

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
            print("create user success")
            self.set_userID(db)
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
                return True 
        return False

    def insert_transaction(self, db, currency, side, quant, timestamp):
        t = Transaction(db, currency, self.__id, side, quant, timestamp)
        # Determine Buy or Sell, seperate check process => seperate update protfolio
        # 1.sell 2.buy
        if side == 1:
            sql = "select quant from portfolio where user_id = %s and currency_id = %s;" % (self.__id, currency)
            result = db.get_data(sql)
            if result != [] and t.check_quant(result[0][0]):
                t.insert_trans(db)
                self.__transaction.append(t)
                self.__update_cash_balance(db, side, t.get_trans_total())
                return True
        else:
            # When Buy, check cash balance
            if t.check_balance(self.__cash_balance):
                # print("insert_transaction, in if")
                t.insert_trans(db)
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
        sql = "select price from price where currency_id = %s and time_stamp = (select max(time_stamp) from price where currency_id = %s and time_stamp> \'%s\');" % (self.__currency_id, self.__currency_id, self.__timestamp)
        price = db.get_data(sql)
        # print("in Transacation price: ", price)
        return float(price[0][0])
    
    def insert_trans(self, db):
        table = "transaction"
        colName = "currency_id, user_id, type, quant, price, timestamp"
        print("in Transaction Insert", self.__user_id)
        value = (self.__currency_id, self.__user_id, self.__type, self.__quant, self.__price, self.__timestamp)
        db.insert_data(table, colName, value)

class Portfolio:
    def __init__(self, user_id, currency_id):
        self.__user_id = user_id
        self.__currency_id = currency_id
        

                

        

        