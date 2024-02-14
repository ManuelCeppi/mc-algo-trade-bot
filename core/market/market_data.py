import os
import alpha_vantage_client
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.historical.screener import ScreenerClient
from alpaca.data.requests import MostActivesRequest

def __new__(cls):
    return super(cls).__new__(cls)

def __init__(self):
    self.__alpaca_screener_client = ScreenerClient(
        os.environ.get('ALPACA_API_KEY'),
        os.environ.get('ALPACA_SECRET_KEY')
    )
    self.__alpha_vantage_client = alpha_vantage_client.AlphaVantageClient() 
    self.__alpaca_client = StockHistoricalDataClient(
        os.environ.get('ALPACA_API_KEY'),
        os.environ.get('ALPACA_SECRET_KEY')
    )

def get_stocks_rsi_data(symbols):
    stocks_data = []
    for symbol in symbols:
        stocks_data.append(get_stock_rsi_data(symbol=symbol))
    return stocks_data

def get_stock_rsi_data(self, symbol, interval='15min', time_period=10, series_type='open'):
    return self.__alpha_vantage_client.get_stock_data(symbol, 'RSI', interval, time_period, series_type)

def get_stock_price_candle_data(self, symbol, interval='60min'):
    return self.__alpha_vantage_client.get_stock_data(symbol, 'TIME_SERIES_INTRADAY', interval)

def get_stocks_with_higher_volumes(self):
    return self.__alpaca_screener_client.get_most_actives(MostActivesRequest()).most_actives
