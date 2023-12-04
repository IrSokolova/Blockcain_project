from aiogram.fsm.state import StatesGroup, State


class Form(StatesGroup):
    START = State()
    REGISTRATION_UNAME = State()
    REGISTRATION_ADDR = State()
    LOGIN = State()
    BUY = State()
    SELL = State()
