from helpers import socket_parser
from threading import Thread

def get_step_info(client):
    exchange_info = client.futures_exchange_info()['symbols']
    symbol_info = dict()
    for symbol in exchange_info:
        tick_size = symbol['filters'][0]['tickSize']
        min_qty = symbol['filters'][1]['minQty']
        symbol_info[symbol['symbol']] = {
            'min_qty': min_qty, 'tick_size': tick_size}

    return symbol_info


def get_balance(client):
    balance = client.futures_account_balance()[6]
    return dict(
        total=float(balance['balance']),
        available=float(balance['withdrawAvailable'])
    )


def cancel_levels(client, pair, positions):
    symbol, interval = socket_parser(pair)
    order_list = positions[pair]['stop_id'], positions[pair]['take_id']
    Thread(target=client.futures_cancel_orders, kwargs=dict(symbol=symbol, orderIdList=order_list)).start()