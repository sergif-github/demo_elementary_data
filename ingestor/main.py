import time
import requests
import psycopg2
from psycopg2.extras import execute_values
from datetime import datetime, timezone

OPENWEATHER_API_KEY = "4e2dbd1f0d4b289e7a35df763336ed88"
INGEST_INTERVAL_SECONDS = 300

POSTGRES_CONFIG = {
    "host": "postgres",
    "port": 5432,
    "dbname": "weather",
    "user": "admin",
    "password": "admin",
}

CITIES = [
    {"name": "Girona", "lat": 41.9794, "lon": 2.8214},
    {"name": "Roses", "lat": 42.2629, "lon": 3.1748},
]

OPENWEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"


def fetch_weather(city):
    params = {
        "lat": city["lat"],
        "lon": city["lon"],
        "appid": OPENWEATHER_API_KEY,
        "units": "metric",
    }

    response = requests.get(OPENWEATHER_URL, params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def parse_weather(data, city_name):
    return {
        "city": city_name,
        "city_lat": data["coord"]["lat"],
        "city_lon": data["coord"]["lon"],
        "weather_timestamp": datetime.fromtimestamp(
            data["dt"], tz=timezone.utc
        ),
        "temperature": data["main"].get("temp"),
        "feels_like": data["main"].get("feels_like"),
        "humidity": data["main"].get("humidity"),
        "pressure": data["main"].get("pressure"),
        "wind_speed": data.get("wind", {}).get("speed"),
        "wind_deg": data.get("wind", {}).get("deg"),
        "weather_main": data["weather"][0].get("main"),
        "weather_description": data["weather"][0].get("description"),
    }


def insert_weather_rows(conn, rows):
    sql = """
        INSERT INTO raw.weather_data (
            city,
            city_lat,
            city_lon,
            weather_timestamp,
            temperature,
            feels_like,
            humidity,
            pressure,
            wind_speed,
            wind_deg,
            weather_main,
            weather_description
        )
        VALUES %s
    """

    values = [
        (
            r["city"],
            r["city_lat"],
            r["city_lon"],
            r["weather_timestamp"],
            r["temperature"],
            r["feels_like"],
            r["humidity"],
            r["pressure"],
            r["wind_speed"],
            r["wind_deg"],
            r["weather_main"],
            r["weather_description"],
        )
        for r in rows
    ]

    with conn.cursor() as cur:
        execute_values(cur, sql, values)
    conn.commit()


def main():
    if not OPENWEATHER_API_KEY:
        raise RuntimeError("OPENWEATHER_API_KEY is not set")

    print("Starting weather ingestor")

    conn = psycopg2.connect(**POSTGRES_CONFIG)
    print("Connected to Postgres")

    while True:
        rows_to_insert = []

        for city in CITIES:
            try:
                data = fetch_weather(city)
                parsed = parse_weather(data, city["name"])
                rows_to_insert.append(parsed)
                print(
                    f"Fetched weather for {city['name']} at {parsed['weather_timestamp']}"
                )
            except Exception as e:
                print(f"Error fetching data for {city['name']}: {e}")

        if rows_to_insert:
            try:
                insert_weather_rows(conn, rows_to_insert)
                print(f"Inserted {len(rows_to_insert)} rows")
            except Exception as e:
                print(f"Error inserting rows: {e}")
                conn.rollback()

        time.sleep(INGEST_INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
