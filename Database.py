############################
###### Trading System
###### Team: 666
###### Tina Yang
###### Created: 20181119
###########################

import mysql.connector as mc

class Database:
    '''This class will contain everything related to the Database,
    Connect, Insert, Display data from the database
    '''
    def __init__(self):
        ## Connect the database once the class created
        self.connection = mc.connect(user='root',
            password = 'tinayang',
            host = '127.0.0.1',
            database = 'TradingSys',
            auth_plugin = 'mysql_native_password')
    
    def get_data(self, sql):
        self.connection.cmd_query(sql)
        rows = list(self.connection.get_rows())
        return rows[0]

    def insert_data(self, table, colName, value):
        cursor = self.connection.cursor()
        # print(value)
        sql = "INSERT INTO %s (%s) VALUES %s"%(table, colName, value)
        # print(sql)
        cursor.execute(sql)
        self.connection.commit()

    def close(self):
        self.connection.close()
    