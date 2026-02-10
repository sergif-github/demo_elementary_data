select
    city,
    weather_timestamp,
    temperature,
    humidity,
    pressure,
    wind_speed
from {{ source('weather_data_source', 'weather_data') }}
