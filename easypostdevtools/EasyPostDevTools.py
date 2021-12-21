from enum import Enum
from typing import Union

import easypost
from dotenv import dotenv_values

import easypostdevtools.Constants as Constants
from easypostdevtools.Constants import Addresses as AddressesConstants
from easypostdevtools.models.ExtendedEnum import ExtendedEnum
from easypostdevtools.utils.Dates import Dates
from easypostdevtools.utils.JSONReader import JSONReader
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

        @classmethod
        def _get_maps_from_json_file(cls, file_path: str, count: int = 1, allow_duplicates: bool = True) -> list:
            return JSONReader.get_random_maps_from_json_file(file_path, count, allow_duplicates)

        @classmethod
        def _get_map_from_json_file(cls, file_path: str) -> dict:
            maps = cls._get_maps_from_json_file(file_path, 1, False)
            return maps[0]

    class Addresses(Mapper):

        class ADDRESS_RELATIONSHIP(ExtendedEnum):
            SAME_STATE = 1
            DIFFERENT_STATE = 2
            SAME_COUNTRY = 3
            DIFFERENT_COUNTRY = 4

        def __init__(self):
            super().__init__()
            pass

        @classmethod
        def get_map(cls, country: AddressesConstants.COUNTRY = None, state: AddressesConstants.STATE = None) -> dict:
            address_file = AddressesConstants.get_random_address_file(country, state)
            return cls._get_maps_from_json_file(address_file, 1, False)[0]

        @staticmethod
        def get(country: AddressesConstants.COUNTRY = None, state: AddressesConstants.STATE = None) -> easypost.Address:
            address_map = EasyPostDevTools.Addresses.get_map(country, state)
            return easypost.Address.create(**address_map)

        @classmethod
        def get_maps_same_state(cls, amount: int) -> list[dict]:
            state = AddressesConstants.STATE.random()
            state_address_file = AddressesConstants.get_random_address_file(None, state)
            return cls._get_maps_from_json_file(state_address_file, amount, False)

        @staticmethod
        def get_same_state(amount: int) -> list[easypost.Address]:
            maps = EasyPostDevTools.Addresses.get_maps_same_state(amount)
            return [easypost.Address.create(**_map) for _map in maps]

        @staticmethod
        def get_maps_different_states(amount: int) -> list[dict]:
            if amount > AddressesConstants.STATE.amount():
                raise ValueError(f"Amount cannot be greater than {AddressesConstants.STATE.amount()}")
            maps = []
            states = Random.get_random_items_from_list(AddressesConstants.STATE.values(), amount, False)
            for state in states:
                maps.append(EasyPostDevTools.Addresses.get_map(None, state))
            return maps

        @staticmethod
        def get_different_states(amount: int) -> list[easypost.Address]:
            maps = EasyPostDevTools.Addresses.get_maps_different_states(amount)
            return [easypost.Address.create(**_map) for _map in maps]

        @classmethod
        def get_maps_same_country(cls, amount: int) -> list[dict]:
            country = AddressesConstants.COUNTRY.random()
            country_address_file = AddressesConstants.get_random_address_file(country, None)
            return cls._get_maps_from_json_file(country_address_file, amount, False)

        @staticmethod
        def get_same_country(amount: int) -> list[easypost.Address]:
            maps = EasyPostDevTools.Addresses.get_maps_same_country(amount)
            return [easypost.Address.create(**_map) for _map in maps]

        @staticmethod
        def get_maps_different_countries(amount: int) -> list[dict]:
            if amount > AddressesConstants.COUNTRY.amount():
                raise ValueError(f"Amount cannot be greater than {AddressesConstants.COUNTRY.amount()}")
            maps = []
            countries = Random.get_random_items_from_list(AddressesConstants.COUNTRY.values(), amount, False)
            for country in countries:
                maps.append(EasyPostDevTools.Addresses.get_map(country, None))
            return maps

        @staticmethod
        def get_different_countries(amount: int) -> list[easypost.Address]:
            maps = EasyPostDevTools.Addresses.get_maps_different_countries(amount)
            return [easypost.Address.create(**_map) for _map in maps]

        @staticmethod
        def get_maps_amount(relationship: ADDRESS_RELATIONSHIP, amount: int) -> Union[None, list[dict]]:
            if relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.SAME_STATE:
                return EasyPostDevTools.Addresses.get_maps_same_state(amount)
            elif relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.DIFFERENT_STATE:
                return EasyPostDevTools.Addresses.get_maps_different_states(amount)
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
                return EasyPostDevTools.Addresses.get_different_states(amount)
            elif relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.SAME_COUNTRY:
                return EasyPostDevTools.Addresses.get_same_country(amount)
            elif relationship == EasyPostDevTools.Addresses.ADDRESS_RELATIONSHIP.DIFFERENT_COUNTRY:
                return EasyPostDevTools.Addresses.get_different_countries(amount)
            else:
                return []

    class Parcels:
        def __init__(self):
            pass

        @staticmethod
        def get_map() -> dict:
            return {
                "weight": Random.get_random_float_in_range(0.0, 100.0),
                "height": Random.get_random_float_in_range(0.0, 100.0),
                "width": Random.get_random_float_in_range(0.0, 100.0),
                "length": Random.get_random_float_in_range(0.0, 100.0)
            }

        @staticmethod
        def get() -> easypost.Parcel:
            return easypost.Parcel.create(**EasyPostDevTools.Parcels.get_map())

        @staticmethod
        def retrieve(_id: str) -> easypost.Parcel:
            return easypost.Parcel.retrieve(_id)

    class Insurance:
        def __init__(self):
            pass

        @staticmethod
        def get_map(amount: float = None) -> dict:
            return {
                "amount": amount if amount else Random.get_random_float_in_range(0.0, 100.0),
            }

        @staticmethod
        def insure(shipment: easypost.Shipment, amount: float = None) -> easypost.Insurance:
            insurance_map = EasyPostDevTools.Insurance.get_map(amount)
            return shipment.insure(**insurance_map)

    class Shipments(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @staticmethod
        def get_map(to_address_map: dict = None, from_address_map: dict = None, parcel_map: dict = None) -> dict:
            if not (to_address_map and from_address_map):
                address_maps = EasyPostDevTools.Addresses.get_maps_different_states(2)
                to_address_map = address_maps[0]
                from_address_map = address_maps[1]
            if not parcel_map:
                parcel_map = EasyPostDevTools.Parcels.get_map()
            return {
                'to_address': to_address_map,
                'from_address': from_address_map,
                'parcel': parcel_map,
            }

        @staticmethod
        def get_return_map(to_address_map: dict = None, from_address_map: dict = None, parcel_map: dict = None) -> dict:
            _map = EasyPostDevTools.Shipments.get_map(to_address_map, from_address_map, parcel_map)
            _map['is_return'] = True
            return _map

        @staticmethod
        def get(to_address_map: dict = None, from_address_map: dict = None, parcel_map: dict = None) -> easypost.Shipment:
            _map = EasyPostDevTools.Shipments.get_map(to_address_map, from_address_map, parcel_map)
            return easypost.Shipment.create(**_map)

        @staticmethod
        def get_return(to_address_map: dict = None, from_address_map: dict = None, parcel_map: dict = None) -> easypost.Shipment:
            _map = EasyPostDevTools.Shipments.get_return_map(to_address_map, from_address_map, parcel_map)
            return easypost.Shipment.create(**_map)

        @staticmethod
        def create(shipment_map: dict) -> easypost.Shipment:
            return easypost.Shipment.create(**shipment_map)

        @staticmethod
        def add_insurance(shipment: easypost.Shipment, amount: float = None) -> easypost.Shipment:
            EasyPostDevTools.Insurance.insure(shipment, amount)

        @staticmethod
        def refund(shipment: easypost.Shipment) -> easypost.Refund:
            return shipment.refund()

        @staticmethod
        def mark_for_return(shipment_map: dict) -> dict:
            shipment_map['is_return'] = True
            return shipment_map

        # waiting on ability to convert attributes to map to modify shipment for Shipment markForReturn

    class Options(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @classmethod
        def get_map(cls) -> dict:
            return cls._get_map_from_json_file(Constants.OPTIONS_JSON)

    class Rates(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @staticmethod
        def get(shipment_map: dict = None, shipment: easypost.Shipment = None) -> list[easypost.Rate]:
            if shipment:
                return shipment.get_rates()
            else:
                if not shipment_map:
                    shipment_map = EasyPostDevTools.Shipments.get_map()
                return easypost.Shipment.create(**shipment_map).get_rates()

    class Smartrates(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @staticmethod
        def get(shipment_map: dict = None, shipment: easypost.Shipment = None) -> list[easypost.Rate]:
            if shipment:
                return shipment.get_smartrates()
            else:
                if not shipment_map:
                    shipment_map = EasyPostDevTools.Shipments.get_map()
                return easypost.Shipment.create(**shipment_map).get_smartrates()

    class TaxIdentifiers(Mapper):
        def __init__(self):
            super().__init__()
            pass

        # TODO

    class Trackers(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @classmethod
        def get_map(cls) -> dict:
            return cls._get_map_from_json_file(Constants.TRACKERS_JSON)

        @staticmethod
        def get() -> easypost.Tracker:
            _map = EasyPostDevTools.Trackers.get_map()
            return easypost.Tracker.create(**_map)

    class Batch:
        def __init__(self):
            pass

    class CustomsItems(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @classmethod
        def get_random_customs_item_maps(cls, amount: int, allow_duplicates: bool) -> list[dict]:
            return cls._get_maps_from_json_file(Constants.CUSTOMS_ITEMS_JSON, amount, allow_duplicates)

        @staticmethod
        def get(amount: int, allow_duplicates: bool) -> list[easypost.CustomsItem]:
            customs_item_maps = EasyPostDevTools.CustomsItems.get_random_customs_item_maps(amount, allow_duplicates)
            return [easypost.CustomsItem.create(**customs_item_map) for customs_item_map in customs_item_maps]

    class CustomsInfos(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @classmethod
        def get_map(cls, items_amount: int, allow_duplicate_items: bool) -> dict:
            _map = cls._get_map_from_json_file(Constants.CUSTOMS_INFO_JSON)
            _map['custom_items'] = EasyPostDevTools.CustomsItems.get_random_customs_item_maps(items_amount,
                                                                                              allow_duplicate_items)
            return _map

        @staticmethod
        def get(items_amount: int, allow_duplicate_items: bool) -> easypost.CustomsInfo:
            customs_info_map = EasyPostDevTools.CustomsInfos.get_map(items_amount, allow_duplicate_items)
            return easypost.CustomsInfo.create(**customs_info_map)

    class Events:
        def __init__(self):
            pass

    class Fees(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @staticmethod
        def get(shipment_map: dict = None, shipment: easypost.Shipment = None) -> list:
            if shipment:
                return shipment.fees
            else:
                if not shipment_map:
                    shipment_map = EasyPostDevTools.Shipments.get_map()
                return easypost.Shipment.create(**shipment_map).fees

    class Orders:
        def __init__(self):
            pass

    class Pickups(Mapper):
        def __init__(self):
            pass
            super().__init__()
            pass

        @classmethod
        def get_map(cls) -> dict:
            _map = cls._get_map_from_json_file(Constants.PICKUPS_JSON)
            to_address_map = EasyPostDevTools.Addresses.get_map()
            from_address_map = EasyPostDevTools.Addresses.get_map()
            _map['address'] = to_address_map
            parcel_map = EasyPostDevTools.Parcels.get_map()
            shipment_map = EasyPostDevTools.Shipments.get_map(parcel_map=parcel_map, from_address_map=from_address_map,
                                                              to_address_map=to_address_map)
            _map['shipment'] = shipment_map
            dates = Dates.get_future_dates(2)
            _map['min_datetime'] = Dates.to_string(dates[0])
            _map['max_datetime'] = Dates.to_string(dates[1])
            return _map

    class Reports(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @staticmethod
        def get_map() -> dict:
            dates = Dates.get_past_dates(2)
            return {
                'shipment': {
                    'start_date': Dates.to_string(dates[1]),
                    'end_date': Dates.to_string(dates[0])
                }
            }

        @staticmethod
        def get() -> easypost.Report:
            report_map = EasyPostDevTools.Reports.get_map()
            return easypost.Report.create(**report_map)

    class ScanForms:
        def __init__(self):
            pass

    class Webhooks(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @staticmethod
        def get_map() -> dict:
            return {
                'url': 'https://www.example.com/webhooks/test',
            }

        @staticmethod
        def get() -> easypost.Webhook:
            webhook_map = EasyPostDevTools.Webhooks.get_map()
            return easypost.Webhook.create(**webhook_map)

    class Users:
        def __init__(self):
            pass

    class Carriers:
        def __init__(self):
            pass

        @staticmethod
        def get(amount: int = 1) -> list[str]:
            return JSONReader.get_random_items_from_json_file(Constants.CARRIERS_JSON, amount, False)

    class Labels(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @classmethod
        def get_random_label_options(cls) -> dict:
            return cls._get_map_from_json_file(Constants.LABEL_OPTIONS_JSON)

    class PostageLabels(Mapper):
        def __init__(self):
            super().__init__()
            pass

        @staticmethod
        def get(shipment: easypost.Shipment = None, shipment_map: dict = None) -> easypost.PostageLabel:
            if shipment:
                return shipment.postage_label
            else:
                if not shipment_map:
                    shipment_map = EasyPostDevTools.Shipments.get_map()
                return easypost.Shipment.create(**shipment_map).postage_label
