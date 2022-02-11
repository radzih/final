from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram.utils.markdown import hbold, hitalic

from handlers.users.admin_panel import show_admin_panel
from integrations.telegraph import FileUploader
from keyboards.inline.add_item import go_to_admin_kb, confirm_adding_kb
from loader import dp, db, bot


@dp.callback_query_handler(text="add_item")
async def send_photo(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.edit_text("Скиньте фото товара",
                                 reply_markup=go_to_admin_kb)
    await state.set_state("get_photo")


@dp.message_handler(state="get_photo", content_types=types.ContentType.PHOTO)
async def get_item_name(message: types.Message, state: FSMContext, file_uploader: FileUploader, retry_item_name=False):
    if retry_item_name:
        await message.answer("Слишеком долгое название, длина символов не должна превышать 75 штук",
                             reply_markup=go_to_admin_kb)

    else:
        await message.answer("Напишите названия товара",
                             reply_markup=go_to_admin_kb)
        photo = message.photo[-1]
        await message.bot.send_chat_action(message.chat.id, 'upload_photo')
        uploaded_photo = await file_uploader.upload_photo(photo)
        await state.finish()
        await state.set_state("get_item_name")
        await state.update_data(photo_link=uploaded_photo.link)


@dp.message_handler(state="get_item_name", content_types=types.ContentType.TEXT)
async def get_description(message: types.Message, state: FSMContext, retry_description=False):
    if retry_description:
        await message.answer("Описание слишком длинное, напишите короче",
                             reply_markup=go_to_admin_kb)
    else:
        await message.answer("Напишите описание товара",
                             reply_markup=go_to_admin_kb)
        item_name = message.text
        if len(item_name) > 75:
            await get_item_name(message, state, retry_item_name=True)
        state_data = await state.get_data()
        photo_link = state_data['photo_link']
        await state.finish()
        await state.set_state("get_description")
        await state.update_data(photo_link=photo_link, item_name=item_name)


@dp.message_handler(state="get_description", content_types=types.ContentType.TEXT)
async def get_price(message: types.Message, state: FSMContext, retry_price=False, retry_amount=False):
    if retry_price:
        await message.answer("Напишите цену в доларах без пробелов и символов",
                             reply_markup=go_to_admin_kb)
    elif retry_amount:
        await message.answer("Напишите цену в промежутке 0,5330",
                             reply_markup=go_to_admin_kb)
    else:
        description = message.text
        if len(description) > 850:
            await get_description(message, state, retry_description=True)
            return
        await message.answer("Напишите цену товара в долларах",
                             reply_markup=go_to_admin_kb)
        state_data = await state.get_data()
        photo_link = state_data['photo_link']
        item_name = state_data['item_name']
        await state.finish()
        await state.set_state("get_price")
        await state.update_data(photo_link=photo_link, item_name=item_name, description=description)


@dp.message_handler(state="get_price", content_types=types.ContentType.TEXT)
async def get_quantity(message: types.Message, state: FSMContext):
    try:
        price = int(message.text)
    except ValueError:
        await get_price(message, state, retry_price=True)
        return
    if price > 5330:
        await get_price(message, state, retry_amount=True)
        return

    state_data = await state.get_data()
    photo_link = state_data['photo_link']
    item_name = state_data['item_name']
    description = state_data['description']

    await state.set_state("confirm_item")
    await state.update_data(photo_link=photo_link, item_name=item_name,
                            description=description, price=price)
    text = (f"{hbold(item_name)}\n",
            f"<b>Цена: </b>{hbold(price)}$\n",
            f"{hitalic(description)}",
            f"<a href='{photo_link}'>.</a>")
    await message.answer(text=''.join(text),
                         reply_markup=confirm_adding_kb)


@dp.callback_query_handler(text='save', state="confirm_item")
async def add_item(call: types.CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    photo_link = state_data['photo_link']
    item_name = state_data['item_name']
    description = state_data['description']
    price = state_data['price']
    await state.finish()
    await db.add_new_item(item_name, price, description, photo_link)
    await call.answer("Добавлено")
    await show_admin_panel(call, state)
    await bot.get_updates()
