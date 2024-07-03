from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message

from bot.keyboards.reply import get_goods_keyboard
from infrastructure.wb_api.wb_api import WBApi

user_router = Router()


class Form(StatesGroup):
    api_key = State()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Hi", reply_markup=get_goods_keyboard())


@user_router.message(lambda message: message.text == "Получить информацию о товарах")
async def request_api_key(message: Message, state: FSMContext):
    await message.reply("Пожалуйста, введите ваш API ключ:")
    await state.set_state(Form.api_key)


@user_router.message(Form.api_key)
async def handle_api_key(message: Message, state: FSMContext):
    api_key = message.text
    await state.update_data(api_key=api_key)

    api = WBApi(api_key=api_key)

    try:
        data = await api.get_goods(limit_goods=1000, offset_goods=0)
        formatted_data = format_goods_data(data)
        messages = split_message(formatted_data)
        for msg in messages:
            await message.reply(msg)
    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")
    finally:
        await api.close()

    await state.clear()


def format_goods_data(data: dict) -> str:
    items = data.get('data', {}).get('listGoods', [])
    formatted_data = ""

    for item in items:
        vendor_code = item.get('vendorCode', 'N/A')
        discount = item.get('discount', 'N/A')
        sizes = item.get('sizes', [])

        sizes_info = "\n".join(
            [f"Цена: {size.get('price', 'N/A')} руб., "
             f"Цена со скидкой: {size.get('discountedPrice', 'N/A')} руб." for size in sizes])

        formatted_data += (
            f"Артикул: {vendor_code}\n"
            f"Скидка: {discount}%\n"
            f"Размеры и цены:\n{sizes_info}\n\n"
        )

    return formatted_data.strip()


def split_message(message: str, max_length: int = 4096) -> list[str]:
    """Split a message into chunks of max_length."""
    chunks = []
    while len(message) > max_length:
        split_pos = message.rfind('\n', 0, max_length)
        if split_pos == -1:
            split_pos = max_length
        chunks.append(message[:split_pos])
        message = message[split_pos:].lstrip()
    chunks.append(message)
    return chunks
