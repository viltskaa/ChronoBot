from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.utils.formatting import as_section, as_key_value, as_marked_list

from bot.keyboards.inline import simple_menu_keyboard, my_orders_keyboard, \
    OrderCallbackData

menu_router = Router()


@menu_router.message(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Select one of element", reply_markup=simple_menu_keyboard())


# We can use F.data filter to filter callback queries by data field from CallbackQuery object
@menu_router.callback_query(F.data == "create_order")
async def create_order(query: CallbackQuery):
    # Firstly, always answer callback query (as Telegram API requires)
    await query.answer()

    # This method will send an answer to the message with the button, that user pressed
    # Here query - is a CallbackQuery object, which contains message: Message object
    await query.message.answer("Selected")

    # You can also Edit the message with a new text
    # await query.message.edit_text("Selected")


# Let's create a simple list of orders for demonstration purposes
ORDERS = [
    {"id": 1, "title": "Title 1", "status": "1"},
    {"id": 2, "title": "Title 2", "status": "2"},
    {"id": 3, "title": "Title 3", "status": "3"},
]


@menu_router.callback_query(F.data == "my_orders")
async def my_orders(query: CallbackQuery):
    await query.answer()
    await query.message.edit_text("Selected",
                                  reply_markup=my_orders_keyboard(ORDERS))


# To filter the callback data, that was created with CallbackData factory, you can use .filter() method
@menu_router.callback_query(OrderCallbackData.filter())
async def show_order(query: CallbackQuery, callback_data: OrderCallbackData):
    await query.answer()

    # You can get the data from callback_data object as attributes
    order_id = callback_data.order_id

    # Then you can get the order from your database (here we use a simple list)
    order_info = next((order for order in ORDERS if order["id"] == order_id), None)

    if order_info:
        # Here we use aiogram.utils.formatting to format the text
        # https://docs.aiogram.dev/en/latest/utils/formatting.html
        text = as_section(
            as_key_value("Selected #", order_info["id"]),
            as_marked_list(
                as_key_value("Order", order_info["title"]),
                as_key_value("Status", order_info["status"]),
            ),
        )
        # Example:
        # Замовлення #: 2
        # - Товар: Замовлення 2
        # - Статус: Виконано

        await query.message.edit_text(text.as_html(), parse_mode=ParseMode.HTML)

        # You can also use MarkdownV2:
        # await query.message.edit_text(text.as_markdown(), parse_mode=ParseMode.MARKDOWN_V2)
    else:
        await query.message.edit_text("Not Found!")
