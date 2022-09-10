from unicodedata import name
from interface.controllers import position_formatter
from plotly.subplots import make_subplots
from dash import Input, Output, ctx, dcc
from .figures import create_data_table
import plotly.graph_objects as go
import plotly.express as px
from requests import post
from json import loads
import pandas as pd
import pandas_ta as ta


url = 'http://127.0.0.1:5000/api'


def init_callbacks(dash_app):
    @dash_app.callback(
        Output('positions_output', 'children'),
        Input('interval-component', 'n_intervals')
    )
    def position(interval):
        pass

    @dash_app.callback(
        Output('balance_output', 'children'),
        Input('interval-component', 'n_intervals')
    )
    def balance(interval):
        pass

    @dash_app.callback(
        Output('chart_output', 'children'),
        Input('interval-component', 'n_intervals'),
        Input('chart_dropdown', 'value')
    )
    def chart(interval, symbol):
        if symbol != None:
            data = loads(
                post(url+'/get/klines', json=dict(symbol=symbol)).text)
            if data != None:
                df = pd.DataFrame(data)
                df.start = pd.to_datetime(df['start'], unit='ms')
                df[['open', 'close', 'high', 'low', 'volume']] = df[[
                    'open', 'close', 'high', 'low', 'volume']].astype('float')
                df.index = df.start

                set1 = {
                    'x': df.start,
                    'open': df.open,
                    'close': df.close,
                    'high': df.high,
                    'low': df.low,
                    'type': 'candlestick',
                    'name': 'candlestick'
                }

                set2 = {
                    'x': df.start,
                    'y': ta.vwap(high=df.high, low=df.low, close=df.close, volume=df.volume, length=6),
                    'type': 'scatter',
                    'mode': 'lines',
                    'line': {
                        'width': 1,
                        'color': 'blue'
                    },
                    'name': 'VWAP'
                }

                data = [set1, set2]

                layout = go.Layout({
                    'title': {
                        'text': symbol,
                        'font': {
                            'size': 25
                        }
                    }
                })

                fig = go.Figure(data=data, layout=layout).set_subplots(
                    2, 1, row_heights=[0.7, 0.3])
                fig.add_trace(go.Scatter(
                    x=df.start, y=ta.rsi(df.close)), row=2, col=1)
                fig.update_layout(height=800, title_text=symbol,
                                  xaxis_rangeslider_visible='slider' in [])

                return dcc.Graph(
                    id='graph',
                    figure=fig,
                )
            else:
                return None
        else:
            return None
    return dash_app
