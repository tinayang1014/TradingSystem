############################
###### Trading System
###### Team: 666
###### Tina Yang
###### Created: 20181111
###########################
'''
20181113 Test inserting data into Oracle database (success)
20181114 Inserting currency price into database with time pause
'''


from pandas_datareader import data as pdr
import fix_yahoo_finance as yf
import datetime
import time
import mysql.connector as mc


yf.pdr_override()
sys_active = True
stocks = ['BTC-USD', 'LTC-USD', 'ETH-USD']
# start = datetime.datetime(2018,1,1)
start = datetime.datetime(2018, 11, 16)
# start = datetime.datetime.now()
# end = datetime.datetime.now()
# print(end)

def reading_currency_realtime(stock, id, start, end):
    # Reading single currency price in realtime (start, end = now)
    data = pdr.get_data_yahoo(stock, start=start, end=end)
    print(data)
    open = float(data.Open)
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    high = float(data.High)
    low = float(data.Low)
    close = float(data.Close)
    volume = int(data.Volume)
    val = (id, timestamp, open, high, low, close, volume)
    return val

# print(reading_currency_realtime(stocks[0], start, end))


def daterange(start_date, end_date):
    ### Loop through start to end-1
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)


def connect_database():
    # Connect the MySQL database
    connection = mc.connect(user='root',
    password = 'tinayang',
    host = '127.0.0.1',
    database = 'TradingSys',
    auth_plugin = 'mysql_native_password')
    return connection

def insert_realtime_currency_price(connection, sql, val):
    # Insert single currency price into database
    # Do not return
    database_cursor = connection.cursor()
    # sql = "INSERT INTO price VALUE (%s, %s, %s, %s, %s, %s, %s)"
    database_cursor.execute(sql, val)
    connection.commit()

def close_database(connection):
    connection.close()



if __name__ == "__main__":
    connection = connect_database()
    sql = "INSERT INTO price (currency_id, time_stamp, open, high, low, close, volume) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    sys_start = datetime.datetime.now()
    while sys_active:
        end = datetime.datetime.now() 
        for i in range(len(stocks)):
            val = reading_currency_realtime(stocks[i], i+1, start, end)
            insert_realtime_currency_price(connection, sql, val)
        time.sleep(30)
        if (end - sys_start) > datetime.timedelta(minutes=2):
            sys_active = False
    close_database(connection)
        




'''
connection = mc.connect(user='root',
password = 'tinayang',
host = '127.0.0.1',
database = 'TradingSys',
auth_plugin = 'mysql_native_password')

result = connection.cmd_query('select * from price')
print(result)
rows = list(connection.get_rows())
for r in rows[0]:
	print(r)


date_list = []
for single_date in daterange(start, end):
    date_list.append(single_date.strftime("%Y-%m-%d"))


for i in range(len(date_list)):
    id = 1
    date = date_list[i]
    open = open_list[i]
    high = high_list[i]
    low = low_list[i]
    close = close_list[i]
    volume = Volume_list[i]
    val = (id, date, open, high, low, close, volume)
    database_cursor.execute(sql, val)
    
connection.commit()


connection.close()
'''