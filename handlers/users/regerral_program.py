from aiogram import types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config
from keyboards.inline import share_invite_link_kb
from loader import dp, bot, db


@dp.callback_query_handler(text='referral_program')
async def show_referral_program(call: types.CallbackQuery):
    await call.answer()
    referral_link = f't.me/{config.BOT_USERNAME}?start={call.from_user.id}'
    sql_output = await db.get_balance(call.from_user.id)
    balance = sql_output[0]
    text = ('Вы можете получить бонусных 10$ за каждого приглашеного реферала, максимально 100$\n',
            f'Ваш баланс: {balance}$\n',
            'Ваш реферальный код:\n',
            f'<code>{call.from_user.id}</code>\n',
            'Ваша реферальная ссылка:\n',
            f'<code>{referral_link}</code>')

    await call.message.edit_text(''.join(text), reply_markup=share_invite_link_kb)


@dp.inline_handler(text='Поделиться ссылкой')
async def show_referral_link(query: types.InlineQuery):
    query_text = query.query
    referral_link = f't.me/{config.BOT_USERNAME}?start={query.from_user.id}'
    message_text = f'Привет, приглашаю тебя посмотреть телеграм магазин\n{referral_link}'

    await query.answer(
        results=[
            types.InlineQueryResultArticle(
                id="1",
                title="Нажмите сюда чтобы отправить ссылку-приглашение",
                input_message_content=types.InputTextMessageContent(
                    message_text=''.join(message_text),
                    parse_mode="HTML"
                )
            )

        ]
    )