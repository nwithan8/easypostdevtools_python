import random
from enum import Enum


class ExtendedEnum(Enum):
    @classmethod
    def values(cls) -> list:
        return [c for c in cls]

    @classmethod
    def all(cls) -> list:
        return cls.values()

    @classmethod
    def amount(cls) -> int:
        return len(cls.values())

    @classmethod
    def value_of(cls, value):
        return cls(value)

    @classmethod
    def value_of_index(cls, index):
        return cls(cls.values()[index])

    @classmethod
    def index_of(cls, value):
        return cls.values().index(value)

    @classmethod
    def random(cls):
        return random.choice(cls.values())
