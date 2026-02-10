-- Schema para datos raw
CREATE SCHEMA IF NOT EXISTS raw;

-- Tabla principal de datos meteorológicos
CREATE TABLE IF NOT EXISTS raw.weather_data (
    id BIGSERIAL PRIMARY KEY,

    city TEXT NOT NULL,
    city_lat DOUBLE PRECISION,
    city_lon DOUBLE PRECISION,

    weather_timestamp TIMESTAMP NOT NULL,

    temperature DOUBLE PRECISION,
    feels_like DOUBLE PRECISION,
    humidity INTEGER,
    pressure INTEGER,

    wind_speed DOUBLE PRECISION,
    wind_deg INTEGER,

    weather_main TEXT,
    weather_description TEXT,

    ingested_at TIMESTAMP NOT NULL DEFAULT NOW()
);

-- Índices útiles para queries analíticas
CREATE INDEX IF NOT EXISTS idx_weather_city_timestamp
    ON raw.weather_data (city, weather_timestamp);

CREATE INDEX IF NOT EXISTS idx_weather_ingested_at
    ON raw.weather_data (ingested_at);
