from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

class SystemRequest(BaseModel):
    name: str
    modelParams: list[float] = []


class SystemResponse(BaseModel):
    expected: list[float] = []
    predicted: list[float] = []

origins = [
    "http://localhost",
    "http://localhost:5173",
]

app = FastAPI(title='szakdoga')

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
)

@app.get('/')
async def home() -> SystemRequest:
    return SystemRequest(name='asd')

@app.post('/predict/')
async def predict(request: SystemRequest) -> SystemResponse:
    if(request.name == "Mass Spring Damper"):
        expected, predicted = MSDPredict()
    else:
        expected, predicted = []
            
    return SystemResponse(expected=expected, predicted=predicted)


def MSDPredict():
    expected = [1]
    predicted = [1]
    return (expected, predicted)