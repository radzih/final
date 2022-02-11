from aiogram import types
from aiogram.utils.markdown import hbold

from data import config
from filters import ShareItem
from keyboards.inline import show_item_kb
from loader import dp, db, bot


@dp.inline_handler(ShareItem())
async def send_item(query: types.InlineQuery):

    id = query.query.split(':')[-1]
    id = int(id)
    sql_output = await db.get_item_by_id(id)
    if sql_output:



        item_name = sql_output[1]

        price = f"{sql_output[2]}$"
        description = sql_output[3]
        photo_link = sql_output[4]
        show_item_link = f't.me/{config.BOT_USERNAME}?start=item{id}'
        result_text = (f"{hbold(item_name)}\n",
                       f"<b><i>Цена: {price}</i></b>\n",
                       f"{description}",
                       f"<a href='{photo_link}'>.</a>")

        results = [types.InlineQueryResultArticle(id='0',
                                                  title='Нажмите сюда чтобы поделиться товаром',
                                                  input_message_content=types.InputTextMessageContent(
                                                      message_text=''.join(result_text),
                                                      parse_mode="HTML"

                                                  ),
                                                  reply_markup=show_item_kb(show_item_link)
                                                  )]
    else:
        return
    await query.answer(results=results)
