from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hcode, hbold

from keyboards.inline import get_menu_kb
from keyboards.inline.support import make_support_kb, no_questions_kb, confirm_sending_quest_kb, \
    confirm_sending_answer_kb, back_to_support_kb
from loader import dp, db, bot


@dp.callback_query_handler(text='support')
async def get_help(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state('write_question')
    text = 'Напишите свой вопрос и менеджер вам ответит'
    await call.message.edit_text(''.join(text), reply_markup=no_questions_kb)


@dp.message_handler(state='write_question')
async def get_question(message: types.Message, state: FSMContext):
    question = message.text
    text = ('Ваш вопро будет выглядить так: \n',
            f'<code>{hcode(question)}</code>\n',
            'Отправлять?')
    await state.update_data(question=question)
    await message.answer(''.join(text),
                         reply_markup=confirm_sending_quest_kb)


@dp.callback_query_handler(text='send', state='write_question')
async def accept_question(call: types.CallbackQuery, state: FSMContext):
    await call.answer('Отправлено')
    state_data = await state.get_data()
    question = state_data['question']
    await db.add_new_question(user_id=call.from_user.id, question=question)
    await state.finish()
    menu_kb = await get_menu_kb(call.from_user.id)
    await call.message.edit_text(text='Меню магазина', reply_markup=menu_kb)


async def make_message(num_quest: int, total_quest: int, data: list):
    text = (f"Питання {num_quest}/{total_quest}\n"
            f"{data[2]}")
    return text


# Админская часть


@dp.callback_query_handler(text='support_panel')
@dp.callback_query_handler(text="back_to_support", state="answer_to_question")
@dp.message_handler(text='/support')
async def show_all_questions(message: types.Message or CallbackQuery,
                             state: FSMContext, call=None):
    if isinstance(message, CallbackQuery):
        call = message
    if call:
        await message.answer()
        if await state.get_state():
            await state.finish()
    sql_output = [item[0] for item in await db.get_questions()]
    if sql_output:
        first_row = sql_output[0]
        user_id = first_row[1]
        pk = first_row[0]
        text = await make_message(1, len(sql_output), first_row)
        support_kb = await make_support_kb(1, len(sql_output), user_id, pk)
        if call:
            await call.message.edit_text(text=text, reply_markup=support_kb)
        elif message:
            await message.answer(text=text, reply_markup=support_kb)
        await state.set_state('view_questions')
        await state.update_data(num_quest=0)
    else:
        if call:
            await call.message.edit_text(text='Вопросов нет', reply_markup=no_questions_kb)
        elif message:
            await message.answer(text='Вопросов нет', reply_markup=no_questions_kb)


@dp.callback_query_handler(text='next', state='view_questions')
async def show_next_question(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    sql_output = [item[0] for item in await db.get_questions()]

    state_data = await state.get_data()
    num_quest = state_data['num_quest']
    num_quest += 1
    question_data = sql_output[num_quest]
    user_id = question_data[1]
    pk = question_data[0]
    await state.update_data(num_quest=num_quest)
    text = await make_message(num_quest + 1, len(sql_output), question_data)
    support_kb = await make_support_kb(num_quest + 1, len(sql_output), user_id, pk)
    await call.message.edit_text(text=text, reply_markup=support_kb)


@dp.callback_query_handler(text='previous', state='view_questions')
async def show_previous_question(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    sql_output = [item[0] for item in await db.get_questions()]
    state_data = await state.get_data()
    num_quest = state_data['num_quest']
    num_quest -= 1
    question_data = sql_output[num_quest]
    user_id = question_data[1]
    pk = question_data[0]
    await state.update_data(num_quest=num_quest)
    text = await make_message(num_quest + 1, len(sql_output), question_data)
    support_kb = await make_support_kb(num_quest + 1, len(sql_output), user_id, pk)
    await call.message.edit_text(text=text, reply_markup=support_kb)


@dp.callback_query_handler(text_contains="answer", state="view_questions")
async def answer(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.set_state("answer_to_question")
    callback_data = call.data
    user_id = callback_data.split(":")[1]
    pk = int(callback_data.split(":")[2])
    await state.update_data(user_id=user_id, pk=pk)
    sql_output = await db.get_question(pk)
    question = sql_output[0]
    await call.message.edit_text(f'Напишите ответ на вопрос\n{hcode(question)}',reply_markup=back_to_support_kb)


@dp.message_handler(state="answer_to_question")
async def confirm_answer(message: types.Message, state: FSMContext):
    answer_to_question = message.text
    await state.update_data(answer=answer_to_question)
    text = ("Ваш ответ будет выглядить так:\n"
            f"{hbold(answer_to_question)}\n"
            "Отправлять ответ?")
    await message.answer(text=''.join(text),
                         reply_markup=confirm_sending_answer_kb)


@dp.callback_query_handler(text="send", state="answer_to_question")
async def send_answer_to_question(call: types.CallbackQuery, state: FSMContext):
    await call.answer('Отправлено')
    state_data = await state.get_data()
    user_id = state_data["user_id"]
    answer_to_question = state_data["answer"]
    pk = int(state_data["pk"])
    sql_output = await db.get_question(pk)
    question = sql_output[0]
    text = (f"Ответ на ваш вопрос\n {hcode(question)}\n"
            "Таков:\n"
            f"{hbold(answer_to_question)}")
    await bot.send_message(chat_id=user_id, text=''.join(text))
    await db.delete_question_from_database(pk)
    await state.finish()
    await show_all_questions(call, state)

