from aiogram.dispatcher.filters.state import StatesGroup, State


class DonwloadState(StatesGroup):
    url = State()
    type = State()
