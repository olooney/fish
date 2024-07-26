from fastapi.testclient import TestClient
import fish
from fish.api import app
import re

client = TestClient(app)


def test_ping():
    response = client.get("/ping")
    assert response.status_code == 200
    pong = response.json()
    assert isinstance(pong, dict)
    assert len(pong) == 3
    assert pong["message"] == "PONG"
    assert pong["version"] == fish.__version__

    iso8601 = r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d{1,10})?Z?$"
    print(pong["timestamp"])
    assert re.match(iso8601, pong["timestamp"])
