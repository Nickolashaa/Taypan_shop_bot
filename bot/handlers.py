import os

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

from .keyboards import main_keyboard
from .states import OrderCallState

router = Router()


@router.message(CommandStart())
async def start_command(message: Message):
    await message.answer(
        "Добро пожаловать в бота Тайпан! Чем я могу вам помочь?",
        reply_markup=main_keyboard,
    )


@router.callback_query(F.data == "order_call")
async def waiting_for_name(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Подскажите, как я могу к вам обратиться?")
    await state.set_state(OrderCallState.waiting_for_name)


@router.message(OrderCallState.waiting_for_name)
async def waiting_for_phone(message: Message, state: FSMContext):
    await state.update_data(waiting_for_name=message.text)
    await message.answer("Укажите ваш номер телефона...")
    await state.set_state(OrderCallState.waiting_for_phone)


@router.message(OrderCallState.waiting_for_phone)
async def waiting_for_comment(message: Message, state: FSMContext):
    await state.update_data(waiting_for_phone=message.text)
    await message.answer("Напишите комментарий...")
    await state.set_state(OrderCallState.waiting_for_comment)


@router.message(OrderCallState.waiting_for_comment)
async def waiting_for_comment(message: Message, state: FSMContext):
    await state.update_data(waiting_for_comment=message.text)
    await message.answer(
        "Благодарим за вашу заявку! Мы свяжемся с вами в ближайшее время."
    )
    data = await state.get_data()
    await state.clear()
    result = list()
    result.append("Новая заявка на обратный звонок:")
    result.append(f"Имя: {data['waiting_for_name']}")
    result.append(f"Телефон: {data['waiting_for_phone']}")
    result.append(f"Комментарий: {data['waiting_for_comment']}")
    load_dotenv()
    await message.bot.send_message(
        chat_id=os.getenv("ADMIN_ID"), text="\n".join(result)
    )
