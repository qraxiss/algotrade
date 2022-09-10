from data.access import get_default

from dash import html, dcc



start_button = html.Button('Start', id='start',
                           n_clicks=0, className='btn btn-success')
stop_button = html.Button('Stop', id='stop',
                          n_clicks=0, className='btn btn-danger button')

button_output = html.Div(id='button_output')
poisitons_output = html.Div(id='positions_output', className="table")
balance_output = html.Div(id='balance_output', className="table")
chart_output = html.Div(id='chart_output')

coinlist=get_default()['sockets']

chart_dropdown = dcc.Dropdown(["BTCUSDT", "ETHUSDT", "ENJUSDT", "DOGEUSDT"],
                              id="chart_dropdown")

layout = html.Div([

    dcc.Interval(id='interval-component',
                 interval=1*500,  # in milliseconds (10sec)
                 n_intervals=0
                 ),


    # start_button, stop_button,
    # button_output,

    # poisitons_output,

    # balance_output,

    chart_dropdown,
    chart_output

],

    className="col text-center header-center")
