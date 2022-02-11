from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, CommandStart

from filters.isregistered import IsRegistered
from keyboards.inline.menu import get_menu_kb
from loader import dp

@dp.message_handler(CommandStart(deep_link=''), IsRegistered())
@dp.callback_query_handler(text='back_to_menu', state='*')
@dp.message_handler(Command('menu'), IsRegistered())
async def show_menu(message: types.Message or types.CallbackQuery, state: FSMContext = None):
    menu_kb = await get_menu_kb(message.from_user.id)
    if isinstance(message, types.CallbackQuery):
        if state:
            await state.finish()
        await message.message.edit_text(text='Меню магазина', reply_markup=menu_kb)
    else:
        await message.answer(text='Меню магазина', reply_markup=menu_kb)

# @dp.callback_query_handler(text='cancel', state='write_question')
# @dp.callback_query_handler(text='cancel', state='view_questions')
