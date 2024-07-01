from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from bot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())


@admin_router.message(CommandStart())
async def admin_start(message: Message):
    await message.reply("Hi, admin!")
