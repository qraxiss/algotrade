from interface.views.dashboard.figures import create_chart
from interface.controllers import is_plot
from dash import Input, Output, dcc

url = 'http://127.0.0.1:5000/api'


def init_callbacks(dash_app):
    @dash_app.callback(
        Output('chart_output', 'children'),
        Input('interval-component', 'n_intervals'),
        Input('symbol_dropdown', 'value'),
        Input('interval_dropdown', 'value')
    )
    def chart(n, symbol, interval):
        data = is_plot(symbol, interval)
        if not not data:
            fig = create_chart(symbol, interval, data)
            return dcc.Graph(id="graph", figure=fig)
        else:
            return None
    return dash_app
