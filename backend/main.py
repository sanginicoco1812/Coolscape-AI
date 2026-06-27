import joblib
import pandas as pd
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI(title="CoolScape AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

model = joblib.load("../models/real_temperature_model_v3.pkl")

class PredictionInput(BaseModel):
    ndvi: float
    humidity: float
    windSpeed: float
    buildingDensity: float


@app.post("/predict")
def predict_temperature(data: PredictionInput):
    try:
        # Create dataframe in the SAME order used while training
        input_df = pd.DataFrame([{
            "NDVI": data.ndvi,
            "Humidity": data.humidity,
            "WindSpeed": data.windSpeed,
            "BuildingDensity": data.buildingDensity
        }])

        # Predict
        predicted_temperature = model.predict(input_df)[0]

        return {
            "temperature": round(float(predicted_temperature), 2),
            "status": "success"
        }

    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }