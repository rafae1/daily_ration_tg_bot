from enum import Enum


class Eating(Enum):
    BREAKFAST = 1
    SNACK_1 = 2
    LUNCH = 3
    SNACK_2 = 4
    DINNER = 5

    @classmethod
    def verbose(cls, key=None, default=''):
        texts = {
            cls.BREAKFAST.value: "Завтрак",
            cls.SNACK_1.value: "Перекус 1",
            cls.LUNCH.value: "Обед",
            cls.SNACK_2.value: "Перекус 2",
            cls.DINNER.value: "Ужин",
        }
        return texts.get(key, default) if key else texts

    @classmethod
    def get_key(cls, value):
        for k, v in cls.verbose().items():
            if v == value:
                return k
