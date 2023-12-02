from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    START = State()
    REGISTRATION = State()
    LOGIN = State()
