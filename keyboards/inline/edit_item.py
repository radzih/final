from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from keyboards.inline import edit_callback

what_edit_callback = CallbackData("change", "what_edit", "item_id")
back_to_item_callback = CallbackData("back", "item_id")


def choose_what_edit(item_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Изменить название',
                                     callback_data=what_edit_callback.new(what_edit='item_name', item_id=item_id)),
                InlineKeyboardButton(text='Изменить цену',
                                     callback_data=what_edit_callback.new(what_edit="price", item_id=item_id))
            ],
            [
                InlineKeyboardButton(text="Изменить описание",
                                     callback_data=what_edit_callback.new(what_edit="description", item_id=item_id)),
                InlineKeyboardButton(text="Изменить фото",
                                     callback_data=what_edit_callback.new(what_edit="photo", item_id=item_id))
            ],
            [
                InlineKeyboardButton(text="Назад", callback_data=back_to_item_callback.new(item_id=item_id))
            ]
        ]
    )


def back_to_edit_kb(item_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="Отмена", callback_data=edit_callback.new(item_id=item_id))
            ]
        ]
    )


confirm_change_info_callback = CallbackData('confirm', 'item_id', "what_change", "new_value")


def confirm_change(item_id, what_change,new_value):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='Сохранить',
                                     callback_data=confirm_change_info_callback.new(item_id=item_id,
                                                                                    what_change=what_change,
                                                                                    new_value=new_value)),
                InlineKeyboardButton(text='Отмена',
                                     callback_data=edit_callback.new(item_id=item_id))
            ]
        ]
    )
