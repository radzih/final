import logging
import re

from aiogram import types
from aiogram.dispatcher.filters import CommandStart
from aiogram.utils.markdown import hbold
from data import config
from filters import TextIsNotNone
from filters.isregistered import IsRegistered
from handlers.users.menu import show_menu
from keyboards.inline.catalog import show_item_kb, buy_item_kb
from keyboards.inline.edit_item import back_to_item_callback
from loader import dp, db


async def make_list_items(sql_output):
    results = []
    for row in sql_output:
        id = row[0]
        item_name = row[1]
        price = f"{row[2]}$"
        description = row[3]
        photo_link = row[4]
        show_item_link = f't.me/{config.BOT_USERNAME}?start=item{id}'
        result_text = (f"{hbold(item_name)}\n",
                       f"<b><i>Цена: {price}</i></b>",
                       f"<a href='{photo_link}'>.</a>")
        results.append(types.InlineQueryResultArticle(id=id,
                                                      title=item_name,
                                                      description=price,
                                                      thumb_url=photo_link,
                                                      input_message_content=types.InputTextMessageContent(
                                                          message_text=''.join(result_text),
                                                          parse_mode="HTML"

                                                      ),
                                                      reply_markup=show_item_kb(show_item_link)
                                                      ))
    return results


@dp.inline_handler(IsRegistered(), text='')
async def show_sort_items(query: types.InlineQuery):
    query_text = query.query
    logging.info('asd')
    sql_output = await db.show_sort_items()
    results = await make_list_items(sql_output)
    await query.answer(results=results)


@dp.inline_handler(IsRegistered(), TextIsNotNone())
async def show_item_list(query: types.InlineQuery):
    query_text = query.query
    sql_output = await db.show_items(query_text)

    results = await make_list_items(sql_output)

    await query.answer(results=results)


@dp.callback_query_handler(back_to_item_callback.filter())
@dp.message_handler(CommandStart(deep_link=re.compile(r"item\d+")))
async def show_item(message: types.Message or types.CallbackQuery, callback_data: dict = None):
    if isinstance(message, types.Message):
        item_id = int(message.get_args().replace('item', ''))
    else:
        item_id = int(callback_data['item_id'])
    sql_output = await db.get_item_by_id(item_id)
    if sql_output is None:
        if isinstance(message, types.Message):
            await message.answer(text='Такого товара нет', )
            await show_menu(message)
        else:
            await message.message.edit_text(text='Такого товара нет',
                                            )
            await show_menu(message)

    else:
        item_name = sql_output[1]
        price = sql_output[2]
        description = sql_output[3]
        photo_link = sql_output[4]
        text = (f"<b>{item_name}</b>\n"
                f"<b><i>Цена: {price}$</i></b>\n"
                f"<i>{description}</i>"
                f"<a href='{photo_link}'>.</a>")
        if isinstance(message, types.Message):
            await message.answer(text=''.join(text),
                                 reply_markup=buy_item_kb(item_id, message.from_user.id)
                                 )
        else:
            await message.message.edit_text(text=''.join(text),
                                            reply_markup=buy_item_kb(item_id, message.from_user.id))

# @dp.callback_query_handler(text_contains="buy")
# async def
