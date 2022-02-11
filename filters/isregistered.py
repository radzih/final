from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class IsRegistered(BoundFilter):
    async def check(self, message: types.Message or types.InlineQuery) -> bool:
        return await db.check_user_or_register_referral(message.from_user.id) != None
