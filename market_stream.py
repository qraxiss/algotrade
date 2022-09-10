from binance import AsyncClient, BinanceSocketManager
from data.access import get_default
from binance.client import Client
from requests import post
from json import loads
import pandas as pd
import asyncio


url = 'http://127.0.0.1:5000/api'
default = get_default()
period = 30


def market_stream_formatter(stream_json: dict) -> dict:
    stream_json = stream_json['data']['k']
    symbol = stream_json['s']

    klines_json = loads(post(url+'/get/klines', json=dict(symbol=symbol)).text)
    if klines_json == None:
        klines_json = Client().futures_klines(symbol=symbol,
                                              interval=stream_json['i'],
                                              limit=period)
        klines_df = pd.DataFrame(klines_json)[[0, 1, 2, 3, 4, 5]]
        klines_df.columns = ['start', 'open', 'high', 'low', 'close', 'volume']

    else:
        klines_df = pd.DataFrame(klines_json)

    # Transform json to dataframe
    stream_df = pd.DataFrame([stream_json])[
        ['t', 'o', 'h', 'l', 'c', 'v']]
    stream_df.columns = ['start', 'open', 'high', 'low', 'close', 'volume']

    # if candlestick closed
    if stream_json['x'] == True:
        klines_df = pd.concat(
            [klines_df.iloc[1:], stream_df], ignore_index=True)
    else:
        klines_df = pd.concat(
            [klines_df.iloc[:-1], stream_df], ignore_index=True)

    post(url+'/set/klines', json=dict(symbol=symbol, klines=klines_df.to_json()))


async def market_stream():
    async_client = AsyncClient(**default['account'])
    bm = BinanceSocketManager(async_client)
    ts = bm.multiplex_socket(default['sockets'])

    async with ts as tscm:
        while True:
            msg = await tscm.recv()
            market_stream_formatter(msg)

    await async_client.close_connection()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(market_stream())
