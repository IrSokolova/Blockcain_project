import logging
import asyncio
from multiprocessing import Process

from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from front.app import store, app
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
    store.registration("", username)
    await message.answer("Your username is " + username)


# @dp.message_handler(state=Form.bank_p)
# async def process_name(message: types.Message, state: FSMContext):
#     await state.finish()
#
#     GAMES[IN_GAME[0]][IN_GAME[1]][PLAYER_CONFIG] = message.text
#     await message.answer(f'The player \"{PLAYER_CONFIG}\" is added')
#     reset_player_config()

# GAMES = dict()
# IN_GAME = tuple()
# PLAYER_CONFIG = ''
#
#
# def set_player_config(name):
#     global PLAYER_CONFIG
#     PLAYER_CONFIG = name
#
#
# def reset_player_config():
#     global PLAYER_CONFIG
#     PLAYER_CONFIG = ''
#
#
# def set_in_game(uid, game_name):
#     global IN_GAME
#     IN_GAME = (uid, game_name)
#
#
# def set_in_player(name):
#     global IN_GAME
#     IN_GAME = (IN_GAME[0], IN_GAME[1], name)
#
#
# def reset_in_game():
#     global IN_GAME
#     IN_GAME = tuple()
#
#
# def reset_in_player():
#     global IN_GAME
#     IN_GAME = (IN_GAME[0], IN_GAME[1])
#
#
# class Form(StatesGroup):
#     name_c = State()
#     name_l = State()
#     name_p = State()
#     name_s = State()  # start
#     bank_p = State()
#     new_game = State()
#
#
# @dp.message_handler(commands='start')
# async def cmd_start(message: types.Message):
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ['New game', 'Log in to game', 'Show games']
#     keyboard.add(*buttons)
#     await message.answer('Choose an option', reply_markup=keyboard)
#
#
# @dp.message_handler(lambda message: message.text == 'Show games')
# async def cmd_show_games(message: types.Message):
#     await message.answer("Your games:")
#     games = ""
#     for key in GAMES[message.from_id].keys():
#         games = games + '\"' + key + '\", '
#
#     await message.answer(f"{games[:-2]}")
#
#
# @dp.message_handler(lambda message: message.text == 'New game')
# async def cmd_start(message: types.Message):
#     await Form.name_c.set()
#     await message.answer("Enter the name of the game or /cancel")
#
#
# @dp.message_handler(lambda message: message.text == 'Log in to game')
# async def cmd_start(message: types.Message):
#     await Form.name_l.set()
#     await message.answer("Enter the name of the game or /cancel")
#
#
# @dp.message_handler(state=Form.name_c)
# async def process_name(message: types.Message, state: FSMContext):
#     await state.finish()
#
#     if message.from_id not in GAMES.keys():
#         GAMES[message.from_id] = dict()
#     elif message.text in GAMES[message.from_id].keys():
#         await message.answer(f'The game \"{message.text}\" already exists')
#         return
#
#     GAMES[message.from_id][message.text] = dict()
#     await message.answer(f'The game \"{message.text}\" is created')
#
#
# @dp.message_handler(state=Form.name_l)
# async def process_name(message: types.Message, state: FSMContext):
#     await state.finish()
#
#     if message.from_id not in GAMES.keys() or message.text not in GAMES[message.from_id]:
#         await message.answer(f'The game \"{message.text}\" does not exist')
#         return
#
#     set_in_game(message.from_id, message.text)
#
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ['Add player', 'Log out', 'Show players', 'Start']
#     keyboard.add(*buttons)
#
#     await message.answer(f'The game \"{message.text}\" is opened', reply_markup=keyboard)
#
#
# @dp.message_handler(lambda message: message.text == 'Show players')
# async def cmd_start(message: types.Message):
#     await message.answer("Players:")
#     players = ""
#     for key in GAMES[IN_GAME[0]][IN_GAME[1]].keys():
#         players = players + 'name: ' + key + '     bank: ' + str(GAMES[IN_GAME[0]][IN_GAME[1]][key]) + '\n'
#
#     await message.answer(f"{players}")
#
#
# @dp.message_handler(lambda message: message.text == 'Log out')
# async def cmd_start(message: types.Message):
#     reset_in_game()
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ['New game', 'Log in to game', 'Show games']
#     keyboard.add(*buttons)
#     await message.answer("Back to the menu", reply_markup=keyboard)
#
#
# @dp.message_handler(lambda message: message.text == 'Add player')
# async def cmd_start(message: types.Message):
#     await Form.name_p.set()
#     await message.answer("Enter the name of the player or /cancel")
#
#
# @dp.message_handler(state=Form.name_p)
# async def process_name(message: types.Message, state: FSMContext):
#     await state.finish()
#
#     if message.text in GAMES[IN_GAME[0]][IN_GAME[1]].keys():
#         await message.answer(f'The player \"{message.text}\" already exists')
#         return
#
#     set_player_config(message.text)
#     await message.answer("Enter bank of the player or /cancel")
#     await Form.bank_p.set()
#
#
# @dp.message_handler(state=Form.bank_p)
# async def process_name(message: types.Message, state: FSMContext):
#     await state.finish()
#
#     GAMES[IN_GAME[0]][IN_GAME[1]][PLAYER_CONFIG] = message.text
#     await message.answer(f'The player \"{PLAYER_CONFIG}\" is added')
#     reset_player_config()
#
#
# @dp.message_handler(state='*', commands='cancel')
# @dp.message_handler(Text(equals='cancel', ignore_case=True), state='*')
# async def cancel_handler(message: types.Message, state: FSMContext):
#     current_state = await state.get_state()
#     if current_state is None:
#         return
#
#     await state.finish()
#     await message.answer('ОК')
#
#
# @dp.message_handler(lambda message: message.text == 'Start')
# async def cmd_start(message: types.Message):
#     await Form.name_s.set()
#     await message.answer('Enter your name:')
#
#
# @dp.message_handler(state=Form.name_s)
# async def process_name(message: types.Message, state: FSMContext):
#     await state.finish()
#
#     if message.text not in GAMES[IN_GAME[0]][IN_GAME[1]].keys():
#         await message.answer(f'The player \"{message.text}\" does not exist')
#         return
#
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ['Finish']
#     keyboard.add(*buttons)
#
#     set_in_player(message.text)
#     await message.answer(f"You are playing as {message.text} now", reply_markup=keyboard)
#
#
# @dp.message_handler(lambda message: message.text == 'Finish')
# async def cmd_start(message: types.Message):
#     reset_in_player()
#     keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
#     buttons = ['Finish']
#     keyboard.add(*buttons)
#     await message.answer(f"Back to the \"{IN_GAME[1]}\" menu", reply_markup=keyboard)
#
#
# @dp.errors_handler(exception=BotBlocked)
# async def error_bot_blocked(update: types.Update, exception: BotBlocked):
#     print(f"Меня заблокировал пользователь!\nСообщение: {update}\nОшибка: {exception}")
#     return True


async def run_bot():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(run_bot())
