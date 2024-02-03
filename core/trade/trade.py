import os
from alpaca.trading import TradingClient

def __new__(cls):
    return super(cls).__new__(cls)

def __init__(self):
    self.__trading_client = TradingClient(
        os.environ.get('ALPACA_API_KEY'),
        os.environ.get('ALPACA_SECRET_KEY')
    )

def open_trade():
    print("Open trade")

def close_trade(self, position):
    self.__trading_client.close_position(position.symbol, qty=position.qty)


