import requests
import pandas as pd
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv(dotenv_path="./config/.env")

API_URL = os.getenv("API_URL")  # ej: "https://api.open-meteo.com/v1/forecast"
LAT = os.getenv("LAT")
LON = os.getenv("LON")

def extract_weather_data():
    """Extrae datos de clima desde la API pública"""
    try:
        params = {
            "latitude": LAT,
            "longitude": LON,
            "hourly": "temperature_2m,relative_humidity_2m,wind_speed_10m",
            "timezone": "auto"
        }

        response = requests.get(API_URL, params=params)
        response.raise_for_status()

        data = response.json()
        print(" Datos extraidos correctamente")

        # Convertir a DataFrame
        df = pd.DataFrame({
            "datetime": data["hourly"]["time"],
            "temperature_c": data["hourly"]["temperature_2m"],
            "humidity_percent": data["hourly"]["relative_humidity_2m"],
            "wind_speed_ms": data["hourly"]["wind_speed_10m"],
            "latitude": float(LAT),
            "longitude": float(LON),
        })

        return df

    except Exception as e:
        print(" Error en la extraccion:", e)
        return None


if __name__ == "__main__":
    df = extract_weather_data()
    print(df.head())
