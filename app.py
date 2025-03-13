from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
import numpy as np
import joblib
import requests

app = FastAPI()

getenv = dotenv_values(".env")
weather_api = getenv.get('weather_api')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "http://127.0.0.1:8000/docs"}

# Load Models
water_model = joblib.load("models/water_requirement_model.pkl")
fertilizer_model = joblib.load("models/fertilizer_requirement_model.pkl")
encoder = joblib.load("models/crop_encoder.pkl")

# API for Water & Fertilizer Prediction
@app.get("/predict")
def predict_water_fertilizer(
    soil_moisture: float, 
    crop: str, 
    rainfall_mm: float, 
    nitrogen: float, 
    phosphorus: float, 
    potassium: float, 
    uv_index: float
):
    # crop One-Hot Encoding
    crop_encoded = np.zeros(len(encoder.get_feature_names_out(['Crop']))) 
    if crop in encoder.categories_[0]:  # Check if crop exists in trained data
        crop_idx = list(encoder.categories_[0]).index(crop) - 1 
        if crop_idx >= 0:
            crop_encoded[crop_idx] = 1  # Set corresponding index to 1

    # Prepare Input for Water Model
    user_water_input = np.array([soil_moisture, rainfall_mm] + list(crop_encoded)).reshape(1, -1)
    water_required = water_model.predict(user_water_input)[0]

    # Prepare Input for Fertilizer Model
    user_fertilizer_input = np.array([nitrogen, phosphorus, uv_index]).reshape(1, -1)
    fertilizer_needed = fertilizer_model.predict(user_fertilizer_input)[0]

    return {
        "Estimated Water Requirement (liters per meter-square)": round(water_required, 2),
        "Estimated Fertilizer Needed (kg/ha)": round(fertilizer_needed, 2)
    }

@app.get("/report")
def weather_report(location: str = Query(..., description="Enter location for weather report")):
    try:
        api_key = weather_api
        url = f'http://api.weatherstack.com/current?access_key={api_key}&query={location}'
        response = requests.get(url)
        data = response.json()
        
        if "current" not in data:
            return {"error": "Invalid response from weather API", "details": data}
        
        current_weather = data['current']
        observation_time = current_weather['observation_time']
        humidity = current_weather['humidity']
        pressure = current_weather['pressure']

        return {
            "location": location,
            "observation_time":observation_time,
            "temperature": current_weather['temperature'],
            "humidity":humidity,
            "pressure":pressure,
            "weather_descriptions": current_weather['weather_descriptions'],
        }

    except Exception as e:
        return {"error": str(e)}
