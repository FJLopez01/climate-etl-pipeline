import extract
import transform
import load
import datetime

def validate_datetime_columns(df, datetime_cols=["datetime", "etl_loaded_at"]):
    """Verifica que las columnas de tiempo sean datetime.datetime"""
    for col in datetime_cols:
        for i, val in enumerate(df[col]):
            if not isinstance(val, datetime.datetime):
                raise TypeError(
                    f"Fila {i} columna '{col}' NO es datetime.datetime: {type(val)}"
                )
    print("Validacion pasada: todas las columnas de tiempo son datetime.datetime")

def run_pipeline():
    # 1️⃣ Extraer
    df_raw = extract.extract_weather_data()
    if df_raw is None:
        print("Error en la extracción, pipeline detenido")
        return

    # 2️⃣ Transformar
    df_trans = transform.transform_weather_data(df_raw)
    if df_trans is None:
        print("Error en la transformación, pipeline detenido")
        return

    # 3️⃣ Validar tipos de columnas
    try:
        validate_datetime_columns(df_trans)
    except TypeError as e:
        print("Validacion fallida:", e)
        return

    # 4️⃣ Cargar
    load.load_to_postgres(df_trans)

if __name__ == "__main__":
    run_pipeline()
