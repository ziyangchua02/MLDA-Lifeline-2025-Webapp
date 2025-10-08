from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import joblib, pandas as pd
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

model = joblib.load("ctg_best_pipeline_XGB.joblib")
label_map = {0: "Normal", 1: "Suspect", 2: "Pathologic"}

class InputData(BaseModel):
    LB: float; AC: float; FM: float; UC: float; ASTV: float
    MSTV: float; ALTV: float; MLTV: float; DL: float; DS: float
    DP: float; Width: float; Mode: float; Mean: float; Median: float
    Variance: float; Tendency: float

@app.get("/")
def root():
    return {"message": "CTG Predictor is live!"}

@app.post("/predict")
def predict(data: InputData):
    df = pd.DataFrame([data.dict()])
    pred = model.predict(df)[0]
    return {"prediction": label_map[int(pred)]}
