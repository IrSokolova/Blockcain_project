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

unauthorized_msg = 'It seems like you are using our bot in the first time. Please, use /registration or /login'


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id in tg_users.keys():
        await message.answer("Hello, " + tg_users[message.from_user.id])
    else:
        await message.answer(unauthorized_msg)


@router.message(Command("registration"))
async def cmd_reg(message: types.Message, state: FSMContext):
    await state.set_state(Form.REGISTRATION)
    await message.answer("Enter your new username")


@router.message(Command("login"))
async def cmd_login(message: types.Message, state: FSMContext):
    await state.set_state(Form.LOGIN)
    await message.answer("Enter your new username")


@router.message(Command("commands"))
async def cmd_nfts_shop(message: types.Message):
    commands = ('/start\n'
                '/registration\n'
                '/login\n'
                '/nfts_shop\n'
                '/available_nfts\n'
                '/buy_nft\n'
                '/my_nfts\n'
                '/sell_nft\n')
    await message.answer("Available commands:\n" + commands)


@router.message(Command("nfts_shop"))
async def cmd_nfts_shop(message: types.Message):
    await message.answer("Check available NFTs here: http://127.0.0.1:8081/nfts")


@router.message(Command("available_nfts"))
async def cmd_nfts_shop(message: types.Message):
    if message.from_user.id in tg_users.keys():
        response = requests.get('http://127.0.0.1:8081/list_nfts')
        print(response.text)
        await message.answer('Available NFTs:\n' + response.text + '\n Would you like to buy one? /buy_nft')
    else:
        await message.answer(unauthorized_msg)


@router.message(Command("buy_nft"))
async def cmd_nfts_shop(message: types.Message, state: FSMContext):
    if message.from_user.id in tg_users.keys():
        await state.set_state(Form.BUY)
        await message.answer("Enter the id of the NFT that you want to buy")
    else:
        await message.answer(unauthorized_msg)


@router.message(Command("my_nfts"))
async def cmd_nfts_shop(message: types.Message, state: FSMContext):
    if message.from_user.id in tg_users.keys():
        response = requests.get('http://127.0.0.1:8081/list_my_nfts?username=' + tg_users[message.from_user.id])
        print(response.text)
        await message.answer('Your NFTs:\n' + response.text + '\n Would you like to sell one? /sell_nft')
    else:
        await message.answer(unauthorized_msg)


@router.message(Command("sell_nft"))
async def cmd_nfts_shop(message: types.Message, state: FSMContext):
    if message.from_user.id in tg_users.keys():
        await state.set_state(Form.SELL)
        await message.answer("Enter the id of the NFT that you want to sell")
    else:
        await message.answer(unauthorized_msg)


# on state


@router.message(Form.SELL)
async def red_get_username(message: types.Message, state: FSMContext):
    await state.set_state(Form.START)

    nft_id = message.text
    print(nft_id)
    response = requests.get('http://127.0.0.1:8081/list_my_nfts_ids?username=' + tg_users[message.from_user.id])

    ids_lst = [nft_id for nft_id in response.text.split(' ')]
    print(ids_lst)

    if nft_id in ids_lst:  # todo sell
        response = requests.get('http://127.0.0.1:8081/sell?username=' + tg_users[message.from_user.id] +
                                '&nft_id=' + nft_id)
        print(response)
        await message.answer("Thanks, " + tg_users[message.from_user.id])
    else:
        await message.answer('You do not have a token with id=' + nft_id +
                             '. Check /my_nfts to see your NFTs')


@router.message(Form.BUY)
async def red_get_username(message: types.Message, state: FSMContext):
    await state.set_state(Form.START)

    nft_id = message.text
    response = requests.get('http://127.0.0.1:8081/list_nfts_ids')

    ids_lst = [nft_id for nft_id in response.text.split(' ')]
    print(ids_lst)

    if nft_id in ids_lst:  # todo buy
        response = requests.get('http://127.0.0.1:8081/buy?username=' + tg_users[message.from_user.id] +
                                '&nft_id=' + nft_id)
        print(response)
        await message.answer("Thanks, " + tg_users[message.from_user.id])
    else:
        await message.answer('Probably, the token with id=' + nft_id +
                             ' was sold. Check /available_nfts to see available NFTs')


@router.message(Form.REGISTRATION)
async def red_get_username(message: types.Message, state: FSMContext):
    await state.set_state(Form.START)

    username = message.text
    tg_users[message.from_user.id] = username
    registration("", username)  # todo change addr
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
