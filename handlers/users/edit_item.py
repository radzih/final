from aiogram import types
from aiogram.dispatcher import FSMContext

from handlers.users.catalog import show_item
from handlers.users.menu import show_menu
from integrations.telegraph import FileUploader
from keyboards.inline.catalog import edit_callback, delete_callback
from keyboards.inline.edit_item import choose_what_edit, what_edit_callback, back_to_edit_kb, confirm_change, \
    confirm_change_info_callback
from loader import dp, db, bot


async def make_item_card(item_id):
    sql_output = await db.get_item_by_id(item_id)
    item_name = sql_output[1]
    price = sql_output[2]
    description = sql_output[3]
    photo_link = sql_output[4]
    return [f"<b>{item_name}</b>\n",
            f"<b><i>Цена: {price}$</i></b>\n",
            f"{description}",
            f"<a href='{photo_link}'>.</a>\n"]


@dp.callback_query_handler(delete_callback.filter())
async def delete_item(call: types.CallbackQuery, callback_data: dict):
    await call.answer("Удалено")
    item_id = int(callback_data["item_id"])
    print(await db.delete_item(item_id))
    await show_menu(call)
    await bot.get_updates()

@dp.callback_query_handler(edit_callback.filter(), state='*')
async def edit_item(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    await call.answer()
    item_id = int(callback_data['item_id'])
    text = await make_item_card(item_id)
    text.append(f"<b>Выберите что изменить</b>")
    await call.message.edit_text(text=''.join(text),
                                 reply_markup=choose_what_edit(item_id))

@dp.callback_query_handler(what_edit_callback.filter(what_edit='item_name'))
async def change_item_name(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    item_id = callback_data["item_id"]
    await call.message.edit_text("Введите новое название товара", reply_markup=back_to_edit_kb(item_id))
    await state.set_state("get_new_item_name")
    await state.update_data(item_id=item_id)


@dp.callback_query_handler(what_edit_callback.filter(what_edit='price'))
async def change_item_price(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    item_id = callback_data["item_id"]
    await call.message.edit_text("Введите новую цену товара", reply_markup=back_to_edit_kb(item_id))
    await state.set_state("get_new_price")
    await state.update_data(item_id=item_id)


@dp.callback_query_handler(what_edit_callback.filter(what_edit='description'))
async def change_item_description(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    item_id = callback_data["item_id"]
    await call.message.edit_text("Введите новое описание", reply_markup=back_to_edit_kb(item_id))
    await state.set_state("get_new_description")
    await state.update_data(item_id=item_id)


@dp.callback_query_handler(what_edit_callback.filter(what_edit='photo'))
async def change_item_photo(call: types.CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    item_id = callback_data["item_id"]
    await call.message.edit_text("Скиньте новое фото товара", reply_markup=back_to_edit_kb(item_id))
    await state.set_state("get_new_photo")
    await state.update_data(item_id=item_id)


@dp.message_handler(state="get_new_item_name")
async def get_new_item_name(message: types.Message, state: FSMContext):
    new_item_name = message.text
    state_data = await state.get_data()
    item_id = int(state_data['item_id'])
    if len(new_item_name) > 50:
        await message.answer(
            text="Название слишком длинное, его длина не должна превышать 50 символов\nВведите еще раз")
        return
    await state.finish()

    text = await make_item_card(item_id)

    text[0] = f"<b>{new_item_name}</b>\n"
    await message.answer(text=''.join(text),
                         reply_markup=confirm_change(item_id, "item_name", new_item_name))


@dp.message_handler(state='get_new_price')
async def get_new_price(message: types.Message, state: FSMContext):
    state_data = await state.get_data()
    item_id = int(state_data['item_id'])
    try:
        new_price = int(message.text)
    except ValueError:
        await message.answer("Вводите только цифры без знаков и пробелов\nВведите еще раз",
                             reply_markup=back_to_edit_kb(item_id))
        return
    await state.finish()
    text = await make_item_card(item_id)
    text[1] = f"<b><i>Цена: {new_price}$</i></b>\n"
    await message.answer(text=''.join(text),
                         reply_markup=confirm_change(item_id, "price", new_price))


@dp.message_handler(state="get_new_description")
async def get_new_description(message: types.Message, state: FSMContext):
    new_description = message.text
    state_data = await state.get_data()
    item_id = int(state_data['item_id'])
    if len(new_description) > 850:
        await message.answer("Описание слишком длинное, его длина не должна превышать 850 символов\nВведите еще раз",
                             reply_markup=back_to_edit_kb(item_id))
        return

    await state.finish()
    text = await make_item_card(item_id)
    text[2] = f"{new_description}"
    id = await db.new_description(new_description)
    await message.answer(text=''.join(text),
                         reply_markup=confirm_change(item_id, "description",id))


@dp.message_handler(content_types=types.ContentType.PHOTO, state="get_new_photo")
async def get_new_photo(message: types.Message, state: FSMContext, file_uploader: FileUploader):
    photo = message.photo[-1]
    await message.bot.send_chat_action(message.chat.id, 'upload_photo')
    uploaded_photo = await file_uploader.upload_photo(photo)
    new_photo_link = uploaded_photo.link
    state_data = await state.get_data()
    item_id = int(state_data['item_id'])
    await state.finish()
    text = await make_item_card(item_id)
    text[3] = f"<a href='{new_photo_link}'>.</a>\n"
    await message.answer(text=''.join(text),
                         reply_markup=confirm_change(item_id, "photo_link", new_photo_link))


@dp.callback_query_handler(confirm_change_info_callback.filter())
async def change_item_info(call: types.CallbackQuery, callback_data: dict):
    await call.answer("Изменено")
    item_id = int(callback_data["item_id"])
    what_change = callback_data["what_change"]
    new_value = callback_data["new_value"]
    if what_change == "description":
        new_value = await db.get_cashed_description(int(new_value))
    await db.update_item_info(what_change, new_value, item_id)
    await show_item(call, {"item_id": item_id})
