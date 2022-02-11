from aiogram.dispatcher.filters.state import StatesGroup, State


class Loginned(StatesGroup):
    Log = State()
    WriteQuest = State()
    QuestAccept = State()