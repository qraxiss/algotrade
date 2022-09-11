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


url = 'http://127.0.0.1:8000/api'


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
        Input('symbol_dropdown', 'value'),
        Input('interval_dropdown', 'value')
    )
    def chart(n, symbol, interval):
        if symbol != None and interval != None:
            socket = symbol.lower() + '@kline_' + interval

            data = loads(
                post(url+'/get/klines', json=dict(symbol=socket)).text)
            if data != None:
                df = pd.DataFrame(data)
                df[[0,1,2,3,4,5]] = df[[0,1,2,3,4,5]].astype('float')
                df[0] = pd.to_datetime(df[0], unit='ms')
                df.index = df[0]

                set1 = {
                    'x': df[0],
                    'open': df[1],
                    'high': df[2],
                    'low': df[3],
                    'close': df[4],
                    'type': 'candlestick',
                    'name': 'candlestick'
                }

                set2 = {
                    'x': df[0],
                    'y': ta.vwap(high=df[2], low=df[3], close=df[4], volume=df[5], length=6),
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
                    x=df[0], y=ta.rsi(df[2], 7)), row=2, col=1)
                fig.update_layout(height=800, title_text=symbol + " " + interval,
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
