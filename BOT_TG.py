import asyncio
import sqlite3
import time

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from apscheduler.schedulers.asyncio import AsyncIOScheduler

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
scheduler = AsyncIOScheduler()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if message.chat.type == 'private':
        try:
            if not db.user_exists(message.from_user.id):
                await bot.send_message(message.from_user.id, 'Добро пожаловать!')
                db.add_user(message.from_user.id)
        except sqlite3.IntegrityError:
            await bot.send_message(message.from_user.id, 'есть в БД')
        # while True:
        #     with open(os.path.join('/Users','default','Desktop','Projects', 'DEX-bot', 'venv', 'test.txt'), 'r') as f:
        #         text = f.read()
        #     await bot.send_message(message.from_user.id, text)
        #     await asyncio.sleep(10)




async def send_message_to_users(dp: Dispatcher):
    try:
        text = DEX.aggregator()
    except:
        time.sleep(90)
        text = DEX.aggregator()
    if len(text) > 0:
        print('[+] Data is True.', text)
    else:
        print('[-] Data is False. Waiting please!')
    # преобразование связки в удобный вид для вывода одним сообщением
    if len(text) > 0:
        format_text = '<b>ДОСТУПНЫЕ СВЯЗКИ:</b>\n\n'
    else:
        format_text = 'В данный момент связок нет! Ожидайте.'
    for text_str in text:
        format_text += text_str
    format_text += '<b>TON Адрес для поддержки:</b> <code>EQASkuyQpOru2czLSmy9qng7ybGij-8-ey29K35jhylPjqd8</code>'

    # РАССЫЛКА СООБЩЕНИЙ ВСЕМ ПОЛЬЗОВАТЕЛЯМ БОТА
    user_id_tuple = db.user_das()
    print('[+] Users: ', user_id_tuple)
    for user_id in user_id_tuple:
        await bot.send_message(user_id[0], format_text, parse_mode="html")  # user_id[0] потому, что данные приходят в формате (237912374, )
        # await asyncio.sleep(60)


async def schedule_jobs(dp: Dispatcher):
    scheduler.add_job(send_message_to_users, "interval", seconds=120, args=(dp,))

async def on_startup(dp):
    await schedule_jobs(dp)


if __name__ == "__main__":
    scheduler.start()
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)




# async def schedule_jobs(dp: Dispatcher):
#     # ДЛЯ ТЕСТОВ
#     # scheduler.add_job(send_message_to_users, "interval", seconds=20, args=(dp,))
#     scheduler.add_job(create_actually_table, 'cron', day_of_week='mon-sat', hour=23, minute=8, end_date='2024-05-30')
#     scheduler.add_job(create_actually_sheet, 'cron', day_of_week='mon-sat', hour=23, minute=9, end_date='2024-05-30')
#     scheduler.add_job(send_message_to_users, 'cron', day_of_week='mon-sat', hour=23, minute=10, end_date='2024-05-30',
#                       args=(dp,))
#     scheduler.add_job(message_link_from_admin, 'cron', day_of_week='mon-sat', hour=23, minute=11, end_date='2024-05-30',
#                       args=(dp,))
#
#     # РАБОЧИЕ ВАРИАНТЫ
#     # scheduler.add_job(send_message_to_users, 'cron', day_of_week='mon-sat', hour=16, minute=29,
#     #                   end_date='2024-05-30', args=(dp,))
#     # scheduler.add_job(create_actually_table, 'cron', day_of_week='mon', hour=9, minute=00, end_date='2024-05-30')
#     # scheduler.add_job(create_actually_sheet, 'cron', day_of_week='mon-fri', hour=17, minute=50, end_date='2024-05-30')
#     # scheduler.add_job(message_link_from_admin, 'cron', day_of_week='mon-fri', hour=19, minute=00,
#     #                   end_date='2024-05-30', args=(dp,))
#
#     # ПРИМЕР Запуск с Понедельника по Пятницу в 5:30 (утра) до 2021-05-30 00:00:00
#     # scheduler.add_job(func, 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2021-05-30')
#
#
# #
# async def on_startup(dp):
#     await bot.send_message(config.ADMIN_USER_ID, MESSAGE_RESTART, reply_markup=types.ReplyKeyboardRemove())
#     await schedule_jobs(dp)
#
#
# if __name__ == "__main__":
#     scheduler.start()
#     executor.start_polling(dp, skip_updates=True, on_startup=on_startup)











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









