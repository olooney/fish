from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
import pydantic
from typing import List
from .models import MoonModel, MOON_LABELS, MOON_COLORS
from .version import __version__
from datetime import datetime
import pkgutil

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
    probability: float


class MoonResponse(pydantic.BaseModel):
    result: MoonResult
    version: str
    timestamp: str

class MoonBatchResponse(pydantic.BaseModel):
    result: List[MoonResult]
    version: str
    timestamp: str

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
    code, probability = moon_model.predict(x, y)
    label = MOON_LABELS[code]
    color = MOON_COLORS[code]
    return {
        "result": {
            "code": code,
            "label": label,
            "color": color,
            "probability": probability
        },
        "version": __version__,
        "timestamp": datetime.now().isoformat(),
    }

@app.post("/moon/batch_predict")
def batch_predict(moon_requests: List[MoonRequest]) -> MoonBatchResponse:
    results = []
    for request in moon_requests:
        x = request.x
        y = request.y
        code, probability = moon_model.predict(x, y)
        label = MOON_LABELS[code]
        color = MOON_COLORS[code]
        results.append(MoonResult(
            code=code, 
            label=label, 
            color=color,
            probability=probability
        ))
    return MoonBatchResponse(
        result=results,
        version=__version__,
        timestamp=datetime.now().isoformat(),
    )


@app.get("/moon/evaluation/", response_class=HTMLResponse)
def get_evaluation():
    report_bytes = pkgutil.get_data("fish", "data/evaluation.html")
    report_html = report_bytes.decode('utf-8')
    
    return HTMLResponse(content=report_html)
