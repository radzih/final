from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

payment_callback = CallbackData('pay', "pay_by", "item_id")


def what_payment(item_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Telegram Payments', callback_data=payment_callback.new(pay_by='telegram',
                                                                                                  item_id=item_id)),
                InlineKeyboardButton(text='QIWI', callback_data=payment_callback.new(pay_by='qiwi',
                                                                                     item_id=item_id))
            ]
        ]
    )
