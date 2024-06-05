from aiogram.dispatcher.filters.state import State, StatesGroup


class Value(StatesGroup):
    value = State()
    kurs = State()


class File(StatesGroup):
    out = State()


class Wiki(StatesGroup):
    loop = State()


class Download_yt(StatesGroup):
    loop = State()


class Tel(StatesGroup):
    loop = State()


class Trans(StatesGroup):
    loop = State()
    lang = State()
