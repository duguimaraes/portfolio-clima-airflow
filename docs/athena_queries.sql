-- Validacao da view usada pelo dashboard
SELECT
    snapshot_date,
    COUNT(*) AS total_forecasts,
    COUNT(DISTINCT city_id) AS total_capitals
FROM portfolio_clima.capital_weather_latest
GROUP BY snapshot_date;

-- Previsao detalhada para uma capital
SELECT
    forecast_date,
    city_name,
    state,
    temperature_max_c,
    temperature_min_c,
    precipitation_mm,
    temperature_range_c,
    has_rain
FROM portfolio_clima.capital_weather_latest
WHERE city_id = 'cuiaba'
ORDER BY forecast_date;

-- Resumo da previsao atual por capital
SELECT
    city_name,
    state,
    ROUND(AVG(temperature_max_c), 1) AS average_max_temperature_c,
    ROUND(SUM(precipitation_mm), 1) AS total_precipitation_mm,
    SUM(CASE WHEN has_rain THEN 1 ELSE 0 END) AS rainy_days
FROM portfolio_clima.capital_weather_latest
GROUP BY city_name, state
ORDER BY city_name;

-- Historico de snapshots coletados pela pipeline
SELECT
    snapshot_date,
    COUNT(*) AS total_forecasts,
    COUNT(DISTINCT city_id) AS total_capitals
FROM portfolio_clima.capital_weather_gold
GROUP BY snapshot_date
ORDER BY snapshot_date DESC;