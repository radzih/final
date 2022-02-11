import json

import aiogram
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import InputFile
from aiogram.utils.exceptions import CantParseEntities

from keyboards.inline import admin_panel_kb
from keyboards.inline.admin_panel import send_spam_kb, error_parse_html_kb
from loader import dp, db, bot


@dp.callback_query_handler(text='admin_panel', state="*")
async def show_admin_panel(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.answer()
    try:
        await call.message.edit_text('Административная панель', reply_markup=admin_panel_kb)
    except aiogram.utils.exceptions.BadRequest:
        await call.message.answer('Административная панель', reply_markup=admin_panel_kb)


@dp.callback_query_handler(text='spam')
async def enter_message_to_spam(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('Напишите сообщение которое нужно отправить')
    await state.set_state('write_message')


@dp.message_handler(state='write_message')
async def confirm_message(message: types.Message, state: FSMContext):
    message_to_send = message.text
    await state.update_data(message=message_to_send)
    text = ('Ваше сообщение будет выглядить так: \n',
            f'{message_to_send}\n',
            'Отправлять?')
    try:
        await message.answer(''.join(text),
                             reply_markup=send_spam_kb)
    except CantParseEntities:
        await message.answer('Ошибка парсинга html тегов,\nПроверьте правильность ввода',
                             reply_markup=error_parse_html_kb)
        await state.finish()


@dp.callback_query_handler(text='send', state='write_message')
async def send_message_to_all(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('Делаю рассылку')
    sql_output = await db.get_all_users_ids()
    users_ids = [user_id[0] for user_id in sql_output]
    state_data = await state.get_data()
    message = state_data['message']

    for user_id in users_ids:
        await bot.send_message(chat_id=user_id, text=message)
    await state.finish()
    await show_admin_panel(call, state)


@dp.callback_query_handler(text="get_orders")
async def send_orders(call: types.CallbackQuery):

    sql_output = await db.get_all_orders()
    orders = []
    for i in sql_output:
        orders.append(i[0])
    if len(orders) == 0:
        await call.answer("Нету заказов")
    else:
        await call.answer()
        with open("json/orders.json", 'w') as file:
            json.dump(orders, file)
        json_file = InputFile("json/orders.json")
        await call.message.answer_document(document=json_file, caption=f"#orders")
