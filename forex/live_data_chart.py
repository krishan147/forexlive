import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import random
import plotly.graph_objs as go
from collections import deque
import time
import requests
import datetime
gbp_rate_list = []
gbp_timestamp_list = []
gbp_datetime_list = []

eur_timestamp_list = []
eur_rate_list = []
eur_datetime_list = []

kwd_timestamp_list = []
kwd_rate_list = []
kwd_datetime_list = []

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='graphone', animate=True),
        dcc.Interval(id='updateone',interval=1*3000),
    ]
)

@app.callback(Output('graphone', 'figure'),events=[Event('updateone', 'interval')])
def update_graph_scatter():

    traces = list()
    url = 'https://www.freeforexapi.com/api/live?pairs=USDGBP,USDEUR,USDKWD'
    request = requests.get(url)
    time.sleep(2)

    gbp_rate = request.json()['rates']["USDGBP"]["rate"]
    gbp_time = request.json()['rates']["USDGBP"]["timestamp"]
    gbp_rate_list.append(gbp_rate)
    gbp_timestamp_list.append(gbp_time)

    eur_rate = request.json()['rates']["USDEUR"]["rate"]
    eur_time = request.json()['rates']["USDEUR"]["timestamp"]
    eur_rate_list.append(eur_rate)
    eur_timestamp_list.append(eur_time)

    kwd_rate = request.json()['rates']["USDKWD"]["rate"]
    kwd_time = request.json()['rates']["USDKWD"]["timestamp"]
    kwd_rate_list.append(kwd_rate)
    kwd_timestamp_list.append(kwd_time)

    print(gbp_timestamp_list)
    print (gbp_rate_list)

    merged_rate_list = gbp_rate_list + eur_rate_list +kwd_rate_list


    traces.append(plotly.graph_objs.Scatter(
            x=gbp_timestamp_list,
            y=gbp_rate_list,
            mode= 'lines+markers'
            ))

    traces.append(plotly.graph_objs.Scatter(
            x=eur_timestamp_list,
            y=eur_rate_list,
            mode= 'lines+markers'
            ))

    traces.append(plotly.graph_objs.Scatter(
            x=kwd_timestamp_list,
            y=kwd_rate_list,
            mode= 'lines+markers'
            ))

   # return {'data': traces}


    return {'data': traces,'layout' : go.Layout(xaxis=dict(range=[min(gbp_timestamp_list),max(gbp_timestamp_list)]),
                                                yaxis=dict(range=[min(merged_rate_list),max(merged_rate_list)]),)}


if __name__ == '__main__':
    app.run_server(debug=True)