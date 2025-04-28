from ta.trend import EMAIndicator, ADXIndicator
from ta.momentum import RSIIndicator
import pandas as pd


class BaseStrategy:
    def __init__(self, data, symbol):
        self.df = pd.DataFrame(data, columns=[
            "timestamp", "open", "high", "low", "close", "volume",
            'close_time', 'quote_asset_volume', 'trades', 'taker_base_vol',
            'taker_quote_vol', 'ignore'
        ])
        self.df[['open', 'high', 'low', 'close']] = self.df[['open', 'high', 'low', 'close']].astype(float)
        self.signal = "NEUTRAL"
        self.symbol = symbol
        self.unsupported_keys = ["timestamp", "open", "high", "low", "volume", 'close_time', 'quote_asset_volume', 'trades', 'taker_base_vol', 'taker_quote_vol', 'ignore']

    
    def calculate_indicators(self):
        """Child classlar o‘zlari keraklisini override qiladi"""
        raise NotImplementedError
    
    def generate_signals(self):
        """Child classlar o‘zlari override qiladi"""
        raise NotImplementedError
    
    def decide(self):
        raise NotImplementedError

    def run(self):
        self.calculate_indicators()
        self.generate_signals()
        self.decide()

    def get_context(self):
        raise NotImplementedError
    
    def generate_text(self):
        raise NotImplementedError


class TrendFollowStrategy(BaseStrategy):
    def calculate_indicators(self):
        self.df['ema21'] = EMAIndicator(self.df['close'], window=21).ema_indicator()
        self.df['ema100'] = EMAIndicator(self.df['close'], window=100).ema_indicator()
        self.df['rsi'] = RSIIndicator(self.df['close'], window=14).rsi()
        self.df['adx'] = ADXIndicator(high=self.df['high'], low=self.df['low'], close=self.df['close'], window=14).adx()

    def generate_signals(self):
        self.df['ema21_prev'] = self.df['ema21'].shift(1)
        self.df['ema100_prev'] = self.df['ema100'].shift(1)

        self.df['bullish_crossover'] = (self.df['ema21_prev'] <= self.df['ema100_prev']) & (self.df['ema21'] > self.df['ema100'])
        self.df['bearish_crossover'] = (self.df['ema21_prev'] >= self.df['ema100_prev']) & (self.df['ema21'] < self.df['ema100'])

        self.df['below_ema21'] = self.df['close'].shift(1) < self.df['ema21'].shift(1)
        self.df['above_ema21'] = self.df['close'] > self.df['ema21']
        self.df['pullback'] = self.df['below_ema21'] & self.df['above_ema21']

        self.df['above_ema21_prev'] = self.df['close'].shift(1) > self.df['ema21'].shift(1)
        self.df['below_ema21_now'] = self.df['close'] < self.df['ema21']
        self.df['rally'] = self.df['above_ema21_prev'] & self.df['below_ema21_now']

        self.df['long_signal'] = (
            (self.df['ema21'] > self.df['ema100']) &
            (self.df['close'] > self.df['ema21']) &
            (self.df['bullish_crossover'] | self.df['pullback']) &
            (self.df['adx'] > 25) &
            (self.df['rsi'].between(50, 70))
        )

        self.df['short_signal'] = (
            (self.df['ema21'] < self.df['ema100']) &
            (self.df['close'] < self.df['ema21']) &
            (self.df['bearish_crossover'] | self.df['rally']) &
            (self.df['adx'] > 25) &
            (self.df['rsi'].between(30, 50))
        )

        self.unsupported_keys += ['bullish_crossover', 'bearish_crossover', 'ema21_prev', 'ema100_prev', 'below_ema21', 'above_ema21', 'above_ema21_prev', 'below_ema21_now', 'rally', 'pullback', 'long_signal', 'short_signal']

        return self.df
    
    def decide(self):
        if self.df['long_signal'].iloc[-1]:
            self.signal = "LONG"
        elif self.df['short_signal'].iloc[-1]:
            self.signal = "SHORT"

    def get_context(self):
        context = {
            "signal": self.signal,
            "other_data": self.generate_signals().iloc[-1].to_dict()
        }
        return context
    
    def generate_text(self):
        result = self.get_context()
        text = f"{self.symbol} - Follow-Trend Strategy\n\n"
        if result['signal'] != 'NEUTRAL':
            text += f"SIGNAL {result['signal']}{'🔴' if result['signal'] == 'SHORT' else '🔵'}\n\n"
            for key in result['other_data']:
                if key not in self.unsupported_keys:
                    text += f"{key.upper()}: {result['other_data'][key]}\n"
        else:
            text += f"SIGNAL {result['signal']}📊\n\n"
            for key in result['other_data'].keys():
                if key not in self.unsupported_keys:
                    text += f"{key.upper()}: {result['other_data'][key]}\n"
        return text, result['signal']
