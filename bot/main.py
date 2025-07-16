from aiogram import Bot, Dispatcher
import asyncio
import os
from dotenv import load_dotenv
from routers import main_router, order_call_router


async def main():
    load_dotenv()
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    dp.include_router(main_router)
    dp.include_router(order_call_router)
    print("Bot started.")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot stopped.")
