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

symbol_dropdown = dcc.Dropdown(coinlist, id="symbol_dropdown")
interval_dropdown = dcc.Dropdown(["1m", "3m", "5m", "15m"], id="interval_dropdown")

dropdowns = html.Div([symbol_dropdown, interval_dropdown], className="dropdowns")

layout = html.Div([

    dcc.Interval(id='interval-component',
                 interval=1000,  # in milliseconds (5 seconds)
                 n_intervals=0
                 ),
    dropdowns,
    chart_output
],

    className="col text-center header-center")
