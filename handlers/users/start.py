from re import compile

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.builtin import CommandStart

from data import config
from filters import NotRegistered
from handlers.users.menu import show_menu
from keyboards.inline import no_access_kb, i_subscribed_kb
from keyboards.inline.start import reenter_code_or_join_channel_kb
from loader import dp, db, bot


@dp.message_handler(CommandStart(deep_link=''), NotRegistered())
async def bot_start(message: types.Message, state: FSMContext):
    user_channel_status = await bot.get_chat_member(chat_id=f'@{config.CHANNEL_USERNAME}', user_id=message.from_user.id)
    if user_channel_status["status"] != 'left':
        await db.register_user(referral_id=config.CHANNEL_ID, referred_id=message.from_user.id)
        await show_menu(call)
        return
    await message.answer('Ошибка\n'
                         'У вас нет доступа\n'
                         'Чтобы использовать бота введите код приглашения,'
                         ' или перейдите по реферальной ссылке или вступите в групу',
                         reply_markup=no_access_kb)


@dp.message_handler(CommandStart(deep_link=compile(r'\d+')), NotRegistered())
async def check_deep_link(message: types.Message):
    try:
        deep_link_args = int(message.get_args())
        data = await db.check_user_or_register_referral(deep_link_args)
    except ValueError:
        data = None

    if data is None:
        await message.answer('Ошибка\n'
                             'Такая реферальная ссылка не найдена,\n'
                             'Можете ввести код приглашения вручную или вступите в групу',
                             reply_markup=no_access_kb)

    else:

        referral_id = data[0]
        referral_info = await bot.get_chat_member(referral_id, referral_id)
        referral_name = referral_info["user"]["first_name"]
        await message.answer(f'Поздравляю вас пригласил <a href=\"tg://user?id={referral_id}\">{referral_name}</a>'
                             f', вы можете использовать бота,\n')
        await db.register_user(referral_id=referral_id, referred_id=message.from_user.id)
        balance = await db.get_balance(referral_id)
        if balance < 100:
            await db.add_10_dollars(user_id=referral_id)
        await show_menu(message)



@dp.callback_query_handler(text='reenter_code')
@dp.callback_query_handler(text='enter_invite_code')
async def get_invite_code(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text('Введите код приглашения')
    await state.set_state('get_invite_code_or_subscribe')


@dp.callback_query_handler(text='join_to_channel')
async def get_invite_code(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    await state.finish()
    await call.message.edit_text(f'Подпишитесь на <a href=\'https://t.me/{config.CHANNEL_USERNAME}\'>наш</a> канал',
                                 reply_markup=i_subscribed_kb)


@dp.message_handler(state='get_invite_code_or_subscribe')
async def check_invite_code(message: types.Message, state: FSMContext):
    try:
        invite_code = int(message.text)
        data = await db.check_user_or_register_referral(invite_code=invite_code)
    except ValueError:
        data = None
    if data is None:
        await state.finish()
        await message.answer('Такого кода не существует, проверьте правильность ввода,\n'
                             'или вступите в канал',
                             reply_markup=reenter_code_or_join_channel_kb)



    else:
        await state.finish()
        referral_id = data[0]
        referral_info = await bot.get_chat_member(referral_id, referral_id)
        referral_name = referral_info["user"]["first_name"]
        await db.register_user(referral_id=referral_id, referred_id=message.from_user.id)
        balance = await db.get_balance(referral_id)
        if balance < 100:
            await db.add_10_dollars(user_id=referral_id)
        await message.answer(f'Поздравляю вас пригласил <a href=\"tg://user?id={referral_id}\">{referral_name}</a>'
                             f', вы можете использовать бота,\n')

        await show_menu(message)

@dp.callback_query_handler(text='i_subscribied')
async def check_subs(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    user_channel_status = await bot.get_chat_member(chat_id=f'@{config.CHANNEL_USERNAME}', user_id=call.from_user.id)
    if user_channel_status["status"] != 'left':
        await db.register_user(referral_id=config.CHANNEL_ID, referred_id=call.from_user.id)
        await show_menu(call)


    else:
        await call.message.edit_text('Мы не видим что вы подписались на '
                                     f'<a href=\'https://t.me/{config.CHANNEL_USERNAME}\'>наш</a> канал',
                                     reply_markup=i_subscribed_kb)
