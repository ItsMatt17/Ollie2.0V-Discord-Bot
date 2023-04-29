import json
import os


class FileUtils:

    @staticmethod
    def json_file_open(file_path: str) -> dict:
        if not file_path.endswith(".json"):
            raise Exception("File is not a json file")
        if not os.path.exists(file_path):
            raise Exception("File does not exist")

        with open(file_path, "r") as file:
            data = json.load(file)
        return data

    @staticmethod
    def json_file_write(data: dict, file_path: str) -> None:
        if not file_path.endswith(".json"):
            raise Exception("File is not a json file")
        if not os.path.exists(file_path):
            raise Exception("File does not exist")

        with open(file_path, "w") as file:
            json.dump(data, file)

    @staticmethod
    def is_user_in_data(data: dict, user_id: int | str) -> bool:
        if data.get(user_id) is None:
            return False
        return True
