from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command, CommandStart, or_f

import logging

from api import get_klines
from config import ADMIN_ID, SYMBOLS
from strategies import TrendFollowStrategy, MACDCrossoverStrategy, BollingerBandSqueezeStrategy, StochasticOscillatorStrategy, SMACrossoverStrategy
from keyboards import strategies

STRATEGIES = {
    "trendfollowstrategy": TrendFollowStrategy, 
    "macdcrossoverstrategy": MACDCrossoverStrategy,
    "bollingerbandsqueezestrategy": BollingerBandSqueezeStrategy,
    "stochasticoscillatorstrategy": StochasticOscillatorStrategy,
    "smacrossoverstrategy": SMACrossoverStrategy
}

router = Router()

@router.message(Command(commands=['menu', 'start']))
async def start_command(message: Message):
    await message.answer("Quyidagi Strategiyalar orqali Kripto valyutalarni tekshirishingiz mumkin!", reply_markup=strategies)

@router.callback_query(F.data.startswith("strategy"))
async def strategy_check(callback: CallbackQuery):
    strategy = callback.data.split(":")[1]
    for symbol in SYMBOLS:
        try:
            klines, error = await get_klines(symbol, limit=999)
            if error:
                logging.error(f"{symbol} - olishda xatolik")
            else:
                strategy_instance = STRATEGIES[strategy](klines, symbol)
                strategy_instance.run()
                text, signal = strategy_instance.generate_text()
                logging.info(f"{symbol} - Tekshiruvdan o'tdi - {signal}")
                await callback.answer(f"{strategy_instance.get_name()}")
                await callback.message.answer(text)
        except Exception as e:
            logging.error(e)

@router.message(Command(commands=['check']))
async def checking_coins(message: Message):
    for symbol in SYMBOLS:
        try:
            klines, error = await get_klines(symbol, limit=999)
            if error:
                logging.error(f"{symbol} - olishda xatolik")
            else:
                for strategy in STRATEGIES.values():
                    strategy_instance = strategy(klines, symbol)
                    strategy_instance.run()
                    text, signal = strategy_instance.generate_text()
                    logging.info(f"{symbol} - Tekshiruvdan o'tdi - {signal}")
                    await message.answer(text)
        except Exception as e:
            logging.error(e)