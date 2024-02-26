import pandas as pd

def check_if_stock_is_neutral_from_overbought(stock_data):
    isNeutralFromOverbought = False
    # Calcola l'RSI utilizzando i dati più recenti

    rsi_data = stock_data['Technical Analysis: RSI']
    # Converte i dati in un DataFrame di pandas per facilitare l'analisi
    df = pd.DataFrame(rsi_data).T
    df['RSI'] = pd.to_numeric(df['RSI'])

    # Calcola la media mobile semplice (SMA) dell'RSI: periodo di 5
    rsi_sma = df['RSI'].rolling(window=5).mean()

    # Controlla se l'RSI è sceso sotto il livello overbought (per esempio, 70) e se la SMA dell'RSI è inferiore a overbought_level
    overbought_level = 70

    last_rsi = df.iloc[-1]['RSI']

    if (last_rsi > overbought_level or last_rsi < overbought_level) and rsi_sma.iloc[-1] <= overbought_level:
        isNeutralFromOverbought = True
    
    return isNeutralFromOverbought

def check_if_stock_is_neutral_from_oversold(stock_data):
    isNeutralFromOversold = False
    # Estrai i dati RSI dal risultato
    rsi_data = stock_data['Technical Analysis: RSI']

    # Converte i dati in un DataFrame di pandas per facilitare l'analisi
    df = pd.DataFrame(rsi_data).T
    df['RSI'] = pd.to_numeric(df['RSI'])

    # Calcola la media mobile semplice (SMA) dell'RSI
    rsi_sma = df['RSI'].rolling(window=5).mean()

    # Controlla se l'RSI è sceso al di sotto del livello di ipervenduto (per esempio, 30) e se la SMA dell'RSI è superiore al livello di ipervenduto
    oversold_level = 30

    last_rsi = df.iloc[0]['RSI']

    if last_rsi < oversold_level and rsi_sma.iloc[0] >= oversold_level:
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
    df = pd.DataFrame(stock_price_candle_data['Time Series (60min)']).T
    df['3. low'] = pd.to_numeric(df['3. low'])

    previous_price_candle = df.iloc[1]

    if(pd.to_numeric(actual) < previous_price_candle['3. low']):
        is_bearish = True
    return is_bearish

def check_if_stock_is_bullish_candle(actual, stock_price_candle_data):
    # Check if the actual candle maximum is higher than the previous hour candle maximum
    is_bullish = False

    df = pd.DataFrame(stock_price_candle_data['Time Series (60min)']).T
    df['2. high'] = pd.to_numeric(df['2. high'])
    
    previous_price_candle = df.iloc[1]
    
    if(pd.to_numeric(actual) > previous_price_candle['2. high']):
        is_bullish = True
    return is_bullish

def check_if_stock_volume_is_higher_than_previous_candle(actual, stock_price_candle_data):
    # Check if the actual candle volume is higher than the previous hour candle volume
    is_higher = False

    df = pd.DataFrame(stock_price_candle_data['Time Series (60min)']).T
    df['5. volume'] = pd.to_numeric(df['5. volume'])

    previous_hour_price_candle = df.iloc[0]
    
    if(pd.to_numeric(actual) > previous_hour_price_candle['5. volume']):
        is_higher = True
    return is_higher