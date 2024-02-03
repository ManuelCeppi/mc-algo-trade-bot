import os
from alpaca.broker import BrokerClient

def __new__(cls):
    return super(cls).__new__(cls)

def __init__(self):
    self.__account_id = os.environ.get('ALPACA_ACCOUNT_ID')
    self.__broker_client = BrokerClient(
        os.environ.get('ALPACA_API_KEY'),
        os.environ.get('ALPACA_SECRET_KEY')
    )

# Get open positions from alpaca API
def get_open_positions(self):
    return self.__broker_client.get_all_positions_for_account(account_id=self.__account_id)