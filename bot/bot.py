import logging
import asyncio
from os import getenv

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

import requests

from contract.contract import Contract
from deploy import functions
from state import Form

# bot_token = "6854007310:AAFfo073BeGTfC5FkE2j2MvghRMIj18kKMw"
tg_users = dict()  # tg_user_id : username
addresses = dict()  # tg_user_id : address

bot_token = getenv("BOT_TOKEN")   # todo
if not bot_token:
    exit("Error: no token provided")

bot = Bot(token=bot_token)

router = Router()
dp = Dispatcher()
dp.include_router(router)
logging.basicConfig(level=logging.INFO)

unauthorized_msg = 'It seems like you are using our bot in the first time. Please, use /registration or /login'

contract = Contract(functions)


async def set_commands():
    await bot.set_my_commands([
        types.BotCommand(command="start", description="Launch the bot"),
        types.BotCommand(command="help", description="Help"),
        types.BotCommand(command="registration", description="Registration for new users"),
        types.BotCommand(command="login", description="Login"),
        types.BotCommand(command="nfts_shop", description="Check NFTs shop"),
        types.BotCommand(command="available_nfts", description="List NFTs available for buying"),
        types.BotCommand(command="buy_nft", description="Buy NFT"),
        types.BotCommand(command="my_nfts", description="Check your NFTs"),
        types.BotCommand(command="sell_nft", description="Sell NFT"),
        types.BotCommand(command="my_account", description="Check your account"),
    ])


@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    if message.from_user.id in tg_users.keys():
        await message.answer("Hello, " + tg_users[message.from_user.id])
    else:
        await message.answer(unauthorized_msg)


@router.message(Command("registration"))
async def cmd_reg(message: types.Message, state: FSMContext):
    await state.set_state(Form.REGISTRATION_UNAME)
    await message.answer("Enter your new username")


@router.message(Command("login"))
async def cmd_login(message: types.Message, state: FSMContext):
    await state.set_state(Form.LOGIN)
    await message.answer("Enter your new username")


@router.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Use the menu in the lower left corner to see the available commands")


@router.message(Command("nfts_shop"))
async def cmd_nfts_shop(message: types.Message):
    await message.answer("Check available NFTs here: http://127.0.0.1:8081/nfts")


@router.message(Command("my_account"))
async def cmd_my_account(message: types.Message):
    if message.from_user.id in tg_users.keys():
        await message.answer("You can check your account here: http://127.0.0.1:8081/account?username=" +
                             tg_users[message.from_user.id])
    else:
        await message.answer(unauthorized_msg)


@router.message(Command("available_nfts"))
async def cmd_available_nfts(message: types.Message):
    if message.from_user.id in tg_users.keys():
        response = requests.get('http://127.0.0.1:8081/list_nfts')
        print(response.text)
        await message.answer('Available NFTs:\n' +
                             response.text +
                             '\n Would you like to buy one? /buy_nft')
    else:
        await message.answer(unauthorized_msg)


@router.message(Command("buy_nft"))
async def cmd_buy_nft(message: types.Message, state: FSMContext):
    if message.from_user.id in tg_users.keys():
        await state.set_state(Form.BUY)
        await message.answer("Enter the id of the NFT that you want to buy")
    else:
        await message.answer(unauthorized_msg)


@router.message(Command("my_nfts"))
async def cmd_my_nfts(message: types.Message, state: FSMContext):
    if message.from_user.id in tg_users.keys():
        response = requests.get('http://127.0.0.1:8081/list_my_nfts?username=' +
                                tg_users[message.from_user.id])
        print(response.text)
        await message.answer('Your NFTs:\n' +
                             response.text +
                             '\n Would you like to sell one? /sell_nft')
    else:
        await message.answer(unauthorized_msg)


@router.message(Command("sell_nft"))
async def cmd_sell_nft(message: types.Message, state: FSMContext):
    if message.from_user.id in tg_users.keys():
        await state.set_state(Form.SELL)
        await message.answer("Enter the id of the NFT that you want to sell")
    else:
        await message.answer(unauthorized_msg)


# on state


@router.message(Form.SELL)
async def sell(message: types.Message, state: FSMContext):
    await state.set_state(Form.START)

    nft_id = message.text
    print(nft_id)
    response = requests.get('http://127.0.0.1:8081/list_my_nfts_ids?username=' +
                            tg_users[message.from_user.id])

    ids_lst = [nft_id for nft_id in response.text.split(' ')]
    print(ids_lst)

    if nft_id in ids_lst:
        contract.sell_nft(int(nft_id), addresses[message.from_user.id])
        response = requests.get('http://127.0.0.1:8081/sell?username=' +
                                tg_users[message.from_user.id] +
                                '&nft_id=' + nft_id)
        print(response)
        await message.answer("Thanks, " + tg_users[message.from_user.id])
    else:
        await message.answer('You do not have a token with id=' +
                             nft_id +
                             '. Check /my_nfts to see your NFTs')


@router.message(Form.BUY)
async def buy(message: types.Message, state: FSMContext):
    await state.set_state(Form.START)

    nft_id = message.text
    response = requests.get('http://127.0.0.1:8081/list_nfts_ids')

    ids_lst = [nft_id for nft_id in response.text.split(' ')]
    print(ids_lst)

    if nft_id in ids_lst:
        try:
            contract.buy_nft(int(nft_id), addresses[message.from_user.id])
            response = requests.get('http://127.0.0.1:8081/buy?username=' +
                                    tg_users[message.from_user.id] +
                                    '&nft_id=' + nft_id)
            print(response)
            await message.answer("Thanks, " + tg_users[message.from_user.id])
        except Exception as e:
            await message.answer(error_msg(e))

    else:
        await message.answer('Probably, the token with id=' +
                             nft_id +
                             ' was sold. Check /available_nfts to see available NFTs')


@router.message(Form.REGISTRATION_UNAME)
async def reg_uname(message: types.Message, state: FSMContext):
    await state.set_state(Form.REGISTRATION_ADDR)

    username = message.text
    tg_users[message.from_user.id] = username
    registration(username, "")
    await message.answer("Enter your address")


@router.message(Form.REGISTRATION_ADDR)
async def reg_addr(message: types.Message, state: FSMContext):
    await state.set_state(Form.START)

    address = message.text
    addresses[message.from_user.id] = address
    registration(tg_users[message.from_user.id], address)
    await message.answer("Registration succeed. Thanks, " + tg_users[message.from_user.id])


@router.message(Form.LOGIN)
async def login(message: types.Message, state: FSMContext):
    await state.set_state(Form.START)

    username = message.text
    response = requests.get('http://127.0.0.1:8081/user_exists?username=' + username)

    if response.text == 'True':
        tg_users[message.from_user.id] = username
        await message.answer("Hello, " + username)
    else:
        await message.answer("User does not exist. Try /registration")


def registration(username, address):
    response = requests.get('http://127.0.0.1:8081/registration?address=' +
                            address +
                            '&username=' +
                            username)
    print(response)


def error_msg(e):
    print(e)
    return "Error occurred: " + str(e).split('VM Exception while processing transaction: revert')[1].split("'")[0]


async def run_bot():
    await dp.start_polling(bot)


if __name__ == '__main__':
    dp.startup.register(set_commands)
    asyncio.run(run_bot())
