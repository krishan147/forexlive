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
gbp_divide_rate_list = []
gbp_timestamp_list = []
gbp_datetime_list = []

eur_timestamp_list = []
eur_rate_list = []
eur_datetime_list = []

kwd_timestamp_list = []
kwd_rate_list = []
kwd_datetime_list = []

perm_symbols_check_list = []
temp_symbols_check_list = []

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        dcc.Graph(id='graphone', animate=True),
        dcc.Interval(id='updateone',interval=1*3000),
    ]
)

@app.callback(Output('graphone', 'figure'),events=[Event('updateone', 'interval')])
def update_graph_scatter():
    start_graph = 0
    traces = list()

    symbols = ["USDGBP","USDEUR","USDKWD"]

    url = 'https://www.freeforexapi.com/api/live?pairs=USDGBP,USDEUR,USDKWD'
    request = requests.get(url)
    gbp_rate = request.json()['rates'][symbol]["rate"]
    gbp_time = request.json()['rates'][symbol]["timestamp"]

    if perm_symbols_check_list != []:
        for symbol in symbols:
            gbp_rate = request.json()['rates'][symbol]["rate"]
            temp_symbols_check_list.append(gbp_rate)

        if str(perm_symbols_check_list) == str(temp_symbols_check_list):
            start_graph = 0
        if str(perm_symbols_check_list) != str(temp_symbols_check_list):
            start_graph = 1

    if perm_symbols_check_list == []:
        for symbol in symbols:
            gbp_rate = request.json()['rates'][symbol]["rate"]
            perm_symbols_check_list.append(gbp_rate)
            start_graph = 1

    if start_graph == 1:
        if (gbp_rate_list == []) or (gbp_rate != gbp_rate_list[-1]):
            gbp_rate_list.append(gbp_rate)
            gbp_divide_rate_list.append((gbp_rate))
            gbp_timestamp_list.append(gbp_time)
            if len(gbp_rate_list) > 1:

# krishan need to figure out how to create averages and then get hem to come up in 3 different lists? not sure....

                temp_gbp_rate_list = gbp_rate_list[1:]
                temp_gbp_divide_rate_list = gbp_divide_rate_list[:-1]
                cut_gbp_timestamp_list = gbp_timestamp_list[1:]
                gbp_rate_diff = [c / t for c, t in zip(temp_gbp_divide_rate_list, temp_gbp_rate_list)]

                # eur_rate = request.json()['rates']["USDEUR"]["rate"]
                # eur_time = request.json()['rates']["USDEUR"]["timestamp"]
                # eur_rate_list.append(eur_rate)
                # eur_timestamp_list.append(eur_time)
                #
                # kwd_rate = request.json()['rates']["USDKWD"]["rate"]
                # kwd_time = request.json()['rates']["USDKWD"]["timestamp"]
                # kwd_rate_list.append(kwd_rate)
                # kwd_timestamp_list.append(kwd_time)

                print (cut_gbp_timestamp_list)
                print (gbp_rate_diff)

              #  merged_rate_list = gbp_rate_list + eur_rate_list +kwd_rate_list




                traces.append(plotly.graph_objs.Scatter(
                        x=cut_gbp_timestamp_list,
                        y=gbp_rate_diff,
                        mode= 'lines+markers'
                        ))

                # traces.append(plotly.graph_objs.Scatter(
                #         x=eur_timestamp_list,
                #         y=eur_rate_list,
                #         mode= 'lines+markers'
                #         ))
                #
                # traces.append(plotly.graph_objs.Scatter(
                #         x=kwd_timestamp_list,
                #         y=kwd_rate_list,
                #         mode= 'lines+markers'
                #         ))

                return {'data': traces,'layout' : go.Layout(xaxis=dict(range=[min(cut_gbp_timestamp_list),max(cut_gbp_timestamp_list)]),
                                                            yaxis=dict(range=[min(gbp_rate_diff),max(gbp_rate_diff)]),)}

            else:
                pass

        if gbp_rate == gbp_rate_list[-1]:
            pass

    if start_graph != 0:
        pass

if __name__ == '__main__':
    app.run_server(debug=True)