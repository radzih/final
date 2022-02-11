from aiogram import types

POST_REGULAR_SHIPPING = types.ShippingOption(
    id='post_reg',
    title='Новой почтой',
    prices=[
        types.LabeledPrice(
            'Доставка новой почтой', 5_00),
    ]
)

PICKUP_SHIPPING = types.ShippingOption(id='pickup',
                                       title='Самовывоз',
                                       prices=[
                                           types.LabeledPrice('Самовывоз из магазина', 0)
                                       ])