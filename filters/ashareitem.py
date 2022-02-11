import re

from aiogram import types
from aiogram.dispatcher.filters import BoundFilter

from data import config


class ShareItem(BoundFilter):
    async def check(self, query: types.InlineQuery) -> bool:
        return re.match(r'item:\d+', query.query)
