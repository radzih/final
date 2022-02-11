from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data import config


class TextIsNotNone(BoundFilter):
    async def check(self, query: types.InlineQuery) -> bool:
        return query.query is not None
