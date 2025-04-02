# import pandas as pd
# import numpy as np
# import openmeteo_requests
# import requests_cache
# from retry_requests import retry
# import joblib
# from fastapi import FastAPI, Query
# from fastapi.middleware.cors import CORSMiddleware
# from dotenv import dotenv_values
# import requests

# app = FastAPI()

# getenv = dotenv_values(".env")
# # weather_api = getenv.get('weather_api')
# weather_api = "1236669c1abf975e5b7339f2629851d8"

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["GET"],
#     allow_headers=["*"],
# )

# @app.get("/")
# async def root():
#     return {"message": "https://smart-growth-3.onrender.com/docs"}

# water_model = joblib.load("models/water_req_model.pkl")
# fertilizer_model = joblib.load("models/fertilizer_req_model.pkl")
# encoder = joblib.load("models/crop_encoder.pkl") 

# print("Models loaded successfully!")

# # API for Water & Fertilizer Prediction
# @app.get("/predict")
# def predict_water_fertilizer(
#     crop: str, 
#     latitude: float,
#     longitude: float,
# ):
#     cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
#     retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)

#     # static input of parameter 
#     soil_moisture = 0.5
#     rainfall_mm = 0.5
#     nitrogen = 0.5
#     phosphorus = 0.5
#     potassium = 0.5
#     uv_index = 0.5

#     url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,uv_index_max,sunshine_duration,daylight_duration,sunset,sunrise,uv_index_clear_sky_max,rain_sum,showers_sum,snowfall_sum,precipitation_sum,precipitation_hours,precipitation_probability_max,apparent_temperature_min,apparent_temperature_max,weather_code,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration&current=apparent_temperature,temperature_2m,relative_humidity_2m,is_day,wind_speed_10m,wind_direction_10m,wind_gusts_10m,precipitation,showers,snowfall,rain,weather_code,cloud_cover,pressure_msl,surface_pressure"
#     response = retry_session.get(url)
#     weather_data = response.json()    

    # # Validate input parameters soil_moisture
    # blynk_url = "https://blynk.cloud/external/api/get?token=NIkHnxrx2UMZaMcFF1NS38yvfH4W3INr&V1"
    # try:
    #     response = requests.get(blynk_url)
    #     soil_moisture = float(response.text)
    # except Exception as e:
    #     return {"error": "Failed to fetch soil_moisture", "details": str(e)}
    
#     # # Validate input parameters rainfall_mm
    # blynk_url = "https://blynk.cloud/external/api/get?token=NIkHnxrx2UMZaMcFF1NS38yvfH4W3INr&V2"
    # try:
    #     response = requests.get(blynk_url)
    #     rainfall_mm = float(response.text)
    # except Exception as e:
    #     return {"error": "Failed to fetch rainfall_mm", "details": str(e)}
    
#     # # Validate input parameters nitrogen
#     # blynk_url = "https://blynk.cloud/external/api/get?token=NIkHnxrx2UMZaMcFF1NS38yvfH4W3INr&V3"
#     # try:
#     #     response = requests.get(blynk_url)
#     #     nitrogen = float(response.text)
#     # except Exception as e:
#     #     return {"error": "Failed to fetch nitrogen", "details": str(e)}
    
#     # # Validate input parameters phosphorus
#     # blynk_url = "https://blynk.cloud/external/api/get?token=NIkHnxrx2UMZaMcFF1NS38yvfH4W3INr&V4"
#     # try:
#     #     response = requests.get(blynk_url)
#     #     phosphorus = float(response.text)
#     # except Exception as e:
#     #     return {"error": "Failed to fetch phosphorus", "details": str(e)}
    
#     # # Validate input parameters potassium
#     # blynk_url = "https://blynk.cloud/external/api/get?token=NIkHnxrx2UMZaMcFF1NS38yvfH4W3INr&V5"
#     # try:
#     #     response = requests.get(blynk_url)
#     #     potassium = float(response.text)
#     # except Exception as e:
#     #     return {"error": "Failed to fetch potassium", "details": str(e)}
    
#     # # Validate input parameters uv_index
#     # blynk_url = "https://blynk.cloud/external/api/get?token=NIkHnxrx2UMZaMcFF1NS38yvfH4W3INr&V6"
#     # try:
#     #     response = requests.get(blynk_url)
#     #     uv_index = float(response.text)
#     # except Exception as e:
#     #     return {"error": "Failed to fetch uv_index", "details": str(e)}

#     crop_encoded = np.zeros(len(encoder.get_feature_names_out(['Crop']))) 
#     # model is trained on 4 crops, so we need to check if the crop is in the encoder categories
    
#     if crop in encoder.categories_[0]:
#         crop_idx = list(encoder.categories_[0]).index(crop) - 1 
#         if crop_idx >= 0:
#             crop_encoded[crop_idx] = 1 

#     user_water_input = np.array([soil_moisture, rainfall_mm] + list(crop_encoded)).reshape(1, -1)
#     water_required = water_model.predict(user_water_input)[0]

#     user_fertilizer_input = np.array([nitrogen, phosphorus,potassium, uv_index]).reshape(1, -1)
#     fertilizer_needed = fertilizer_model.predict(user_fertilizer_input)[0]

#     # )))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))))

#     return {
#         "Estimated Water Requirement (liters per meter-square)": round(water_required, 2),
#         "Estimated Fertilizer Needed (kg/ha)": round(fertilizer_needed, 2),
#         "soil_moisture":soil_moisture,  
#         "crop":crop,
#         "rainfall_mm":rainfall_mm,  
#         "nitrogen":nitrogen, 
#         "phosphorus":phosphorus, 
#         "potassium":potassium, 
#         "uv_index":uv_index,
#         "weather_data":weather_data,
#     }

# @app.get("/report")
# def weather_report(location: str = Query(..., description="Enter location for weather report")):
#     try:
#         api_key = weather_api
#         url = f'http://api.weatherstack.com/current?access_key={api_key}&query={location}'
#         response = requests.get(url)
#         data = response.json()
        
#         if "current" not in data:
#             return {"error": "Invalid response from weather API", "details": data}
        
#         current_weather = data['current']
#         observation_time = current_weather['observation_time']
#         humidity = current_weather['humidity']
#         pressure = current_weather['pressure']

#         return {
#             "location": location,
#             "observation_time":observation_time,
#             "temperature": current_weather['temperature'],
#             "humidity":humidity,
#             "pressure":pressure,
#             "weather_descriptions": current_weather['weather_descriptions'],
#         }
#     except Exception as e:
#         return {"error": str(e)}



import numpy as np
import requests_cache
from retry_requests import retry
import joblib
import requests
import io
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

app = FastAPI()

# Load API Keys securely
load_dotenv()
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

def load_model(url):
    response = requests.get(url)
    return joblib.load(io.BytesIO(response.content))

water_model = joblib.load("models/water_req_model.pkl")
fertilizer_model = joblib.load("models/fertilizer_req_model.pkl")
encoder = joblib.load("models/crop_encoder.pkl")

@app.get("/predict")
def predict_water_fertilizer(crop: str, land:float ,latitude: float,  longitude: float):
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,uv_index_max,sunshine_duration,daylight_duration,sunset,sunrise,uv_index_clear_sky_max,rain_sum,showers_sum,snowfall_sum,precipitation_sum,precipitation_hours,precipitation_probability_max,apparent_temperature_min,apparent_temperature_max,weather_code,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration&current=apparent_temperature,temperature_2m,relative_humidity_2m,is_day,wind_speed_10m,wind_direction_10m,wind_gusts_10m,precipitation,showers,snowfall,rain,weather_code,cloud_cover,pressure_msl,surface_pressure"
    response = retry_session.get(url)
    weather_data = response.json() 

    # Static input parameters (these should ideally be fetched dynamically)
    blynk_url = "https://blynk.cloud/external/api/get?token=NIkHnxrx2UMZaMcFF1NS38yvfH4W3INr&V3"
    try:
        response = requests.get(blynk_url)
        soil_moisture = float(response.text)
        DRY_VALUE = 1023  # Example value (fully dry)
        WET_VALUE = 300   # Example value (fully wet)

        # Simulating response from sensor
        response_text =soil_moisture  # Example ADC value received as string
        soil_moisture = float(response_text)

        # Convert ADC value to percentage
        moisture_percentage = (1 - (soil_moisture - WET_VALUE) / (DRY_VALUE - WET_VALUE)) * 100
        soil_moisture_percentage = max(0, min(100, moisture_percentage))  # Ensure value stays in 0-100%

    except Exception as e:
        return {"error": "Failed to fetch soil_moisture", "details": str(e)}
    
    # blynk_url = "https://blynk.cloud/external/api/get?token=NIkHnxrx2UMZaMcFF1NS38yvfH4W3INr&V2"
    # try:
    #     response = requests.get(blynk_url)
    #     rainfall_mm = float(response.text)
    # except Exception as e:
    #     return {"error": "Failed to fetch rainfall_mm", "details": str(e)}
        # rain_sum
    rainfall_mm = weather_data.get("daily", {}).get("rain_sum", [None])[0]

    # nitrogen = np.random.randint(20, 80)
    # phosphorus = np.random.randint(15, 50)
    # potassium = np.random.randint(20, 60)
    nitrogen =80.3
    phosphorus = 30.2
    potassium = 40.2
    
    uv_index = weather_data.get("daily", {}).get("uv_index_max", [0])[0]

    # One-hot encode the crop
    crop_encoded = np.zeros(len(encoder.get_feature_names_out(['Crop'])))
    if crop in encoder.categories_[0]:
        crop_idx = list(encoder.categories_[0]).index(crop)  # Fixed indexing
        crop_encoded[crop_idx] = 1 

    # Model Predictions
    water_required_per_m2 = water_model.predict([[soil_moisture, rainfall_mm] + list(crop_encoded)])[0]

    fertilizer_needed_per_hectare = fertilizer_model.predict([[nitrogen, phosphorus, potassium, uv_index]])[0]
    total_fertilizer_needed = fertilizer_needed_per_hectare * land  # Already in kg per hectare


    return {
        "Estimated Water Requirement (liters/m2)": round(water_required_per_m2, 2),
        "Estimated Fertilizer Needed (kg)": round(total_fertilizer_needed, 2),
        "crop": crop,
        "soil_moisture_percentage": soil_moisture_percentage,  
        "rainfall_mm": rainfall_mm,  
        "nitrogen": nitrogen, 
        "phosphorus": phosphorus, 
        "potassium": potassium, 
        "uv_index": uv_index,
        "weather_data": weather_data,
    }


@app.get("/weather")
def weather(latitude: float,  longitude: float):
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&daily=temperature_2m_max,temperature_2m_min,uv_index_max,sunshine_duration,daylight_duration,sunset,sunrise,uv_index_clear_sky_max,rain_sum,showers_sum,snowfall_sum,precipitation_sum,precipitation_hours,precipitation_probability_max,apparent_temperature_min,apparent_temperature_max,weather_code,wind_speed_10m_max,wind_gusts_10m_max,wind_direction_10m_dominant,shortwave_radiation_sum,et0_fao_evapotranspiration&current=apparent_temperature,temperature_2m,relative_humidity_2m,is_day,wind_speed_10m,wind_direction_10m,wind_gusts_10m,precipitation,showers,snowfall,rain,weather_code,cloud_cover,pressure_msl,surface_pressure"
    cache_session = requests_cache.CachedSession('.cache', expire_after=3600)
    retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
    response = retry_session.get(url)
    weather_data = response.json()
    temperature_2m = weather_data.get("current", {}).get("temperature_2m", 0)

    
    return {"temperature": temperature_2m,}