from enum import Enum
from typing import Union

import easypost
from dotenv import dotenv_values

from easypostdevtools import Constants
from easypostdevtools.models.ExtendedEnum import ExtendedEnum
from easypostdevtools.utils.JSONReader import JSONReader
from easypostdevtools.Constants import Addresses as AddressesConstants
from easypostdevtools.utils.Random import Random


class KeyType(Enum):
    """
    Enum for key types
    """
    TEST = 1
    PRODUCTION = 2


def setup_key(key: str = None, env_dir: str = None, key_type: KeyType = None):
    if not key and not env_dir and not key_type:
        raise ValueError("Must provide either key, or envDir and keyType")
    if key:
        easypost.api_key = key
    else:
        path = f"{env_dir}/.env"
        config = dotenv_values(dotenv_path=path)
        if key_type == KeyType.TEST:
            easypost.api_key = config.get("EASYPOST_TEST_KEY")
        elif key_type == KeyType.PRODUCTION:
            easypost.api_key = config.get("EASYPOST_PROD_KEY")


class EasyPostDevTools:
    def __init__(self):
        pass

    class Mapper:
        def __init__(self):
            pass

        @staticmethod
        def to_json(obj: object):
            return obj.__dict__

        @staticmethod
        def to_map(obj: object):
            return EasyPostDevTools.Mapper.to_json(obj)

    class Addresses(Mapper):

        class ADDRESS_RELATIONSHIP(ExtendedEnum):
            SAME_STATE = 1
            DIFFERENT_STATE = 2
            SAME_COUNTRY = 3
            DIFFERENT_COUNTRY = 4

        def __init__(self):
            super().__init__()
            pass

        @staticmethod
        def get_map(country: AddressesConstants.COUNTRY = None, state: AddressesConstants.STATE = None) -> dict:
            address_file = AddressesConstants.get_random_address_file(country, state)
            maps = JSONReader.get_random_maps_from_json_file(address_file, 1, True)
            return maps[0]

        @staticmethod
        def get(country: AddressesConstants.COUNTRY = None, state: AddressesConstants.STATE = None) -> easypost.Address:
            address_map = EasyPostDevTools.Addresses.get_map(country, state)
            return easypost.Address.create(**address_map)

        @staticmethod
        def get_maps_same_state(amount: int) -> list[dict]:
            state = AddressesConstants.STATE.random()
            state_address_file = AddressesConstants.get_random_address_file(None, state)
            return JSONReader.get_random_maps_from_json_file(state_address_file, amount, False)

        @staticmethod
        def get_same_state(amount: int) -> list[easypost.Address]:
            maps = EasyPostDevTools.Addresses.get_maps_same_state(amount)
            return [easypost.Address.create(**_map) for _map in maps]

        @staticmethod
        def get_maps_different_state(amount: int) -> list[dict]:
            if amount > AddressesConstants.STATE.amount():
                raise ValueError(f"Amount cannot be greater than {AddressesConstants.STATE.amount()}")
            maps = []
            states = Random.get_random_items_from_list(AddressesConstants.STATE.values(), amount)
            for state in states:
                maps.append(EasyPostDevTools.Addresses.get_map(None, state))
            return maps

        @staticmethod
        def get_different_state(amount: int) -> list[easypost.Address]:
            maps = EasyPostDevTools.Addresses.get_maps_different_state(amount)
            return [easypost.Address.create(**_map) for _map in maps]

        @staticmethod
        def get_maps_same_country(amount: int) -> list[dict]:
            country = AddressesConstants.COUNTRY.random()
            country_address_file = AddressesConstants.get_random_address_file(country, None)
            return JSONReader.get_random_maps_from_json_file(country_address_file, amount, False)

        @staticmethod
        def get_same_country(amount: int) -> list[easypost.Address]:
            maps = EasyPostDevTools.Addresses.get_maps_same_country(amount)
            return [easypost.Address.create(**_map) for _map in maps]

        @staticmethod
        def get_maps_different_countries(amount: int) -> list[dict]:
            if amount > AddressesConstants.COUNTRY.amount():
                raise ValueError(f"Amount cannot be greater than {AddressesConstants.COUNTRY.amount()}")
            maps = []
            countries = Random.get_random_items_from_list(AddressesConstants.COUNTRY.values(), amount)
            for country in countries:
                maps.append(EasyPostDevTools.Addresses.get_map(country, None))
            return maps

        @staticmethod
        def get_different_countries(amount: int) -> list[easypost.Address]:
            maps = EasyPostDevTools.Addresses.get_maps_different_countries(amount)
            return [easypost.Address.create(**_map) for _map in maps]

        @staticmethod
        def get_maps(relationship: ADDRESS_RELATIONSHIP, amount: int) -> Union[None, list[dict]]:
            if relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.SAME_STATE:
                return EasyPostDevTools.Addresses.get_maps_same_state(amount)
            elif relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.DIFFERENT_STATE:
                return EasyPostDevTools.Addresses.get_maps_different_state(amount)
            elif relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.SAME_COUNTRY:
                return EasyPostDevTools.Addresses.get_maps_same_country(amount)
            elif relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.DIFFERENT_COUNTRY:
                return EasyPostDevTools.Addresses.get_maps_different_countries(amount)
            else:
                return None

        @staticmethod
        def get_amount(relationship: ADDRESS_RELATIONSHIP, amount: int) -> list[easypost.Address]:
            if relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.SAME_STATE:
                return EasyPostDevTools.Addresses.get_same_state(amount)
            elif relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.DIFFERENT_STATE:
                return EasyPostDevTools.Addresses.get_different_state(amount)
            elif relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.SAME_COUNTRY:
                return EasyPostDevTools.Addresses.get_same_country(amount)
            elif relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.DIFFERENT_COUNTRY:
                return EasyPostDevTools.Addresses.get_different_countries(amount)
            else:
                return []

    class Parcels(Mapper):
        def __init__(self):
            super().__init__()
            pass

    class Insurance:
        def __init__(self):
            pass

    class Shipments(Mapper):
        def __init__(self):
            super().__init__()
            pass

    class Options:
        def __init__(self):
            pass

    class Rates(Mapper):
        def __init__(self):
            super().__init__()
            pass

    class Smartrates(Mapper):
        def __init__(self):
            super().__init__()
            pass

    class TaxIdentifiers(Mapper):
        def __init__(self):
            super().__init__()
            pass

    class Trackers(Mapper):
        def __init__(self):
            super().__init__()
            pass

    class Batch:
        def __init__(self):
            pass

    class CustomsInfos(Mapper):
        def __init__(self):
            super().__init__()
            pass

    class CustomsItems(Mapper):
        def __init__(self):
            super().__init__()
            pass

    class Events:
        def __init__(self):
            pass

    class Fees(Mapper):
        def __init__(self):
            super().__init__()
            pass

    class Orders:
        def __init__(self):
            pass

    class Pickups:
        def __init__(self):
            pass

    class Reports(Mapper):
        def __init__(self):
            super().__init__()
            pass

    class ScanForms:
        def __init__(self):
            pass

    class Webhooks(Mapper):
        def __init__(self):
            super().__init__()
            pass

    class Users:
        def __init__(self):
            pass

    class Carriers:
        def __init__(self):
            pass

    class Labels:
        def __init__(self):
            pass

    class PostageLabels(Mapper):
        def __init__(self):
            super().__init__()
            pass
