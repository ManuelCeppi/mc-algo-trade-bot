
def check_if_stock_is_neutral_from_overbought(stock_data):
    pass

def check_if_stock_is_neutral_from_oversold(stock_data):
    pass

def check_stop_loss_and_take_profit(position):
    to_close = False
    is_profitable = position.unrealized_plpc > 0.04
    is_stop_loss = position.unrealized_plpc < -0.02
    if(is_profitable or is_stop_loss):
        # Close position
        to_close = True
    return to_close
