import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
from random import random
import plotly
datetime_list = []
eur_rate_list = []
gbp_rate_list = []
kwd_rate_list = []

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div([
        dcc.Graph(id='live-update-graph-scatter', animate=True),
        dcc.Interval(
            id='interval-component',
            interval=1*8000
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

        if symbol == 'USDEUR':
            eur_rate_list.append(rate)
        if symbol == 'USDZAR':
            gbp_rate_list.append(rate)
        if symbol == 'USDAUD':
            kwd_rate_list.append(rate)

        print (eur_rate_list)
        print (gbp_rate_list)
        print (kwd_rate_list)

        traces.append(plotly.graph_objs.Scatter(
            x = datetime_list,
            y = eur_rate_list,
            mode='lines+markers'
        ))

        traces.append(plotly.graph_objs.Scatter(
            x = datetime_list,
            y = gbp_rate_list,
            mode='lines+markers'
        ))

        traces.append(plotly.graph_objs.Scatter(
            x = datetime_list,
            y = kwd_rate_list,
            mode='lines+markers'
        ))

        return {'data': traces}

if __name__ == '__main__':
    app.run_server(debug=True)

# x = datetime_list,
# y = eur_rate_list,