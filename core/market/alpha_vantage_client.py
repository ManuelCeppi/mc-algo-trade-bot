import os
import requests

def __new__(cls):
    return super(cls).__new__(cls)

def __init__(self):
    self.__alpha_vantage_api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')

def get_stock_data(self, symbol, function, interval, time_period, series_type):
    # Get stock data from Alpha Vantage API
    url = self.build_url(function = function, symbol = symbol, interval = interval, time_period = time_period, series_type = series_type)
    url = 'https://www.alphavantage.co/query?function={function}&symbol={symbol}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.__alpha_vantage_api_key}'
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

