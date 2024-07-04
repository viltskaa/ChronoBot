from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_goods_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="Получить информацию о товарах"),
            KeyboardButton(text="test")
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard
