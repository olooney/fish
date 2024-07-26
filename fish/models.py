import json
import pkgutil
from typing import Iterable, Dict, Union
from enum import Enum
import pydantic


MOON_LABELS = ["Blue", "Orange"]
MOON_COLORS = ["#1F77B4", "#FF7F0E"]


class GenderCategory(Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class MoonModel:
    def __init__(self, model_data):
        self.data = model_data

    @classmethod
    def load(cls, filename: str = None):
        if filename is None:
            raw_data = pkgutil.get_data("fish", "data/data.json")
            data = json.loads(raw_data.decode("utf-8"))
        else:
            with open(filename) as file:
                data = json.load(file)

        return cls(data)

    def predict(self, x: float, y: float) -> int:
        return 0 if x + y < 1 else 1
