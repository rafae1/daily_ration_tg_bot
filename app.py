import logging

import aiosqlite
from aiogram import Bot
from aiogram import Dispatcher
from aiogram import executor

from configs import TOKEN, DB_NAME
from configs import admin_id

logging.basicConfig(
    format=u'%(filename)s [LINE:%(lineno)d] '
           u'#%(levelname)-8s [%(asctime)s]  %(message)s',
    level=logging.INFO
)

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher(bot)


async def create_pool():
    return await aiosqlite.connect(DB_NAME)


conn = dp.loop.run_until_complete(create_pool())


async def on_startup(dp):
    await bot.send_message(admin_id, "Я запущен!")


async def on_shutdown(dp):
    await bot.close()


if __name__ == '__main__':
    from handlers import dp

    executor.start_polling(dp, on_shutdown=on_shutdown, on_startup=on_startup)
