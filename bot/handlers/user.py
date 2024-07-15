from aiogram import Router
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message
import prettytable as pt

from bot.keyboards.reply import get_data_keyboard, set_api_keyboard, by_article_keyboard, yes_or_no_keyboard
from infrastructure.wb_api.wb_api import WBApi

user_router = Router()


class Form(StatesGroup):
    api_key = State()
    article = State()
    cost = State()
    discount = State()


@user_router.message(CommandStart())
async def user_start(message: Message):
    await message.answer("Добро пожаловать!", reply_markup=set_api_keyboard())


@user_router.message(lambda message: message.text == "Назад")
async def return_request(message: Message):
    await message.answer("Возвращение в меню для поиска информации по артикулу", reply_markup=by_article_keyboard())


@user_router.message(lambda message: message.text == "Посмотреть данные по артикулу")
async def set_article(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите артикул:")
    await state.set_state(Form.article)


@user_router.message(lambda message: message.text == "Изменить артикул")
async def update_article(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите новый артикул:")
    await state.set_state(Form.article)


@user_router.message(lambda message: message.text == "Изменить скидку и цену товара")
async def update_cost(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите новую цену товара:")
    await state.set_state(Form.cost)


@user_router.message(Form.cost)
async def update_discount(message: Message, state: FSMContext):
    cost = message.text
    await state.update_data(cost=cost)
    await message.answer("Пожалуйста, введите новую скидку товара:")
    await state.set_state(Form.discount)


@user_router.message(lambda message: message.text == "Вернуться в главное меню")
@user_router.message(lambda message: message.text == "Добавить расписание")
async def add_time_for_article(message: Message, state: FSMContext):
    article = await get_article(state)
    await message.answer(f"Пожалуйста, введите цену (в рублях) для артикля {article}:")
    await state.set_state(Form.article_price)


@user_router.message(Form.article_price)
async def set_article_price(message: Message, state: FSMContext):
    price = float(message.text)
    await state.update_data(price=price)
    current_price = await get_price(state)
    article = await get_article(state)
    await message.answer(f"Введите время начала действия цены ({current_price} р) для артикля {article}:")
    await state.set_state(Form.article_time_start)


@user_router.message(Form.article_time_start)
async def set_article_time_start(message: Message, state: FSMContext):
    time = datetime.strptime(message.text, '%H:%M')
    await state.update_data(time=time)
    current_time = await get_time(state)
    article = await get_article(state)
    price = await get_price(state)
    await message.answer(f"Новое правило для артикля {article} : с {current_time.strftime('%H:%M')} цена {price}")
    await state.set_state(Form.article_time_start)


@user_router.message(lambda message: message.text == "Вернуться")
async def return_request(message: Message):
    await message.answer("Возвращение в главное меню", reply_markup=get_data_keyboard())


@user_router.message(lambda message: message.text == "Посмотреть корзины")
async def get_cart_by_article(message: Message, state: FSMContext):
    api = None

    try:
        current_key = await get_key(state)
        api = WBApi(api_key=current_key)
        current_article = await get_article(state)
        data = await api.get_goods(limit_goods=1000, offset_goods=0)
        nm_id = get_id_from_article(data, current_article)

        if nm_id is None:
            await message.reply("Некорректный артикул")
            return

        res = await api.get_nm_report([int(nm_id)])
        forms = format_cart(res)
        await message.reply(forms)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        await api.close()


@user_router.message(lambda message: message.text == "Посмотреть цену")
async def get_good_by_article(message: Message, state: FSMContext):
    api = None

    try:
        current_key = await get_key(state)
        api = WBApi(api_key=current_key)
        current_article = await get_article(state)
        data = await api.get_goods(limit_goods=1000, offset_goods=0)
        nm_id = get_id_from_article(data, current_article)

        if nm_id is None:
            await message.reply("Некорректный артикул")
            return

        res = await api.get_goods(limit_goods=1000, offset_goods=0, filter_nm_id=nm_id)
        forms = format_goods_data(res)
        messages = split_message(forms)
        for msg in messages:
            await message.reply(msg, parse_mode=ParseMode.HTML)
        await message.answer("Хотите изменить цену и скидку товара?", reply_markup=yes_or_no_keyboard())

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        await api.close()


@user_router.message(Form.discount)
async def get_good_by_article(message: Message, state: FSMContext):
    api = None

    try:
        current_key = await get_key(state)
        api = WBApi(api_key=current_key)
        current_article = await get_article(state)
        current_cost = int(await get_cost(state))
        discount = message.text
        await state.update_data(discount=discount)
        current_discount = int(await get_discount(state))
        data = await api.get_goods(limit_goods=1000, offset_goods=0)
        nm_id = int(get_id_from_article(data, current_article))

        if nm_id is None:
            await message.reply("Некорректный артикул")
            return

        res = await api.change_cost(nm_id, current_cost, current_discount)
        if res['status'] != 200:
            await message.reply(f"Произошла ошибка: {res['title']}. {res['detail']}", reply_markup=by_article_keyboard())
        else:
            await message.reply("Цена успешно изменена!", reply_markup=by_article_keyboard())

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        await api.close()


@user_router.message(lambda message: message.text == "Посмотреть все корзины")
async def get_cart(message: Message, state: FSMContext):
    api = None

    try:
        current_key = await get_key(state)
        api = WBApi(api_key=current_key)
        data = await api.get_goods(limit_goods=1000, offset_goods=0)
        ids = get_nm_id(data)
        ids = list(divide(ids))

        for id in ids:
            res = await api.get_nm_report(id)
            forms = format_cart(res)
            await message.reply(forms)

    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        await api.close()


@user_router.message(lambda message: message.text == "Посмотреть все цены")
async def get_goods_info(message: Message, state: FSMContext):
    api = None

    try:
        current_key = await get_key(state)
        api = WBApi(api_key=current_key)
        data = await api.get_goods(limit_goods=1000, offset_goods=0)
        formatted_data = format_goods_data(data)
        messages = split_message(formatted_data)
        for msg in messages:
            await message.reply(msg, parse_mode=ParseMode.HTML)
    except Exception as e:
        await message.answer(f"Произошла ошибка: {e}")
    finally:
        await api.close()


@user_router.message(lambda message: message.text == "Проверить API ключ")
async def request_check_key(message: Message, state: FSMContext):
    current_key = await get_key(state)
    if current_key is None:
        await message.answer("API ключ не задан")
    else:
        await message.answer(f"Текущий API ключ: {current_key}")


async def get_key(state: FSMContext) -> str:
    data = await state.get_data()
    return data.get("api_key")


async def get_article(state: FSMContext) -> str:
    data = await state.get_data()
    return data.get("article")


async def get_cost(state: FSMContext) -> str:
    data = await state.get_data()
    return data.get("cost")


async def get_discount(state: FSMContext) -> str:
    data = await state.get_data()
    return data.get("discount")


async def get_time(state: FSMContext) -> datetime:
    data = await state.get_data()
    return data.get("time")


async def get_price(state: FSMContext) -> float:
    data = await state.get_data()
    return data.get("price")


@user_router.message(lambda message: message.text == "Установить API ключ")
async def set_api_key(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите ваш API ключ:")
    await state.set_state(Form.api_key)


@user_router.message(lambda message: message.text == "Изменить API ключ")
async def update_api_key(message: Message, state: FSMContext):
    await message.answer("Пожалуйста, введите новый API ключ:")
    await state.set_state(Form.api_key)


@user_router.message(Form.api_key)
async def confirm_api_key(message: Message, state: FSMContext):
    api_key = message.text
    await state.update_data(api_key=api_key)
    current_key = await get_key(state)
    await message.answer(f"API ключ успешно установлен: {current_key}", reply_markup=get_data_keyboard())


@user_router.message(Form.article)
async def confirm_article(message: Message, state: FSMContext):
    article = message.text.upper()
    await state.update_data(article=article)
    current_article = await get_article(state)
    await message.answer(f"Артикул успешно установлен: {current_article}", reply_markup=by_article_keyboard())


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

    table = pt.PrettyTable(['Артикул', 'Скидка', 'Цена', 'Цена со скидкой'])
    table.align['Артикул'] = 'l'
    table.align['Скидка'] = 'r'
    table.align['Цена'] = 'r'
    table.align['Цена со скидкой'] = 'r'

    for item in items:
        vendor_code = item.get('vendorCode', 'N/A')
        discount = item.get('discount', 'N/A')
        sizes = item.get('sizes', [])

        for size in sizes:
            price = size.get('price', 'N/A')
            discounted_price = size.get('discountedPrice', 'N/A')
            table.add_row([vendor_code, f'{discount}%', f'{price} руб.', f'{discounted_price} руб.'])

    return table.get_string()


def split_message(table_str: str, max_length: int = 4000) -> list[str]:
    lines = table_str.split('\n')
    header = '\n'.join(lines[:3])
    chunks = []
    current_chunk = header
    for line in lines[3:]:
        if len(current_chunk) + len(line) + 1 > max_length - len('<pre></pre>'):
            chunks.append(f"<pre>{current_chunk}</pre>")
            current_chunk = header
        current_chunk += '\n' + line
    chunks.append(f"<pre>{current_chunk}</pre>")
    return chunks
