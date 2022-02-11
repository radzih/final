from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from data import config


def show_item_kb(show_item_link):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Показать товар',
                                     url=show_item_link)
            ]
        ]
    )


buy_callback = CallbackData("buy", "item_id")
edit_callback = CallbackData("edit", "item_id")
delete_callback = CallbackData("delete", "item_id")


def buy_item_kb(id, user_id):
    buy_item_kb = InlineKeyboardMarkup()

    buy_item_kb.add(InlineKeyboardButton(text='Купить товар', callback_data=buy_callback.new(item_id=id)),
                    InlineKeyboardButton(text='Поделиться товаром', switch_inline_query=f"item:{id}"))
    buy_item_kb.add(InlineKeyboardButton(text="Меню",callback_data='back_to_menu'))
    if str(user_id) in config.ADMINS:
        buy_item_kb.add(InlineKeyboardButton(text="Редактировать", callback_data=edit_callback.new(item_id=id)),
                        InlineKeyboardButton(text="Удалить товар", callback_data=delete_callback.new(item_id=id))
                        )

    return buy_item_kb
