from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

i_subscribed_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Я подписался',
                                 callback_data='i_subscribied'),
            InlineKeyboardButton(text='Ввести код приглашения',
                                 callback_data='enter_invite_code')
        ]
    ]
)
no_access_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Ввести код приглашения',
                                 callback_data='enter_invite_code')
        ],
        [
            InlineKeyboardButton(text='Вступить в канал',
                                 callback_data='join_to_channel')
        ]

    ])

reenter_code_or_join_channel_kb = InlineKeyboardMarkup(
                                 inline_keyboard=[
                                     [
                                         InlineKeyboardButton(text='Вступить в канал',
                                                              callback_data='join_to_channel'),

                                         InlineKeyboardButton(text='Ввести код приглашения еще раз',
                                                              callback_data='reenter_code')
                                     ]
                                 ]
                             )