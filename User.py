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
            colName = "login, password"
            value = (self.__userName, self.__password)
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
                return True 
        return False

    def insert_transaction(self, db, currency, side, quant, timestamp):
        self.__transaction.append(Transaction(db, currency, self.__id, side, quant, timestamp))
    
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
        self.insert_trans(db)
    
    def get_currency_price(self, db):
        sql = "select price from price where time_stamp = (select min(time_stamp) from price where time_stamp> \'%s\');" % (self.__timestamp)
        price = db.get_data(sql)
        # print("in Transacation price: ", price)
        return price[0][0]
    
    def insert_trans(self, db):
        table = "transaction"
        colName = "currency_id, user_id, type, quant, price, timestamp"
        # print("in Transaction Insert", self.__user_id)
        value = (self.__currency_id, self.__user_id, self.__type, self.__quant, self.__price, self.__timestamp)
        db.insert_data(table, colName, value)


        

                

        

        