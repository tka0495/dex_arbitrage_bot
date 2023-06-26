from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import logging

import main

logging.basicConfig(level=logging.INFO)

TOKEN = '5994439984:AAEIcuqCnlZX9Fqp3sbqGe6hQGkBrTUzH_Y'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# class ReportStatesGroup(StatesGroup):
#     crypto_network = State()
#     check_transaction = State()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
            await bot.send_message(message.from_user.id, 'Hello {}!\nNice to meet you in our bot!'.format(message.from_user.full_name))
            await bot.send_message(message.from_user.id, 'Please click /transaction for payment in crypto!')
            # await asyncio.sleep(10)

@dp.message_handler(commands=['transaction'])
async def transaction(message: types.Message):
    await bot.send_message(message.from_user.id, 'Input your transaction hash in Polygon Network!')

@dp.message_handler()
async def check_transaction(message: types.Message):
    if message.text.startswith('0x'):
        transaction = message.text
        transaction_status = main.transaction_check(transaction)[0]
        if transaction_status == 'Success':
            await bot.send_message(message.from_user.id, 'Transaction Successful\nWelcome to our team!')
            await bot.send_message(message.from_user.id, main.transaction_check(transaction)[1])
        else:
            await bot.send_message(message.from_user.id, 'Transaction Unsuccessful\nPlease, check transaction hash!')
            await bot.send_message(message.from_user.id, main.transaction_check(transaction))
    else:
        await bot.send_message(message.from_user.id, 'Uncorrected transaction hash!')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


