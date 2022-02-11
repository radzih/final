from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

share_invite_link_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Поделиться ссылкой', switch_inline_query='Поделиться ссылкой'),
            InlineKeyboardButton(text='Назад', callback_data='back_to_menu'),
        ]
    ]
)
