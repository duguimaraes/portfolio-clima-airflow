# Pipeline de Dados Climaticos com Airflow

## Objetivo

Este projeto tem como objetivo construir um pipeline de dados simples, mas com fundamentos reais de engenharia de dados.

O pipeline ira consumir dados de uma API publica de clima, armazenar os dados em camadas, transformar o JSON bruto em tabelas analiticas e futuramente orquestrar o processo com Apache Airflow.

## Fonte de dados

A fonte de dados escolhida foi a API Open-Meteo:

https://open-meteo.com/

Ela foi escolhida porque permite consultar previsoes climaticas por latitude e longitude sem necessidade de chave de API.

## Camadas do projeto

- Bronze: dados brutos extraidos da API, em formato JSON.
- Silver: dados tratados e organizados em formato tabular.
- Gold: dados prontos para analise, com indicadores derivados.

## Primeira consulta utilizada

Endpoint base:

```text
https://api.open-meteo.com/v1/forecast
```

Parametros principais:

```text
latitude=-15.5961
longitude=-56.0967
daily=temperature_2m_max,temperature_2m_min,precipitation_sum
timezone=America/Cuiaba
```

## Tecnologias previstas

- Python
- Git e GitHub
- Apache Airflow
- BigQuery Sandbox ou outra opcao gratuita de cloud

## Pipeline atual

O pipeline local esta dividido em tres etapas principais:

1. Extracao dos dados da API Open-Meteo.
2. Transformacao do JSON bruto da camada Bronze em CSV tratado na camada Silver.
3. Criacao da camada Gold com indicadores analiticos.

Fluxo:

Open-Meteo API -> Bronze JSON -> Silver CSV -> Gold CSV

Scripts principais:

- src/extract_weather.py
- src/transform_weather.py
- src/create_gold_weather.py
- src/run_pipeline.py

Para executar o pipeline completo:

python src/run_pipeline.py