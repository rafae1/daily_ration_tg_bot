from datetime import datetime

from app import conn
from configs import conf


class DailyRation:
    select_fields = ["eating", "title", "ingredients", "cooking", "pic_name"]

    @staticmethod
    def get_current_week_and_day():
        start_date = datetime.strptime(conf["start_date"], '%Y-%m-%d')
        diff_between_start = (datetime.now() - start_date).days
        marathon_day_num = diff_between_start % conf["marathon_duration"] - 1
        week = marathon_day_num // 7 + 1
        day = marathon_day_num % 7 + 1
        return [week, day]

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
                field: row[i] for i, field in enumerate(cls.select_fields)
            } for row in rows
        ]

    @classmethod
    async def get_today_eating(cls, message):
        week, day = cls.get_current_week_and_day()
        today_eating_sql = f"""
            SELECT {', '.join(cls.select_fields)}
            FROM recipes
            WHERE week = {week} AND day = {day} AND eating = '{message}';
        """
        cursor = await conn.execute(today_eating_sql)
        row = await cursor.fetchone()
        return {
            field: row[i] for i, field in enumerate(cls.select_fields)
        }

    @classmethod
    async def get_random_eating(cls, message):
        today_eating_sql = f"""
            SELECT {', '.join(cls.select_fields)}
            FROM recipes
            WHERE eating = '{message[6:]}'
            ORDER BY RANDOM() LIMIT 1;
        """
        cursor = await conn.execute(today_eating_sql)
        row = await cursor.fetchone()
        return {
            field: row[i] for i, field in enumerate(cls.select_fields)
        }

    @classmethod
    async def get_recipe_by_str(cls, message):
        message_text = message.text
        err_msg = "Длина поисковой строки должна быть > 3 символов"
        err = err_msg if len(message_text) < 4 else None
        lower_message = message_text.lower()
        capitalized_message = message_text.capitalize()
        # sqlite does not have case-sensitive search
        # upper/lower functions do not work with Unicode
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
               field: row[i] for i, field in enumerate(cls.select_fields)
           } for row in rows
        ], err
