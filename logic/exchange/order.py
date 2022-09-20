from binance.helpers import round_step_size
from threading import Thread
from api import request


class Order:
    def __init__(self, params, resources) -> None:
        self.step_info = resources.step_info
        self.positions = resources.positions
        self.balance = resources.balance
        self.default = resources.default
        self.client = resources.client
        self.config = resources.config
        self.params = params
        self.orders = None
        self.order = None

        self.side = self.params['side']
        self.pair = self.params['pair']
        self.symbol = self.params['pair'].split('@')[0].upper()
        self.mode_params = self.default['mode_params']['BOTH']
        # so as not to calculate in vain if the trade order is not valid.
        self.order = self.is_order_valid()
        if self.order != False:
            # prepare params for the order
            self.levels()
            self.quantity()
            self.round()
            self.common_params = dict(
                symbol=self.symbol, quantity=str(self.params['quantity']))

            if self.order == 'new':
                self.new_order()
            elif self.order == 'close':
                self.close_order()

    def is_order_valid(self):
        if self.params['pair'] not in self.positions:
            if self.balance['available'] > (self.config['position_percentage']/100)*self.balance['total']:
                if self.config['max_position'] > len(self.positions):
                    return 'new'

        else:
            if self.side != self.positions[self.pair]['side']:
                return 'close'

        return False

    def levels(self):
        if self.params['side'] == 'BUY':
            self.params['stop_loss'] = (
                1 - (self.params['stop_loss']/100)) * self.params['price']
            self.params['take_profit'] = (
                1 + (self.params['take_profit']/100)) * self.params['price']

        else:
            self.params['stop_loss'] = (1 +
                                        (self.params['stop_loss']/100)) * self.params['price']
            self.params['take_profit'] = (1 -
                                          (self.params['take_profit']/100)) * self.params['price']

    def quantity(self):
        self.params['quantity'] = (self.config['leverage'] * self.balance['total']) * (
            self.config['position_percentage']/100) / self.params['price']

    def round(self):
        steps = self.step_info[self.symbol]

        self.params['quantity'] = round_step_size(
            self.params['quantity'], steps['min_qty'])
        self.params['stop_loss'] = round_step_size(
            self.params['stop_loss'], steps['tick_size'])
        self.params['take_profit'] = round_step_size(
            self.params['take_profit'], steps['tick_size'])

    def new_order(self):

        sl_params = dict(**self.mode_params[f'{self.side}_STOP_LOSS'],
                         stopPrice=self.params['stop_loss'])
        tp_params = dict(**self.mode_params[f'{self.side}_TAKE_PROFIT'],
                         stopPrice=self.params['take_profit'])
        position_params = dict(**self.mode_params[f'{self.side}'])

        self.levels_ = [dict(**self.common_params, **sl_params),
                        dict(**self.common_params, **tp_params)]

        self.orders = self.client.futures_place_batch_order(
            batchOrders=self.levels_)

        # check orders succesfuly opens
        self.success = False
        if 'code' in self.orders[0] and 'code' in self.orders[1]:
            pass
        elif 'code' not in self.orders[0] and 'code' in self.orders[1]:
            pass

        elif 'code' in self.orders[0] and 'code' not in self.orders[1]:
            pass

        else:
            try:
                self.client.futures_create_order(**position_params)
            except Exception as err:
                pass

    def close_order(self):
        close_params = self.mode_params[f'{self.side}_CLOSE']
        self.orders = dict(close_order=self.client.futures_create_order(
            **self.common_params, **close_params))

        order_list = self.positions[self.pair]['take_id'], self.positions[self.pair]['stop_id']

class OrderManagement(Order):
    def __init__(self, params, resources) -> None:
        super().__init__(params, resources)

        if self.orders != None:
            if self.order == 'new':
                self.put_order()

            if self.order == 'close':
                self.delete_order()

    def put_order(self):
        position = dict(
            side=self.side,
            price=self.params['price'],
            quantity=self.quantity,
            id=self.orders['new_order']['orderId'],
            positionSide=self.orders['new_order']['positionSide'],
            levels=dict(
                stop=dict(
                    id=self.orders['stop_order']['orderId'],
                    price=self.orders['stop_order']['stopPrice']
                ),
                take=dict(
                    id=self.orders['take_order']['orderId'],
                    price=self.orders['take_order']['stopPrice']
                )
            )
        )

        Thread(target=request, kwargs=dict(api='/positions',
               method='put', json=dict(pair=self.pair, position=position))).start()

    def delete_order(self):
        position_data = dict(
            pair=self.pair)

        Thread(target=request, kwargs=dict(api='/positions',
               method='delete', json=position_data)).start()
