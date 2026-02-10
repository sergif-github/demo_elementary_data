-- Modelo de métricas agregadas
select
    city,
    date_trunc('hour', weather_timestamp) as hour,
    avg(temperature) as avg_temp,
    max(temperature) as max_temp,
    min(temperature) as min_temp,
    stddev(temperature) as stddev_temp,
    avg(humidity) as avg_humidity,
    max(humidity) as max_humidity,
    min(humidity) as min_humidity,
    avg(pressure) as avg_pressure,
    avg(wind_speed) as avg_wind_speed,
    count(*) as rows_count
from {{ ref('stg_weather_data') }}
group by city, date_trunc('hour', weather_timestamp)
