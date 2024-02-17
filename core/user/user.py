import os
from alpaca.trading.client import TradingClient

class User:
    def __init__(self):
        self.__trading_client = TradingClient(
            os.environ.get('ALPACA_API_KEY'),
            os.environ.get('ALPACA_SECRET_KEY')
        )

    # Get open positions from alpaca API
    def get_open_positions(self):
        return self.__trading_client.get_all_positions()