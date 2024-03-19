import os
import requests
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
class FinancialModelingClient:
    def __init__(self):
        self.__financial_modeling_api_key = os.environ.get('FINANCIAL_MODELING_API_KEY')

    def get_stock_data(self, function, symbol, interval, from_date, to_date, time_period, type):
        url = self.build_url(function, symbol, interval, from_date=from_date, to=to_date, period=time_period, type=type)
        # logger.info(f"FinancialModelingClient - Getting stock data from {url}")
        response = requests.get(url)
        return response.json()
    
    def build_url(self, function, symbol, interval, **kwargs):
        url = f'https://financialmodelingprep.com/api/v3/'
        if(interval):
            url += f'{function}/{interval}/{symbol}?'
        else:
            url += f'{function}/{symbol}?'

        for key, value in kwargs.items():
            if(value):
                if(key == 'from_date'):
                    key = 'from'
                url += f'{key}={value}&'
        url += f'apikey={self.__financial_modeling_api_key}'
        return url

