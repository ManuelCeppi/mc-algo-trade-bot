
def check_if_stock_is_neutral_from_overbought(stock_data):
    #TODO think about how to implement this
    pass

def check_if_stock_is_neutral_from_oversold(stock_data):
    #TODO think about how to implement this
    pass

def check_stop_loss_and_take_profit(position):
    # TODO This is probably not the best way: it should be done by alpaca itself.
    to_close = False
    is_profitable = position.unrealized_plpc > 0.04
    is_stop_loss = position.unrealized_plpc < -0.02
    if(is_profitable or is_stop_loss):
        # Close position
        to_close = True
    return to_close

def check_if_stock_is_bearish_candle(stock_price_candle_data):
    # Check if the actual candle minimum is lower than the previous hour candle minimum
    is_bearish = False
    actual_price_candle = stock_price_candle_data['Time Series (60min)'][0]
    previous_price_candle = stock_price_candle_data['Time Series (60min)'][1]
    if(actual_price_candle['3. low'] < previous_price_candle['3. low']):
        is_bearish = True
    return is_bearish

def check_if_stock_is_bullish_candle(stock_price_candle_data):
    # Check if the actual candle maximum is higher than the previous hour candle maximum
    is_bullish = False
    actual_price_candle = stock_price_candle_data['Time Series (60min)'][0]
    previous_price_candle = stock_price_candle_data['Time Series (60min)'][1]
    if(actual_price_candle['2. high'] > previous_price_candle['2. high']):
        is_bullish = True
    return is_bullish

def check_if_stock_volume_is_higher_than_previous_candle(stock_price_candle_data):
    # Check if the actual candle volume is higher than the previous hour candle volume
    is_higher = False
    actual_price_candle = stock_price_candle_data['Time Series (60min)'][0]
    previous_price_candle = stock_price_candle_data['Time Series (60min)'][1]
    if(actual_price_candle['5. volume'] > previous_price_candle['5. volume']):
        is_higher = True
    return is_higher