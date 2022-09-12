from data.access import get_default

from dash import html, dcc


chart_output = html.Div(id='chart_output')

coinlist = get_default()['sockets']

coin_dict = dict()
for coin in coinlist:
    try:
        coin_dict[coin.split('@')[0].upper()] = None
    except:
        pass

coinlist = list(coin_dict)

symbol_dropdown = dcc.Dropdown(
    coinlist, id="symbol_dropdown", placeholder="SYMBOL")
interval_dropdown = dcc.Dropdown(
    ["1m", "3m", "5m", "15m"], id="interval_dropdown", placeholder="INTERVAL")

dropdowns = html.Div([symbol_dropdown, interval_dropdown],
                     className="dropdowns")

rsi = html.Div(
    [html.Div([html.Span(['RSI Parameters'],
                         className="input-group-text"),
                dcc.Input(id='rsi_l', placeholder='period', type='number', step="0.0001")],
              className="input-group-prepend")],
    className="input-group")

vwap = html.Div(
    [html.Div([html.Span(['VWAP Parameters'],
                         className="input-group-text"),
                dcc.Input(id='vwap_l', placeholder='period', type='number'),
                dcc.Input(id='vwap_short', placeholder='long sensivity', type='number', step="0.0001"),
                dcc.Input(id='vwap_long', placeholder='short sensivity', type='number', step="0.0001")],
              className="input-group-prepend")],
    className="input-group")

layout = html.Div([

    dcc.Interval(id='interval-component',
                 interval=1000,  # in milliseconds (1 seconds)
                 n_intervals=0
                 ),
    vwap,
    rsi,
    dropdowns,

    chart_output
],

    className="col text-center header-center")
