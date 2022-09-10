from binance.helpers import round_step_size
from binance.client import Client


def calc_levels(order_params, config):
    if order_params['stop_loss'] == 0:
        order_params['stop_loss'] = config['stop_loss']

    if order_params['take_profit'] == 0:
        order_params['take_profit'] = config['take_profit']

    if order_params['side'] == 'BUY':
        order_params['stop_loss'] = 1 - \
            (order_params['stop_loss']/100) * order_params['price']
        order_params['take_profit'] = 1 + \
            (order_params['take_profit']/100) * order_params['price']
    elif order_params['side'] == 'SELL':
        order_params['stop_loss'] = 1 + \
            (order_params['stop_loss']/100) * order_params['price']
        order_params['take_profit'] = 1 - \
            (order_params['take_profit']/100) * order_params['price']

    return order_params


def calc_quantity(order_params, config, balance) -> dict:
    return ((config['position_percentage']/100) * balance['total']
            * (config['leverage'])) / (order_params['price'])


def round_steps(order_params, market_info: dict) -> dict:
    quantity_round = market_info[order_params['symbol']]['min_qty']
    level_round = market_info[order_params['symbol']]['tick_size']
    for k, v in order_params.items():
        if k == 'quantity':
            order_params[k] = round_step_size(v, quantity_round)
        elif k == 'take_profit' or k == 'stop_loss':
            order_params[k] = round_step_size(v, level_round)

    return order_params


def new_order(client: Client, order_params: dict, config: dict,
              balance: dict, market_info: dict, default: dict) -> None:
    order_params = calc_levels(order_params, config)
    order_params['quantity'] = calc_quantity(order_params, config, balance)
    order_params = round_steps(order_params, market_info)

    common_params = dict(
        symbol=order_params['symbol'],
        quantity=order_params['quantity']
    )

    position_params = default['market_params']['HEDGE']

    side = order_params['side']
    stop_loss = order_params['stop_loss']
    take_profit = order_params['take_profit']

    try:
        sl_params = position_params[f'{side}_STOP_LOSS']
        client.futures_create_order(
            **common_params, **sl_params, stopPrice=stop_loss)

        tp_params = position_params[f'{side}_TAKE_PROFIT']
        client.futures_create_order(
            **common_params, **tp_params, stopPrice=take_profit)

        market_params = position_params[f'{side}']
        client.futures_create_order(**common_params, **market_params)
    except Exception as e:
        while True:
            try:
                client.futures_cancel_all_open_orders(
                    symbol=order_params['symbol'])
                break
            except Exception as cancel_e:
                pass
        #         send_telegram_messages(
        #             default['telegram'], "cancel_error\n"+cancel_e)

        # send_telegram_messages(default['telegram'], e)


def close_order(client: Client, order_params: dict, account_data: dict, default: dict) -> None:
    position_params = default['market_params']['HEDGE']

    common_params = dict(
        symbol=order_params['symbol'],
        quantity=account_data[order_params['symbol']]['quantity']
    )
    while True:
        try:
            client.futures_create_order(**position_params, **common_params)
            break
        except Exception as close_e:
            send_telegram_messages(
                default['telegram'], "close_error\n"+close_e)
