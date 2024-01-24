import datetime
import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def algo_trade_start_function(event, context):
    current_time = datetime.datetime.now().time()
    name = context.function_name
    # Test purpose print
    print("Your cron function " + name + " ran at " + str(current_time))
    logger.info("Algo trade bot - Start function")
    # TODO Choose stocks to trade (env variables?)
    logger.info("lambda function is running")

def get_stocks_to_trade():
    return [];

# To test locally, uncomment the following line
algo_trade_start_function("event", type('',(object,),{"function_name":"test"})()) 
