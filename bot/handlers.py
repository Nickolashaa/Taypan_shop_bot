import os
import asyncio
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from aiogram.types.input_file import FSInputFile  # ← правильный импорт
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


# Заказать звонок
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


# Контакты
@router.callback_query(F.data == "contacts")
async def contancts(call: CallbackQuery):
    await call.answer()
    await call.message.answer(
        text=(
            "Для связи с нами вы можете заказать звонок "
            "или связаться с нами по следующим контактам:\n"
            "Вот наши контакты\n"
            "Номер: 8(960)382-87-32\n"
            "Почта: fasad-taypan@mail.ru\n"
            "Сайт: www.fasad-taypan.com\n"
        ), reply_markup=main_keyboard
    )


# Информация
@router.callback_query(F.data == "info")
async def info(call: CallbackQuery):
    await call.answer()
    await call.message.answer("Вот все товары, которые мы предоставляем!")

    files = [
        "assets/Гибкая доска без цвета.png",
        "assets/Гибкая доска окрашенная в масса.png",
        "assets/Гибкий каменный стол.png",
        "assets/Гибкий кирпич в модулях на фасадной сетке.png",
        "assets/Гибкий мрамор.png",
        "assets/Гибкий ригель на фасадной сетке.png",
        "assets/Дагестанский камень.png",
        "assets/Мраморная штукатурка.png",
        "assets/Штучный гибкий кирпич.png",
        "assets/Штучный гибкий ригель.png",
    ]

    for file_path in files:
        await asyncio.sleep(1)
        file = FSInputFile(file_path)
        await call.message.bot.send_photo(
            chat_id=call.from_user.id,
            photo=file,
        )

    await call.bot.send_chat_action(chat_id=call.from_user.id, action="upload_document")
    price_file = FSInputFile("assets/Тайпан Прайс.pdf")
    await call.message.bot.send_document(
        chat_id=call.from_user.id,
        document=price_file,
        caption="Вот наш прайс-лист на товары и услуги.",
        reply_markup=main_keyboard,
    )
