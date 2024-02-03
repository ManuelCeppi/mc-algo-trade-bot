import datetime
import logging
import core.trade.trade as trading
import core.market.market_data as market_data
import core.user.user as user

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def algo_trade_start_function(event, context):
    # Create clients
    dataClient = market_data.MarketData()
    tradeClient = trading.Trade()
    userClient = user.User()

    current_time = datetime.datetime.now().time()
    name = context.function_name
    
    logger.info("Algo trade bot - Start function")
    # Get open positions from alpaca user
    logger.info("Algo trade bot - Getting stocks to trade")
    open_positions = user.get_open_positions()

    # Check if there are open positions: if there are, the selling flow will start;
    # Otherwise, the buying flow will start
    if open_positions:
        algo_trade_selling_strategy_function()
    else:
        algo_trade_buying_strategy_function()

    logger.info("Algo trade bot - End function")



def algo_trade_buying_strategy_function():
    pass

def algo_trade_selling_strategy_function(positions):
    # Looping through open positions
    for position in positions:
        # Check if the position is profitable, or if it has reached the stop loss
        is_profitable = position.unrealized_plpc > 0.04
        is_stop_loss = position.unrealized_plpc < -0.02
        if(is_profitable or is_stop_loss):
            # Close position
            trading.close_trade(position)
            continue
        # If the position is not profitable, or has not reached the stop loss, keep it open
        # TODO RSI strategy
    pass

def get_stocks_to_trade():
    #TODO get stocks from env variables
    return ['AAPL']

def get_stock_data(stocks_to_trade):
    market_data.get_stocks_data()
    return []

# To test locally, uncomment the following line
algo_trade_start_function("event", type('',(object,),{"function_name":"test"})()) 
