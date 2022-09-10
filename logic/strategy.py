from data.access import get_config


def is_order_valid(account_data, order_params):
    config = get_config()
    positions = account_data['positions']
    balance = account_data['positions']

    if order_params['symbol'] not in positions:

        if balance['available'] < (config['percentage']/100)*balance['total']:
            if config['max_position'] > len(positions):
                return 'NEW'

    else:

        if order_params['side'] != positions['symbol']['side']:
            return 'CLOSE'

    return False


def signal():
    pass
