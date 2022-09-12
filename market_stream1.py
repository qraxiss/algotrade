from binance import AsyncClient, BinanceSocketManager
from data.access import get_default
from binance.client import Client
from json import dumps, loads
from threading import Thread
from time import time, sleep
from requests import post
import numpy as np
import asyncio


url = 'http://127.0.0.1:5000/api'
default = get_default()
period = 30
sockets = default['sockets'][:20]


def get_klines(socket):
    symbol, interval = socket.replace('kline_', '').split('@')
    symbol = symbol.upper()
    klines_json = Client().futures_klines(symbol=symbol,
                                          interval=interval,
                                          limit=period)

    post('http://127.0.0.1:5000/api/set/klines',
         json=dict(symbol=socket, klines=klines_json))


def first_start():
    threads = list()
    length = len(sockets)
    i = 0
    start = time()
    for socket in sockets:
        i += 1

        threads.append(Thread(target=get_klines, args=(socket,)))
        threads[-1].start()

        if i % 41 == 0:
            sleep(12)

        print(f'process:{i}/{length}\ntotal time:{time()-start}')

    for thread in threads:
        thread.join()


def market_stream_formatter(stream: dict) -> dict:
    kline = stream['data']['k']
    kline = np.array(list(kline.values()))[
        [0, 6, 8, 9, 7, 10, 1, 13, 11, 14, 15, 16]].tolist()

    if stream['data']['k']['x']:
        close = True
    else:
        close = False

    stream = stream['stream']

    post(url+'/append/klines', json=dict(stream=stream, kline=kline, close=close))


async def market_stream():
    async_client = AsyncClient(**default['account'])
    bm = BinanceSocketManager(async_client)
    ts = bm.multiplex_socket(sockets)

    async with ts as tscm:
        while True:
            msg = await tscm.recv()
            Thread(target=market_stream_formatter, args=(msg,)).start()

    await async_client.close_connection()


if __name__ == '__main__':
    first_start()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(market_stream())
