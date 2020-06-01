from datetime import datetime

from configs import START_DATE
from eating import Eating
from helpers import format_field
from app import conn


class DailyRation:
    select_fields = ["eating", "title", "ingredients", "cooking", "pic_name"]

    @staticmethod
    def get_current_week_and_day():
        marathon_day_num = (datetime.now() - START_DATE).days
        week = marathon_day_num // 7 + 1
        day = marathon_day_num % 7 + 1
        return [week, day]

    @classmethod
    async def get_daily_ration(cls):
        week, day = cls.get_current_week_and_day()
        print(week, day)
        today_daily_ration_sql = f"""
            SELECT {', '.join(cls.select_fields)} 
            FROM recipes 
            WHERE week = {week} and day = {day};
        """
        cursor = await conn.execute(today_daily_ration_sql)
        rows = await cursor.fetchall()
        return [
            {
                field: format_field(field, row[i])
                for i, field in enumerate(cls.select_fields)
            } for row in rows
        ]

    @classmethod
    async def get_today_eating(cls, message):
        week, day = cls.get_current_week_and_day()
        eating = Eating.get_key(message)
        today_eating_sql = f"""
            SELECT {', '.join(cls.select_fields)} 
            FROM recipes 
            WHERE week = {week} and day = {day} and eating = {eating};
        """
        cursor = await conn.execute(today_eating_sql)
        row = await cursor.fetchone()
        return {
            field: format_field(field, row[i])
            for i, field in enumerate(cls.select_fields)
        }

    @classmethod
    async def get_random_eating(cls, message):
        eating = Eating.get_key(message[6:])
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
