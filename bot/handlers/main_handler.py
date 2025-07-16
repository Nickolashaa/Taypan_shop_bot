from aiogram.types import Message
from aiogram.filters import CommandStart
from ..routers import main_router


@main_router.message(CommandStart())
async def start_command(message: Message):
    await message.answer("Добро пожаловать в бота Тайпан! Чем я могу вам помочь?")