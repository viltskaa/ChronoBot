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
    cart = State()
    cart_one = State()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.reply("Hi", reply_markup=get_goods_keyboard())


@user_router.message(lambda message: message.text == "k")
async def request_check_key(message: Message, state: FSMContext):
    if await get_key(state) is None:
        await message.reply("Ключ не задан")
        return
    await message.reply(f"Текущий ключ: {get_key(state)}")


# @user_router.message(Form.api_key)
async def request_set_key(message: Message, state: FSMContext):
    api_key = message.text
    await state.clear()
    await state.update_data(api_key=api_key)


# @user_router.message(lambda message: message.text == "Сколько в корзинах")
@user_router.message(lambda message: message.text == "c")
async def request_api_key(message: Message, state: FSMContext):
    if await get_key(state) is None:
        await message.answer("Пожалуйста, введите ваш API ключ:")
        await state.set_state(Form.cart)
    else:
        await message.reply("Ключ задан")


@user_router.message(lambda message: message.text == "c1")
async def request_api_key(message: Message, state: FSMContext):
    await message.answer("Введите артикул")
    await state.set_state(Form.cart_one)


@user_router.message(Form.cart_one)
async def handle_cart_one(message: Message, state: FSMContext):
    api_key = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczMDQxNjIyNCwiaWQiOiIzNDRlMzA1Ni1jMDU4LTQxMmEtODk3Zi1kZjJkYTdiNDdiYjQiLCJpaWQiOjQ1ODkwNDkwLCJvaWQiOjg5NzE2NiwicyI6MTAyMiwic2lkIjoiMTZhMGZiZWEtYWVmZi00YjgxLThmNzEtZjYyZDlhYjJmMGM1IiwidCI6ZmFsc2UsInVpZCI6NDU4OTA0OTB9.QL4J2FabaLOHCdPovbyaUWKw28VdRbruv-PY1m5tLhWea_0DEcExywqEvwcRAiHfQyNOydOJe2biakFg68iH9Q'
    await state.update_data(api_key=api_key)
    api = WBApi(api_key=api_key)

    try:
        # article = message.text
        article = 'RO03'
        data = await api.get_goods(limit_goods=1000, offset_goods=0)
        nmid = get_id_from_article(data, article)

        if nmid is None:
            await message.reply("Некорректный артикул")
            return

        res = await api.get_nm_report([int(nmid)])
        forms = format_cart(res)
        await message.reply(forms)

    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")
    finally:
        await api.close()

    await state.clear()


@user_router.message(Form.cart)
async def handle_cart(message: Message, state: FSMContext):
    # api_key = message.text
    api_key = 'eyJhbGciOiJFUzI1NiIsImtpZCI6IjIwMjQwMjI2djEiLCJ0eXAiOiJKV1QifQ.eyJlbnQiOjEsImV4cCI6MTczMDQxNjIyNCwiaWQiOiIzNDRlMzA1Ni1jMDU4LTQxMmEtODk3Zi1kZjJkYTdiNDdiYjQiLCJpaWQiOjQ1ODkwNDkwLCJvaWQiOjg5NzE2NiwicyI6MTAyMiwic2lkIjoiMTZhMGZiZWEtYWVmZi00YjgxLThmNzEtZjYyZDlhYjJmMGM1IiwidCI6ZmFsc2UsInVpZCI6NDU4OTA0OTB9.QL4J2FabaLOHCdPovbyaUWKw28VdRbruv-PY1m5tLhWea_0DEcExywqEvwcRAiHfQyNOydOJe2biakFg68iH9Q'
    await state.update_data(api_key=api_key)

    api = WBApi(api_key=api_key)

    try:
        data = await api.get_goods(limit_goods=1000, offset_goods=0)
        ids = get_nm_id(data)
        ids = list(divide(ids))

        for id in ids:
            res = await api.get_nm_report(id)
            forms = format_cart(res)
            await message.reply(forms)

    except Exception as e:
        await message.reply(f"Произошла ошибка: {e}")
    finally:
        await api.close()

    await state.clear()


# @user_router.message(lambda message: message.text == "Получить информацию о товарах")
@user_router.message(lambda message: message.text == "G")
async def request_api_key(message: Message, state: FSMContext):
    if await get_key(state) is None:
        await message.answer("Пожалуйста, введите ваш API ключ:")
        await state.set_state(Form.api_key)
    else:
        await message.reply("Ключ задан")


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


def get_nm_id(data: dict) -> list[int]:
    items = data.get('data', {}).get('listGoods', [])
    ids = []
    for item in items:
        ids.append(item.get('nmID'))

    return ids


def get_id_from_article(data: dict, article: str) -> str | None:
    items = data.get('data', {}).get('listGoods', [])

    for item in items:
        if item.get('vendorCode') == article:
            return item.get('nmID')

    return None


def divide(ids: list[int]):
    for i in range(0, len(ids), 20):
        yield ids[i:i + 20]


def format_cart(data: dict) -> str:
    items = data.get('data', [])
    formatted_data = ""

    for item in items:
        vendor_code = item.get('vendorCode', 'N/A')
        history: list = item.get('history', [])

        kol = "\n".join(
            [f"{_.get('addToCartCount', 'N/A')} руб." for _ in history])

        formatted_data += (
            f"Артикул: {vendor_code}\n"
            f"Положили в корзину: {kol} штук \n\n"
        )

    return formatted_data.strip()


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


async def get_key(state: FSMContext):
    data = await state.get_data()
    return data.get('api_key')





