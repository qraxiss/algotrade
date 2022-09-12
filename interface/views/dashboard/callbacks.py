from interface.views.dashboard.figures import create_chart
from interface.controllers import is_plot
from dash import Input, Output, dcc

url = 'http://127.0.0.1:80/api'


def init_callbacks(dash_app):
    @dash_app.callback(
        Output('chart_output', 'children'),

        Input('interval-component', 'n_intervals'),
        Input('interval_dropdown', 'value'),
        Input('symbol_dropdown', 'value'),
        Input('vwap_short', 'value'),
        Input('vwap_long', 'value'),
        Input('vwap_l', 'value'),
        Input('rsi_l', 'value'),
        
    )
    def chart(n, interval, symbol, vwap_short, vwap_long, vwap_l, rsi_l):
        data = is_plot(symbol, interval)
        if not not data:
            fig = create_chart(symbol, interval, data, vwap_short, vwap_long, rsi_l, vwap_l)
            return dcc.Graph(id="graph", figure=fig)
        else:
            return None
    return dash_app
