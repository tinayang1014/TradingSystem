############################
###### Trading System
###### Team: 666
###### Tina Yang
###### Created: 20181119
###########################

import asyncio
import websockets
import json

class Socket:
    def __init__(self, stock):
        self.stock = stock
        asyncio.get_event_loop().run_until_complete(self.start_gdax_websocket())
    
    def organize_message(self, message):
        message = json.loads(message)
        if 'side' in message.keys():
            # time is a str with ISO 8601 format: 2018-11-19T20:29:20.550000Z
            time = message['time']
            ####### Handle time format

            ######^^^^^^^^^^^^^^^^^^^^
            open = message['open_24h']
            price = message['price']
            best_bid = message['best_bid']
            best_ask = message['best_ask']
            value = (time, open, price, best_bid, best_ask)
            return value
        

    async def start_gdax_websocket(self):
        async with websockets.connect('wss://ws-feed.pro.coinbase.com') as websocket:
            await websocket.send(self.build_request())
            async for m in websocket:
                # print(m)
                value = self.organize_message(m)
                print(value)
                # await asyncio.sleep(10)
                
    
    def build_request(self):
        request = "{\"type\": \"subscribe\",  \"channels\": [{ \"name\": \"ticker\", \"product_ids\": [\"%s\"] }]}"%(self.stock)
        # print(request)
        return request

if __name__ == "__main__":
    s = Socket("BTC-USD")