# HEATSHIELD INDIA

AI-powered urban heat decision-support dashboard for Indian cities, built for the ISRO/Bharatiya Antariksh Hackathon.

Live frontend: https://polite-lebkuchen-5eb8db.netlify.app

> Note: the Netlify site hosts the frontend. Temperature prediction needs the FastAPI backend running locally or deployed separately with `VITE_API_URL` pointed to that backend.

## What It Does

- Predicts urban heat risk for Delhi, Mumbai, Hyderabad, and Bengaluru.
- Uses city-specific ML model selection for temperature prediction.
- Calculates an Urban Cooling Index from vegetation, humidity, wind speed, building density, and predicted temperature.
- Generates an AI confidence score for the prediction.
- Explains heat risk through dynamic AI factors such as low NDVI, high building density, low wind speed, high humidity, and high predicted temperature.
- Provides city-specific cooling recommendations.
- Displays satellite-style city heatmaps with blue place markers, temperature labels, and zone categories.
- Includes place search and a heat-threshold control to focus on hotter regions.
- Presents the experience through a dark ISRO-inspired dashboard UI with space visuals, custom cursor effects, and responsive cards.

## Supported Cities

- Delhi
- Mumbai
- Hyderabad
- Bengaluru

## Tech Stack

- Frontend: React, Vite, CSS
- Backend: FastAPI, Python
- ML: scikit-learn/joblib city models
- Maps: Plotly heatmaps with satellite basemap
- Deployment: Netlify for the frontend

## Project Structure

```text
Coolscape-AI/
├── backend/
│   ├── main.py
│   └── requirements.txt
├── heatshield-frontend/
│   ├── public/heatmaps/
│   ├── src/App.jsx
│   ├── src/index.css
│   └── package.json
├── city_heatmap.py
├── models/
├── datasets/
└── README.md
```

## Run Locally

### Backend

```bash
cd backend
uvicorn main:app --reload
```

If you are using the project virtual environment:

```bash
cd backend
../venv/bin/python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

### Frontend

```bash
cd heatshield-frontend
npm install
npm run dev
```

Open the local app at:

```text
http://localhost:5173/
```

## Prediction API

Endpoint:

```text
POST /predict
```

Example request:

```bash
curl -X POST http://127.0.0.1:8000/predict \
  -H "Content-Type: application/json" \
  -d '{
    "city": "Delhi",
    "ndvi": 0.18,
    "humidity": 72,
    "windSpeed": 6,
    "buildingDensity": 82
  }'
```

Expected response fields:

- `temperature`
- `city`
- `risk`
- `coolingIndex`
- `confidence`
- `factors`
- `recommendations`
- `status`

## Regenerate Heatmaps

```bash
python3 city_heatmap.py
```

This refreshes the city-wise HTML maps used by the frontend in `heatshield-frontend/public/heatmaps/`.

## Landsat April-June 2025 Dataset

The project includes an Earth Engine export script for Landsat 8/9 Collection 2 Level 2 data from April 1, 2025 through June 30, 2025.

The script exports:

- NDVI from Landsat red and near-infrared surface reflectance bands
- Land Surface Temperature in Celsius from the Landsat thermal band
- Latitude/longitude point samples for Delhi, Mumbai, Hyderabad, and Bengaluru

Authenticate Google Earth Engine once:

```bash
earthengine authenticate
```

Run the exporter:

```bash
python3 landsat_apr_jun_2025_export.py
```

The CSV exports are created in this Google Drive folder:

```text
heatshield_landsat_apr_jun_2025
```

After the Earth Engine export tasks finish, download the CSV files into `datasets/`. Those files can then be used to rebuild master datasets, retrain city models, or regenerate city heatmaps.

## Deployment

Frontend deployment:

```bash
cd heatshield-frontend
npm run build
npx netlify deploy --prod --dir dist
```

For public prediction support, deploy the backend separately and configure the frontend environment variable:

```text
VITE_API_URL=https://your-backend-url
```

## Data Note

The current dashboard is not fully real-time. It uses project datasets, generated city heatmaps, trained models, and user-provided environmental inputs. It is designed so live satellite, weather, and municipal sensor feeds can be connected later.

## Team

Powered by Team 404 Brain Not Found.
