-- Tabla para temperaturas medias mensuales de Barcelona
CREATE TABLE IF NOT EXISTS public.barcelona_monthly_temp (
    any_year INTEGER PRIMARY KEY,
    temp_gener FLOAT,
    temp_febrer FLOAT,
    temp_marc FLOAT,
    temp_abril FLOAT,
    temp_maig FLOAT,
    temp_juny FLOAT,
    temp_juliol FLOAT,
    temp_agost FLOAT,
    temp_setembre FLOAT,
    temp_octubre FLOAT,
    temp_novembre FLOAT,
    temp_desembre FLOAT
);

-- Índices opcionales para consultas rápidas por año
CREATE INDEX IF NOT EXISTS idx_bcn_temp_year
    ON public.barcelona_monthly_temp (any_year);
