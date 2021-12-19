import random
import string

from easypostdevtools.models.ExtendedEnum import ExtendedEnum


class Random:
    @staticmethod
    def get_random_boolean() -> bool:
        return bool(random.getrandbits(1))

    @staticmethod
    def get_random_int_in_range(minimum: int, maximum: int) -> int:
        return random.randint(minimum, maximum)

    @staticmethod
    def get_random_int() -> int:
        return Random.get_random_int_in_range(0, 100)

    @staticmethod
    def get_random_double_in_range(minimum: float, maximum: float) -> float:
        return random.uniform(minimum, maximum)

    @staticmethod
    def get_random_double() -> float:
        return Random.get_random_double_in_range(0, 100)

    @staticmethod
    def get_random_float_in_range(minimum: float, maximum: float) -> float:
        return Random.get_random_double_in_range(minimum, maximum)

    @staticmethod
    def get_random_float() -> float:
        return Random.get_random_double()

    @staticmethod
    def get_random_character() -> str:
        return chr(random.randint(0, 255))

    @staticmethod
    def get_random_string_of_length(length: int) -> str:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    @staticmethod
    def get_random_string() -> str:
        return Random.get_random_string_of_length(random.randint(3, 10))

    @staticmethod
    def get_random_items_from_list(items: list, amount: int, allow_duplicates: bool) -> list:
        if not allow_duplicates and amount > len(items):
            raise ValueError("Amount must be less than or equal to list size when unique is true")
        selections = []
        for i in range(amount):
            choice = random.choice(items)
            if not allow_duplicates:
                items.remove(choice)
            selections.append(choice)
        return selections

    @staticmethod
    def get_random_item_from_list(items: list) -> object:
        return random.choice(items)

    @staticmethod
    def get_random_enum(enum: ExtendedEnum) -> ExtendedEnum:
        return enum.random()
