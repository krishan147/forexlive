import dash
from dash.dependencies import Output, Event
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from collections import deque
import time
import requests
import datetime
gbp_timestamp_list = []
gbp_rate_list = []
eur_timestamp_list = []
eur_rate_list = []

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='graphhone', animate=True),
        dcc.Interval(id='updateone', interval=1*3000),
        # dcc.Graph(id='graphtwo', animate=True),
        # dcc.Interval(id='updatetwo',interval=1*3000),
    ]
)

@app.callback(Output('graphhone', 'figure'),events=[Event('updateone', 'interval')])
def update_graph_scatter():
    currency_symbols = ['USDGBP']
    url = 'https://www.freeforexapi.com/api/live?pairs='

    for symbol in currency_symbols:
        request = requests.get(url + symbol)
        time.sleep(2)
        rate =  request.json()['rates'][symbol]["rate"]
        timestamp =  request.json()['rates'][symbol]["timestamp"]
        gbp_timestamp_list.append(timestamp)
        gbp_rate_list.append(rate)
        str_gbp_timestamp_list = [str(i) for i in gbp_timestamp_list]
        cut_gbp_timestamp_list = [w[:-3] for w in str_gbp_timestamp_list]
        gbp_datetime_list = [datetime.datetime.fromtimestamp(int(x)).strftime("%x %X") for x in cut_gbp_timestamp_list]

    data = plotly.graph_objs.Scatter(
            x=gbp_datetime_list,
            y=gbp_rate_list,
            name='Scatter',
            mode= 'lines+markers'
            )

    return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(gbp_datetime_list),max(gbp_datetime_list)]),yaxis=dict(range=[min(gbp_rate_list),max(gbp_rate_list)]),)}

# @app.callback(Output('graphtwo', 'figure'),events=[Event('updatetwo', 'interval')])
# def update_graph_scatter2():
#     currency_symbols = ['USDEUR']
#     url = 'https://www.freeforexapi.com/api/live?pairs='
#
#     for symbol in currency_symbols:
#         request = requests.get(url + symbol)
#         time.sleep(2)
#         rate =  request.json()['rates'][symbol]["rate"]
#         timestamp =  request.json()['rates'][symbol]["timestamp"]
#         eur_timestamp_list.append(timestamp)
#         eur_rate_list.append(rate)
#         str_eur_timestamp_list = [str(i) for i in eur_timestamp_list]
#         cut_eur_timestamp_list = [w[:-3] for w in str_eur_timestamp_list]
#         eur_datetime_list = [datetime.datetime.fromtimestamp(int(x)).strftime("%x %X") for x in cut_eur_timestamp_list]
#
#     data = plotly.graph_objs.Scatter(
#             x=eur_datetime_list,
#             y=eur_rate_list,
#             name='Scatter',
#             mode= 'lines+markers'
#             )
#
#     return {'data': [data],'layout' : go.Layout(xaxis=dict(range=[min(eur_datetime_list),max(eur_datetime_list)]),yaxis=dict(range=[min(eur_rate_list),max(eur_rate_list)]),)}

if __name__ == '__main__':
    app.run_server(debug=True)