import os
from . import financial_modeling_client
from alpaca.data.historical.screener import ScreenerClient
from alpaca.data.requests import MostActivesRequest
from datetime import datetime, timezone

class MarketDataClient:
    def __init__(self):
        self.__alpaca_screener_client = ScreenerClient(
            os.environ.get('ALPACA_API_KEY'),
            os.environ.get('ALPACA_SECRET_KEY')
        )
        self.__financial_modeling_client = financial_modeling_client.FinancialModelingClient() 
    
    def get_stocks_rsi_data(self, symbols):
        stocks_data = []
        for symbol in symbols:
            stocks_data.append(self.get_stock_rsi_data(symbol=symbol))
        return stocks_data

    def get_stock_rsi_data(self, symbol):
        return self.__financial_modeling_client.get_stock_data('technical_indicator', symbol, '15min', time_period=10, type='rsi')
    
    def get_stock_otc_quote(self, symbol):
        return self.__financial_modeling_client.get_stock_data('otc/real-time-price', symbol, '1min', None, None)
    
    def get_stock_intraday_data(self, symbol, interval='1hour'):
        return self.__financial_modeling_client.get_stock_data('historical-chart', symbol, interval, datetime.today(), datetime.today(), None, None)

    def get_stocks_with_higher_volumes(self):
        return self.__alpaca_screener_client.get_most_actives(MostActivesRequest(top=15)).most_actives
