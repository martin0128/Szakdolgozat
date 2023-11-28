import math
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from tensorflow import keras
import numpy as np
from scipy.integrate import solve_ivp
from sklearn.metrics import r2_score
import os

class SystemRequest(BaseModel):
    name: str
    modelParams: list[float] = []


class SystemResponse(BaseModel):
    expected: list[list[float]] = []
    predicted: list[list[float]] = []
    r2Score: float

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
        expected, predicted, r2Score = MSDPredict(request.modelParams)
    elif(request.name == "Inverted Pendulum"):
        expected, predicted, r2Score = InvertedPredict(request.modelParams)
    elif(request.name == "SIRD"):
        expected, predicted, r2Score = SIRDPredict(request.modelParams)
    elif(request.name == "Predator-Prey"):
        expected, predicted, r2Score = PredatorPredict(request.modelParams)
    else:
        expected, predicted = []
            
    return SystemResponse(expected=expected, predicted=predicted, r2Score=r2Score)


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
        output.append([times[i], position[i], speed[i], modelParams[0], modelParams[1], modelParams[2]])
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
    score = r2_score(position, predicted[:,1])
    score2 = r2_score(speed, predicted[:,2])
    realscore = (score + score2) / 2
    return (expected,[predicted[:,1], predicted[:,2]], realscore)

def InvertedPredict(params):
    model = keras.models.load_model("./Inverted")
    frequency = 2000
    x = 9.81
    y = params[0]
    z = params[1]
    modelParams = [x,y,z]
    tStart = float(0)
    tEnd = float(20)

    t = np.linspace(0, 20, frequency)

    x0 = [1, 0]
    sol = solve_ivp(InvertedPendulum, [tStart, tEnd], x0, t_eval=t, args=(modelParams))
    times = sol.t
    position = sol.y[0]
    speed = sol.y[1]
    output = []
    for i in range(len(times)):
        output.append([times[i], position[i], speed[i], modelParams[0], modelParams[1], modelParams[2]])
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
    score = r2_score(position, predicted[:,1])
    score2 = r2_score(speed, predicted[:,2])
    realscore = (score + score2) / 2
    return (expected,[predicted[:,1], predicted[:,2]], realscore)

def SIRDPredict(params):
    model = keras.models.load_model('./SIRDModel')
    frequency = 2000
    modelParams = params
    tStart = float(0)
    tEnd = float(90)

    t = np.linspace(15, 90, frequency)

    I0 = 1
    x0 = [modelParams[0] - I0, I0, 0, 0]
    sol = solve_ivp(SIRD, [tStart, tEnd], x0, t_eval=t, args=(modelParams))
    time = sol.t
    times = sol.y[0]
    position = sol.y[1]
    speed = sol.y[2]
    l4 = sol.y[3]
    output = []
    for i in range(len(times)):
        output.append([time[i],times[i],position[i], speed[i], l4[i], modelParams[1], modelParams[2], modelParams[3]])
    output = np.array(output)
    susmin = np.min(output[:,1])
    susmax = np.max(output[:,1])
    infmin = np.min(output[:,2])
    infmax = np.max(output[:,2])
    recmin = np.min(output[:,3])
    recmax = np.max(output[:,3])
    decmin = np.min(output[:,4])
    decmax = np.max(output[:,4])
    output[:,1] = NormalizeData(output[:,1])
    output[:,2] = NormalizeData(output[:,2])
    output[:,3] = NormalizeData(output[:,3])
    output[:,4] = NormalizeData(output[:,4])
    x_test, y_test = createXY(output, 400)
    predictArray= x_test[[0]]
    predicted = np.array([x_test[0,0]])
    for i in range(1,400):
        predicted = np.append(predicted,np.array([x_test[0,i]]), axis=0)
    for i in range(len(x_test)+1):
        prediction = model.predict(predictArray)
        predictArray=predictArray[0][len(predictArray):]
        predictArray = np.append(predictArray, prediction, axis=0)
        predictArray = np.expand_dims(predictArray,0)
        predicted = np.append(predicted,prediction,axis=0)
    predicted[:,1] = denormalizeData(predicted[:,1],susmin,susmax)
    predicted[:,2] = denormalizeData(predicted[:,2],infmin,infmax)
    predicted[:,3] = denormalizeData(predicted[:,3],recmin,recmax)
    predicted[:,4] = denormalizeData(predicted[:,4],decmin,decmax)

    expected = sol.y
    score = r2_score(times, predicted[:,1])
    score2 = r2_score(position, predicted[:,2])
    score3 = r2_score(speed, predicted[:,3])
    score4 = r2_score(l4, predicted[:,4])
    realscore = (score + score2 +score3 +score4) /4
    return (expected,[predicted[:,1], predicted[:,2], predicted[:,3], predicted[:,4]], realscore)

def PredatorPredict(params):
    model = keras.models.load_model("./PredatorPrey")
    q = params[0]/365
    w = params[1]/365
    e = params[2]/365
    r = params[3]/365
    t = 20000
    x = PredatorPrey(t,q,w,e,r)
    output = []
    for i in range(x.shape[1]):
        if (i % 10 == 0):
            output.append([x[0,i], x[1,i], params[0], params[1], params[2], params[3]])
    output = np.array(output)
    preymin = np.min(output[:,0])
    preymax = np.max(output[:,0])
    predmin = np.min(output[:,1])
    predmax = np.max(output[:,1])
    output[:,0] = NormalizeData(output[:,0])
    output[:,1] = NormalizeData(output[:,1])
    x_test, y_test = createXY(output, 60)
    predictArray= x_test[[0]]
    predicted = np.array([x_test[0,0]])
    for i in range(1,60):
        predicted = np.append(predicted,np.array([x_test[0,i]]), axis=0)
    for i in range(len(x_test)+1):
        prediction = model.predict(predictArray)
        predictArray=predictArray[0][len(predictArray):]
        predictArray = np.append(predictArray, prediction, axis=0)
        predictArray = np.expand_dims(predictArray,0)
        predicted = np.append(predicted,prediction,axis=0)
    predicted[:,0] = denormalizeData(predicted[:,0], preymin, preymax)
    predicted[:,1] = denormalizeData(predicted[:,1], predmin, predmax)
    output[:,0] = denormalizeData(output[:,0], preymin, preymax)
    output[:,1] = denormalizeData(output[:,1], predmin, predmax)
    expected = [output[:,0], output[:,1]]

    score = r2_score(output[:,0], predicted[:,0])
    score2 = r2_score(output[:,1], predicted[:,1])
    realscore = (score + score2) / 2

    return (expected, [predicted[:,0], predicted[:,1]], realscore)
        

def MassSpringDamper(t, y, a, b, c):
    dxdt = np.zeros(2)

    dxdt[0] = y[1]
    dxdt[1] = -(c / a) * y[0] - (b / a) * y[1]
    return dxdt

def InvertedPendulum(t, x, a, b, c):
    dxdt = np.zeros(2)

    dxdt[0] = x[1]
    dxdt[1] = (a / b) * math.sin(x[0]) - c * x[1]
    return dxdt

def SIRD(t, x, a, b, c, d):
    dxdt = np.zeros(4)

    dxdt[0] = -(b / a) * x[0] * x[1]
    dxdt[1] = (b / a) * x[0] * x[1] - c * x[1] - d * x[1]
    dxdt[2] = c * x[1]
    dxdt[3] = d * x[1]
    return dxdt

def PredatorPrey(t,a,b,c,d):
  hk = 10
  lk = 10
  x = np.zeros((2,t))
  x[0,0] = hk
  x[1,0] = lk
  for i in range(t-1):
    hkk = hk + b*hk - a*lk*hk
    lkk = lk + c*lk*hk - d*lk
    x[0,i+1] = hkk
    x[1,i+1] = lkk
    hk = hkk
    lk = lkk
  return x

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

def NormalizeData(data):
  min = np.min(data)
  max = np.max(data)
  for i in range(len(data)):
    data[i] = (data[i] - min) / (max - min)
  return data

def denormalizeData(data, min, max):
  for i in range(len(data)):
    data[i] = data[i] * (max - min) + min
  return data