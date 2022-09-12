from requests import post
from json import loads

url = 'http://127.0.0.1:5000/api'

def is_plot(symbol, interval):
    if symbol != None and interval != None:
            socket = symbol.lower() + '@kline_' + interval

            data = loads(post(url+'/get/klines', json=dict(symbol=socket)).text)
            if data != None:
                return data
            
            else:
                return False