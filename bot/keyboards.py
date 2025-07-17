from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Заказать звонок", callback_data="order_call"),
        ],
        [
            InlineKeyboardButton(text="Информация", callback_data="info"),
        ],
        [
            InlineKeyboardButton(text="Контакты", callback_data="contacts"),
        ],
    ]
)
