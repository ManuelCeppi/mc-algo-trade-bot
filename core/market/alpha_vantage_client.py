import os
import requests

class AlphaVantageClient:
    def __init__(self):
        self.__alpha_vantage_api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')

    def get_stock_data(self, symbol, function, interval, time_period, series_type):
        # Get stock data from Alpha Vantage API
        url = self.build_url(function = function, symbol = symbol, interval = interval, time_period = time_period, series_type = series_type)
        r = requests.get(url)
        data = r.json()
        return data

    def build_url(self, **kwargs):
        url = 'https://www.alphavantage.co/query?'
        for key, value in kwargs.items():
            if(value):
                url += f'{key}={value}&'
        url += f'apikey={self.__alpha_vantage_api_key}'
        return url

