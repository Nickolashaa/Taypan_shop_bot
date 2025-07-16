from aiogram import F
from aiogram.types import Message, CallbackQuery
from ..routers import order_call_router
from aiogram.fsm.context import FSMContext
from ..states import OrderCallState
from dotenv import load_dotenv
import os


@order_call_router.callback_query(F.data == "order_call")
async def waiting_for_name(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.answer("Подскажите, как я могу к вам обратиться?")
    await state.set_state(OrderCallState.waiting_for_name)

@order_call_router.Message(OrderCallState.waiting_for_name)
async def waiting_for_phone(message: Message, state: FSMContext):
    await state.update_data(waiting_for_name=message.text)
    await message.answer("Укажите ваш номер телефона...")
    await state.set_state(OrderCallState.waiting_for_phone)
    
@order_call_router.Message(OrderCallState.waiting_for_phone)
async def waiting_for_comment(message: Message, state: FSMContext):
    await state.update_data(waiting_for_phone=message.text)
    await message.answer("Напишите комментарий...")
    await state.set_state(OrderCallState.waiting_for_comment)
    
@order_call_router.Message(OrderCallState.waiting_for_comment)
async def waiting_for_comment(message: Message, state: FSMContext):
    await state.update_data(waiting_for_comment=message.text)
    await message.answer("Благодарим за вашу заявку! Мы свяжемся с вами в ближайшее время.")
    data = await state.get_data()
    await state.clear()
    result = list()
    result.append("Новая заявка на обратный звонок:")
    result.append(f"Имя: {data['waiting_for_name']}")
    result.append(f"Телефон: {data['waiting_for_phone']}")
    result.append(f"Комментарий: {data['waiting_for_comment']}")
    load_dotenv()
    await message.bot.send_message(
        admin_id=os.getenv("ADMIN_ID"),
        text="\n".join(result)
    )