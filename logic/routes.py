from logic import (is_order_valid, new_order, close_order)
from flask import current_app as app, request
from data.access import get_config
from interface import MyFlask
from json import loads
import os

app: MyFlask


@app.route('/webhook', methods=['POST'])
def webhook():
    order_params = loads(request.data)
    order = is_order_valid(app.account_data, order_params)

    if order == 'NEW':
        new_order(app.client, order_params, get_config(),
                  app.account_data, app.step_info, app.default)

    elif order == 'CLOSE':
        close_order(app.client, order_params, app.account_data, app.default)


@app.route('/open_streams', methods=['POST'])
def open_streams():
    try:
        os.system('python3.10 logic/streams.py > log.txt &')
        return {'status': 'started'}
    except Exception as e:
        return {'status': f'{e}'}


@app.route('/close_streams', methods=['POST'])
def close_streams():
    try:
        os.system('pkill -f streams.py')
        return {'status': 'closed'}
    except Exception as e:
        return {'status': f'{e}'}
