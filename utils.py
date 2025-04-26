import pandas as pd
import ta

def calculate_rsi(data, window=14) -> pd.DataFrame:
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        'close_time', 'quote_asset_volume', 'trades', 'taker_base_vol',
        'taker_quote_vol', 'ignore'
    ])

    df['close'] = df['close'].astype(float)

    df["rsi"] = ta.momentum.RSIIndicator(close=df['close'], window=window).rsi()

    return df

def calculate_ema(data, window=20) -> pd.DataFrame:
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        'close_time', 'quote_asset_volume', 'trades', 'taker_base_vol',
        'taker_quote_vol', 'ignore'
    ])

    df['close'] = df['close'].astype(float)

    df[f"ema{window}"] = ta.trend.EMAIndicator(close=df['close'], window=window).ema_indicator()

    return df

def calculate_adx(data, window=14) -> pd.DataFrame:
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        'close_time', 'quote_asset_volume', 'trades', 'taker_base_vol',
        'taker_quote_vol', 'ignore'
    ])

    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)

    df['adx'] = ta.trend.ADXIndicator(high=df['high'], low=df['low'], close=df['close'], window=window).adx()
    
    return df

def calculate_sma(data, window=14) -> pd.DataFrame:
    df = pd.DataFrame(data, columns=[
        "timestamp", "open", "high", "low", "close", "volume",
        'close_time', 'quote_asset_volume', 'trades', 'taker_base_vol',
        'taker_quote_vol', 'ignore'
    ])

    df['close'] = df['close'].astype(float)

    df['sma'] = ta.trend.SMAIndicator(close=df['close'], window=window).sma_indicator()

    return df
