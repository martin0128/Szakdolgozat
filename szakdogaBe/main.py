from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from tensorflow import keras
import numpy as np
from scipy.integrate import solve_ivp
import os

class SystemRequest(BaseModel):
    name: str
    modelParams: list[float] = []


class SystemResponse(BaseModel):
    expected: list[list[float]] = []
    predicted: list[list[float]] = []

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
        expected, predicted = MSDPredict(request.modelParams)
    else:
        expected, predicted = []
            
    return SystemResponse(expected=expected, predicted=predicted)


def MSDPredict(params):
    model = keras.models.load_model("./Models")
    frequency = 2000
    modelParams = params
    tStart = float(0)
    tEnd = float(20)

    t = np.linspace(0, 20, frequency)

    x0 = [1, 0]
    sol = solve_ivp(MassSpringDamper, [tStart, tEnd], x0, t_eval=t, args=(modelParams))
    times = sol.t
    position = sol.y[0]
    speed = sol.y[1]
    output = []
    for i in range(len(times)):
        output.append([times[i], position[i], speed[i], params[0], params[1], params[2]])
    output = np.array(output)
    x_test, y_test = createXY(output, 100)
    predictArray= x_test[[0]]
    predicted = np.array([x_test[0,0]])
    for i in range(1,100):
        predicted = np.append(predicted,np.array([x_test[0,i]]), axis=0)
    for i in range(len(x_test)+1):
        prediction = model.predict(predictArray)
        predictArray=predictArray[0][len(predictArray):]
        predictArray = np.append(predictArray, prediction, axis=0)
        predictArray = np.expand_dims(predictArray,0)
        predicted = np.append(predicted,prediction,axis=0)

    expected = sol.y
    return (expected,[predicted[:,1], predicted[:,2]])

def MassSpringDamper(t, y, a, b, c):
    dxdt = np.zeros(2)

    dxdt[0] = y[1]
    dxdt[1] = -(c / a) * y[0] - (b / a) * y[1]
    return dxdt

def createXY(data, lookback):
  input = []
  output = []
  for i in range(len(data)):
    if(i+lookback+1 < len(data)):
      temp = []
      for j in range(lookback):
        temp.append(data[i+j])
      input.append(temp)
      output.append(data[i+lookback+1])
  return np.array(input), np.array(output)