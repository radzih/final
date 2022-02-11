from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

go_to_admin_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Отмена", callback_data="admin_panel")
        ]
    ]
)

confirm_adding_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Сохранить", callback_data='save'),
            InlineKeyboardButton(text="Отменить", callback_data='admin_panel')
        ]
    ]
)
