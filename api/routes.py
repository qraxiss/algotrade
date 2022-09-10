from flask import current_app as app, request
from data.access import set_config
from json import loads, dumps
from config import MyFlask
import pandas as pd

app: MyFlask

@app.route('/api/get/config', methods=["POST"])
def get_config_api():
    return dumps(app.my_config)


@app.route('/api/get/config', methods=["POST"])
def set_config_api():
    """
    request.data = {
        "leverage":3,
        "max_position":6
        .
        .
        .
    }
    """

    data = loads(request.data)
    app.my_config = data
    set_config(data)

    return request.data


@app.route('/api/get/klines', methods=["POST"])
def get_klines():
    """
    request.data = {
        "symbol":"BTCUSDT"
    }
    """
    data = loads(request.data)
    try:
        return app.klines[data['symbol']].to_json()
    except KeyError:
        return dumps(None)


@app.route('/api/set/klines', methods=["POST"])
def set_klines():
    """
    request.data = {
        "symbol":"BTCUSDT",
        "klines":klines_json
    }
    """

    data = loads(request.data)

    app.klines[data['symbol']] = pd.DataFrame(loads(data['klines']))

    return dumps(data['klines'])


@app.route('/api/get/account', methods=["POST"])
def get_account_data():
    """
    request.data = {
        "type":"positions"
    }
    """
    data = loads(request.data)
    if data['type'] == 'all':
        return dumps(app.account_data)

    return dumps(app.account_data[data['type']])


@app.route('/api/set/account', methods=["POST"])
def set_account_data():
    """
    request.data = {
        "type":"positions",
        "data":data
    }
    """
    data = loads(request.data)

    if data['type'] == 'all':
        app.account_data = data['data']
        return dumps(data['data'])
    app.account_data[data['tpye']] = data['data']
    return request.data


@app.route('/api/get/default', methods=["POST"])
def get_default_data():
    """
    request.data = {
        "type":"sockets"
    }
    """
    data = loads(request.data)
    return dumps(app.default[data['type']])
