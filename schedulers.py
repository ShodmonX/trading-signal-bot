import logging

from config import SYMBOLS, ADMIN_ID
from api import get_klines
from strategies import TrendFollowStrategy

async def check_signals(bot):
    for symbol in SYMBOLS:
        try:
            klines, error = await get_klines(symbol, limit=999)
            if error:
                logging.error(f"{symbol} - olishda xatolik")
            else:
                strategy = TrendFollowStrategy(klines, symbol)
                strategy.run()
                text, signal = strategy.generate_text()
                logging.info(f"{symbol} - Tekishruvdan o'tdi - {signal}")
                if signal != 'NEUTRAL':
                    bot.send_message(ADMIN_ID, text)
                
        except Exception as e:
            logging.error(e)