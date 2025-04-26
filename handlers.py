from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import logging

from api import get_klines
from config import ADMIN_ID, SYMBOLS
from signals import follow_trend

router = Router()

@router.message(Command(commands=['check']))
async def checking_coins(message: Message):
    for symbol in SYMBOLS:
        try:
            klines, error = await get_klines(symbol, limit=999)
            if error:
                logging.error(f"{symbol} - olishda xatolik")
            else:
                result = follow_trend(klines)
                print(result[0])
                text = f"{symbol}"
                if result[0] == 'NEUTRAL':
                    text = f"{symbol} - SIGNAL YO'Q📊\n\n"
                    text += f"PRICE: {float(result[1])}\n"
                    text += f"EMA21: {float(result[2])}\n"
                    text += f"EMA100: {float(result[3])}\n"
                    text += f"RSI: {float(result[4])}\n"
                    text += f"ADX: {float(result[5])}\n"
                elif result[0] == 'SHORT':
                    text = f"{symbol} - SIGNAL SHORT🔴\n\n"
                    text += f"PRICE: {float(result[1])}\n"
                    text += f"EMA21: {float(result[2])}\n"
                    text += f"EMA100: {float(result[3])}\n"
                    text += f"RSI: {float(result[4])}\n"
                    text += f"ADX: {float(result[5])}\n"
                elif result[0] == 'LONG':
                    text = f"{symbol} - SIGNAL LONG🔵\n\n"
                    text += f"PRICE: {float(result[1])}\n"
                    text += f"EMA21: {float(result[2])}\n"
                    text += f"EMA100: {float(result[3])}\n"
                    text += f"RSI: {float(result[4])}\n"
                    text += f"ADX: {float(result[5])}\n"
                await message.answer(text)
        except Exception as e:
            print(1)
            logging.error(e)