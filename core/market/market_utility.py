import pandas as pd
import logging
import os
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

def check_if_stock_is_neutral_from_overbought(rsi_data):
    isNeutralFromOverbought = False
    # Calcola l'RSI utilizzando i dati più recenti
    # Converte i dati in un DataFrame di pandas per facilitare l'analisi
    df = pd.DataFrame(rsi_data)
    df['rsi'] = pd.to_numeric(df['rsi'])

    # Controlla se l'RSI è sceso sotto il livello overbought (per esempio, 70) e se la SMA dell'RSI è inferiore a overbought_level
    overbought_level = 70
    tolerance = os.environ.get('RSI_LIMITS_TOLERANCE')

    actual_rsi = df.iloc[0]['rsi']
    last_rsi = df.iloc[1]['rsi']
    logger.info(f"neutral_from_overbought - Actual RSI: {actual_rsi} - Last RSI: {last_rsi}")
    if (last_rsi >= overbought_level and float(actual_rsi + float(tolerance))  < overbought_level):
        isNeutralFromOverbought = True
    
    return isNeutralFromOverbought

def check_if_stock_is_neutral_from_oversold(rsi_data):
    isNeutralFromOversold = False
    # Estrai i dati RSI dal risultato
    # Converte i dati in un DataFrame di pandas per facilitare l'analisi    
    df = pd.DataFrame(rsi_data)
    df['rsi'] = pd.to_numeric(df['rsi']) # Converte la colonna RSI in numerico: l'rsi proveniente da FMP è già SMA 

    # Controlla se l'RSI è sceso al di sotto del livello di ipervenduto (per esempio, 30) e se la SMA dell'RSI è superiore al livello di ipervenduto
    oversold_level = 30
    tolerance = os.environ.get('RSI_LIMITS_TOLERANCE')

    actual_rsi = df.iloc[0]['rsi']
    last_rsi = df.iloc[1]['rsi']
    logger.info(f"neutral_from_oversold - Actual RSI: {actual_rsi} - Last RSI: {last_rsi}")

    if (last_rsi <= oversold_level and actual_rsi > float(oversold_level + float(tolerance))):
        isNeutralFromOversold = True

    return isNeutralFromOversold

def check_stop_loss_and_take_profit(position):
    # TODO This is probably not the best way: it should be done by alpaca itself.
    to_close = False
    is_profitable = float(position.unrealized_plpc) >= 0.01
    is_stop_loss = float(position.unrealized_plpc) <= -0.01
    if(is_profitable or is_stop_loss):
        # Close position
        to_close = True
    return to_close

def check_if_stock_is_bearish_candle(stock_price_candle_data):
    # Check if the actual candle minimum is lower than the previous hour candle minimum
    is_bearish = False
    
    # Converte i dati in un DataFrame di pandas per facilitare l'analisi
    df = pd.DataFrame(stock_price_candle_data)
    # Check if there are atleast 2 candles 
    if(len(df) < 2):
        return is_bearish
    df['low'] = pd.to_numeric(df['low'])
    previous_price_candle = df.iloc[0]
    actual_price_canlde = df.iloc[1]
    logger.info(f"bearish - Previous price candle: {previous_price_candle['low']} - Actual: {actual_price_canlde['low']}")
    if(actual_price_canlde['low'] < previous_price_candle['low']):
        is_bearish = True
    return is_bearish

def check_if_stock_is_bullish_candle(stock_price_candle_data):
    # Check if the actual candle maximum is higher than the previous hour candle maximum
    is_bullish = False

    df = pd.DataFrame(stock_price_candle_data)
    if(len(df) < 2):
        return is_bullish
    df['high'] = pd.to_numeric(df['high'])
    
    actual_price_candle = df.iloc[0]
    previous_price_candle = df.iloc[1]
    logger.info(f"bullish - Previous price candle: {previous_price_candle['high']} - Actual: {actual_price_candle['high']}")
    
    if(actual_price_candle['high'] > previous_price_candle['high']):
        is_bullish = True
    return is_bullish

def check_if_stock_volume_is_higher_than_previous_candle(stock_price_candle_data):
    # Check if the actual candle volume is higher than the previous hour candle volume
    is_higher = False

    df = pd.DataFrame(stock_price_candle_data)
    df['volume'] = pd.to_numeric(df['volume'])

    actual_price_candle = df.iloc[0]
    previous_price_candle = df.iloc[1]
    logger.info(f"volumes - Previous price candle: {previous_price_candle['volume']} - Actual: {actual_price_candle['volume']}")
   
    if(actual_price_candle['volume'] > previous_price_candle['volume']):
        is_higher = True
    return is_higher