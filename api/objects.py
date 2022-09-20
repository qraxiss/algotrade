from logic import OrderManagement, Strategy, cancel_levels
from data.access import set_config
from helpers import err_return
from api.base import BaseApi
import asyncio


class Klines(BaseApi):
    def get(self, pair):
        try:
            self.json['data'] = self.resources.klines[pair][-self.data['limit']:]
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False
        return self.json

    def post(self, pair):
        try:
            self.resources.klines[pair] = self.data
            self.resources.strategy[pair] = Strategy(
                values=self.resources.values, pair=pair, config=self.resources.config)
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json

    def delete(self, pair):
        try:
            del self.resources.klines[pair]
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json

    def put(self, pair):
        try:
            if self.data['closed']:
                del self.resources.klines[pair][0]
                self.resources.klines[pair].append(self.data['kline'])
                self.resources.strategy[pair].signal(
                    self.resources.klines[pair])
            else:
                self.resources.klines[pair][-1] = self.data['kline']

            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json


class Config(BaseApi):
    def get(self):
        try:
            self.json['data'] = self.resources.config
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json

    def put(self):
        try:
            path = ""
            value = self.data['value']

            for key in self.data['keys']:
                path += f'["{key}"]'

            exec(f'self.resources.my_config{path}={value}')
            set_config(self.resources.config)

            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json


class Positions(BaseApi):
    def get(self):
        try:
            self.json['data'] = self.resources.positions
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json

    def put(self):
        try:
            self.resources.positions[self.data['pair']] = self.data['position']
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json

    def delete(self):
        try:
            cancel_levels(self.resources.client,
                          self.data['pair'], self.resources.positions)
            del self.resources.positions[self.data['pair']]
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json


class Balance(BaseApi):
    def get(self):
        try:
            self.json['data'] = self.resources.balance
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json

    def put(self):
        try:
            self.resources.balance['total'] = self.data['total']
            self.resources.balance['available'] = self.data['available']
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json


class Default(BaseApi):
    def get(self):
        try:
            self.json['data'] = self.resources.default[self.data['key']]
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json


class Order(BaseApi):
    def post(self):
        order = OrderManagement(params=self.data, resources=self.resources)


class WebsocketManage(BaseApi):
    def post(self):
        try:
            self.resources.websocket.kline_thread(socket=self.data['pair'])
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json

    def delete(self):
        try:
            self.resources.websocket.kline_close(self.data['pair'])
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json


class UserSocketManage(BaseApi):
    def post(self):
        try:
            self.resources.websocket.user_thread(
                account=self.resources.default['account'])
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json

    def delete(self):
        try:
            self.resources.websocket.user_close()
            self.json['outcome'] = True
        except Exception as err:
            self.json['err'] = err_return(str(type(err)))
            self.json['outcome'] = False

        return self.json


class StrategyApi(BaseApi):
    pass
