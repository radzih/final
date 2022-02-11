from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from loader import db


class NotRegistered(BoundFilter):
    async def check(self, message: types.Message) -> bool:
        return await db.check_user_or_register_referral(message.from_user.id) == None
