from fastapi import FastAPI, HTTPException
import pydantic
from typing import List
from .models import MoonModel, MOON_LABELS, MOON_COLORS
from .version import __version__
from datetime import datetime

app = FastAPI(
    title="Fish Model Server",
    version=__version__,
)
moon_model = MoonModel.load()


class PingResponse(pydantic.BaseModel):
    message: str
    version: str
    timestamp: str


class MoonRequest(pydantic.BaseModel):
    x: float
    y: float


class MoonResult(pydantic.BaseModel):
    code: int
    label: str


class MoonResponse(pydantic.BaseModel):
    result: MoonResult


@app.get("/ping")
def ping() -> PingResponse:
    """
    Simple low-overhead PING route to check if the server is up.
    """
    return {
        "message": "PONG",
        "version": __version__,
        "timestamp": datetime.now().isoformat(),
    }


@app.post("/moon/predict")
def moon_predict(moon_request: MoonRequest) -> MoonResponse:
    x = moon_request.x
    y = moon_request.y
    code = moon_model.predict(x, y)
    label = MOON_LABELS[code]
    color = MOON_COLORS[code]
    return {
        "result": {
            "code": code,
            "label": label,
            "color": color,
        },
    }
