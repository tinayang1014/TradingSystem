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
        listUserName = db.get_data(sql)
        