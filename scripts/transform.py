import pandas as pd
import numpy as np
from datetime import datetime

def transform_weather_data(df: pd.DataFrame) -> pd.DataFrame:
    """Transforma y limpia los datos del clima"""
    try:
        # Convertir columna datetime a Python datetime
        df["datetime"] = pd.to_datetime(df["datetime"]).apply(lambda x: x.to_pydatetime())

        # Eliminar duplicados
        df = df.drop_duplicates(subset=["datetime"])

        # Agregar marca de tiempo ETL
        df["etl_loaded_at"] = datetime.utcnow()

        print(" Datos transformados correctamente")
        return df

    except Exception as e:
        print(" Error en la transformación:", e)
        return None


if __name__ == "__main__":
    import extract
    df_raw = extract.extract_weather_data()
    df_trans = transform_weather_data(df_raw)
    print(df_trans.head())