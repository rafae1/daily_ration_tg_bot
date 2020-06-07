import asyncio
import itertools
import os
import re

import aiohttp
import aiosqlite
from bs4 import BeautifulSoup

from configs import conf


class Scrapper:
    weeks = range(1, 9)  # 8 weeks
    days_in_week = range(1, 8)  # 7 days in week
    all_days_with_recipes = itertools.product(weeks, days_in_week)

    login_url = f"{conf['parser']['main_page']}/login"
    ration_url = f"{conf['parser']['main_page']}/marafon/food-custom"

    url_from_css = re.compile(r"\((.*)\)")

    download_dir = "downloads/"
    if not os.path.exists("downloads/"):
        os.makedirs("downloads/")

    def __init__(self):
        self.session = None
        self.recipes = []

    async def parse(self):
        async with aiohttp.ClientSession() as self.session:
            await self.authorize()
            for week, day in self.all_days_with_recipes:
                content = await self.get_daily_ration(
                    {"week": week, "number": day}
                )
                await self.parse_daily_ration(content, week, day)
        await self.save_all_recipes()

    async def authorize(self):
        data = {
            "LoginForm[email]": conf['parser']['login'],
            "LoginForm[password]": conf['parser']['password'],
        }
        async with self.session.post(self.login_url, data=data) as response:
            return await response.text()

    async def get_daily_ration(self, params):
        async with self.session.get(self.ration_url, params=params) as resp:
            soup = BeautifulSoup(await resp.text(), 'html.parser')
            return soup.find("div", class_="food_list")

    async def parse_daily_ration(self, content, week, day):
        parsed_ration = content.find_all("div", class_="food_item")
        for ind, eating in enumerate(parsed_ration):
            title = self.get_recipe_title(eating)
            ingredients = self.get_recipe_ingredients(eating)
            cooking = self.get_recipe_cooking(eating)
            pic_name = await self.save_recipe_picture(eating)
            row = (week, day, ind + 1, title, ingredients, cooking, pic_name)
            self.recipes.append(row)

    async def save_all_recipes(self):
        async with aiosqlite.connect(conf["db_name"]) as conn:
            await conn.execute("""
                CREATE TABLE IF NOT EXISTS recipes
                (week integer, day integer, eating integer, title text,
                ingredients text, cooking text, pic_name text)
            """)
            await conn.executemany("""
                INSERT INTO recipes
                VALUES (?,?,?,?,?,?,?)
            """, self.recipes)
            await conn.commit()

    @staticmethod
    def get_recipe_title(eating):
        return eating.find("div", class_="food_item_name").text

    @staticmethod
    def get_recipe_ingredients(eating):
        ingredients_divs = eating.find_all("td", class_="ingredients")
        return "\n".join([ingr.text for ingr in ingredients_divs])

    @staticmethod
    def get_recipe_cooking(eating):
        cooking_div = eating.find("div", class_="cooking")
        return cooking_div.text if cooking_div else ""

    async def save_recipe_picture(self, eating):
        pic_styles_div = eating.find("div", class_="food_item_img")
        pic_div_styles = pic_styles_div["style"] if pic_styles_div else ""
        pic_name = ""
        if not pic_div_styles:
            return pic_name
        pic_url = self.url_from_css.search(pic_div_styles).group(1)
        async with self.session.get(
                f"{conf['parser']['main_page']}{pic_url}") as response:
            img_data = await response.content.read()
            pic_name = pic_url.split("/")[-1]
            with open(self.download_dir + pic_name, 'wb') as handler:
                handler.write(img_data)
        return pic_name


if __name__ == '__main__':
    scrapper = Scrapper()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrapper.parse())
