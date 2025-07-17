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

info_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Услуги", callback_data="info_services"),
        ],
        [
            InlineKeyboardButton(text="Цены", callback_data="info_prices"),
        ],
        [
            InlineKeyboardButton(text="Гарантии", callback_data="info_warranties"),
        ],
    ]
)
