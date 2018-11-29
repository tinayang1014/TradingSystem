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
import dateutil.parser
import Database

class Socket:
    def __init__(self, stock):
        self.stock = stock
        self.db = Database.Database()
        self.__value = ()
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
            time = dateutil.parser.parse(time).strftime('%Y-%m-%d %H:%M:%S')
            open = float(message['open_24h'])
            price = float(message['price'])
            best_bid = float(message['best_bid'])
            best_ask = float(message['best_ask'])
            self.__value = (currency_id, time, open, price, best_bid, best_ask)

    
    def insert_price(self):
        colName = 'currency_id, time_stamp, open, price, best_bid, best_ask'
        # print("insert_price", self.__value)
        self.db.insert_data('price', colName, self.__value)
        print("insert price success", self.refresh_web_price())

    def refresh_web_price(self):
        return (self.__value[0], self.__value[3])

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
                self.organize_message(m)
                # print(self.__value)
                if self.__value != ():
                    # print(self.refresh_web_price())
                    self.insert_price()
                    

    
    def build_request(self):
        request = "{\"type\": \"subscribe\",  \"channels\": [{ \"name\": \"ticker\", \"product_ids\": [\"%s\"] }]}"%(self.stock)
        # print(request)
        return request

if __name__ == "__main__":
    s = Socket("BTC-USD")