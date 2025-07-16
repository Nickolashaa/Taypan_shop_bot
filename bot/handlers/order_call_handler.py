from aiogram import F
from aiogram.types import Message, CallbackQuery
from ..routers import order_call_router


@order_call_router.callback_query(F.data == "order_call")
async def start_command(call: CallbackQuery):
    await call.answer()
    await call.message.answer("Добро пожаловать в бота Тайпан! Чем я могу вам помочь?")
    