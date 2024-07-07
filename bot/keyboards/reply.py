from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def get_data_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="Посмотреть все цены"),
            KeyboardButton(text="Посмотреть все корзины"),
            KeyboardButton(text="Посмотреть данные по артикулу"),
            KeyboardButton(text="Изменить API ключ")
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard


def by_article_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="Посмотреть цену"),
            KeyboardButton(text="Посмотреть корзины"),
            KeyboardButton(text="Добавить расписание"),
            KeyboardButton(text="Изменить артикул"),
            KeyboardButton(text="Вернуться")
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard

def set_api_keyboard() -> ReplyKeyboardMarkup:
    buttons = [
        [
            KeyboardButton(text="Установить API ключ"),
            KeyboardButton(text="Проверить API ключ")
        ],
    ]

    keyboard = ReplyKeyboardMarkup(
        keyboard=buttons,
        resize_keyboard=True
    )
    return keyboard
