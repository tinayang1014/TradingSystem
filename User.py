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
    
    def set_credential(self, userName, password):
        self.__userName = userName
        self.__password = password
    
    def get_userName(self):
        return self.__userName
    
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
                return True
            else:
                return False
        else:
            return False

        

        

        