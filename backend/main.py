from pathlib import Path

import joblib
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="CoolScape AI Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "model_artifacts"

if not MODEL_DIR.exists():
    MODEL_DIR = BASE_DIR.parent / "models"

MODEL_PATHS = {
    "Delhi": MODEL_DIR / "real_temperature_model_v3.pkl",
    "Mumbai": MODEL_DIR / "mumbai_temperature_model.pkl",
    "Hyderabad": MODEL_DIR / "hyderabad_temperature_model.pkl",
    "Bengaluru": MODEL_DIR / "bengaluru_temperature_model.pkl",
}

_loaded_models = {}

CITY_RECOMMENDATIONS = {
    "Delhi": [
        "Expand dense tree cover around heat hotspot corridors.",
        "Deploy cool roofs on public buildings and high-density blocks.",
        "Use reflective pavements in exposed transport and market zones.",
    ],
    "Mumbai": [
        "Protect coastal ventilation paths from dense obstruction.",
        "Build shaded walkways for humid pedestrian corridors.",
        "Use humidity-sensitive planning for outdoor work and transit nodes.",
    ],
    "Hyderabad": [
        "Restore lakes and buffer zones to improve evaporative cooling.",
        "Create green corridors between dense urban neighborhoods.",
        "Scale cool roofs across commercial and residential hotspots.",
    ],
    "Bengaluru": [
        "Protect existing tree canopy in high-growth neighborhoods.",
        "Develop green IT corridors around office clusters.",
        "Preserve ventilation corridors across expanding urban edges.",
    ],
}

class PredictionInput(BaseModel):
    city: str = "Delhi"
    ndvi: float
    humidity: float
    windSpeed: float
    buildingDensity: float


def clamp(value: float, minimum: float, maximum: float) -> float:
    return max(minimum, min(maximum, value))


def calculate_cooling_index(data: PredictionInput, predicted_temp: float) -> float:
    ndvi_score = clamp(data.ndvi * 100, 0, 100)
    wind_score = clamp(data.windSpeed * 5, 0, 100)
    density_score = 100 - clamp(data.buildingDensity, 0, 100)
    humidity_score = 100 - clamp(abs(data.humidity - 55) * 2, 0, 100)
    heat_score = 100 - clamp((predicted_temp - 30) * 5, 0, 100)

    cooling_index = (
        ndvi_score * 0.30
        + wind_score * 0.20
        + density_score * 0.20
        + humidity_score * 0.15
        + heat_score * 0.15
    )
    return round(clamp(cooling_index, 0, 100), 1)


def calculate_confidence(data: PredictionInput) -> float:
    range_penalty = 0
    if not 0 <= data.ndvi <= 1:
        range_penalty += 20
    if not 0 <= data.humidity <= 100:
        range_penalty += 15
    if not 0 <= data.windSpeed <= 30:
        range_penalty += 15
    if not 0 <= data.buildingDensity <= 100:
        range_penalty += 15

    stress_penalty = 0
    if data.ndvi < 0.15:
        stress_penalty += 4
    if data.humidity > 85:
        stress_penalty += 4
    if data.windSpeed < 3:
        stress_penalty += 4
    if data.buildingDensity > 90:
        stress_penalty += 4

    return round(clamp(94 - range_penalty - stress_penalty, 55, 98), 1)


def get_model(city: str):
    if city not in _loaded_models:
        _loaded_models[city] = joblib.load(MODEL_PATHS[city])
    return _loaded_models[city]


@app.get("/")
def health_check():
    return {
        "status": "success",
        "service": "HeatShield India AI Backend",
        "models": list(MODEL_PATHS.keys()),
    }


@app.post("/predict")
def predict_temperature(data: PredictionInput):
    city = data.city

    if city not in MODEL_PATHS:
        return {
            "status": "error",
            "message": "Invalid city selected"
        }

    model_input = [[
        data.ndvi,
        data.humidity,
        data.windSpeed,
        data.buildingDensity,
    ]]

    prediction = get_model(city).predict(model_input)[0]
    predicted_temp = round(float(prediction), 2)
    risk = (
        "Extreme" if predicted_temp >= 45 else
        "High" if predicted_temp >= 40 else
        "Moderate" if predicted_temp >= 35 else
        "Low"
    )

    factors = []

    if data.ndvi < 0.25:
        factors.append("Low vegetation cover is increasing surface heat.")
    if data.buildingDensity > 70:
        factors.append("High building density is trapping urban heat.")
    if data.windSpeed < 10:
        factors.append("Low wind speed is reducing natural ventilation.")
    if data.humidity > 65:
        factors.append("High humidity may increase perceived heat stress.")
    if predicted_temp >= 40:
        factors.append("High predicted temperature indicates a priority cooling zone.")

    if not factors:
        factors.append("Urban climate inputs are balanced with no severe heat amplifier detected.")

    recommendations = CITY_RECOMMENDATIONS[city].copy()

    if predicted_temp >= 40:
        recommendations.append("Prioritize cooling interventions in hotspot zones.")

    cooling_index = calculate_cooling_index(data, predicted_temp)
    confidence = calculate_confidence(data)

    return {
        "temperature": predicted_temp,
        "city": city,
        "risk": risk,
        "coolingIndex": cooling_index,
        "confidence": confidence,
        "factors": factors,
        "recommendations": recommendations,
        "status": "success"
    }
