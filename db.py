from datetime import datetime

from configs import conf
from eating import Eating
from app import conn


class DailyRation:
    select_fields = ["eating", "title", "ingredients", "cooking", "pic_name"]

    @staticmethod
    def get_current_week_and_day():
        start_date = datetime.strptime(conf["start_date"], '%Y-%m-%d')
        marathon_day_num = (datetime.now() - start_date).days % conf["marathon_duration"] - 1
        week = marathon_day_num // 7 + 1
        day = marathon_day_num % 7 + 1
        return [week, day]

    @staticmethod
    def format_field(field_name, value):
        if field_name == "eating":
            return Eating.verbose(value)
        else:
            return value

    @classmethod
    async def get_daily_ration(cls):
        week, day = cls.get_current_week_and_day()
        today_daily_ration_sql = f"""
            SELECT {', '.join(cls.select_fields)} 
            FROM recipes 
            WHERE week = {week} AND day = {day};
        """
        cursor = await conn.execute(today_daily_ration_sql)
        rows = await cursor.fetchall()
        return [
            {
                field: cls.format_field(field, row[i])
                for i, field in enumerate(cls.select_fields)
            } for row in rows
        ]

    @classmethod
    async def get_today_eating(cls, message):
        week, day = cls.get_current_week_and_day()
        eating = Eating.get_key_by_value(message)
        today_eating_sql = f"""
            SELECT {', '.join(cls.select_fields)} 
            FROM recipes 
            WHERE week = {week} AND day = {day} AND eating = {eating};
        """
        cursor = await conn.execute(today_eating_sql)
        row = await cursor.fetchone()
        return {
            field: format_field(field, row[i])
            for i, field in enumerate(cls.select_fields)
        }

    @classmethod
    async def get_random_eating(cls, message):
        eating = Eating.get_key_by_value(message[6:])
        today_eating_sql = f"""
            SELECT {', '.join(cls.select_fields)} 
            FROM recipes 
            WHERE eating = {eating}
            ORDER BY RANDOM() LIMIT 1;
        """
        cursor = await conn.execute(today_eating_sql)
        row = await cursor.fetchone()
        return {
            field: format_field(field, row[i])
            for i, field in enumerate(cls.select_fields)
        }

    @classmethod
    async def get_recipe_by_str(cls, message):
        message_text = message.text
        err = None
        if len(message_text) < 4:
            err = "Длина поисковой строки должна быть > 3 символов"
        lower_message = message_text.lower()
        capitalized_message = message_text.capitalize()
        search_by_str = f"""
            SELECT {', '.join(cls.select_fields)}
            FROM recipes 
            WHERE 
            title LIKE '%{lower_message}%' OR 
            title LIKE '%{capitalized_message}%' OR
            ingredients LIKE '%{lower_message}%' OR 
            ingredients LIKE '%{capitalized_message}%'
            GROUP BY title;
        """
        cursor = await conn.execute(search_by_str)
        rows = await cursor.fetchall()
        return [
            {
                field: format_field(field, row[i])
                for i, field in enumerate(cls.select_fields)
            } for row in rows
        ], err
