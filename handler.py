import operator
import os
import logging
import core.trade.trade as trading
import core.market.market_data as market_data
import core.user.user as user
import core.market.market_utility as market_utility
from alpaca.trading.enums import OrderSide

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

__data_client = market_data.MarketDataClient()
__trading_client = trading.TradeClient()
__user_client = user.User()

def algo_trade_start_function(event, context):
    logger.info("Algo trade bot - Start function")
    # Get open positions from alpaca user
    open_positions = __user_client.get_open_positions()
    # Looping positions and check if they are closable (stop loss or take profit)
    if(open_positions):
        logger.info("Algo trade bot - Checking open positions")
        for position in open_positions:
            to_close = market_utility.check_stop_loss_and_take_profit(position)
            if(to_close):
                logger.info(f"Algo trade bot - Closing position {position.symbol}")
                __trading_client.close_trade(position)
    
    # Get stocks with higher volumes
    higher_volumes_stocks = __data_client.get_stocks_with_higher_volumes()
    logger.info(f"Algo trade bot - Found {higher_volumes_stocks} stocks with higher volumes")
    
    # Looping found stocks
    for stock in higher_volumes_stocks:
        asset = __trading_client.get_asset(stock.symbol)
        if(asset.tradable == False):
            logger.info(f"Algo trade bot - Stock {stock.symbol} is not tradable")
            continue
        found = False
        for p in open_positions:
            if(operator.eq(p.symbol, stock.symbol)):
                logger.info(f"Algo trade bot - Stock {stock.symbol} is already in open positions")
                found = True
                break
        if(found):
            continue
        # Apply buying strategy
        position_has_been_opened = algo_trade_long_strategy_function(stock)
        if(position_has_been_opened):
            logger.info(f"Algo trade bot - Opened long position for {stock.symbol}")
            continue
        else:
            # Get asset to check if its shortable
            if(asset.shortable):
                position_has_been_opened = algo_trade_short_strategy_function(stock)
                if(position_has_been_opened):
                    logger.info(f"Algo trade bot - Opened short position for {stock.symbol}")
    # Check if there are open positions: if there are, the selling flow will start;
    # Otherwise, the buying flow will start
    logger.info("Algo trade bot - End function")

def algo_trade_long_strategy_function(stock):
    position_has_been_opened = False
    # Applying rsi strategy + price candle + volume for long positions
    stock_rsi_data = __data_client.get_stock_rsi_data(stock.symbol)
    logger.info(f"Algo trade bot - Stock {stock.symbol} RSI data: {stock_rsi_data}")
    is_neutral_from_oversold = market_utility.check_if_stock_is_neutral_from_oversold(stock_rsi_data)
    logger.info(f"Algo trade bot - Stock {stock.symbol} is neutral from oversold: {is_neutral_from_oversold}")
    # First condition - RSI
    if(is_neutral_from_oversold):
        # Second condition - Price candle
        stock_price_candle_data = __data_client.get_stock_price_candle_data(stock.symbol)
        is_bullish_candle = market_utility.check_if_stock_is_bullish_candle(stock_price_candle_data)
        logger.info(f"Algo trade bot - Stock {stock.symbol} is bullish candle: {is_bullish_candle}")
        if(is_bullish_candle):
            # Third condition - Volume
            higher_volumes = market_utility.check_if_stock_volume_is_higher_than_previous_candle(stock_price_candle_data)
            logger.info(f"Algo trade bot - Stock {stock.symbol} has higher volumes: {higher_volumes}")
            if(higher_volumes):
                # Open long position
                __trading_client.open_trade(stock.symbol, 1, OrderSide.BUY.value)
                position_has_been_opened = True
    return position_has_been_opened

def algo_trade_short_strategy_function(stock):
    position_has_been_opened = False
    # Applying rsi strategy + price candle + volume for short positions
    stock_rsi_data = __data_client.get_stock_rsi_data(stock.symbol)
    is_neutral_from_overbought = market_utility.check_if_stock_is_neutral_from_overbought(stock_rsi_data)
    logger.info(f"Algo trade bot - Stock {stock.symbol} is neutral from overbought: {is_neutral_from_overbought}")
    # First condition - RSI
    if(is_neutral_from_overbought):
        # Second condition - Price candle
        stock_price_candle_data = __data_client.get_stock_price_candle_data(stock.symbol)
        is_bearish_candle = market_utility.check_if_stock_is_bearish_candle(stock_price_candle_data)
        logger.info(f"Algo trade bot - Stock {stock.symbol} is bearish candle: {is_bearish_candle}")
        if(is_bearish_candle):
            # Third condition - Volume
            higher_volumes = market_utility.check_if_stock_volume_is_higher_than_previous_candle(stock_price_candle_data)
            logger.info(f"Algo trade bot - Stock {stock.symbol} has higher volumes: {higher_volumes}")
            if(higher_volumes):
                # Open short position
                __trading_client.open_trade(stock.symbol, 1, OrderSide.SELL.value)
                position_has_been_opened = True
    return position_has_been_opened