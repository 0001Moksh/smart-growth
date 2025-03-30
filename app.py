import pandas as pd
import numpy as np
import openmeteo_requests
import requests_cache
from retry_requests import retry
import joblib
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from dotenv import dotenv_values
import requests

app = FastAPI()

getenv = dotenv_values(".env")
# weather_api = getenv.get('weather_api')
weather_api = "1236669c1abf975e5b7339f2629851d8"

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "https://smart-growth-3.onrender.com/docs"}

water_model = joblib.load("models/water_req_model.pkl")
fertilizer_model = joblib.load("models/fertilizer_req_model.pkl")
encoder = joblib.load("models/crop_encoder.pkl") 

print("Models loaded successfully!")


# API for Water & Fertilizer Prediction
@app.get("/predict")
def predict_water_fertilizer(
    soil_moisture: float, 
    crop: str, 
    rainfall_mm: float, 
    nitrogen: float, 
    phosphorus: float, 
    potassium: float, 
    uv_index: float,
    latitude: float,
    longitude: float,
):
    crop_encoded = np.zeros(len(encoder.get_feature_names_out(['Crop']))) 
    if crop in encoder.categories_[0]:
        crop_idx = list(encoder.categories_[0]).index(crop) - 1 
        if crop_idx >= 0:
            crop_encoded[crop_idx] = 1 

    user_water_input = np.array([soil_moisture, rainfall_mm] + list(crop_encoded)).reshape(1, -1)
    water_required = water_model.predict(user_water_input)[0]

    user_fertilizer_input = np.array([nitrogen, phosphorus,potassium, uv_index]).reshape(1, -1)
    fertilizer_needed = fertilizer_model.predict(user_fertilizer_input)[0]

    # )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))
    cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
    retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
    # openmeteo = openmeteo_requests.Client(session = retry_session)
    # url = "https://api.open-meteo.com/v1/forecast"
    # params = {
    # 	"latitude": latitude,
    # 	"longitude": longitude,
    # 	"daily": ["temperature_2m_max", "temperature_2m_min", "uv_index_max", "sunshine_duration", "daylight_duration", "sunset", "sunrise", "uv_index_clear_sky_max", "rain_sum", "showers_sum", "snowfall_sum", "precipitation_sum", "precipitation_hours", "precipitation_probability_max", "apparent_temperature_min", "apparent_temperature_max", "weather_code", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant", "shortwave_radiation_sum", "et0_fao_evapotranspiration"],
    # 	"current": ["apparent_temperature", "temperature_2m", "relative_humidity_2m", "is_day", "wind_speed_10m", "wind_direction_10m", "wind_gusts_10m", "precipitation", "showers", "snowfall", "rain", "weather_code", "cloud_cover", "pressure_msl", "surface_pressure"]
    # }
    
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,uv_index_max,sunshine_duration,daylight_duration,sunset,sunrise,uv_index_clear_sky_max,rain_sum,showers_sum,snowfall_sum,precipitation_sum,precipitation_hours,precipitation_probability_max,apparent_temperature_min,apparent_temperature_max,weather_code,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration&current=apparent_temperature,temperature_2m,relative_humidity_2m,is_day,wind_speed_10m,wind_direction_10m,wind_gusts_10m,precipitation,showers,snowfall,rain,weather_code,cloud_cover,pressure_msl,surface_pressure"
    response = retry_session.get(url)
    weather_data = response.json()    
    return {
        "Estimated Water Requirement (liters per meter-square)": round(water_required, 2),
        "Estimated Fertilizer Needed (kg/ha)": round(fertilizer_needed, 2),
        "soil_moisture":soil_moisture,  
        "crop":crop,
        "rainfall_mm":rainfall_mm, 
        "nitrogen":nitrogen, 
        "phosphorus":phosphorus , 
        "potassium":potassium , 
        "uv_index":uv_index,
        "weather_data":weather_data,
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
