import psycopg2
from psycopg2.extras import execute_values
from dotenv import load_dotenv
import os
import pandas as pd
import datetime

# Cargar variables de entorno
load_dotenv(dotenv_path="./config/.env")

def load_to_postgres(df: pd.DataFrame):
    """Carga los datos transformados a la tabla weather_data en PostgreSQL"""

    try:
        # Conexión a PostgreSQL
        conn = psycopg2.connect(
            host=os.getenv("PG_HOST"),
            port=os.getenv("PG_PORT"),
            dbname=os.getenv("PG_DB"),
            user=os.getenv("PG_USER"),
            password=os.getenv("PG_PASSWORD")
        )
        cursor = conn.cursor()

        # Crear tabla si no existe
        create_table_query = """
        CREATE TABLE IF NOT EXISTS weather_data (
            id SERIAL PRIMARY KEY,
            datetime TIMESTAMP,
            temperature_c FLOAT,
            humidity_percent FLOAT,
            wind_speed_ms FLOAT,
            latitude FLOAT,
            longitude FLOAT,
            etl_loaded_at TIMESTAMP
        );
        """
        cursor.execute(create_table_query)
        conn.commit()

        # Preparar registros para inserción (convertir explícitamente a datetime.datetime)
        values = []
        for _, row in df.iterrows():
            values.append((
                row["datetime"].to_pydatetime() if hasattr(row["datetime"], "to_pydatetime") else row["datetime"],
                row["temperature_c"],
                row["humidity_percent"],
                row["wind_speed_ms"],
                row["latitude"],
                row["longitude"],
                row["etl_loaded_at"].to_pydatetime() if hasattr(row["etl_loaded_at"], "to_pydatetime") else row["etl_loaded_at"]
            ))

        insert_query = """
        INSERT INTO weather_data (
            datetime, temperature_c, humidity_percent, wind_speed_ms,
            latitude, longitude, etl_loaded_at
        ) VALUES %s
        """

        execute_values(cursor, insert_query, values)
        conn.commit()

        print(f"{len(df)} registros insertados en weather_data")

        cursor.close()
        conn.close()

    except Exception as e:
        print("Error al cargar datos en PostgreSQL:", e)


if __name__ == "__main__":
    import extract, transform
    df_raw = extract.extract_weather_data()
    df_trans = transform.transform_weather_data(df_raw)
    load_to_postgres(df_trans)
