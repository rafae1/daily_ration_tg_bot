from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, InputFile, ReplyKeyboardMarkup, \
    KeyboardButton

from db import DailyRation
from app import dp

menu_buttons = [
    "Рацион на весь день",
    "Завтрак",
    "Перекус 1",
    "Обед",
    "Перекус 2",
    "Ужин",
    "Любой Завтрак",
    "Любой Перекус 1",
    "Любой Обед",
    "Любой Перекус 2",
    "Любой Ужин",
]

__recipe_template__ = """
<strong>{}</strong>: {}

<strong>Ингредиенты:</strong>
{}
{}
"""

menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=menu_buttons[0])],
        [KeyboardButton(text=eating) for eating in menu_buttons[1:6]],
        [KeyboardButton(text=eating) for eating in menu_buttons[6:]],
    ],
    resize_keyboard=True
)


async def send_recipe(message, recipe):
    text = __recipe_template__.format(
        recipe['eating'],
        recipe['title'],
        recipe['ingredients'],
        recipe['cooking']
    )
    photo = InputFile(f"downloads/{recipe['pic_name']}")
    await message.answer_photo(photo, text)


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выберите из меню ниже", reply_markup=menu)


@dp.message_handler(Text(equals=menu_buttons[0]))
async def get_daily_ration(message: Message):
    recipes = await DailyRation.get_daily_ration()
    for recipe in recipes:
        await send_recipe(message, recipe)


@dp.message_handler(Text(equals=menu_buttons[1:6]))
async def get_today_eating(message: Message):
    recipe = await DailyRation.get_today_eating(message.text)
    await send_recipe(message, recipe)


@dp.message_handler(Text(equals=menu_buttons[6:]))
async def get_random_eating(message: Message):
    recipe = await DailyRation.get_random_eating(message.text)
    await send_recipe(message, recipe)


@dp.message_handler()
async def get_recipes_by_str(message: Message):
    recipes, err = await DailyRation.get_recipe_by_str(message)
    if err:
        await message.answer(err)
        return
    for recipe in recipes:
        await send_recipe(message, recipe)
