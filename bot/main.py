import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from .handlers import router


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(router)
    print("Bot started.")
    await dp.start_polling(bot)
