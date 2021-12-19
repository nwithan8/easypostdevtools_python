from enum import Enum

from easypostdevtools.models.ExtendedEnum import ExtendedEnum
from easypostdevtools.utils.Random import Random

CUSTOMS_ITEMS_JSON = "json/customs_items.json"
CUSTOMS_INFO_JSON = "json/customs_info.json"
CARRIERS_JSON = "json/carriers.json"
LABEL_OPTIONS_JSON = "json/label_options.json"
TRACKERS_JSON = "json/trackers.json"
OPTIONS_JSON = "json/options.json"
PICKUPS_JSON = "json/pickups.json"


class JsonFile:
    def __init__(self, file_name: str, parent_folder: str):
        self._file_name = file_name
        self._parent_folder = parent_folder

    @property
    def json_path(self):
        return f"{self._parent_folder}/{self._file_name.lower()}.min.json"


class JsonAddressFile(JsonFile):
    def __init__(self, abbreviation: str, parent_folder: str):
        super(JsonAddressFile, self).__init__(f"{abbreviation}-addresses", parent_folder)

    @property
    def address_file(self):
        return f"json/addresses/{self.json_path}"


class Addresses:
    class COUNTRY(ExtendedEnum):
        UNITED_STATES = JsonAddressFile("US", "united-states")
        CANADA = JsonAddressFile("BC", "canada")
        CHINA = JsonAddressFile("BJ", "china")
        HONG_KONG = JsonAddressFile("HK", "china")
        UNITED_KINGDOM = JsonAddressFile("UK", "europe")
        GERMANY = JsonAddressFile("DE", "europe")
        SPAIN = JsonAddressFile("ES", "europe")
        MEXICO = JsonAddressFile("MX", "mexico")
        AUSTRALIA = JsonAddressFile("VT", "australia")

    class STATE(ExtendedEnum):
        ARIZONA = JsonAddressFile("AZ", "united-states")
        CALIFORNIA = JsonAddressFile("CA", "united-states")
        IDAHO = JsonAddressFile("ID", "united-states")
        KANSAS = JsonAddressFile("KS", "united-states")
        NEVADA = JsonAddressFile("NV", "united-states")
        NEW_YORK = JsonAddressFile("NY", "united-states")
        TEXAS = JsonAddressFile("TX", "united-states")
        UTAH = JsonAddressFile("UT", "united-states")
        WASHINGTON = JsonAddressFile("WA", "united-states")

    @classmethod
    def get_state_address_file(cls, state: STATE) -> str:
        return state.value.address_file

    @classmethod
    def get_country_address_file(cls, country: COUNTRY) -> str:
        return country.value.address_file

    @classmethod
    def get_address_file(cls, country: COUNTRY = None, state: STATE = None) -> str:
        if not country and not state:
            raise ValueError("Must specify either country or state")
        if country == Addresses.COUNTRY.UNITED_STATES:
            return cls.get_random_state_address_file()
        else:
            return cls.get_country_address_file(country)

    @classmethod
    def get_random_state_address_file(cls) -> str:
        state = cls.STATE.random()
        return state.value.address_file

    @classmethod
    def get_random_country_address_file(cls) -> str:
        country = cls.COUNTRY.random()
        return country.value.address_file

    @classmethod
    def get_random_address_file(cls, country: COUNTRY = None, state: STATE = None) -> str:
        if country:
            return cls.get_country_address_file(country)
        elif state:
            return cls.get_state_address_file(state)
        else:
            if Random.get_random_boolean():
                return cls.get_random_country_address_file()
            else:
                return cls.get_random_state_address_file()

