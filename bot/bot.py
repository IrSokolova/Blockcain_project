import logging
import asyncio

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

import requests

from state import Form

bot_token = "6854007310:AAFfo073BeGTfC5FkE2j2MvghRMIj18kKMw"

# bot_token = getenv("BOT_TOKEN")   # todo
# if not bot_token:
#     exit("Error: no token provided")

bot = Bot(token=bot_token)

router = Router()
dp = Dispatcher()
dp.include_router(router)
logging.basicConfig(level=logging.INFO)


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Hello!")


@router.message(Command("registration"))
async def cmd_reg(message: types.Message, state: FSMContext):
    await state.set_state(Form.REGISTRATION)
    await message.answer("Enter your new username")


@router.message(Form.REGISTRATION)
async def red_get_username(message: types.Message, state: FSMContext):
    await state.set_state(Form.START)

    username = message.text
    registration("", username)
    await message.answer("Your username is " + username)


def registration(username, address):
    response = requests.get('http://127.0.0.1:8081/registration?address=' + address + '&username=' + username)
    print(response)


async def run_bot():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run_bot())
