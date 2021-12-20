from datetime import datetime, timedelta

from easypostdevtools.utils.Random import Random


class Dates:
    @staticmethod
    def to_string(date: datetime, string_format: str = "%Y-%m-%d") -> str:
        return date.strftime(string_format)

    @staticmethod
    def is_leap_year(year: int) -> bool:
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    @staticmethod
    def get_last_day_of_month(month: int, year: int) -> int:
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        elif month == 2:
            if Dates.is_leap_year(year):
                return 29
            else:
                return 28
        else:
            raise ValueError("Invalid month")

    @staticmethod
    def is_last_day_of_month(date: datetime) -> bool:
        return date.day == Dates.get_last_day_of_month(date.month, date.year)

    @staticmethod
    def is_last_month_of_year(date: datetime) -> bool:
        return date.month == 12

    @staticmethod
    def is_last_day_of_year(date: datetime) -> bool:
        return Dates.is_last_month_of_year(date) and Dates.is_last_day_of_month(date)

    @staticmethod
    def get_future_date_this_year():
        if Dates.is_last_day_of_year(datetime.now()):
            raise Exception("This year is over.")

        if Dates.is_last_day_of_month(datetime.now()):
            # pull from next month on
            month = Random.get_random_int_in_range(datetime.now().month + 1, 12)
        else:
            # pull from next day on
            month = Random.get_random_int_in_range(datetime.now().month, 12)

        max_days = Dates.get_last_day_of_month(month, datetime.now().year)

        if month == datetime.now().month:
            # pull from tomorrow on
            day = Random.get_random_int_in_range(datetime.now().day + 1, max_days)
        else:
            # pull from day 1 on
            day = Random.get_random_int_in_range(1, max_days)

        return datetime(datetime.now().year, month, day)

    @staticmethod
    def get_future_date_this_month():
        if Dates.is_last_day_of_month(datetime.now()):
            raise Exception("This month is over.")

        max_days = Dates.get_last_day_of_month(datetime.now().month, datetime.now().year)
        day = Random.get_random_int_in_range(datetime.now().day + 1, max_days)

        return datetime(datetime.now().year, datetime.now().month, day)

    @staticmethod
    def get_date_after(date: datetime) -> datetime:
        if date.month == 12:
            # if it's December, set up the next date to be in January
            date.replace(month=1, day=1, year=date.year + 1)
        return date + timedelta(days=Random.get_random_int_in_range(1, 30))

    @staticmethod
    def get_date_before(date: datetime) -> datetime:
        if date.month == 1:
            # if it's January, set up the next date to be in December
            date.replace(month=12, day=31, year=date.year - 1)
        return date - timedelta(days=Random.get_random_int_in_range(1, 30))

    @staticmethod
    def get_future_dates(number_of_dates: int) -> list[datetime]:
        dates = []
        current_date = datetime.now()
        for i in range(number_of_dates):
            current_date = Dates.get_date_after(current_date)
            dates.append(current_date)
        return dates

    @staticmethod
    def get_past_dates(number_of_dates: int) -> list[datetime]:
        dates = []
        current_date = datetime.now()
        for i in range(number_of_dates):
            current_date = Dates.get_date_before(current_date)
            dates.append(current_date)
        return dates
