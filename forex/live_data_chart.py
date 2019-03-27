import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
from random import random
import plotly
datetime_list = []
rate_list = []

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-graph-scatter', animate=True),
        dcc.Interval(
            id='interval-component',
            interval=1*1000
        )
    ])
)

@app.callback(Output('live-update-graph-scatter', 'figure'),
              events=[Event('interval-component', 'interval')])
def update_graph_scatter():

    import requests
    import time
    traces = list()

    currency_symbols = ['USDEUR','USDGBP','USDKWD']
    url = 'https://www.freeforexapi.com/api/live?pairs='
    #while True:

    for symbol in currency_symbols:
        request = requests.get(url + symbol)
        time.sleep(2)
        rate =  request.json()['rates'][symbol]["rate"]
        timestamp =  request.json()['rates'][symbol]["timestamp"]
        datetime_list.append(timestamp)
        rate_list.append(rate)
        print (rate_list)
        print (datetime_list)

        traces.append(plotly.graph_objs.Scatter(
            x=datetime_list,
            y=rate_list,
            mode= 'lines+markers'
            ))

    return {'data': traces}

if __name__ == '__main__':
    app.run_server(debug=True)