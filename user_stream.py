from binance import AsyncClient, BinanceSocketManager
from logic.tg_msg import send_telegram_messages
from data.access import get_default
from binance.client import Client
from json import loads, dumps
from requests import post
import asyncio

url = "http://127.0.0.1:80/api"
default = get_default()

client = Client(**default['account'])

def user_stream_formatter(stream_json: dict) -> dict:
    if stream_json['e'] == 'ORDER_TRADE_UPDATE':
        order = stream_json['o']
        symbol = order['s']
        order_type = None

        account_data = dict()
        account_data = loads(post(url+'/get/account', json=dict(type="all")))

        # Close
        if (((order['o'] == 'STOP_MARKET' or order['o'] == 'TAKE_PROFIT_MARKET') and order['rp'] != 0) or
                (order['o'] == 'MARKET' or order['o'] == 'LIMIT') and order['rp'] != 0):

            # order_type
            order_type = 'CLOSE'

            # close sl & tp
            client.futures_cancel_all_open_orders(symbol=symbol)

            # update local balance
            position_volume = account_data['positions'][symbol]['volume']
            account_data['balance']['available'] += position_volume + order['rp']
            account_data['balance']['total'] += order['rp']

            # update local positions
            del account_data['positions'][symbol]

        # New
        elif (order['o'] == 'MARKET' or order['o'] == 'LIMIT') and order['rp'] == 0:
            # order type
            order_type = 'NEW'

            # update local balance
            position_volume = order['q'] * order['ap']
            account_data['balance']['available'] -= position_volume

            # update local positions
            account_data['positions'][symbol] = dict(
                volume=position_volume,
                quantity=order['q'],
                side=order['S']
            )

        telegram_msg = telegram_message_formatter(
            msg_type=order_type, order=order)

        send_telegram_messages(default['telegram'], telegram_msg)

        post(url+'/set/account', json=dict(type="all", data=dumps(account_data)))


async def user_stream():
    async_client = AsyncClient(**default['account'])
    bm = BinanceSocketManager(async_client)

    ts = bm.futures_user_socket()

    async with ts as tscm:
        while True:
            msg = await tscm.recv()
            user_stream_formatter(msg)
    await async_client.close_connection()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(user_stream())