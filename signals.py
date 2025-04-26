import utils

def calculate_indicators(data):
    """
        Indocatorlarni hisoblaymiz
    """

    result_data = utils.calculate_ema(data, window=21).copy()
    result_data['ema100'] = utils.calculate_ema(data, window=100)['ema100']
    result_data['rsi'] = utils.calculate_rsi(data, window=14)['rsi']
    result_data['adx'] = utils.calculate_adx(data, window=14)['adx']
    
    return result_data

def generate_signals(data):
    data = calculate_indicators(data)
    
    data['ema21_prev'] = data['ema21'].shift(1)
    data['ema100_prev'] = data['ema100'].shift(1)
    data['bullish_crossover'] = (data['ema21_prev'] <= data['ema100_prev']) & (data['ema21'] > data['ema100'])
    data['bearish_crossover'] = (data['ema21_prev'] >= data['ema100_prev']) & (data['ema21'] < data['ema100'])
    
    
    data['below_ema21'] = data['close'].shift(1) < data['ema21'].shift(1)
    data['above_ema21'] = data['close'] > data['ema21']
    data['pullback'] = data['below_ema21'] & data['above_ema21']
    
    data['above_ema21_prev'] = data['close'].shift(1) > data['ema21'].shift(1)
    data['below_ema21_now'] = data['close'] < data['ema21']
    data['rally'] = data['above_ema21_prev'] & data['below_ema21_now']
    
    data['long_signal'] = (
        (data['ema21'] > data['ema100']) &  
        (data['close'] > data['ema21']) &  
        (data['bullish_crossover'] | data['pullback']) &  
        (data['adx'] > 25) &  
        (data['rsi'].between(50, 70))
    )    
    
    data['short_signal'] = (
        (data['ema21'] < data['ema100']) &  
        (data['close'] < data['ema21']) &  
        (data['bearish_crossover'] | data['rally']) &  
        (data['adx'] > 25) &  
        (data['rsi'].between(30, 50)) 
    )
    
    return data

def follow_trend(data):
    """
        result: LONG, SHORT, NEUTRAL
        CLOSE:
        EMA21:
        EMA21_PREV:
        EMA100:
        EMA100_PREV:
        RSI:
        ADX:
    """
    data_with_signals = generate_signals(data)
    if data_with_signals['long_signal'].iloc[-1]:
        result = "LONG"
    elif data_with_signals['short_signal'].iloc[-1]:
        result = "SHORT"
    else:
        result = "NEUTRAL"
    return result, data_with_signals['close'].iloc[-1],\
           data_with_signals['ema21'].iloc[-2], data_with_signals['ema100'].iloc[-1],\
           data_with_signals['rsi'].iloc[-1], data_with_signals['adx'].iloc[-1]
    

    