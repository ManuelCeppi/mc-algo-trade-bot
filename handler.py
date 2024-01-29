import datetime
import logging
import core.trade.trade as trading
import core.market.market_data as market_data

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def algo_trade_start_function(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    # Test purpose print
    # print("Your cron function " + name + " ran at " + str(current_time))
    logger.info("Algo trade bot - Start function")
    # TODO Choose stocks to trade (env variables?) Start with AAPL just for testing

    logger.info("Getting stocks to trade")
    stocks_to_trade = get_stocks_to_trade();
    logger.info("Trading " + str(stocks_to_trade) + " stocks")

    logger.info("Getting stock data")
    stock_info = get_stock_data(stocks_to_trade);

def get_stocks_to_trade():
    #TODO get stocks from env variables
    return ['AAPL']

def get_stock_data(stocks_to_trade):
    market_data.get_stocks_data()
    return []

# To test locally, uncomment the following line
algo_trade_start_function("event", type('',(object,),{"function_name":"test"})()) 
