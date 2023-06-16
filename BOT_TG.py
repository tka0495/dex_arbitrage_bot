import asyncio
import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import DEX
from db import Database
import datetime

import logging

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, \
    ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton

import os

logging.basicConfig(level=logging.INFO)

TOKEN = '5979449278:AAEwnbR621lcx7K4LrQGr2XaBzsjnu8Y-FA'
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
db = Database('database.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        # await bot.send_message(message.from_user.id, message.from_user.id)
        if not db.user_exists(message.from_user.id):
            db.add_user(message.from_user.id)
        # while True:
        #     with open(os.path.join('/Users','default','Desktop','Projects', 'DEX-bot', 'venv', 'test.txt'), 'r') as f:
        #         text = f.read()
        #     await bot.send_message(message.from_user.id, text)
        #     await asyncio.sleep(10)


@dp.message_handler()
async def on_startup():
    while True:
        text = []
        try:
            text = DEX.aggregator()
        except:
            time.sleep(90)
            text = DEX.aggregator()
        print('text = ', text)
        # преобразование связки в удобный вид для вывода одним сообщением
        format_text = ''
        for text_str in text:
            format_text += text_str

        # РАССЫЛКА СООБЩЕНИЙ ВСЕМ ПОЛЬЗОВАТЕЛЯМ БОТА
        user_id_tuple = db.user_das()
        print(user_id_tuple)
        for user_id in user_id_tuple[0]:
            await bot.send_message(user_id, format_text) # user_id[0] потому, что данные приходят в формате (237912374, )
            await asyncio.sleep(60)

if __name__ == "__main__":
    executor.start(dp, on_startup())
    executor.start_polling(dp, skip_updates=True)




# await bot.send_message(message.from_user.id, 'Hello {}'.format(datetime.datetime.now().strftime("%H:%M:%S  %d.%m.%Y")))


# button2 = KeyboardButton('Информация')
# kb_menu = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# kb_menu.row(button2, button3, button4)

# inline_kb = InlineKeyboardMarkup(row_width=1)
# inline_btn1 = InlineKeyboardButton(text='Обновить', callback_data='update')
# inline_kb.add(inline_btn1)









# @dp.message_handler(text=['В меню', 'Обратно'])
# @dp.message_handler(commands=['start'])
# async def command_help(message : types.Message):
#     if message.text == 'В меню':
#         await bot.send_message(message.from_user.id, 'Приветствие', reply_markup=kb_menu)
#         await message.delete()
#     elif message.text == 'Обратно':
#         await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=kb_menu)
#         await message.delete()









