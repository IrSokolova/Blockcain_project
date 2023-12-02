import logging
import asyncio

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

import requests

from state import Form

bot_token = "6854007310:AAFfo073BeGTfC5FkE2j2MvghRMIj18kKMw"
tg_users = dict()  # tg_user_id : username

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
    if message.from_user.id in tg_users.keys():
        await message.answer("Hello, " + tg_users[message.from_user.id])
    else:
        await message.answer("It seems like you are using our bot in the first time. "
                             "Please, use /registration or /login")


@router.message(Command("registration"))
async def cmd_reg(message: types.Message, state: FSMContext):
    await state.set_state(Form.REGISTRATION)
    await message.answer("Enter your new username")


@router.message(Command("login"))
async def cmd_login(message: types.Message, state: FSMContext):
    await state.set_state(Form.LOGIN)
    await message.answer("Enter your new username")


@router.message(Command("nfts_shop"))
async def cmd_nfts_shop(message: types.Message):
    await message.answer("Check available NFTs here: http://127.0.0.1:8081/nfts")


@router.message(Form.REGISTRATION)
async def red_get_username(message: types.Message, state: FSMContext):
    await state.set_state(Form.START)

    username = message.text
    tg_users[message.from_user.id] = username
    registration("", username)
    await message.answer("Registration succeed. Thanks, " + username)


@router.message(Form.LOGIN)
async def red_get_username(message: types.Message, state: FSMContext):
    await state.set_state(Form.START)

    username = message.text
    response = requests.get('http://127.0.0.1:8081/user_exists?username=' + username)

    if response.text == 'True':
        tg_users[message.from_user.id] = username
        await message.answer("Hello, " + username)
    else:
        await message.answer("User does not exist. Try /registration")


def registration(username, address):
    response = requests.get('http://127.0.0.1:8081/registration?address=' + address + '&username=' + username)
    print(response)


async def run_bot():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run_bot())
