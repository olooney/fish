from io import BytesIO
import joblib
import pkgutil
from typing import Iterable, Dict, Union
from enum import Enum
import pydantic
import numpy as np


MOON_LABELS = ["Blue", "Orange"]
MOON_COLORS = ["#1F77B4", "#FF7F0E"]


class GenderCategory(Enum):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"


class MoonModel:
    def __init__(self, data):
        self._model = data

    @classmethod
    def load(cls, filename: str = None):
        if filename is None:
            raw_data = pkgutil.get_data("fish", "data/moon_model.v1.joblib")
            file = BytesIO(raw_data)
            data = joblib.load(file)
        else:
            data = joblib.load(filename)

        return cls(data)

    def predict(self, x: float, y: float) -> int:
        X = np.array([ [x, y] ])
        Y = self._model.predict(X)
        return Y[0].item()


