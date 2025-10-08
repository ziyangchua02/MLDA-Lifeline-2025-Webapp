from fastapi import FastAPI
from pydantic import BaseModel
import joblib

# -------------------------------
# Load your trained model
# -------------------------------
model = joblib.load("ctg_best_pipeline_XGB_reduced.joblib")

# Label mapping (numeric → readable output)
label_map = {0: "Normal", 1: "Suspect", 2: "Pathologic"}

# -------------------------------
# Initialize FastAPI
# -------------------------------
app = FastAPI(
    title="CTG Model Predictor",
    description="Predict fetal state (Normal / Suspect / Pathologic) from CTG input features",
    version="1.0"
)

# -------------------------------
# Define input schema (17 features)
# -------------------------------
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

# -------------------------------
# Prediction endpoint
# -------------------------------
@app.post("/predict")
def predict(data: InputData):
    try:
        # Convert input into correct order for the model
        X = [[
            data.LB, data.AC, data.FM, data.UC,
            data.ASTV, data.MSTV, data.ALTV, data.MLTV,
            data.DL, data.DS, data.DP, data.Width,
            data.Mode, data.Mean, data.Median,
            data.Variance, data.Tendency
        ]]

        # Debug: see the input in the console
        print("DEBUG — Input to model:", X)

        # Run prediction
        y_pred = model.predict(X)

        # Debug: see model output
        print("DEBUG — Raw prediction:", y_pred)

        # Convert prediction to readable label
        result = label_map[int(y_pred[0])]

        return {"prediction": result}

    except Exception as e:
        import traceback
        print("\n🚨 ERROR TRACEBACK 🚨")
        traceback.print_exc()
        return {"error": str(e)}

# -------------------------------
# Root endpoint (optional)
# -------------------------------
@app.get("/")
def home():
    return {"message": "CTG Model Predictor API is running! Go to /docs to test."}
