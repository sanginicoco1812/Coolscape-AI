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

models = {
    "Delhi": joblib.load("../models/real_temperature_model_v3.pkl"),
    "Mumbai": joblib.load("../models/mumbai_temperature_model.pkl"),
    "Hyderabad": joblib.load("../models/hyderabad_temperature_model.pkl"),
    "Bengaluru": joblib.load("../models/bengaluru_temperature_model.pkl"),
}

class PredictionInput(BaseModel):
    city: str = "Delhi"
    ndvi: float
    humidity: float
    windSpeed: float
    buildingDensity: float

@app.post("/predict")
def predict_temperature(data: PredictionInput):
    city = data.city

    if city not in models:
        return {
            "status": "error",
            "message": "Invalid city selected"
        }

    input_df = pd.DataFrame([{
        "NDVI": data.ndvi,
        "Humidity": data.humidity,
        "WindSpeed": data.windSpeed,
        "BuildingDensity": data.buildingDensity
    }])

    prediction = models[city].predict(input_df)[0]

    return {
        "temperature": round(float(prediction), 2),
        "city": city,
        "status": "success"
    }