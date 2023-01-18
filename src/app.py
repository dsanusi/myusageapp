import qrcode
from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import psutil
import pandas as pd
from datetime import datetime
import os

app = Dash(__name__)
server = app.server
df = pd.DataFrame(columns=['time', 'CPU', 'RAM'])

app.layout = html.Div([
    html.H4('usage analysis'),
    dcc.Graph(id="time-series-chart"),
    html.P("Select metric:"),
    dcc.Dropdown(
        id="ticker",
        options=[{"label": "CPU", "value": "CPU"}, {"label": "RAM", "value": "RAM"}],
        value="CPU",
        clearable=False,
    ),
    dcc.Interval(id='interval-component', interval=1*1000, n_intervals=0)
])

@app.callback(
    Output("time-series-chart", "figure"),
    Input("interval-component", "n_intervals"),
    Input("ticker", "value"))
def update_data(n_interval, ticker):
    global df
    df = df.append({'time':str(datetime.now()), 'CPU':psutil.cpu_percent(), 'RAM':psutil.virtual_memory().percent}, ignore_index=True)
    return px.line(df, x='time', y=ticker)


app.run_server(debug=True)
