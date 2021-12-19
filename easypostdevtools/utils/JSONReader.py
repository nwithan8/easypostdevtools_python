import json

from easypostdevtools.utils.Random import Random


class JSONReader:
    @staticmethod
    def read_json_file_json(path: str) -> dict:
        """
        Reads a JSON file and returns the JSON object.
        :param path: The path to the JSON file.
        :return: The JSON object.
        """
        with open(path) as json_file:
            return json.load(json_file)

    @staticmethod
    def read_json_file_array(path: str) -> list:
        """
        Reads a JSON file and returns the JSON array.
        :param path: The path to the JSON file.
        :return: The JSON array.
        """
        with open(path) as json_file:
            return json.load(json_file)

    @staticmethod
    def get_random_maps_from_json_file(path: str, amount: int, allow_duplicates: bool) -> list[dict]:
        data = JSONReader.read_json_file_array(path)
        return Random.get_random_items_from_list(data, amount, allow_duplicates)

    @staticmethod
    def get_random_items_from_json_file(path: str, amount: int, allow_duplicates: bool) -> list:
        data = JSONReader.read_json_file_array(path)
        return Random.get_random_items_from_list(data, amount, allow_duplicates)
