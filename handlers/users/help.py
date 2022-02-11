from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandHelp

from loader import dp
from states import Loginned


@dp.message_handler(CommandHelp(),state=Loginned.Log)
async def bot_help(message: types.Message):
    text = ("Список команд: ",
            "/help - Получить справку",
            "/menu - Показать меню")
    
    await message.answer("\n".join(text))
