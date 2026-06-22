-- Consulta detalhada da camada Gold
SELECT *
FROM portfolio_clima.weather_gold
ORDER BY date
LIMIT 10;

-- Resumo da previsao por cidade
SELECT
    city,
    COUNT(*) AS forecast_days,
    ROUND(AVG(temperature_max_c), 1) AS average_max_temperature_c,
    SUM(CASE WHEN has_rain THEN 1 ELSE 0 END) AS rainy_days,
    ROUND(SUM(precipitation_mm), 1) AS total_precipitation_mm
FROM portfolio_clima.weather_gold
GROUP BY city;