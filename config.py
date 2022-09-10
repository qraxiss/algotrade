import asyncio
from flask import Flask
from os import environ, path
from dotenv import load_dotenv
from binance.client import Client
from binance import ThreadedWebsocketManager
from data.access import get_config, get_default

BASE_DIR = path.abspath(path.dirname(__file__))
load_dotenv(path.join(BASE_DIR, ".env"))


"""Flask Config"""


class Config:
    """Flask configuration variables."""

    # General Config
    FLASK_APP = "wsgi.py"
    FLASK_ENV = environ.get("FLASK_ENV")
    SECRET_KEY = environ.get("SECRET_KEY")

    # Assets
    LESS_BIN = environ.get("LESS_BIN")
    ASSETS_DEBUG = environ.get("ASSETS_DEBUG")
    LESS_RUN_IN_DEBUG = environ.get("LESS_RUN_IN_DEBUG")

    # Static Assets
    STATIC_FOLDER = "templates"
    TEMPLATES_FOLDER = "static"
    COMPRESSOR_DEBUG = environ.get("COMPRESSOR_DEBUG")



"""Modified Flask Object"""
class MyFlask(Flask):
    my_config = get_config()

    account_data = dict(
        positions=dict(
            symbol=dict(
                side="SELL",
                volume=2,
                quantity=5
            ),
            btcusdt=dict(
                side="BUY",
                volume=2,
                quantity=5
            ),
            ethusdt=dict(
                side="BUY",
                volume=2,
                quantity=5
            )
        ),
        balance=dict(
            total=35,
            available=167
        )
    )
    klines = dict(
        symbol=None
    )
    step_info = None

    default = get_default()

    client = Client(**default['account'])

    websocket = None
