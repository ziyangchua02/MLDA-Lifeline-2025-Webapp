from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import joblib

app = FastAPI(
    title="CTG Model Predictor",
    description="Predict fetal state (Normal / Suspect / Pathologic) from CTG input features",
    version="1.0"
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

@app.get("/")
def home():
    return {"message": "CTG Predictor API is running! Go to /docs to test."}


@app.post("/predict")
def predict(data: InputData):
    try:
        input_dict = {
            "LB": data.LB, "AC": data.AC, "FM": data.FM, "UC": data.UC,
            "ASTV": data.ASTV, "MSTV": data.MSTV, "ALTV": data.ALTV, "MLTV": data.MLTV,
            "DL": data.DL, "DS": data.DS, "DP": data.DP, "Width": data.Width,
            "Mode": data.Mode, "Mean": data.Mean, "Median": data.Median,
            "Variance": data.Variance, "Tendency": data.Tendency
        }

        X = pd.DataFrame([input_dict])

        print("DEBUG — Input shape:", X.shape)
        print("DEBUG — Columns:", X.columns.tolist())

        y_pred = model.predict(X)
        result = label_map[int(y_pred[0])]
        return {"prediction": result}

    except Exception as e:
        import traceback
        print("\n🚨 ERROR TRACEBACK 🚨")
        traceback.print_exc()
        return {"error": str(e)}
