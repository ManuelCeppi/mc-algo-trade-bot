import pandas as pd
import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def check_if_stock_is_neutral_from_overbought(rsi_data):
    isNeutralFromOverbought = False
    # Calcola l'RSI utilizzando i dati più recenti

    # Converte i dati in un DataFrame di pandas per facilitare l'analisi
    df = pd.DataFrame(rsi_data)
    df['rsi'] = pd.to_numeric(df['rsi'])

    # Calcola la media mobile semplice (SMA) dell'RSI: periodo di 5
    rsi_sma = df['rsi'].rolling(window=5).mean()

    # Controlla se l'RSI è sceso sotto il livello overbought (per esempio, 70) e se la SMA dell'RSI è inferiore a overbought_level
    overbought_level = 70

    actual_rsi = df.iloc[0]['rsi']
    last_rsi = df.iloc[1]['rsi']
    logger.info(f"neutral_from_overbought - Actual RSI: {actual_rsi} - Last RSI: {last_rsi}")
    if (last_rsi > overbought_level and actual_rsi < overbought_level) and rsi_sma.iloc[0] <= overbought_level:
        isNeutralFromOverbought = True
    
    return isNeutralFromOverbought

def check_if_stock_is_neutral_from_oversold(rsi_data):
    isNeutralFromOversold = False
    # Estrai i dati RSI dal risultato

    # Converte i dati in un DataFrame di pandas per facilitare l'analisi
    
    df = pd.DataFrame(rsi_data)
    df['rsi'] = pd.to_numeric(df['rsi'])

    # Calcola la media mobile semplice (SMA) dell'RSI
    rsi_sma = df['rsi'].rolling(window=5).mean()

    # Controlla se l'RSI è sceso al di sotto del livello di ipervenduto (per esempio, 30) e se la SMA dell'RSI è superiore al livello di ipervenduto
    oversold_level = 30

    actual_rsi = df.iloc[0]['rsi']
    last_rsi = df.iloc[1]['rsi']
    logger.info(f"neutral_from_oversold - Actual RSI: {actual_rsi} - Last RSI: {last_rsi}")
    # Check if the RSI is below the oversold level and if the RSI SMA is above the oversold level
    if (last_rsi < oversold_level and actual_rsi > oversold_level) and rsi_sma.iloc[0] >= oversold_level:
        isNeutralFromOversold = True

    return isNeutralFromOversold

def check_stop_loss_and_take_profit(position):
    # TODO This is probably not the best way: it should be done by alpaca itself.
    to_close = False
    is_profitable = float(position.unrealized_plpc) >= 0.02
    is_stop_loss = float(position.unrealized_plpc) <= -0.01
    if(is_profitable or is_stop_loss):
        # Close position
        to_close = True
    return to_close

def check_if_stock_is_bearish_candle(actual, stock_price_candle_data):
    # Check if the actual candle minimum is lower than the previous hour candle minimum
    is_bearish = False
    
    # Converte i dati in un DataFrame di pandas per facilitare l'analisi
    df = pd.DataFrame(stock_price_candle_data)
    df['low'] = pd.to_numeric(df['low'])

    previous_price_candle = df.iloc[0]
    logger.info(f"bearish - Previous price candle: {previous_price_candle['low']} - Actual: {actual}")
    if(pd.to_numeric(actual) < previous_price_candle['low']):
        is_bearish = True
    return is_bearish

def check_if_stock_is_bullish_candle(actual, stock_price_candle_data):
    # Check if the actual candle maximum is higher than the previous hour candle maximum
    is_bullish = False

    df = pd.DataFrame(stock_price_candle_data)
    df['high'] = pd.to_numeric(df['high'])
    
    previous_price_candle = df.iloc[0]
    logger.info(f"bullish - Previous price candle: {previous_price_candle['high']} - Actual: {actual}")
    if(pd.to_numeric(actual) > previous_price_candle['high']):
        is_bullish = True
    return is_bullish

def check_if_stock_volume_is_higher_than_previous_candle(actual, stock_price_candle_data):
    # Check if the actual candle volume is higher than the previous hour candle volume
    is_higher = False

    df = pd.DataFrame(stock_price_candle_data)
    df['volume'] = pd.to_numeric(df['volume'])

    previous_hour_price_candle = df.iloc[0]
    logger.info(f"volumes - Previous price candle: {previous_hour_price_candle['volume']} - Actual: {actual}")
   
    if(pd.to_numeric(actual) > previous_hour_price_candle['volume']):
        is_higher = True
    return is_higher