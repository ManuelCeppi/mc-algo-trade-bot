import os
from alpaca.trading import TradingClient
from alpaca.trading.requests import  OrderRequest
from alpaca.trading.requests import MarketOrderRequest

class TradeClient:
    def __init__(self):
        self.__trading_client = TradingClient(
            os.environ.get('ALPACA_API_KEY'),
            os.environ.get('ALPACA_SECRET_KEY'),
            paper=True
        )

    def open_trade(self, stock, qty, side, type='market', time_in_force='day'):
        order = MarketOrderRequest(
            symbol=stock,
            qty=qty,
            side=side,
            time_in_force=time_in_force
        )

        return self.__trading_client.submit_order(order)
    
    def open_trade_notional(self, stock, notional, side, time_in_force='day'):
        order = MarketOrderRequest(
            symbol=stock,
            notional=notional,
            side=side,
            type=type,
            time_in_force=time_in_force
        )

        self.__trading_client.submit_order(order)
                                           
    def close_trade(self, position):
        self.__trading_client.close_position(position.symbol)

    def get_asset(self, symbol):
        return self.__trading_client.get_asset(symbol)
    
    def get_trade_account(self):
        return self.__trading_client.get_account()


