import os
from alpaca.data.historical import StockHistoricalDataClient
from alpaca.data.requests import StockBarsRequest

def __new__(cls):
    return super(cls).__new__(cls)

def __init__(self):
    self.__alpaca_client = StockHistoricalDataClient(
        os.environ.get('ALPACA_API_KEY'),
        os.environ.get('ALPACA_SECRET_KEY')
    )

def get_stocks_data(stocks):
    stocks_data = []
    for stock in stocks:
        stocks_data.append(get_stock_data(stock))
    return stocks_data

def get_stock_data(stock):
    #Get stock data from Alpaca API
    return []

# no keys required

# single symbol request

latest_quote = client.get_crypto_latest_quote(request_params)

# must use symbol to access even though it is single symbol
latest_quote["ETH/USD"].ask_price
