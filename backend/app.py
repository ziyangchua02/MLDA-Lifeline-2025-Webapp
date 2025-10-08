from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("ctg_best_pipeline_XGB.joblib")
label_map = {0: "Normal", 1: "Suspect", 2: "Pathologic"}

class InputData(BaseModel):
    LB: float
    AC: float
    FM: float
    UC: float
    ASTV: float
    MSTV: float
    ALTV: float
    MLTV: float
    DL: float
    DS: float
    DP: float
    Width: float
    Mode: float
    Mean: float
    Median: float
    Variance: float
    Tendency: float

@app.post("/predict")
def predict(data: InputData):
    input_dict = data.dict()
    X = pd.DataFrame([input_dict])
    y_pred = model.predict(X)
    result = label_map[int(y_pred[0])]
    return {"prediction": result}

@app.get("/")
def read_root():
    return {"message": "Backend running"}
