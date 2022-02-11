from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config


async def get_menu_kb(user_id: str):
    menu_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Каталог', switch_inline_query_current_chat=''),
                InlineKeyboardButton(text='Обратная связь', callback_data='support')
            ],
            [
                InlineKeyboardButton(text='Реферальная програма', callback_data='referral_program'),
            ]
        ]
    )
    if str(user_id) in config.ADMINS:
        menu_kb.add(InlineKeyboardButton(
            text='Административная панель',
            callback_data='admin_panel'
        ))
    if str(user_id) in config.SUPPORT:
        menu_kb.add(InlineKeyboardButton(
            text='Помощь покупателям',
            callback_data='support_panel'
        ))
    return menu_kb
