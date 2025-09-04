# 🌤️ Climate ETL Pipeline

Un pipeline completo de **Extracción, Transformación y Carga (ETL)** que obtiene datos climáticos en tiempo real desde APIs públicas y los almacena en una base de datos PostgreSQL para análisis posterior.

## 📋 Tabla de Contenidos

- [🎯 Descripción del Proyecto](#-descripción-del-proyecto)
- [🏗️ Arquitectura](#️-arquitectura)
- [🛠️ Tecnologías Utilizadas](#️-tecnologías-utilizadas)
- [📊 Fuente de Datos](#-fuente-de-datos)
- [🚀 Instalación y Configuración](#-instalación-y-configuración)
- [⚙️ Uso](#️-uso)
- [📈 Estructura de Datos](#-estructura-de-datos)
- [🔧 Configuración](#-configuración)
- [📝 Próximas Mejoras](#-próximas-mejoras)
- [👨‍💻 Autor](#-autor)

## 🎯 Descripción del Proyecto

Este proyecto implementa un pipeline ETL automatizado que:

- **Extrae** datos climáticos desde la API pública de Open-Meteo
- **Transforma** los datos aplicando limpieza, validación y estructuración
- **Carga** la información procesada en una base de datos PostgreSQL
- **Valida** la calidad de los datos antes de la carga
- Proporciona un flujo robusto con manejo de errores

### Caso de Uso
Ideal para análisis climático, monitoreo ambiental, dashboards meteorológicos y como base para sistemas de alertas climáticas.

## 🏗️ Arquitectura

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Open-Meteo    │    │                  │    │   PostgreSQL    │
│      API        │───▶│  ETL Pipeline    │───▶│    Database     │
│  (Raw Weather   │    │                  │    │ (Structured     │
│     Data)       │    │                  │    │     Data)       │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Data Quality   │
                    │   Validation     │
                    └──────────────────┘
```

## 🛠️ Tecnologías Utilizadas

- **Python 3.8+** - Lenguaje principal
- **PostgreSQL** - Base de datos relacional
- **APIs REST** - Open-Meteo API
- **Librerías principales:**
  - `requests` - Consumo de APIs
  - `pandas` - Manipulación de datos
  - `psycopg2` - Conector PostgreSQL
  - `python-dotenv` - Gestión de variables de entorno

## 📊 Fuente de Datos

**Open-Meteo API**: https://api.open-meteo.com/v1/forecast

- ✅ API gratuita y sin necesidad de registro
- ✅ Datos climáticos globales actualizados cada hora
- ✅ Múltiples parámetros meteorológicos disponibles
- ✅ Formato JSON estándar

### Parámetros Extraídos:
- Temperatura (°C)
- Humedad relativa (%)
- Velocidad del viento (m/s)
- Timestamp de las mediciones
- Coordenadas geográficas

## 🚀 Instalación y Configuración

### Prerrequisitos

1. **Python 3.8+**
2. **PostgreSQL** (local o remoto)
3. **Git**

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/climate-etl-pipeline.git
cd climate-etl-pipeline
```

### 2. Crear entorno virtual

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno

Crear archivo `config/.env`:

```env
# API Configuration
API_URL=https://api.open-meteo.com/v1/forecast
LAT=19.4326  # Latitud (ejemplo: Ciudad de México)
LON=-99.1332  # Longitud
PARAMETERS=temperature_2m,relative_humidity_2m,wind_speed_10m

# PostgreSQL Configuration
PG_HOST=localhost
PG_PORT=5432
PG_DB=climate_db
PG_USER=tu_usuario
PG_PASSWORD=tu_password
```

### 5. Crear base de datos

```sql
CREATE DATABASE climate_db;
```

## ⚙️ Uso

### Ejecución Manual

```bash
# Ejecutar pipeline completo
python main.py
```

### Ejecución de Módulos Individuales

```bash
# Solo extracción
python scripts/extract.py

# Solo transformación
python scripts/transform.py

# Solo carga
python scripts/load.py
```

### Automatización (Opcional)

Programar ejecución cada hora usando cron:

```bash
# Editar crontab
crontab -e

# Agregar línea para ejecutar cada hora
0 * * * * cd /ruta/al/proyecto && python main.py
```

## 📈 Estructura de Datos

### Tabla: `weather_data`

| Campo | Tipo | Descripción |
|-------|------|-------------|
| `id` | SERIAL | ID único autoincremental |
| `datetime` | TIMESTAMP | Fecha y hora de la medición |
| `temperature_c` | FLOAT | Temperatura en Celsius |
| `humidity_percent` | FLOAT | Humedad relativa en porcentaje |
| `wind_speed_ms` | FLOAT | Velocidad del viento en m/s |
| `latitude` | FLOAT | Latitud de la ubicación |
| `longitude` | FLOAT | Longitud de la ubicación |
| `etl_loaded_at` | TIMESTAMP | Timestamp de carga en BD |

### Ejemplo de Datos

```sql
SELECT * FROM weather_data LIMIT 3;

id |      datetime       | temperature_c | humidity_percent | wind_speed_ms | latitude | longitude |     etl_loaded_at
---+--------------------+---------------+------------------+---------------+----------+-----------+--------------------
 1 | 2025-09-03 14:00:00 |          23.5 |             65.2 |           3.8 |  19.4326 |  -99.1332 | 2025-09-03 16:00:25
 2 | 2025-09-03 15:00:00 |          24.1 |             62.8 |           4.2 |  19.4326 |  -99.1332 | 2025-09-03 16:00:25
 3 | 2025-09-03 16:00:00 |          23.8 |             68.1 |           3.5 |  19.4326 |  -99.1332 | 2025-09-03 16:00:25
```

## 🔧 Configuración

### Estructura del Proyecto

```
climate-etl-pipeline/
├── config/
│   └── .env                 # Variables de entorno
├── scripts/
│   ├── extract.py          # Extracción de datos
│   ├── transform.py        # Transformación de datos
│   └── load.py             # Carga a PostgreSQL
├── main.py                 # Pipeline principal
├── requirements.txt        # Dependencias
├── README.md              # Este archivo
└── .gitignore            # Archivos ignorados por Git
```

### Personalización

**Cambiar ubicación geográfica:**
```env
LAT=40.7128   # Nueva York
LON=-74.0060
```

**Agregar más parámetros climáticos:**
```env
PARAMETERS=temperature_2m,relative_humidity_2m,wind_speed_10m,precipitation,pressure_msl
```

## 📝 Próximas Mejoras

- [ ] **Dashboard interactivo** con Streamlit
- [ ] **Alertas automáticas** por condiciones climáticas extremas
- [ ] **Múltiples ubicaciones** en una sola ejecución
- [ ] **API propia** para consultar datos históricos
- [ ] **Dockerización** del pipeline
- [ ] **Tests unitarios** y de integración
- [ ] **Logging avanzado** con rotación de archivos
- [ ] **Métricas de performance** del pipeline

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

**Ing. Frank Joseph Lopez Cruz**  
Ingeniero en Datos  

- 🌐 Portfolio: [tu-portfolio.com](https://tu-portfolio.com)
- 💼 LinkedIn: [www.linkedin.com/in/fjlopez2901](https://www.linkedin.com/in/fjlopez2901/)
- 📧 Email: lopez.frank.2901@gmail.com

---

⭐ **Si este proyecto te fue útil, ¡no olvides darle una estrella!**
