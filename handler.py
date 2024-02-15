import logging
import core.trade.trade as trading
import core.market.market_data as market_data
import core.user.user as user
import core.market.market_utility as market_utility
from alpaca.trading.enums import OrderSide

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def algo_trade_start_function(event, context):
    # Create clients
    data_client = market_data.MarketDataClient()
    trading_client = trading.TradeClient()
    user_client = user.User()
    logger.info("Algo trade bot - Start function")
    # Get open positions from alpaca user
    open_positions = user_client.get_open_positions()
    # Looping positions and check if they are closable (stop loss or take profit)
    if(open_positions):
        logger.info("Algo trade bot - Checking open positions")
        for position in open_positions:
            to_close = market_utility.check_stop_loss_and_take_profit(position)
            if(to_close):
                trading_client.close_trade(position)
        return # TODO For now not opening new positions if there are open positions
    
    logger.info("Algo trade bot - No open positions")
    # Get stocks with higher volumes
    higher_volumes_stocks = market_data.get_stocks_with_higher_volumes()
    # Looping found stocks
    for stock in higher_volumes_stocks:
        # Apply buying strategy
        position_has_been_opened = algo_trade_long_strategy_function(stock, trading_client, data_client)
        if(position_has_been_opened):
            continue
        else:
            position_has_been_opened = algo_trade_short_strategy_function(stock, trading_client, data_client)
    # Check if there are open positions: if there are, the selling flow will start;
    # Otherwise, the buying flow will start
    logger.info("Algo trade bot - End function")

def algo_trade_long_strategy_function(stock, trading_client, data_client):
    position_has_been_opened = False
    # Applying rsi strategy + price candle + volume for long positions
    stock_rsi_data = data_client.get_stock_rsi_data(stock)
    is_neutral_from_oversold = market_utility.check_if_stock_is_neutral_from_oversold(stock_rsi_data)
    # First condition - RSI
    if(is_neutral_from_oversold):
        # Second condition - Price candle
        stock_price_candle_data = data_client.get_stock_price_candle_data(stock)
        is_bullish_candle = market_utility.check_if_stock_is_bullish_candle(stock_price_candle_data)
        if(is_bullish_candle):
            # Third condition - Volume
            higher_volumes = market_utility.check_if_stock_volume_is_higher_than_previous_candle(stock_price_candle_data)
            if(higher_volumes):
                # Open long position
                trading_client.open_trade(stock, OrderSide.BUY.value, 1)
                position_has_been_opened = True
    return position_has_been_opened

def algo_trade_short_strategy_function(stock, trading_client, data_client):
    position_has_been_opened = False
    # Applying rsi strategy + price candle + volume for short positions
    stock_rsi_data = data_client.get_stock_rsi_data(stock)
    is_neutral_from_overbought = market_utility.check_if_stock_is_neutral_from_overbought(stock_rsi_data)
    # First condition - RSI
    if(is_neutral_from_overbought):
        # Second condition - Price candle
        stock_price_candle_data = data_client.get_stock_price_candle_data(stock)
        is_bearish_candle = market_utility.check_if_stock_is_bearish_candle(stock_price_candle_data)
        if(is_bearish_candle):
            # Third condition - Volume
            higher_volumes = market_utility.check_if_stock_volume_is_higher_than_previous_candle(stock_price_candle_data)
            if(higher_volumes):
                # Open short position
                trading_client.open_trade(stock, OrderSide.SELL.value, 1)
                position_has_been_opened = True
    return position_has_been_opened

# To test locally, uncomment the following line
algo_trade_start_function("event", type('',(object,),{"function_name":"test"})()) 
