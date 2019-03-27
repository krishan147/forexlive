def data():
    import requests
    import time
    datetime_list = []
    rate_list = []

    currency_symbols = ['USDEUR','USDGBP','USDKWD']
    url = 'https://www.freeforexapi.com/api/live?pairs='
    while True:

        for symbol in currency_symbols:
            request = requests.get(url + symbol)
            time.sleep(2)
            rate =  request.json()['rates'][symbol]["rate"]
            timestamp =  request.json()['rates'][symbol]["timestamp"]
            datetime_list.append(timestamp)
            rate_list.append(rate)
         #   print (symbol, rate, timestamp)
            print (rate_list)
            print (datetime_list)

data()