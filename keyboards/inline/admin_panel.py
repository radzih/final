from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

admin_panel_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Выгрузить заказы', callback_data='get_orders')
        ],
        [
            InlineKeyboardButton(text='Добавить товар', callback_data='add_item'),
            InlineKeyboardButton(text='Рассылка', callback_data='spam')
        ],
        [
            InlineKeyboardButton(text="Главное меню", callback_data='back_to_menu')
        ]
    ]
)

send_spam_kb = InlineKeyboardMarkup(
    inline_keyboard=
    [
        [
            InlineKeyboardButton(text='Отправить', callback_data='send'),
            InlineKeyboardButton(text='Отмена', callback_data='admin_panel')
        ]

    ]
)

error_parse_html_kb = InlineKeyboardMarkup(
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text='Написать заново', callback_data='spam'),
                                         InlineKeyboardButton(text='Назад', callback_data='admin_panel')
                                     ]
                                 ]
                             )