from aiogram import types
from aiogram.dispatcher.filters import BoundFilter


class QueryIsNone(BoundFilter):
    async def check(self, query: types.InlineQuery) -> bool:
        return None == query.query
