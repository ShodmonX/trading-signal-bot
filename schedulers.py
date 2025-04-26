import logging

from config import SYMBOLS, ADMIN_ID
from api import get_klines
from signals import follow_trend

async def check_signals(bot):
    for symbol in SYMBOLS:
        try:
            klines, error = await get_klines(symbol, limit=999)
            if error:
                logging.error(f"{symbol} - olishda xatolik")
            else:
                result = follow_trend(klines)
                text = f"{symbol}"
                if result[0] == 'NEUTRAL':
                    text = f"{symbol} - SIGNAL YO'Q\n\n"
                    text += f"PRICE: {result[1]}\n"
                    text += f"EMA21: {result[2]}\n"
                    text += f"EMA100: {result[3]}\n"
                    text += f"RSI: {result[4]}\n"
                    text += f"ADX: {result[5]}\n"
                elif result[0] == 'SHORT':
                    text = f"{symbol} - SIGNAL SHORT\n\n"
                    text += f"PRICE: {result[1]}\n"
                    text += f"EMA21: {result[2]}\n"
                    text += f"EMA100: {result[3]}\n"
                    text += f"RSI: {result[4]}\n"
                    text += f"ADX: {result[5]}\n"
                elif result[0] == 'LONG':
                    text = f"{symbol} - SIGNAL LONG\n\n"
                    text += f"PRICE: {result[1]}\n"
                    text += f"EMA21: {result[2]}\n"
                    text += f"EMA100: {result[3]}\n"
                    text += f"RSI: {result[4]}\n"
                    text += f"ADX: {result[5]}\n"
                await bot.send_message(ADMIN_ID, text)
        except Exception as e:
            logging.error(e)