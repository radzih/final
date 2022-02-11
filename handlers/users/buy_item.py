from aiogram import types
from aiogram.types import LabeledPrice

from data.item_shiping import POST_REGULAR_SHIPPING, PICKUP_SHIPPING
from keyboards.inline import buy_callback, get_menu_kb
from keyboards.inline.buy_item import what_payment, payment_callback
from loader import dp, bot, db
from utils.misc.item import Item




@dp.callback_query_handler(buy_callback.filter())
async def pay_by_telegram(call: types.CallbackQuery, callback_data: dict):
    await call.answer()
    await call.message.edit_text(text="Оплатите ниже")
    item_id = int(callback_data["item_id"])
    sql_output = await db.get_item_by_id(item_id)
    bonus_balance = await db.get_balance(call.from_user.id)
    item = Item(title=sql_output[1],
                description='⠀',
                currency="USD",
                prices=[
                    LabeledPrice(
                        label=sql_output[1],
                        amount=sql_output[2] * 100
                    ),
                    LabeledPrice(
                        label='Скидка',
                        amount=f"-{bonus_balance[0] * 100}"
                    ) if bonus_balance[0] else LabeledPrice(label='Скидка', amount=0),

                ],
                need_shipping_address=True,
                need_name=True,
                need_email=True,
                need_phone_number=True,
                start_parameter="create_invoice_item",
                photo_url=sql_output[4],
                photo_size=600,
                is_flexible=True,
                send_email_to_provider=True
                )

    await bot.send_invoice(chat_id=call.from_user.id,
                           **item.generate_invoice(),
                           payload=f'{item_id}')


@dp.shipping_query_handler()
async def choose_shipping(query: types.ShippingQuery):
    if query.shipping_address.country_code != "UA":
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        ok=False,
                                        error_message="Сюда не доставляем")
    else:
        await bot.answer_shipping_query(shipping_query_id=query.id,
                                        shipping_options=[POST_REGULAR_SHIPPING, PICKUP_SHIPPING],
                                        ok=True)


@dp.pre_checkout_query_handler()
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query_id=pre_checkout_query.id,
                                        ok=True)
    item_id = pre_checkout_query.invoice_payload
    order_info = dict(pre_checkout_query.order_info)
    order_info["item_id"] = item_id
    order_info_str = str(order_info)
    await db.new_order(pre_checkout_query.from_user.id,order_info_str)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text="Спасибо за покупку! Ожидайте отправку")
    menu_kb = await get_menu_kb(pre_checkout_query.from_user.id)
    await bot.send_message(chat_id=pre_checkout_query.from_user.id,
                           text='Меню магазина', reply_markup=menu_kb)


