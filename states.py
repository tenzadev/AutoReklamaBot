from aiogram.dispatcher.filters.state import State, StatesGroup


class AutoInfo(StatesGroup):
    title = State()
    year = State()
    color = State()
    price = State()
    probeg = State()
    image = State()
    phone = State()
    confirm = State()
