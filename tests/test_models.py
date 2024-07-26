import pytest
from fish.models import (
    GenderCategory,
    MoonModel,
)
from pydantic import ValidationError


def test_model():
    model = MoonModel.load()
    assert model.predict(-1, 1)[0] == 0
    assert model.predict(1, -1)[0] == 1
