############################
###### Trading System
###### Team: 666
###### Tina Yang
###### Created: 20181119
###########################

import asyncio
import websockets
import json
import time
import Database
import datetime
import pytz, dateutil.parser

class Socket:
    def __init__(self, stock):
        self.stock = stock
        self.db = Database.Database()
        self.__value = {1:(1,0,0), 2:(2,0,0), 3:(3,0,0)}
        # self.__currency_id = 0
        # print("in socket init")
        asyncio.set_event_loop(asyncio.new_event_loop())
        asyncio.get_event_loop().run_until_complete(self.start_gdax_websocket())
    
    def get_currency_id(self):
        currency_id = self.db.get_data("select currency_id from symbol where symbol = \'%s\';" % (self.stock))
        # print(currency_id[0][0])
        # print(type(currency_id[0][0]))
        return currency_id[0][0]

    def organize_message(self, message):
        message = json.loads(message)
        if 'side' in message.keys():
            currency_id = self.get_currency_id()
            # time is a str with ISO 8601 format: 2018-11-19T20:29:20.550000Z
            time = message['time']
            ####### Handle time format
            # Default is EUROPE time, convert to current time zone >>>>>>>>>
            time=dateutil.parser.parse(time)
            localtime=time.astimezone(pytz.timezone("US/Eastern"))
            localiso=localtime.isoformat()

            time = dateutil.parser.parse(localiso).strftime('%Y-%m-%d %H:%M:%S')
            # open = float(message['open_24h'])
            price = float(message['price'])
            # best_bid = float(message['best_bid'])
            # best_ask = float(message['best_ask'])
            return (currency_id, time, price)

    
    
    def insert_price(self, new):
        self.__value[new[0]] = new
        colName = 'currency_id, time_stamp, price'
        # print("insert_price", self.__value)
        self.db.insert_data('price', colName, new)
        print("insert price success", self.refresh_web_price(new))

    def refresh_web_price(self, new):
        return (new[0], new[2])

    async def start_gdax_websocket(self):
        # print("in start gdax websocket")
        async with websockets.connect('wss://ws-feed.pro.coinbase.com') as websocket:
            # print("1")
            await websocket.send(self.build_request())
            time.sleep(10)
            # print("2")
            async for m in websocket:
                # print("3")
                # print(m)
                new = self.organize_message(m)
                print(new)
                if new != None and new[2] != self.__value[new[0]][2]:
                    # print(self.refresh_web_price())
                    self.insert_price(new)
                    

    
    def build_request(self):
        request = "{\"type\": \"subscribe\",  \"channels\": [{ \"name\": \"ticker\", \"product_ids\": [\"%s\"] }]}"%(self.stock)
        # print(request)
        return request

# if __name__ == "__main__":
#     s = Socket("BTC-USD")
import pytz, dateutil.parser
import datetime

utctime = dateutil.parser.parse("2010-05-08T23:41:54.000Z")
a="2018-11-19T20:29:20.550000Z"
b=datetime.datetime(a)
date_time_obj = datetime.datetime.strptime(a, '%Y-%m-%d%H:%M:%S')
date_object = dateutil.parser.parse(a)

print(type(utctime))

