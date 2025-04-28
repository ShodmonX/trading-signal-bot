from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import logging

from api import get_klines
from config import ADMIN_ID, SYMBOLS
from strategies import TrendFollowStrategy

router = Router()

@router.message(Command(commands=['check']))
async def checking_coins(message: Message):
    for symbol in SYMBOLS:
        try:
            klines, error = await get_klines(symbol, limit=999)
            if error:
                logging.error(f"{symbol} - olishda xatolik")
            else:
                strategy = TrendFollowStrategy(klines, symbol)
                strategy.run()
                text, signal = strategy.generate_text()
                await message.answer(text)
        except Exception as e:
            logging.error(e)