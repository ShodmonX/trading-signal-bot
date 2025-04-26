from aiogram import Bot, Dispatcher

import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from config import BOT_TOKEN, ADMIN_ID
from schedulers import check_signals
from handlers import router

logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

async def on_startup():
    scheduler.add_job(check_signals, 'cron', minute=5, kwargs={'bot': bot})
    scheduler.start()
    await bot.send_message(ADMIN_ID, "Bot muvaffaqiyatli ishga tushurildi.")

async def on_shutdown():
    await bot.send_message(ADMIN_ID, "Bot ishdan to'xtadi.")

async def main():
    dp.include_router(router)
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Bot ishdan to'xtadi!")
    except Exception as e:
        logging.error(e)